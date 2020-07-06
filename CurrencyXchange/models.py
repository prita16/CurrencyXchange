from django.db import models
import uuid
from django.contrib.auth.models import User

class WalletDetails(models.Model):
	wallet_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	wallet_amount = models.FloatField(default=0, null=True)
	currency_choices=(
		('USD', 'USD'),
		('INR', 'INR'),
		('AUD', 'AUD'),
		('EUR', 'EUR')
	)
	currency_type= models.CharField(max_length=3, choices=currency_choices)
	currency_to = models.CharField(max_length=5)
	description = models.CharField(max_length=100)
	method_choices=(
		('netbanking', 'netbanking'),
		('card', 'card')
	)
	file = models.FileField(blank=False, null=False)
	payment_mode = models.CharField(max_length=50, choices=method_choices)
	_id = models.OneToOneField(User, on_delete=models.CASCADE, db_column='id')
	timestamp = models.DateTimeField(auto_now_add=True, editable=False)
