import jwt
from django.conf import settings
from django.core.mail import send_mail
from django.utils import timezone


def send_verification_email(user):
    token = jwt.encode(
        {"user_id": user.id, "exp": timezone.now() + timezone.timedelta(hours=1)},
        settings.SECRET_KEY,
        algorithm="HS256",
    )
    verification_link = f"{settings.SITE_URL}/users/auth/verify-email/{token}/"

    send_mail(
        "Verify Your Email",
        f"Click the link to verify your email: {verification_link}",
        "from@splitwise.com",
        [user.email],
        fail_silently=False,
    )
