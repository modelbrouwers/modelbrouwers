from django.db.models import Q


from tastypie import fields
from tastypie.authentication import BasicAuthentication, SessionAuthentication
from tastypie.authorization import ReadOnlyAuthorization
from tastypie.resources import ModelResource, ALL, ALL_WITH_RELATIONS


from albums.models import Album, Photo
# for the availble fields, look in albums/models.py!


class AlbumAuthorization(ReadOnlyAuthorization):
    def read_list(self, object_list, bundle):
        user = bundle.request.user
        q_public = Q(public=True)
        q_own = Q(user__id=user.id)
        return object_list.filter(Q(q_public | q_own)).order_by('order', 'title')

class AlbumResource(ModelResource):
    cover = fields.ForeignKey('albums.api.resources.PhotoResource', 'cover', null=True)

    class Meta:
        queryset = Album.objects.filter(trash=False).order_by('-last_upload')
        resource_name = 'album'
        fields = ['id', 'title', 'description', 'created', 'last_upload', 'views', 'build_report', 'votes']
        # authentication = BasicAuthentication()
        authentication = SessionAuthentication()
        authorization = AlbumAuthorization()

class OwnAlbumsResource(AlbumResource):
    class Meta(AlbumResource.Meta):
        resource_name = 'own_albums'
    
    def apply_authorization_limits(self, request, object_list):
        return object_list.filter(user=request.user)




class PhotoResource(ModelResource):
    album = fields.ForeignKey(AlbumResource, 'album')

    class Meta:
        queryset = Photo.objects.filter(album__public=True, album__trash=False, trash=False)
        resource_name = 'photo'
        fields = ['width', 'height', 'image', 'description', 'uploaded', 'modified', 'views']

        filtering = {
            'album': ALL_WITH_RELATIONS,
        }