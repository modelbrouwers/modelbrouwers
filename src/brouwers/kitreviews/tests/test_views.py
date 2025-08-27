import random

from django.urls import reverse
from django.utils.translation import gettext as _

from django_webtest import WebTest

from brouwers.albums.tests.factories import AlbumFactory
from brouwers.forum_tools.tests.factories import ForumUserFactory, TopicFactory
from brouwers.kits.models import Brand
from brouwers.kits.tests.factories import ModelKitFactory
from brouwers.users.tests.factories import UserFactory
from brouwers.utils.tests.mixins import LoginRequiredMixin, WebTestFormMixin
from brouwers.utils.tests.recaptcha import mock_recaptcha

from ..models import KitReview
from .factories import KitReviewFactory, KitReviewPropertyFactory


class IndexViewTests(WebTest):
    def setUp(self):
        super().setUp()
        self.url = reverse("kitreviews:index")

    def test_index_shows_latest_reviews(self):
        """
        Assert that the index page shows the latest 5 reviews and (TODO) a form
        to search for a kit.
        """
        kitreviews = KitReviewFactory.create_batch(10)
        index = self.app.get(self.url)
        expected = [repr(review) for review in kitreviews[5:]]
        expected.reverse()
        self.assertQuerySetEqual(index.context["reviews"], expected, transform=repr)


class AddReviewViewTests(WebTestFormMixin, LoginRequiredMixin, WebTest):
    """
    Tests for the 'add a kit review' page.
    """

    def setUp(self):
        super().setUp()
        self.url = reverse("kitreviews:add_review")

    def test_submit_review(self):
        """
        Asserts that submitting a review is only possible as logged in user.
        """
        # test that auth is required
        add_page = self.app.get(self.url)
        self._test_login_required(self.url, response=add_page)

        # add some test data - dummy albums etc.
        user = UserFactory.create()
        invalid_albums = AlbumFactory.create_batch(3)
        AlbumFactory.create_batch(4, user=user)
        kits = ModelKitFactory.create_batch(3)
        KitReviewPropertyFactory.create_batch(3)

        self.assertFalse(KitReview.objects.exists())
        add_page = self.app.get(self.url, user=user)
        form = add_page.forms[0]

        # try some invalid input
        self.assertNotIn(
            "model_kit", form.fields
        )  # no kit submitted - a review must belong to a kit
        with self.assertRaises(ValueError):
            form["album"].select(
                str(random.choice(invalid_albums).pk)
            )  # an album from a different user
        form["raw_text"] = ""  # empty review

        response = form.submit()
        _form = response.context["form"]
        self.assertFormError(_form, "raw_text", errors=[_("This field is required.")])
        self.assertFormError(_form, "model_kit", errors=[_("This field is required.")])

        # now select a kit
        kit = random.choice(kits)
        self._add_field(form, "model_kit", str(kit.pk))
        # and enter a review text
        form["raw_text"] = "My very short review"

        response = form.submit()
        review = KitReview.objects.get()
        self.assertRedirects(response, review.get_absolute_url())
        self.assertEqual(review.ratings.count(), 3)
        self.assertEqual(review.model_kit, kit)
        self.assertEqual(review.raw_text, "My very short review")
        self.assertEqual(review.reviewer, user)

    def test_submit_review_for_kit(self):
        kit = ModelKitFactory.create()
        user = UserFactory.create()
        url = reverse("kitreviews:review-add", kwargs={"slug": kit.slug})
        add_page = self.app.get(url, user=user)
        form = add_page.forms[0]
        self._add_field(form, "model_kit", kit.pk)
        form["raw_text"] = "My review with newlines\nFoo"

        response = form.submit()

        review = KitReview.objects.get()
        self.assertRedirects(response, review.get_absolute_url())
        self.assertEqual(review.model_kit, kit)
        self.assertEqual(review.raw_text, "My review with newlines\nFoo")
        self.assertEqual(review.reviewer, user)

    def test_submit_review_with_topic(self):
        """
        Assert that only the relevant topics are listed.
        """
        kit = ModelKitFactory.create()
        user = UserFactory.create()
        forum_user = ForumUserFactory.create(username=user.username)
        user.forumuser_id = forum_user.pk
        user.save()

        topic1 = TopicFactory.create()
        topic2 = TopicFactory.create(author=forum_user)

        url = reverse("kitreviews:review-add", kwargs={"slug": kit.slug})
        add_page = self.app.get(url, user=user)

        form = add_page.forms[0]

        # non-authored topics may not be shown
        with self.assertRaisesRegex(
            ValueError, rf"^Option {topic1.pk} not found \(from"
        ):
            form["topic"].select(topic1.pk)
        form["topic"].select(topic2.pk)
        form["raw_text"] = "Dummy review"
        self._add_field(form, "model_kit", kit.pk)

        form.submit().follow()

        review = KitReview.objects.get()
        self.assertEqual(review.topic, topic2)


