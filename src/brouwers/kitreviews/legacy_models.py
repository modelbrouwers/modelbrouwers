# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from __future__ import unicode_literals

from django.db import models


class Categorie(models.Model):
    categorie_id = models.AutoField(primary_key=True)
    naam = models.TextField()

    class Meta:
        app_label = 'kitreviews'
        managed = False
        db_table = 'categorieen'

    def __unicode__(self):
        return self.naam


class Fabrikant(models.Model):
    fabrikant_id = models.AutoField(primary_key=True)
    naam = models.TextField()

    class Meta:
        app_label = 'kitreviews'
        managed = False
        db_table = 'fabrikanten'

    def __unicode__(self):
        return self.naam


class Kit(models.Model):
    kit_id = models.AutoField(primary_key=True)
    modelnaam = models.TextField()
    type = models.TextField()
    schaal = models.SmallIntegerField()
    moeilijkheid = models.IntegerField()
    categorie = models.ForeignKey(Categorie, on_delete=models.CASCADE)
    foto = models.TextField(blank=True, null=True)
    fabrikant = models.ForeignKey(Fabrikant, on_delete=models.CASCADE)
    te_koop = models.CharField(max_length=3)
    url_shop = models.TextField(blank=True, null=True)
    datum = models.DateTimeField()
    bouwbeschrijving = models.TextField()

    class Meta:
        app_label = 'kitreviews'
        managed = False
        db_table = 'kits'

    def __unicode__(self):
        return self.modelnaam


class Reviewer(models.Model):
    reviewer_id = models.AutoField(primary_key=True)
    naam = models.TextField()
    emailadres = models.TextField()

    class Meta:
        app_label = 'kitreviews'
        managed = False
        db_table = 'reviewers'

    def __unicode__(self):
        return self.naam


class Review(models.Model):
    review_id = models.AutoField(primary_key=True)
    commentaar = models.TextField()
    url_bouwverslag_mb = models.TextField(blank=True, null=True)
    url_album = models.TextField(blank=True, null=True)
    url_bouwverslag_twenot = models.TextField(blank=True, null=True)
    pluspunten = models.TextField(blank=True, null=True)
    minpunten = models.TextField(blank=True, null=True)
    indruk = models.IntegerField()
    kit = models.ForeignKey(Kit, on_delete=models.CASCADE)
    reviewer = models.ForeignKey(Reviewer, on_delete=models.CASCADE)
    datum = models.DateTimeField()

    class Meta:
        app_label = 'kitreviews'
        managed = False
        db_table = 'reviews'

    def __unicode__(self):
        return unicode(self.kit)


class Uitbreiding(models.Model):
    uitbreiding_id = models.AutoField(primary_key=True)
    naam = models.TextField()
    fabrikantnaam = models.TextField()
    kit = models.ForeignKey(Kit, on_delete=models.CASCADE)

    class Meta:
        app_label = 'kitreviews'
        managed = False
        db_table = 'uitbreidingen'

    def __unicode__(self):
        return self.naam
