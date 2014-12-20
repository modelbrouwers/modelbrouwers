from django.contrib.auth import get_user_model

from tastypie.authentication import SessionAuthentication
from tastypie.authorization import ReadOnlyAuthorization
from tastypie.resources import ModelResource


User = get_user_model()


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
        return bundle.obj.username # get_profile is deprecated
