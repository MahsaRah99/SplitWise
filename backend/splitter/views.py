from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import generics, status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from users.permissions import IsVerified

from .models import Expense, Group, ParticipantExpense
from .schema import group_id_parameter, payer_id_parameter, simple_mode_parameter
from .serializers import (
    ExpenseCreateSerializer,
    ExpenseDetailedSerializer,
    ExpenseUpdateSerializer,
    GroupFinalizeSerializer,
    GroupSerializer,
    HomePageSerializer,
    ParticipantExpenseSerializer,
)

User = get_user_model()


class HomePageView(generics.GenericAPIView):
    serializer_class = HomePageSerializer

    def get(self, request, *args, **kwargs):
        serializer = HomePageSerializer(context={"user": request.user})
        return Response(data=serializer.data, status=status.HTTP_200_OK)


class GroupViewset(ModelViewSet):
    serializer_class = GroupSerializer
    queryset = Group.objects.all()

    def get_permissions(self):
        if self.action == "create":
            permission_classes = [IsVerified]
        else:
            permission_classes = []  # group participants
        return [permission() for permission in permission_classes]

    def list(self, request, *args, **kwargs):
        return Response(None, status=status.HTTP_204_NO_CONTENT)


class JoinGroupView(generics.GenericAPIView):
    permission_classes = [IsVerified]

    def post(self, request, token):
        user = request.user
        group = get_object_or_404(Group, invite_token=token)

        if user not in group.members.all():
            group.members.add(user)
            return Response(
                {
                    "type": "redirect",
                    "url": "splitter:group-home-page",
                },
                status=status.HTTP_200_OK,
            )

        return Response(
            {"message": "You are already a member of this group."},
            status=status.HTTP_400_BAD_REQUEST,
        )


class ExpenseViewSet(ModelViewSet):
    queryset = Expense.objects.all()

    def get_serializer_class(self):
        if self.action == "retrieve":
            return ExpenseDetailedSerializer
        elif self.action == "partial_update":
            return ExpenseUpdateSerializer
        else:
            return ExpenseCreateSerializer

    def get_permissions(self):
        if self.action in ["create", "list"]:
            permission_classes = [IsVerified]  # group participants
        else:
            permission_classes = []  # expense payer
        return [permission() for permission in permission_classes]

    def get_serializer_context(self):
        context = super().get_serializer_context()
        group_id = self.request.data.get("group_id")
        if not group_id:
            raise ValidationError("group_id must be provided")
        group = get_object_or_404(Group, id=group_id)
        context.update({"group": group})
        return context

    def list(self, request, *args, **kwargs):
        group_id = self.request.data.get("group_id")
        qs = self.get_queryset()
        data = qs.filter(group_id=group_id).values("payer__username", "description")
        return Response(data, status=status.HTTP_200_OK)


class MarkExpenseAsPaid(generics.UpdateAPIView):
    serializer_class = ParticipantExpenseSerializer

    def update(self, request, expense_id, *args, **kwargs):
        participant_expense = get_object_or_404(ParticipantExpense, id=expense_id)
        participant_expense.is_paid = True
        participant_expense.save(update_fields=["is_paid"])
        srz_data = self.serializer_class(instance=participant_expense)
        return Response(data=srz_data.data, status=status.HTTP_200_OK)


@extend_schema(parameters=[simple_mode_parameter, payer_id_parameter])
class GroupFinalizeView(generics.RetrieveAPIView):
    serializer_class = GroupFinalizeSerializer
    queryset = Group.objects.all()

    def get(self, request, group_id, *args, **kwargs):

        group = get_object_or_404(Group, id=group_id)

        serializer = self.get_serializer(data=request.data, context={"group": group})
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


# can't you do this on the Expense table instead?
#     credited = ParticipantExpense.objects.filter(
#         expense__group=group,
#         is_paid=False
#     ).values('expense__payer').annotate(
#         total_paid=Sum('amount_owed')
#     )
# instead write:
#     credited = Expense.objects.filter(
#         group=group,
#     ).values('payer').annotate(
#         total_paid=Sum('amount')
