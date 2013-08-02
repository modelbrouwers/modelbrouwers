class SouthRouter(object):
    # def db_for_read(self, model, **hints):
    #     if model._meta.app_label == 'south':
    #         return 'default'
    #     return None
    
    # def db_for_write(self, model, **hints):
    #     if model._meta.app_label == 'south':
    #         return 'default'
    #     return None

    def allow_syncdb(self, db, model):
        if db == 'mysql' and model._meta.app_label == 'south':
            return True
        return None