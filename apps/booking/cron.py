from datetime import timedelta
from django.utils import timezone
from .models import Cart

def delete_unused_carts():
    delete_before_date = timezone.now() - timedelta(days=1)

    carts = Cart.objects.filter(timestamp__lte=delete_before_date, status=0)
    carts.delete()