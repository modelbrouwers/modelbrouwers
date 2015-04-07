from django.conf import settings


MYSQL_MODELS = [
    'Forum',
    'ForumPostCountRestriction',
    'ForumUser',
    'Report',
    'Topic',
    ]

SYNCDB_MODELS = [
    'ForumLinkBase',
    'ForumLinkSynced',
    'ForumCategory',
]


class ForumToolsRouter(object):
    def db_for_read(self, model, **hints):
        "ForumUser -> use the MySQL db"
        if model.__name__ in MYSQL_MODELS and model._meta.app_label == 'forum_tools':
            return 'mysql'
        return 'default'

    def db_for_write(self, model, **hints):
        "ForumUser -> use the MySQL db"
        if model.__name__ in MYSQL_MODELS and model._meta.app_label == 'forum_tools':
            return 'mysql'
        return 'default'

    def allow_relation(self, obj1, obj2, **hints):
        "ForumUser -> use the MySQL db"
        for model in MYSQL_MODELS:
            if model in [obj1.__class__.__name__, obj2.__class__.__name__]:
                return False
        return True

    def allow_migrate(self, db, model):
        if db == 'mysql':
            if model._meta.app_label == 'forum_tools':
                if model._meta.db_table.startswith(settings.PHPBB_TABLE_PREFIX):
                    return settings.TESTING  # allow migrate if we're running tests
                else:
                    return True
            return False
        elif db == 'default':  # postgres db
            if model._meta.app_label == 'forum_tools' and model.__name__ not in SYNCDB_MODELS:
                return False
        return True
