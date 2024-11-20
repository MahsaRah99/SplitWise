from typing import Dict, List, Union

from django.contrib.auth import get_user_model
from rest_framework import serializers

from .models import Expense, Group, ParticipantExpense
from .utils import get_total_owed_to_payer, simplify_transactions

User = get_user_model()


class HomePageSerializer(serializers.Serializer):
    groups = serializers.SerializerMethodField()

    def get_groups(self, obj) -> List[Dict[str, int]]:
        user = self.context.get("user")
        qs = Group.objects.filter(participants=user).values("id", "name")
        return qs


class GroupSerializer(serializers.ModelSerializer):
    members = serializers.StringRelatedField(read_only=True, many=True)

    class Meta:
        model = Group
        fields = ("name", "invite_link", "members")
        read_only_fields = ("members", "invite_link")

    def create(self, validated_data):
        user = self.context["request"].user
        group = Group.objects.create(**validated_data)
        group.members.add(user)
        return group


class ExpenseCreateSerializer(serializers.ModelSerializer):
    participants = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), many=True, write_only=True
    )
    payer_name = serializers.StringRelatedField(source="payer", read_only=True)
    participants_names = serializers.SlugRelatedField(
        many=True, read_only=True, slug_field="username", source="participants"
    )

    class Meta:
        model = Expense
        fields = (
            "description",
            "amount",
            "participants",
            "payer_name",
            "participants_names",
            "date",
        )
        extra_kwargs = {"group": {"write_only": True}}

    def validate_participants(self, value):
        user = self.context["request"].user
        if not value:
            raise serializers.ValidationError("Participants cannot be empty.")

        if len(value) == 1 and user in value:
            raise serializers.ValidationError(
                "Participants must include at least one user other than the payer."
            )

        return value

    def create(self, validated_data):
        user = self.context["request"].user
        group = self.context.get("group")
        participants = validated_data.pop("participants", None)

        per_person_amount = validated_data["amount"] / len(participants)

        expense = Expense.objects.create(group=group, payer=user, **validated_data)

        for participant in participants:
            if participant == user:
                continue
            ParticipantExpense.objects.create(
                expense=expense, amount_owed=per_person_amount, user=participant
            )

        return expense


class ExpenseUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Expense
        fields = (
            "group",
            "description",
            "amount",
            "payer",
            "participants",
            "date",
        )
        read_only_fields = (
            "amount",
            "payer",
            "participants",
        )


class ExpenseDetailedSerializer(serializers.ModelSerializer):
    payer_name = serializers.StringRelatedField(source="payer", read_only=True)
    participant_expenses = serializers.SerializerMethodField()

    class Meta:
        model = Expense
        fields = (
            "id",
            "group",
            "description",
            "amount",
            "payer_name",
            "participant_expenses",
            "date",
        )

    def get_participant_expenses(self, obj):
        qs = ParticipantExpense.objects.filter(expense=obj)
        return ParticipantExpenseSerializer(qs, many=True).data


class ParticipantExpenseSerializer(serializers.ModelSerializer):
    user_name = serializers.StringRelatedField(source="user", read_only=True)

    class Meta:
        model = ParticipantExpense
        fields = ("user_name", "amount_owed", "is_paid")


class GroupFinalizeSerializer(serializers.Serializer):
    payer = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), required=False
    )
    simple_mode = serializers.BooleanField(default=True)
    finals = serializers.SerializerMethodField()

    def get_finals(self, obj=None) -> Union[list, dict]:
        simple_mode = self.validated_data.get("simple_mode")
        payer = self.validated_data.get("payer")
        group = self.context.get("group")

        if not group:
            raise serializers.ValidationError("Group instance is required.")

        if not simple_mode and not payer:
            raise serializers.ValidationError(
                "Payer should be specified in the detailed mode"
            )

        if simple_mode:
            return simplify_transactions(group)
        else:
            return get_total_owed_to_payer(group, payer)
