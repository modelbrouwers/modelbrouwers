from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _

from datetime import date, datetime
import os

#TODO: comments on albums/photos

WRITABLE_CHOICES = (
	("u", _("user")),
	#("g", _("group")),
	("o", _("everyone")),#everyone = every logged in user
	)

class Category(models.Model):
	name = models.CharField(_("name"), max_length=256, unique=True)
	order = models.PositiveSmallIntegerField(default=1, blank=True, null=True)
	
	class Meta:
		verbose_name = _("category")
		verbose_name_plural = _("categories")
		ordering = ['order', 'name']
	
	def __unicode__(self):
		return self.name
	
	def get_absolute_url(self):
		return "/albums/category/%s" % self.id

class Album(models.Model):
	user = models.ForeignKey(User)
	title = models.CharField(_("album title"), max_length="256",
			default="album %s" % datetime.now().strftime("%d-%m-%Y"))
	description = models.CharField(_("album description"),
			max_length=500, blank=True)
	category = models.ForeignKey(Category, blank=True, null=True)
	
	#Logging and statistics
	created = models.DateTimeField(auto_now_add=True)
	modified = models.DateTimeField(_("last modified"), auto_now=True)
	#(default=datetime.now) 	#auto_now or something like that?
	views = models.PositiveIntegerField(default=0)
	
	#User preferences
	order = models.PositiveSmallIntegerField(default=1, blank=True, null=True)
	public = models.BooleanField(_("Public?"),
			help_text=_("Can this album be viewed by everyone? Untick to make the album available only to yourself."), default=True)
	
	#Misc features
	build_report = models.URLField(max_length=500,
			help_text=_("Link to the forumtopic of the build."), blank=True)
	votes = models.IntegerField(_("appreciation"), default=0)
	#albums can be voted, so we can have an 'album of the month' feature
	writable_to = models.CharField(max_length=1, choices=WRITABLE_CHOICES, default="u")
	#writable to only user, group or everyone (unix like permissions)
	trash = models.BooleanField() #put in trash before removing from db
	
	class Meta:
		verbose_name = _("album")
		verbose_name_plural = _("albums")
		#order_with_respect_to = "user"
		ordering = ('order',)
		unique_together = (('user', 'title'),)
	
	def __unicode__(self):
		return self.title
	
	def get_absolute_url(self):
		return "/albums/album/%s/" % self.id

class Photo(models.Model):
	""" Helper functions """	
	def get_image_path(self, filename):
		name, extension = os.path.splitext(filename)
		filename = name.lower() + extension
		return os.path.join('albums', str(self.album.id), filename)
	
	""" Model Fields """
	#image properties
	user = models.ForeignKey(User) #we need to know the owner (public albums)
	album = models.ForeignKey(Album)
	width = models.PositiveSmallIntegerField(blank=True, null=True)
	height = models.PositiveSmallIntegerField(blank=True, null=True)
	image = models.ImageField(upload_to=get_image_path, height_field='height', width_field='width')
	description = models.CharField(_("photo description"), max_length=500, blank=True)
	
	#Logging and statistics
	uploaded = models.DateTimeField(auto_now_add=True)
	modified = models.DateTimeField(_("last modified"), auto_now=True)
	views = models.PositiveIntegerField(default=0)
	
	order = models.PositiveSmallIntegerField(default=1, blank=True, null=True)
	
	class Meta:
		verbose_name = _("Photo")
		verbose_name_plural = _("Photos")
		ordering = ['album', 'order']
	
	def __unicode__(self):
		return "image from %s in %s" % (self.user, self.album.title)
	
	def get_absolute_url(self):
		return "/albums/photo/%s/" % self.id
