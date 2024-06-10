from django.urls import path
from Accounts.views import SignUpView

urlpatterns = [
    path("signup/", SignUpView.as_view(), name="signup"),
]
