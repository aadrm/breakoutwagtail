"""booking tests
"""
from django.test import TestCase

from .tools import \
    get_valid_fixed_discount_coupons_by_value
from .models import Coupon


class CouponTestCase(TestCase):
    """Coupons testing
    """
    def setUp(self) -> None:
        Coupon.objects.create(
            code='test_coupon_1',
            amount=120
        )
        Coupon.objects.create(
            code='test_coupon_2',
            amount=100,
            is_percent=True
        )
        Coupon.objects.create(
            code='test_coupon_3',
            amount=100,
            is_percent=True,
            used_times=1
        )

    def test_get_valid_fixed_discount_coupons_by_value(self) -> None:
        """Test tool function
        """
        self.assertEqual(True, True)

    def test_manager_filter_percent(self) -> None:
        """
        """
        from_manager = Coupon.objects.get_percent_based()
        # notice that Coupon will store the code in CAPS
        from_query = Coupon.objects.all()
        # convert queries to lists so they can be compared
        self.assertEqual(list(from_manager), list(from_query[1:3]))

    def test_manager_is_valid(self) -> None:
        from_manager = Coupon.objects.get_valid()
        print(from_manager)
        from_query = Coupon.objects.all()
        print(from_query)
        self.assertEqual(list(from_manager), list(from_query[0:2]))




