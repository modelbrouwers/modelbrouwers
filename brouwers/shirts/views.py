from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.mail import EmailMultiAlternatives
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.utils.translation import ugettext as _

from brouwers.general.shortcuts import render_to_response
from models import ShirtOrder
from forms import ShirtOrderForm

TEXT_TEMPLATE = _("""Dear %(username)s,\n
This is an order confirmation for a Modelbrouwers.nl shirt with the following options: color %(color)s; size %(size)s; type %(type)s. The order was placed on %(date)s.\n
To complete this order, please make a payment to Sergei Maertens on the following account: \nIBAN: BE47 1325 1771 2380\nBIC: BNAG BE BB.\nBe sure to mention your order ID: %(orderid)s.\n
The price for this order is %(price)s euros.\n\n
Sincerely,\nSergei Maertens
""")

@login_required
def index(request):
    if request.method == "POST":
        order = ShirtOrder(user=request.user)
        form = ShirtOrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            # mailing
            subject, from_email = _('Modelbrouwers.nl shirt order'), 'admins@modelbrouwers.nl'
            text_content = TEXT_TEMPLATE % {
                'username': order.user.get_profile().forum_nickname,
                'color': order.get_color_display(),
                'size': order.get_size_display(),
                'type': order.get_type_display(),
                'date': order.order_time.strftime("%d-%m-%Y, %H:%i"),
                'price': order.price,
                'orderid': order.id,
            }
            html_content = render_to_response(request, 'shirts/mail.html', {'order': order})
            
            msg = EmailMultiAlternatives(subject, text_content, from_email, [request.user.email])
            msg.attach_alternative(html_content, "text/html")
            msg.send()
            
            messages.success(request, _("You have placed order %(orderid)s") % {'orderid':order.id})
            return HttpResponseRedirect(reverse(index))
    else:
        form = ShirtOrderForm()
    return render_to_response(request, 'shirts/base.html', {'form': form})
