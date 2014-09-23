import sys

MYSQL_MODELS = [
    'Forum',
    'ForumPostCountRestriction',
    'ForumUser',
    'Report',
    'Topic',
    ]

MYSQL_MODELS_NO_SYNCDB = [
    'Forum',
    'ForumUser',
    'Report',
    'ForumLinkBase',
    'ForumLinkSynced',
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

    def allow_syncdb(self, db, model):
        if db == 'mysql':
            if model._meta.app_label == 'south':
                return True
            # FIXME: quick and dirty hack
            elif model._meta.app_label == 'forum_tools' and 'test' in sys.argv:
                return True
            elif (model._meta.app_label == 'forum_tools' \
                    and model.__name__ in MYSQL_MODELS_NO_SYNCDB \
                    ) or model._meta.app_label != 'forum_tools':
                return False
        elif db == 'default':
            if model._meta.app_label == 'forum_tools' and model.__name__ not in SYNCDB_MODELS:
                return False
        return True
