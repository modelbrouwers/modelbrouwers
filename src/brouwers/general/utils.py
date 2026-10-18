import logging
from pathlib import Path

from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.http import HttpRequest
from django.template import Context, loader

import geoip2.database
import geoip2.errors
import geoip2.models

logger = logging.getLogger(__name__)


def clean_username(username):
    return username.replace("'", "ʹ").lower()


def clean_username_fallback(username):
    return username.replace("'", " ").lower()


def get_client_ip(request: HttpRequest) -> str:
    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    if x_forwarded_for:
        return x_forwarded_for.split(",")[0]
    remote_address = request.META.get("REMOTE_ADDR")
    assert remote_address
    return remote_address


def ip_to_country(ip_address: str) -> geoip2.models.Country | None:
    assert ip_address
    assert ip_address
    db_path = Path(settings.GEOIP_DATABASE_PATH)
    if not db_path.exists() or not db_path.is_file():
        logger.debug("Database does not exist at path %s", db_path)
        return None
    with geoip2.database.Reader(db_path) as reader:
        try:
            return reader.country(ip_address)
        except geoip2.errors.AddressNotFoundError:
            logger.debug("ip_address_lookup_failed", extra={"address": ip_address})
            return None


def lookup_country(ip_address: str) -> str:
    assert ip_address
    country = ip_to_country(ip_address)
    if country is None:
        return "?"
    return f"{country.country.name} / {country.continent.code}"


def send_inactive_user_mail(user) -> None:
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
