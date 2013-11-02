@register.simple_tag
def handlebars_js():
    return """<script src="%shandlebars.js"></script>""" % settings.STATIC_URL