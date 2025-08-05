from django.db import models
from django.contrib.auth.models import User


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Plan(BaseModel):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    duration_days = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.name} - ${self.price} for {self.duration_days} days"


class Subscription(BaseModel):
    ACTIVE = "active"
    CANCELLED = "Cancelled"
    EXPIRED = "Expired"

    STATUS_CHOICES = [
        (ACTIVE, "Active"),
        (CANCELLED, "Cancelled"),
        (EXPIRED, "Expired"),
    ]

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="user_subscriptions"
    )
    plan = models.ForeignKey(
        Plan, on_delete=models.CASCADE, related_name="plan_subscriptions"
    )
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=ACTIVE)

    def __str__(self):
        return f"{self.user.username} - {self.plan.name} - ({self.status})"


class ExchangeRateLog(models.Model):
    base_currency = models.CharField(max_length=3)
    target_currency = models.CharField(max_length=3)
    rate = models.DecimalField(max_digits=10, decimal_places=2)
    fetched_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Time: {self.fetched_at}, 1 {self.base_currency} = {self.rate} {self.target_currency}."
