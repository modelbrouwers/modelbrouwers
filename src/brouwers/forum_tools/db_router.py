from django.conf import settings

# models with tables in the forum database
MYSQL_MODELS = [
    'Forum',
    'ForumPostCountRestriction',
    'ForumUser',
    'Report',
    'Topic',
]

# models with tables in the django database
SYNCDB_MODELS = [
    'BuildReportsForum',
    'ForumLinkBase',
    'ForumLinkSynced',
    'ForumCategory',
]


class ForumToolsRouter(object):
    def db_for_read(self, model, **hints):
        if model.__name__ in MYSQL_MODELS and model._meta.app_label == 'forum_tools':
            return 'mysql'
        return 'default'

    def db_for_write(self, model, **hints):
        if model.__name__ in MYSQL_MODELS and model._meta.app_label == 'forum_tools':
            return 'mysql'
        return 'default'

    def allow_relation(self, obj1, obj2, **hints):
        for model in MYSQL_MODELS:
            if model in [obj1.__class__.__name__, obj2.__class__.__name__]:
                return False
        return True

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """
        forum_tools is the only app that uses the phpBB database, so all the
        rest must sync to the default database.
        """
        if app_label != 'forum_tools':
            return db == 'default'

        # forum_tools app, only migrate the phpBB tables for the mysql db
        if db == 'mysql':
            model = hints.get('model')
            if model is not None:
                unmanaged = model._meta.db_table.startswith(settings.PHPBB_TABLE_PREFIX)
                return unmanaged or model.__name__ in MYSQL_MODELS or settings.TESTING
        else:
            return True
