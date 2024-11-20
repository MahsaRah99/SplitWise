from django.urls import path
from rest_framework import routers

from . import views

app_name = "splitter"

router = routers.SimpleRouter()
router.register("group", views.GroupViewset, basename="group")
router.register("expense", views.ExpenseViewSet, basename="expense")

urlpatterns = [
    path("home/user/", views.HomePageView.as_view(), name="home-page"),
    path("group/join/<uuid:token>/", views.JoinGroupView.as_view(), name="join-group"),
    path(
        "expense/paid/<int:expense_id>/",
        views.MarkExpenseAsPaid.as_view(),
        name="expense_paid",
    ),
    path(
        "group/finalize/<int:group_id>/",
        views.GroupFinalizeView.as_view(),
        name="group-finalize",
    ),
] + router.urls