class SearchViewTests(WebTest):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.url = reverse("kitreviews:find_kit")

        cls.kit1 = ModelKitFactory.create(name="Suzuki Katana")
        cls.kit2 = ModelKitFactory.create(name="MiG-17F")
        cls.kit3 = ModelKitFactory.create(name="Challenger Mk. IV", kit_number="1234")

        cls.reviews = [
            KitReviewFactory.create(model_kit=cls.kit1),
            KitReviewFactory.create(model_kit=cls.kit2),
        ]

    def test_search_form(self):
        """
        Test that the search form works as expected.
        """

        with self.subTest(search_by="brand"):
            search_page = self.app.get(self.url)
            form = search_page.forms[0]
            form["brand"].select(self.kit1.brand.pk)
            search_results = form.submit()
            queryset = search_results.context["kits"]
            self.assertQuerySetEqual(queryset, [repr(self.kit1)], transform=repr)
            self.assertEqual(queryset[0].num_reviews, 1)

        with self.subTest(search_by="scale"):
            search_page = self.app.get(self.url)
            form = search_page.forms[0]
            form["scale"].select(self.kit2.scale.pk)
            search_results = form.submit()
            queryset = search_results.context["kits"]
            self.assertQuerySetEqual(queryset, [repr(self.kit2)], transform=repr)
            self.assertEqual(queryset[0].num_reviews, 1)

        with self.subTest(search_by="name"):
            search_page = self.app.get(self.url)
            form = search_page.forms[0]
            form["kit_name"] = "challenger"
            search_results = form.submit()
            self.assertQuerySetEqual(
                search_results.context["kits"], [repr(self.kit3)], transform=repr
            )

        with self.subTest(search_by="name 2"):
            search_page = self.app.get(self.url)
            form = search_page.forms[0]
            form["kit_name"] = "katana"
            search_results = form.submit()
            self.assertQuerySetEqual(
                search_results.context["kits"], [repr(self.kit1)], transform=repr
            )

        with self.subTest(search_by="kit_number"):
            search_page = self.app.get(self.url)
            form = search_page.forms[0]
            form["kit_number"] = "1234"
            search_results = form.submit()
            self.assertQuerySetEqual(
                search_results.context["kits"], [repr(self.kit3)], transform=repr
            )

    def test_invalid_search_form(self):
        """
        Test invalid search form input
        """
        # search by brand
        max_pk = Brand.objects.order_by("pk").last().pk
        response = self.client.get(self.url, {"brand": max_pk + 1})
        self.assertIn("brand", response.context["form"].errors)
        self.assertNotIn("kits", response.context)

    def test_posting_works(self):
        """
        Not intended, but it should work too
        """
        # search by brand
        response = self.client.post(self.url, {"brand": self.kit1.brand.pk})
        queryset = response.context["kits"]
        self.assertQuerySetEqual(queryset, [repr(self.kit1)], transform=repr)
        self.assertEqual(queryset[0].num_reviews, 1)

    @mock_recaptcha(is_valid=True, action="login")
    def test_anonymous_add_kit(self, m):
        """
        When not logged in, you may not get the popup to add a kit, but you must
        be presented with a login button.
        """
        # search by brand
        search_page = self.app.get(self.url)
        form = search_page.forms[0]
        form["kit_name"] = "gibberish"
        search_results = form.submit()
        queryset = search_results.context["kits"]
        self.assertFalse(queryset.exists())

        search_url = search_results.request.url

        self.assertEqual(len(search_results.forms), 2)
        login_form = search_results.forms[1]
        self.assertEqual(login_form.action, reverse("users:login"))
        login_page = login_form.submit()

        user = UserFactory.create(password="letmein")
        login_page.form["username"] = user.username
        login_page.form["password"] = "letmein"
        login_page.form["captcha"] = "dummy"
        search_results = login_page.form.submit().follow()
        self.assertEqual(search_results.request.url, search_url)
        self.assertContains(search_results, _("Add kit"))


class KitReviewsListViewTests(WebTest):
    def setUp(self):
        super().setUp()

        self.kit1 = ModelKitFactory.create()
        self.reviews1 = KitReviewFactory.create_batch(3, model_kit=self.kit1)
        self.kit2 = ModelKitFactory.create()
        self.reviews2 = KitReviewFactory.create_batch(1, model_kit=self.kit2)

        self.url = reverse("kitreviews:review-list", kwargs={"slug": self.kit1.slug})

    def test_correct_reviews_list(self):
        kit_detail = self.app.get(self.url)
        reviews = kit_detail.context["object_list"]
        expected_reviews = [repr(x) for x in self.reviews1]
        # TODO: ordering comes later - we'll order by review votes
        self.assertQuerySetEqual(
            reviews, expected_reviews, ordered=False, transform=repr
        )


class LegacyRedirectViewTests(WebTest):
    """
    Ensure that the old links still work
    """

    def test_redirect(self):
        url = "/kitreviews/kitreview_search_result_review.php"
        review = KitReviewFactory.create(legacy_id=42)

        # test success
        response = self.app.get(url, params={"review": "42"})
        self.assertRedirects(response, review.get_absolute_url(), status_code=301)

        response = self.app.get(url, params={"review": 42, "kit": "abcdefgh"})
        self.assertRedirects(response, review.get_absolute_url(), status_code=301)

        # test error handling
        self.app.get(url, params={"review": "abcdefgh"}, status=404)
        self.app.get(url, status=404)

        # test valid input, but unknown kit
        response = self.app.get(url, params={"review": 41}, status=404)
