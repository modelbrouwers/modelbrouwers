from tastypie import fields
from tastypie.resources import ModelResource, ALL, ALL_WITH_RELATIONS
from albums.models import Album, Photo

# for the availble fields, look in albums/models.py!

class AlbumResource(ModelResource):
    class Meta:
        queryset = Album.objects.filter(public=True, trash=False).order_by('-last_upload')
        resource_name = 'album'
        fields = ['id', 'title', 'description', 'created', 'last_upload', 'views', 'build_report', 'votes']

class PhotoResource(ModelResource):
    album = fields.ForeignKey(AlbumResource, 'album')

    class Meta:
        queryset = Photo.objects.filter(album__public=True, album__trash=False, trash=False)
        resource_name = 'photo'
        fields = ['width', 'height', 'image', 'description', 'uploaded', 'modified', 'views']

        filtering = {
            'album': ALL_WITH_RELATIONS,
        }