"""Tools for coupon management
"""
import csv
from datetime import timedelta
from decimal import Decimal
from typing import List

from django.utils import timezone
from django.db.models import F

from .models import Coupon

def get_valid_fixed_discount_coupons_by_value(discount: Decimal) -> 'QuerySet[Coupon]':
    """Find fixed discount coupons by value

    Args:
        discount (Decimal): the amount of the coupon's to filter by

    Returns:
        QuerySet[Coupon]: coupons with the value passed as argument 
    """
    return Coupon.objects.get_valid() \
        .get_fixed_discount_based() \
        .filter(amount=discount)


def update_valid_fixed_coupon_value(*, old: Decimal, new: Decimal) -> None:
    """Modify the value of fixed value coupons

    Args:
        old (Decimal): Current value
        new (Decimal): Value to be updated to
    """
    coupons_to_update = get_valid_fixed_discount_coupons_by_value(old)
    if coupons_to_update:
        print('--- Coupons found ----')
        print(coupons_to_update)
        coupons_to_update.update(amount=new)
        print(f'--value updated from {old} to {new}')
    else:
        print(f'No valid coupons found with value: {old}')



def import_coupons():
    with open('cpn.csv', 'r') as cpnfile:
        csvreader = csv.DictReader(cpnfile, delimiter=',')
        coupons = []

        for row in csvreader:
            c = Coupon()
            c.code = row['code']
            c.amount = row['amount'] 
            if row['percent'] == "True":
                c.is_percent = True
            c.created = timezone.now() 
            c.expiry = timezone.now() + timedelta(days=365)
            c.name = row['name']
            c.save()

    for coupon in coupons:
        print(coupon)
