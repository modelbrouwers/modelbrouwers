from django.utils.translation import ugettext_lazy as _

from djchoices import ChoiceItem, DjangoChoices

BASE_URL = "https://www.sisow.nl/Sisow/iDeal/RestHandler.ashx/"


class Payments(DjangoChoices):
    """
    Possible payment methods
    """
    ideal = ChoiceItem("ideal", label=_("iDEAL"))
    idealqr = ChoiceItem("idealqr", label=_("iDEAL QR"))
    overboeking = ChoiceItem("overboeking", label=_("Bankoverboeking"))
    ebill = ChoiceItem("ebill", label=_("Ebill"))
    bunq = ChoiceItem("bunq", label=_("bunq"))
    creditcard = ChoiceItem("creditcard", label=_("Creditcard"))
    maestro = ChoiceItem("maestro", label=_("Maestro"))
    vpay = ChoiceItem("vpay", label=_("V PAY"))
    sofort = ChoiceItem("sofort", label=_("SOFORT Banking"))
    giropay = ChoiceItem("giropay", label=_("Giropay"))
    eps = ChoiceItem("eps", label=_("EPS"))
    mistercash = ChoiceItem("mistercash", label=_("Bancontact"))
    belfius = ChoiceItem("belfius", label=_("Belfius Pay Button"))
    homepay = ChoiceItem("homepay", label=_("ING Home’Pay"))
    kbc = ChoiceItem("kbc", label=_("KBC"))
    cbc = ChoiceItem("cbc", label=_("CBC"))
    paypalec = ChoiceItem("paypalec", label=_("PayPal Express Checkout"))
    afterpay = ChoiceItem("afterpay", label=_("Afterpay"))
    billink = ChoiceItem("billink", label=_("Billink achteraf betalen"))
    capayable = ChoiceItem("capayable", label=_("Capayable gespreid betalen"))
    focum = ChoiceItem("focum", label=_("Focum AchterafBetalen"))
    klarna = ChoiceItem("klarna", label=_("Klarna Factuur"))
    vvv = ChoiceItem("vvv", label=_("VVV Giftcard"))
    webshop = ChoiceItem("webshop", label=_("Webshop Giftcard"))
