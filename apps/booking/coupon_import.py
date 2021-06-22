
import csv
from datetime import timedelta
from django.utils import timezone
from .models import Coupon

# name, code, amount, is_percent, created, expiry

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

