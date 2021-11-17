from django.db import models
from django.contrib.auth.models import User


class Order(models.Model):
    payment_type = models.ForeignKey(
        "PaymentType", on_delete=models.CASCADE, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_on = models.DateTimeField(auto_now_add=True)
    completed_on = models.DateTimeField(null=True, blank=True)
    products = models.ManyToManyField("Product", through="OrderProduct")
