from django.db.models import Q


from tastypie import fields
from tastypie.authentication import SessionAuthentication
from tastypie.authorization import ReadOnlyAuthorization
from tastypie.resources import ModelResource, ALL, ALL_WITH_RELATIONS


from albums.models import Album, Photo
# for the availble fields, look in albums/models.py!

### AUTHORIZATION ##############################################################
class AlbumAuthorization(ReadOnlyAuthorization):
    def read_list(self, object_list, bundle):
        user = bundle.request.user
        q_public = Q(public=True)
        q_own = Q(user__id=user.id)
        return object_list.filter(Q(q_public | q_own)).order_by('order', 'title')


class OwnAlbumAuthorization(AlbumAuthorization):
    def read_list(self, object_list, bundle):
        qs = super(OwnAlbumAuthorization, self).read_list(object_list, bundle)
        return qs.filter(user=bundle.request.user)


### RESOURCES ##################################################################

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
        authorization = OwnAlbumAuthorization()


class PhotoResource(ModelResource):
    album = fields.ForeignKey(AlbumResource, 'album')
    thumb_url = fields.CharField(attribute='thumb_url', readonly=True)

    class Meta:
        queryset = Photo.objects.filter(album__public=True, album__trash=False, trash=False)
        resource_name = 'photo'
        fields = ['id', 'width', 'height', 'image', 'description', 'uploaded', 'modified', 'views']

        filtering = {
            'album': ALL_WITH_RELATIONS,
        }