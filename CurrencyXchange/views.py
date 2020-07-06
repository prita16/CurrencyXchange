# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import JsonResponse
from django.views.generic import View
import traceback
import sys
import requests
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate, login
from .models import WalletDetails
import json
from rest_framework.parsers import MultiPartParser, FileUploadParser

from rest_framework.views import APIView
from rest_framework import status

class Signup(View):
	"""Class Based API for User Auth SignUp."""

	def post(self, request, *args, **kwargs):
		try:
			username = request.POST.get('username', None)
			password = request.POST.get('password', None)

			if 'username' in request.POST and 'password' in request.POST:
				user = User.objects.create_user(username=username,
												password=password)
				user.save()
				return JsonResponse({"Result":"success"}, status=200)
			else:
				return JsonResponse({"Result":"failed"}, status=400)
		except Exception as e:
			print(traceback.print_exc(file=sys.stdout))
			return JsonResponse({"Result":traceback.print_exc(file=sys.stdout)}, status=500)
		

class SignIn(View):
	"""Class Based API for User Auth SignIn."""

	def post(self, request, *args, **kwargs):
		try:
			username = request.POST.get('username', None)
			password = request.POST.get('password', None)

			user = authenticate(username=username, password=password)
			if user is not None:
				return JsonResponse({"Result":"success"}, status=200)
			else:
				return JsonResponse({"Result":"Not User"}, status=400)
		except Exception as e:
			print(traceback.print_exc(file=sys.stdout))
			return JsonResponse({"Result":traceback.print_exc(file=sys.stdout)}, status=500)


class CreateWallet(View):
	"""Class Based API for creating a e-wallet."""

	def post(self, request, *args, **kwargs):
		try:
			username = request.POST.get('username', None)
			wallet_amount = request.POST.get('wallet_amount', None)
			payment_mode = request.POST.get('payment_mode', None)
			currency_type = request.POST.get('currency_type', None)

			if User.objects.filter(username=username).exists():
				try:
					db_user = User.objects.get(username=username)
					_obj = WalletDetails()
					_obj._id_id=db_user.id

					try:
						if float(wallet_amount)>0:
							_obj.wallet_amount = float(wallet_amount)
						else:
							return JsonResponse({"Result":"wallet amount should be greater than 0."}, status=400)
					except Exception as e:
						return JsonResponse({"Result":"wallet amount should be in number."}, status=400)
					
					if payment_mode == 'netbanking' or payment_mode == 'card':
						_obj.payment_mode = str(payment_mode)
					else:
						return JsonResponse({"Result":"payment mode must be 'netbanking' or 'card'."}, status=400)
					
					if (currency_type).upper() == 'INR' or currency_type .upper()== 'USD' or currency_type.upper() == 'EUR' or currency_type.upper() == 'AUD':
						_obj.currency_type = str(currency_type)
					else:
						return JsonResponse({"Result":"currency type must be INR/USD/EUR/AUD"}, status=400)
					_obj.save()
					return JsonResponse({"Result":"created successfully."}, status=201)
			   
				except Exception as e:
					return JsonResponse({"Result":"Already exists"}, status=400)
			else:
				return JsonResponse({"Result":"User does not exists"}, status=400)
		except Exception as e:
			print(traceback.print_exc(file=sys.stdout))
			return JsonResponse({"Result":traceback.print_exc(file=sys.stdout)}, status=500)



class ReadWallet(View):
	"""Class Based API for reading a e-wallet balance."""

	def get(self, request, *args, **kwargs):
		try:
			username = request.GET.get('username', None)
			if User.objects.filter(username=username).exists():
				try:
					db_user = User.objects.get(username=username)
					wlt_obj = WalletDetails.objects.get(_id_id=db_user.id)
					return JsonResponse({"Result":"Success", "Wallet Amount":wlt_obj.wallet_amount, "Currency Type": (wlt_obj.currency_type).upper() }, status=200)
				except Exception as e:
					return JsonResponse({"Result":"Failed"}, status=400)
			else:
				return JsonResponse({"Result":"User does not exists"}, status=400)
		except Exception as e:
			return JsonResponse({"Result":traceback.print_exc(file=sys.stdout)}, status=500)


