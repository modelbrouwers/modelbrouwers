from django.db import models
from django.utils.translation import ugettext_lazy as _


class SisowMethods(models.TextChoices):
    """
    Possible payment methods offered by Sisow.

    Note: paypal and bank_transfer are offered in core Open Cart.
    """

    ideal = "ideal", _("iDEAL")
    # idealqr = "idealqr", _("iDEAL QR")
    # overboeking = "overboeking", _("Bankoverboeking")
    # ebill = "ebill", _("Ebill")
    # bunq = "bunq", _("bunq")
    # creditcard = "creditcard", _("Creditcard")
    # maestro = "maestro", _("Maestro")
    # vpay = "vpay", _("V PAY")
    sofort = "sofort", _("SOFORT Banking")
    # giropay = "giropay", _("Giropay")
    # eps = "eps", _("EPS")
    mistercash = "mistercash", _("Bancontact")
    # belfius = "belfius", _("Belfius Pay Button")
    # homepay = "homepay", _("ING Home’Pay")
    # kbc = "kbc", _("KBC")
    # cbc = "cbc", _("CBC")
    # paypalec = "paypalec", _("PayPal Express Checkout")  # maybe without sisow?
    # afterpay = "afterpay", _("Afterpay")
    # billink = "billink", _("Billink achteraf betalen")
    # capayable = "capayable", _("Capayable gespreid betalen")
    # focum = "focum", _("Focum AchterafBetalen")
    # klarna = "klarna", _("Klarna Factuur")
    # vvv = "vvv", _("VVV Giftcard")
    # webshop = "webshop", _("Webshop Giftcard")


class TransactionStatuses(models.TextChoices):
    success = "Success", _("Een succesvolle transactie")
    expired = "Expired", _("De transactie is verlopen")
    cancelled = "Cancelled", _("De transactie is geannuleerd")
    failure = (
        "Failure",
        _("Een interne fout heeft zich bij de gekozen betaalmethode voorgedaan"),
    )
    pending = (
        "Pending",
        _("In afwachting van daadwerkelijke betaling, betaling is nog niet zeker"),
    )
    reversed = "Reversed", _("De transactie is teruggedraaid")
    denied = (
        "Denied",
        _("De transactie aanvraag is afgewezen door de betaalmethode (Focum/Klarna)"),
    )
    reservation = (
        "Reservation",
        _(
            "Transactie aanvraag is gelukt factuur dient nog te worden aangemaakt (Focum/Klarna)"
        ),
    )
    open = "Open", _("De transactie is nog in behandeling")
