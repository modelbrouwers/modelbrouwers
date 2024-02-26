from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template import Context, loader


def get_forumname_for_username(username):
    return username.replace(
        "_", " "
    )  # FIXME NOT always valid, users can have underscores!


def get_username_for_user(user):
    return get_forumname_for_username(user.username)


def get_username(obj, field="user"):
    user = getattr(obj, field)
    username = get_username_for_user(user)
    return username


def clean_username(username):
    return username.replace("'", "ʹ").lower()


def clean_username_fallback(username):
    return username.replace("'", " ").lower()


# KEEPING SPAMMERS OUT ####################
def get_client_ip(request):
    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    if x_forwarded_for:
        return x_forwarded_for.split(",")[0]
    return request.META.get("REMOTE_ADDR")


def send_inactive_user_mail(user):
    c = Context({"user": user})
    template_name = "mails/new_inactive_user"

    t = loader.get_template(template_name + ".txt")
    text_content = t.render(c)
    t = loader.get_template(template_name + ".html")
    html_content = t.render(c)

    msg = EmailMultiAlternatives("Nieuwe inactieve gebruiker", text_content)
    msg.to = [admin[1] for admin in settings.ADMINS]  # email addresses
    msg.attach_alternative(html_content, "text/html")
    msg.send()
    return
