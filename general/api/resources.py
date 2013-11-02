from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.conf.urls import url


from tastypie.authentication import BasicAuthentication, SessionAuthentication
from tastypie.authorization import ReadOnlyAuthorization
from tastypie.http import HttpUnauthorized, HttpForbidden
from tastypie.resources import ModelResource
from tastypie.utils import trailing_slash


from general.utils import get_forumname_for_username
from general.models import UserProfile

class UserAuthorization(ReadOnlyAuthorization):
    def read_list(self, object_list, bundle):
        return object_list.filter(id=bundle.request.user.id)

class UserResource(ModelResource):
    class Meta:
        queryset = User.objects.all()
        fields = ['username']
        allowed_methods = ['get', 'post']
        resource_name = 'user'
        # authentication = BasicAuthentication() #TODO: switchen naar api key die ze krijgen eenmaal ze ingelogd hebben
        authentication = SessionAuthentication()
        authorization = UserAuthorization()

    def dehydrate_username(self, bundle):
        try:
            return bundle.obj.get_profile().forum_nickname # get_profile is deprecated
        except UserProfile.DoesNotExist:
            pass
        return get_forumname_for_username(bundle.data['username'])