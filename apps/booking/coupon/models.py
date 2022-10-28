"""Coupon Model
"""
from datetime import datetime, timedelta
from django.utils.crypto import get_random_string
from django.db import models
from django.db.models import QuerySet


class CouponQueryset(models.QuerySet):
    """ Common queries for the Coupon class
    """
    def get_percent_based(self) -> 'QuerySet[Coupon]':
        """ Get coupons with percent discount

        Returns:
            QuerySet: Coupons with percent based discount
        """
        return self.filter(is_percent=True)

    def get_fixed_discount_based(self) -> 'QuerySet[Coupon]':
        """ Get coupons with a fixed discount

        Returns:
            QuerySet[Coupon]: Coupons with fixed value discount
        """
        return self.filter(is_percent=False)

    def get_valid(self) -> 'QuerySet[Coupon]':
        """ Get valid coupons

        Returns:
            QuerySet: Coupons that have not passed usage limit or date limit
        """
        coupons = self.annotate(
            remaining_uses=models.ExpressionWrapper(
                models.F('use_limit') - models.F('used_times'),
                output_field=models.IntegerField()
            )
        )
        coupons = coupons.annotate(
            expired=models.ExpressionWrapper(
                models.F('expiry') - models.Value(datetime.now().date()),
                output_field=models.DurationField()
            )
        )
        return coupons.filter(remaining_uses__gt=0, expired__gt=timedelta(0))


