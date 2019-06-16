from django.test import SimpleTestCase

from ..sisow import calculate_sha1


class Sha1Tests(SimpleTestCase):

    def test_calculate_sha1(self):
        merchantid = "2537987391"
        merchantkey = "28f31a03f4d272bb5d6dd6a345cce93b670e2f79"
        purchaseid = "123"
        amount = "100"

        sha1 = calculate_sha1(
            purchaseid=purchaseid,
            merchantid=merchantid,
            merchantkey=merchantkey,
            amount=amount,
        )

        self.assertEqual(sha1, "4bdf789f7800496d9b5883eecd7eca2bae73cd02")
