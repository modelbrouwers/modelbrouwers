from django.db import IntegrityError
from django.db.models import F, Q, Max
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.forms import ValidationError
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.utils.safestring import mark_safe
import django.utils.simplejson as json

from brouwers.general.shortcuts import render_to_response
from models import *
from forms import AlbumForm, EditAlbumFormAjax, PickAlbumForm, OrderAlbumForm
from utils import resize, admin_mode
import itertools

#@login_required
def get_sidebar(request):
    return render_to_response(request, 'albums/ajax/forum/sidebar.html', {})