class Coupon(models.Model):
    """ Coupon
    """
    objects = CouponQueryset.as_manager()

    def now_plus_time():
        return datetime.today() + timedelta(days=1095)

    def code_in_bulk(objs):
        allowed_chars = ('ABCDEFGHJKMNPRTWXYZ2346789')
        # allowed_chars = ('AB')
        unique = False
        while not unique:
            codes = []
            for obj in objs:
                obj.code = get_random_string(12, allowed_chars)
                codes.append(obj.code)

            if len(set(codes)) == len(codes):
                coupons_same_slug = Coupon.objects.filter(code__in=codes)
                if len(coupons_same_slug) == 0:
                    unique = True

    name = models.CharField("reference", max_length=255, blank=True, null=True)
    code = models.SlugField("code", max_length=32, blank=True, unique=True)
    amount = models.DecimalField("discount amount", max_digits=5, decimal_places=2, default=0)
    is_percent = models.BooleanField("is percent", default=False)
    is_apply_to_basket = models.BooleanField("entire basket", default=False)
    is_individual_use = models.BooleanField("can't be combined", default=True)
    is_overrule_individual_use = models.BooleanField("can be combined", default=False)
    is_upgrade = models.BooleanField("Upgrades the item", default=False)
    product_families_included = models.ManyToManyField("booking.ProductFamily", related_name="product_family_include", verbose_name=" include families", blank=True)
    product_families_excluded = models.ManyToManyField("booking.ProductFamily", related_name="product_family_exclude", verbose_name=" exclude families", blank=True)
    product_included = models.ManyToManyField("booking.Product", related_name="product_include", verbose_name="include product", blank=True)
    product_excluded = models.ManyToManyField("booking.Product", related_name="product_exclude", verbose_name="exclude product", blank=True)
    used_times = models.IntegerField("Used times", default=0)
    use_limit = models.IntegerField("Usage limit", default=1)
    created = models.DateTimeField("Created", auto_now=True, auto_now_add=False)
    expiry = models.DateField('Expiration date', blank=True, null=True, default=now_plus_time)
    minimum_spend = models.DecimalField("Minimum spend", max_digits=5, decimal_places=2, default=0)
    dow_valid = models.PositiveSmallIntegerField("Days Valid", default=127) 

    class Meta:
        verbose_name = "Coupon"
        verbose_name_plural = "Coupons"

    def __str__(self):
        return f'{self.code}' + (" %" if self.is_percent else " €") + f'{self.amount}'

    @property
    def is_expired(self):
        is_expired = False
        if self.expiry:
            if self.expiry < datetime.now().date():
                is_expired = True
        return is_expired

    @property
    def is_overused(self):
        if self.use_limit:
            if self.used_times >= self.use_limit:
                return True
            else:
                return False
        else:
            return True

    @property
    def is_valid(self):
        if self.is_overused or self.is_expired:
            return False
        else:
            return True

    @property
    def dow_as_binarylist(self):
        """returns a list of binary digits in reverse from converting the integer that represents the days of the week
        for instance int 1 is 0000001 binary and represents mondays only, 127 is 1111111, which would represent
        every day form sunday to monday"""
        binlist = list('{0:07b}'.format(self.dow_valid))
        binlist.reverse()
        return [int(x) for x in binlist]

    @property
    def dow_as_integerlist(self):
        """returns a list of integers corresponding to the day of the week that the schedule
        affects, monday=0 sunday=6, e.g. [2, 4, 6] means Wednesday, Friday, Sunday"""
        dow_binary_list = self.dow_as_binarylist
        dow_integer_list = list()
        for i, d in enumerate(dow_binary_list):
            if d:
                dow_integer_list.append(i)
        return dow_integer_list

    def add_used_time(self):
        """Increases the counter that tracks how many times a coupon has been applied"""
        self.used_times += 1
        self.save()

    def get_absolute_url(self):
        return reverse("Coupon_detail", kwargs={"pk": self.pk})

    def save(self, *args, **kwargs):
        """ Add Slug creating/checking to save method. """
        self.code_save()
        super(Coupon, self).save(*args, **kwargs)

    def code_save(obj):
        allowed_chars = ('ABCDEFGHJKLMNPQRSTUVWXYZ23456789')
        in_set = type(obj).objects.all()
        
        if not obj.code:
            obj.code = get_random_string(12, allowed_chars)
            code_is_wrong = True
            while code_is_wrong:  # keep checking until we have a valid slug
                code_is_wrong = False
                other_coupons_with_same_slug = in_set.filter(code=obj.code)
                if len(other_coupons_with_same_slug) > 0:
                    code_is_wrong = True
                if code_is_wrong:
                    obj.code = get_random_string(12, allowed_chars)
        else:
            obj.code = obj.code.upper()

    def products_included_queryset(self):
        """returns a queryset with the all the producs related in the fields products_included and
        the product_families_included"""
        products = self.product_included.all()
        families = self.product_families_included.all()

        for family in families:
            family_products = family.products.all()
            products = (products | family_products)

        return products.distinct()

    def products_excluded_queryset(self):
        """returns a queryset with the all the producs related in the fields products_excluded and
        the product_families_excluded"""
        products = self.product_excluded.all()
        families = self.product_families_excluded.all()

        for family in families:
            family_products = family.products.all()
            products = (products | family_products)

        return products.distinct()

    def products_applicable_queryset(self):
        """returns a queryset to with the products to which the coupon is applicable to"""
        if self.products_included_queryset():
            included_products = self.products_included_queryset()
        else:
            included_products = Product.objects.all()

        excluded_products = self.products_excluded_queryset()
        products = Product.objects.filter(pk__in=included_products).exclude(pk__in=excluded_products)
        return products

    def is_applicable(self, product):
        """checks wether the may be applied to certain product"""
        return product in self.products_applicable_queryset()

    def apply_to_cart_item(self, item, cumulative_discount, cart_coupon):
        price = item.price
        price_before = price
        used = False
        if self.is_percent:
            price = (1 - self.amount / 100) * price
            used = True
        elif self.is_upgrade:
            price = item.product.upgrade_price
            used = True
        else:
            price = price - (self.amount - cumulative_discount)
            used = True
            if price < 0:
                price = 0
        if used:
            item.cart_coupons.add(cart_coupon)
            item.price = price
            item.save()
            cumulative_discount += (price_before - price)
        return cumulative_discount