class UpdateWallet(View):
	"""Class Based API for update e-wallet balance."""

	def post(self, request, *args, **kwargs):
		try:
			username = request.POST.get('username', None)
			add_amt = request.POST.get('add_amount', None)

			if User.objects.filter(username=username).exists():
				try:
					db_user = User.objects.get(username=username)
					wlt_obj = WalletDetails.objects.get(_id_id=db_user.id)
					try:
						if float(add_amt)>0:
							final_amt=wlt_obj.wallet_amount+float(add_amt)
						else:
							return JsonResponse({"Result":"wallet amount should be greater than 0."}, status=400)
					except Exception as e:
						print(e)
						return JsonResponse({"Result":"wallet amount should be in number."}, status=400)
					wlt_obj.wallet_amount=final_amt
					wlt_obj.save()
					return JsonResponse({"Result":"Success", "Wallet Amount":final_amt, "Currency Type": (wlt_obj.currency_type).upper() }, status=200)
				except Exception as e:
					print(e)
					return JsonResponse({"Result":"Failed"}, status=400)
			else:
				return JsonResponse({"Result":"User does not exists"}, status=400)
		except Exception as e:
			return JsonResponse({"Result":traceback.print_exc(file=sys.stdout)}, status=500)


class ConvertCurrency(View):
	"""Class Based API for convert currency."""

	def post(self, request, *args, **kwargs):
		try:
			username = request.POST.get('username', None)
			currency_to = request.POST.get('currency_convert_to', None)

			if User.objects.filter(username=username).exists():
				try:
					db_user = User.objects.get(username=username)
					wlt_obj = WalletDetails.objects.get(_id_id=db_user.id)
					
					if (currency_to).upper() == 'INR' or currency_to.upper()== 'USD' or currency_to.upper() == 'EUR' or currency_to.upper() == 'AUD':
						wlt_obj.currency_to=currency_to
						wlt_obj.save()
						req_url = 'http://free.currencyconverterapi.com/api/v5/convert?q='+(wlt_obj.currency_type).upper()+'_'+(currency_to).upper()+'&compact=ultra&apiKey=698ea915b459fda1bc68'
						resp = requests.get(req_url, headers={'content-type': 'application/json'})
						_amt = json.loads(resp.text)
						merge_str = (wlt_obj.currency_type).upper()+'_'+(currency_to).upper()
						rate= _amt[merge_str]
						conv_amount = wlt_obj.wallet_amount*rate
					return JsonResponse({"Result":"Success",
										"Wallet Amount": wlt_obj.wallet_amount,
										"Currency Convert From": (wlt_obj.currency_type).upper(),
										"Currency Convert To": (currency_to).upper(),
										"After Converting (Total Amount)":round(conv_amount, 2)},
										status=200)
				except Exception as e:
					print(e)
					return JsonResponse({"Result":"Failed"}, status=400)
			else:
				return JsonResponse({"Result":"User does not exists"}, status=400)
		except Exception as e:
			return JsonResponse({"Result":traceback.print_exc(file=sys.stdout)}, status=500)


class UploadProfileImage(APIView):
	'''An API to allow users to upload a profile photo'''
	parser_class = (FileUploadParser,)

	def post(self, request, *args, **kwargs):
		try:
			username = request.POST.get('username', None)
			if User.objects.filter(username=username).exists():
				try:
					db_user = User.objects.get(username=username)
					wlt_obj = WalletDetails.objects.get(_id_id=db_user.id)
					wlt_obj.file = request.data['image']
					wlt_obj.save()
					return JsonResponse({"Result":"Success"}, status=200)
				except Exception as e:
					print(e)
					return JsonResponse({"Result":"Failed"}, status=400)
			else:
				return JsonResponse({"Result":"User does not exists"}, status=400)
		except Exception as e:
			return JsonResponse({"Result":traceback.print_exc(file=sys.stdout)}, status=500)
