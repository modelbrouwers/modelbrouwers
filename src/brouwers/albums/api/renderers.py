from rest_framework import renderers


class FineUploaderRenderer(renderers.JSONRenderer):
    media_type = 'text/plain'
