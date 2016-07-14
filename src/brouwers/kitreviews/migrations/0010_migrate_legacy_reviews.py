# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-07-06 16:57
from __future__ import unicode_literals

from HTMLParser import HTMLParser
from urlparse import urlparse, parse_qs

from django.conf import settings
from django.db import migrations, models
from django.utils import timezone

from faker import Faker

FABRIKANT_MAPPING = {}
REVIEWER_MAPPING = {}
KIT_MAPPING = {}
SCALE_MAPPING = {}

faker = Faker()


def migrate_brands(apps):
    Fabrikant = apps.get_model('kitreviews', 'Fabrikant')
    Brand = apps.get_model('kits', 'Brand')

    brands = Brand.objects.all()
    brands = {brand.name.lower(): brand for brand in brands}

    parser = HTMLParser()

    fabrikanten = Fabrikant.objects.using('kitreviews')
    for fabrikant in fabrikanten:
        name = parser.unescape(fabrikant.naam)
        try:
            brand = brands[name.lower()]
        except KeyError:
            brand = Brand.objects.create(name=name)

        if fabrikant not in FABRIKANT_MAPPING:
            FABRIKANT_MAPPING[fabrikant] = brand


def migrate_reviewers(apps):
    Reviewer = apps.get_model('kitreviews', 'Reviewer')
    User = apps.get_model('users', 'User')

    reviewers = Reviewer.objects.using('kitreviews')
    emails = list(reviewers.values_list('emailadres', flat=True).distinct())
    users = User.objects.filter(email__in=emails)
    users = {user.email.lower(): user for user in users}

    for i, reviewer in enumerate(reviewers):
        try:
            user = users[reviewer.emailadres.lower()]
        except KeyError:
            user = User.objects.create(
                email=reviewer.emailadres,
                first_name=reviewer.naam,
                username='fixme_{}{}'.format(i, faker.user_name()[:25])
            )
            users[reviewer.emailadres.lower()] = user

        if user not in REVIEWER_MAPPING:
            REVIEWER_MAPPING[reviewer] = user


def migrate_kits(apps):
    Kit = apps.get_model('kitreviews', 'Kit')
    ModelKit = apps.get_model('kits', 'ModelKit')
    Scale = apps.get_model('kits', 'Scale')
    User = apps.get_model('users', 'User')

    first_user = User.objects.order_by('id').first()

    modelkits = {}
    for model_kit in ModelKit.objects.select_related('brand', 'scale'):
        modelkits.setdefault(model_kit.brand, {})
        modelkits[model_kit.brand].setdefault(model_kit.scale, [])
        modelkits[model_kit.brand][model_kit.scale].append(model_kit)

    scales = {scale.scale: scale for scale in Scale.objects.all()}

    for kit in Kit.objects.using('kitreviews').select_related('fabrikant'):
        brand = FABRIKANT_MAPPING[kit.fabrikant]
        try:
            scale = scales[kit.schaal]
        except KeyError:
            scale = Scale.objects.create(scale=kit.schaal)
            scales[kit.schaal] = scale

        try:
            _scales = modelkits[brand]
        except KeyError:
            modelkits[brand] = {}
        try:
            _kits = _scales[scale]
        except KeyError:
            modelkits[brand][scale], _kits = [], []

        parser = HTMLParser()

        def set_model_kit_image(model_kit):
            if kit.foto and not model_kit.box_image:
                model_kit.box_image = 'kits/box_images/legacy/{}'.format(kit.foto)
                model_kit.save()

        model_kit = next((x for x in _kits if x.kit_number == kit.type), None)
        if model_kit is not None:
            set_model_kit_image(model_kit)
            KIT_MAPPING[kit] = model_kit
            continue

        name = parser.unescape(kit.modelnaam)
        model_kit = next((x for x in _kits if x.name.lower() == name.lower()), None)
        if model_kit is not None:
            set_model_kit_image(model_kit)
            KIT_MAPPING[kit] = model_kit
            continue

        model_kit = ModelKit.objects.create(
            brand=brand, scale=scale, name=name,
            difficulty=10 * kit.moeilijkheid, submitter=first_user,
            is_reviewed=False
        )
        set_model_kit_image(model_kit)
        KIT_MAPPING[kit] = model_kit


def migrate_reviews(apps):
    Review = apps.get_model('kitreviews', 'Review')
    KitReview = apps.get_model('kitreviews', 'KitReview')
    AlbumMigration = apps.get_model('migration', 'AlbumMigration')
    KitReviewProperty = apps.get_model('kitreviews', 'KitReviewProperty')
    KitReviewPropertyRating = apps.get_model('kitreviews', 'KitReviewPropertyRating')

    all_properties = KitReviewProperty.objects.all()

    album_migrations = {x.id: x for x in AlbumMigration.objects.all()}

    for review in Review.objects.using('kitreviews').select_related('kit', 'reviewer'):
        model_kit = KIT_MAPPING[review.kit]
        reviewer = REVIEWER_MAPPING[review.reviewer]

        kit_review = KitReview(
            model_kit=model_kit, reviewer=reviewer,
            submitted_on=review.datum or timezone.now(),
            legacy_id=review.pk
        )

        if review.url_album.startswith('coppermine/'):
            qs = urlparse(review.url_album).query
            qs = parse_qs(qs)
            if 'album' in qs:
                try:
                    album_id = int(qs['album'][0])
                except (ValueError, TypeError):
                    pass
                try:
                    kit_review.album = album_migrations[album_id].new_album
                except KeyError:
                    pass

        if review.url_bouwverslag_twenot:
            kit_review.external_topic_url = review.url_bouwverslag_twenot

        qs_topic = urlparse(review.url_bouwverslag_mb).query
        if qs_topic:
            try:
                topic_id = int(parse_qs(qs_topic).get('t')[0])
            except (KeyError, ValueError, TypeError):
                pass
            else:
                kit_review.topic_id = topic_id

        kit_review.raw_text = "{}\n\n\n{}\n\n\n{}".format(
            review.commentaar,
            review.pluspunten,
            review.minpunten,
        )
        kit_review.save()
        ratings = [KitReviewPropertyRating(
            prop=prop, kit_review=kit_review, rating=review.indruk * 20
        ) for prop in all_properties]
        KitReviewPropertyRating.objects.bulk_create(ratings)


def migrate(apps, schema_editor):
    if settings.TESTING:
        return
    migrate_brands(apps)
    migrate_reviewers(apps)
    migrate_kits(apps)
    migrate_reviews(apps)


class Migration(migrations.Migration):

    dependencies = [
        ('migration', '0002_auto_20150405_2118'),
        ('kits', '0008_auto_20160406_2154'),
        ('kitreviews', '0010_add_legacy_id_field'),
    ]

    operations = [
        migrations.SeparateDatabaseAndState(
            state_operations=[
                migrations.AlterField(
                    model_name='kitreview',
                    name='submitted_on',
                    field=models.DateTimeField(auto_now_add=False, editable=True)
                )
            ]
        ),
        migrations.RunPython(migrate, migrations.RunPython.noop),
        migrations.SeparateDatabaseAndState(
            state_operations=[
                migrations.AlterField(
                    model_name='kitreview',
                    name='submitted_on',
                    field=models.DateTimeField(auto_now_add=True, editable=False)
                )
            ]
        ),
    ]
