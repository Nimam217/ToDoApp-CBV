from mail_templated import EmailMessage

from .threads import EmailThread


def send_activation_email(user, token):
    message = EmailMessage(
        "email/activation_email.tpl",
        {
            "token": token,
            "user": user,
        },
        "admin@gmail.com",
        to=[user.email],
    )

    EmailThread(message).start()


def send_reset_password_email(user, token):
    message = EmailMessage(
        "email/reset_password_email.tpl",
        {
            "token": token,
            "user": user,
        },
        "admin@gmail.com",
        to=[user.email],
    )

    EmailThread(message).start()


def send_web_activation_email(user, token):

    message = EmailMessage(
        "email/web_activation_email.tpl",
        {
            "token": token,
            "user": user,
        },
        "admin@gmail.com",
        to=[user.email],
    )

    EmailThread(message).start()
