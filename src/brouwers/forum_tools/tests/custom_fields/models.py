from django.db import models

from forum_tools.fields import ForumToolsIDField


class MyModel(models.Model):
    forum = ForumToolsIDField(type='forum')
    forum2 = ForumToolsIDField(type='forum', null=True)
    topic = ForumToolsIDField(type='topic', null=True)

