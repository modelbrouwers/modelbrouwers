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


class ForumToolsRouter:

    def db_for_read(self, model, **hints):
        if model.__name__ in MYSQL_MODELS and model._meta.app_label == 'forum_tools':
            return 'mysql'
        return 'default'

    def db_for_write(self, model, **hints):
        if model.__name__ in MYSQL_MODELS and model._meta.app_label == 'forum_tools':
            return 'mysql'
        return 'default'

    def allow_relation(self, obj1, obj2, **hints):
        """
        If both obj1 and obj2 are MYSQL or PostgreSQL models, relation is allowed.
        """
        app_label1, model1 = obj1._meta.app_label, obj1._meta.object_name
        app_label2, model2 = obj2._meta.app_label, obj2._meta.object_name

        # we only look at the 'forum_tools' app in this router
        if app_label1 == app_label2 == 'forum_tools':
            if model1 in MYSQL_MODELS and model2 in MYSQL_MODELS:
                return True
            if model1 not in MYSQL_MODELS and model2 not in MYSQL_MODELS:
                return True
        return None

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
