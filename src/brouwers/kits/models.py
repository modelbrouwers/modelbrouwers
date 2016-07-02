from __future__ import unicode_literals

from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.urlresolvers import reverse
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _

from autoslug import AutoSlugField
from djchoices import DjangoChoices, ChoiceItem


@python_2_unicode_compatible
class Brand(models.Model):
    """
    Model for kit manufacturer.
    """
    name = models.CharField(
        _('brand'), max_length=100,
        db_index=True, unique=True,
        error_messages={'unique': _('This brand already exists')}
    )
    slug = AutoSlugField(_('slug'), unique=True, populate_from='name')
    logo = models.ImageField(_('logo'), upload_to='images/brand_logos/', blank=True)
    is_active = models.BooleanField(
        _('is active'), default=True, db_index=True,
        help_text=_('Whether the brand still exists or not')
    )

    class Meta:
        verbose_name = _('brand')
        verbose_name_plural = _('brands')
        ordering = ['name']

    def __str__(self):
        return self.name


@python_2_unicode_compatible
class Scale(models.Model):
    """
    Possible scales a model kit can have
    """
    scale = models.PositiveSmallIntegerField(
        _('scale'), db_index=True, unique=True,
        error_messages={'unique': _('This scale already exists')}
    )

    class Meta:
        verbose_name = _('scale')
        verbose_name_plural = _('scales')
        ordering = ['scale']

    def get_repr(self, separator=":"):
        return '1%s%d' % (separator, self.scale)

    def __str__(self):
        return self.get_repr()


class KitDifficulties(DjangoChoices):
    very_easy = ChoiceItem(10, _('very easy'))
    easy = ChoiceItem(20, _('easy'))
    medium = ChoiceItem(30, _('medium'))
    hard = ChoiceItem(40, _('hard'))
    very_hard = ChoiceItem(50, _('very hard'))


def get_kit_slug(instance):
    return u"{0} {1}".format(instance.name, instance.brand.name)


@python_2_unicode_compatible
class ModelKit(models.Model):
    """
    Model to hold scale model kit data.
    """
    name = models.CharField(_(u'kit name'), max_length=255, db_index=True)
    brand = models.ForeignKey('Brand', verbose_name=_('brand'), on_delete=models.PROTECT)
    slug = AutoSlugField(_('slug'), unique=True, populate_from=get_kit_slug)
    kit_number = models.CharField(
        _('kit number'), max_length=50,
        blank=True, db_index=True,
        help_text=_(u'Kit number as found on the box.')
    )
    scale = models.ForeignKey(Scale, verbose_name=_('scale'), on_delete=models.PROTECT)
    difficulty = models.PositiveSmallIntegerField(
        _('difficulty'), choices=KitDifficulties.choices,
        default=KitDifficulties.medium, validators=[KitDifficulties.validator]
    )

    box_image = models.ImageField(_('box image'), upload_to='kits/box_images/%Y/%m', blank=True)

    duplicates = models.ManyToManyField(
        "self", blank=True, verbose_name=_('duplicates'),
        help_text=_('Kits that are the same but have another producer.'),
    )

    submitter = models.ForeignKey(settings.AUTH_USER_MODEL)
    submitted_on = models.DateTimeField(auto_now_add=True)
    is_reviewed = models.BooleanField(default=False)

    class Meta:
        verbose_name = _('model kit')
        verbose_name_plural = _('model kits')

    def __str__(self):
        return u"{brand} - {name}".format(brand=self.brand, name=self.name)

    def save(self, *args, **kwargs):
        """
        Always perform a full clean if we're adding new objects.
        """
        if not self.id:
            self.full_clean()
        super(ModelKit, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('kitreviews:kit_detail', args=[self.id])

    def clean(self):
        super(ModelKit, self).clean()

        if self.kit_number and not self.id:
            # validate the uniqueness of kitnumber, scale and brand only if a kit number is supplied
            model = self.__class__
            kits = model.objects.filter(brand=self.brand, kit_number=self.kit_number, scale=self.scale)
            if kits.exists():
                error = _('A kit from {brand} with kut number \'{kit_number}\' already exists')
                raise ValidationError(error.format(brand=self.brand, kit_number=self.kit_number))

    def has_box_image(self):
        if not self.box_image:
            return False
        return self.box_image.storage.exists(self.box_image.name)
