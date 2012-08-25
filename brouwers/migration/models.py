from django.db import models

class UserMigration(models.Model):
    username = models.CharField(max_length=50) #actually 20
    username_clean = models.CharField(max_length=50) #lowercase version
    email = models.EmailField(max_length=254)
    hash = models.CharField(max_length=256, blank=True, null=True)
    
    class Meta:
        ordering = ['username_clean']
    
    def __unicode__(self):
        return u"%s" % self.username
    
    def save(self, *args, **kwargs):
        if not self.username_clean:
            self.username_clean = self.username.lower()
        super(UserMigration, self).save(*args, **kwargs)
