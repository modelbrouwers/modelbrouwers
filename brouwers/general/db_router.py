class ForumUserRouter(object):
    def db_for_read(self, model, **hints):
        "ForumUser -> use the MySQL db"
        if model.__name__ == 'ForumUser' and model._meta.app_label == 'general':
            return 'mysql'
        return 'default'
    
    def db_for_write(self, model, **hints):
        "ForumUser -> use the MySQL db"
        if model.__name__ == 'ForumUser' and model._meta.app_label == 'general':
            return 'mysql'
        return 'default'
    
    def allow_relation(self, obj1, obj2, **hints):
        "ForumUser -> use the MySQL db"
        if 'ForumUser' in [obj1.__class__.__name__, obj2.__class__.__name__]:
            return False
        return True
    
    def allow_syncdb(self, db, model):
        "ForumUser -> use the MySQL db"
        if db =='mysql' or (model._meta.app_label == 'general' and model.__name__ == 'ForumUser'):
            return False
        return True
