#Copyright (c) Kevin Ochieng all rights deserved
from django.shortcuts import render, redirect
from .models import Stock
from .forms import StockForm
from django.contrib import messages

def home(request):
	import requests
	import json

	if request.method == 'POST':
		ticker = request.POST['ticker']
		api_request = requests.get("https://cloud.iexapis.com/stable/stock/" + ticker + "/quote?token=pk_8e69579dfbab4b5ba539bfd4495ed048")
		
		errorFound = False
		error = ''
		try:
			api = json.loads(api_request.content)
		except Exception as err:
			errorFound = True
			api = str(err)
			error = str(err)
		context = {
			'api':api,
			'errorFound':errorFound,
			'errorMessage':error
		}		
		return render(request, 'quotes/home.html', context)
	else:
		context = {
			'api':None,
			'errorFound':False,
			'ticker':'Enter a Ticker symbol above...'
		}				
		return render(request, 'quotes/home.html', context)

def about(request):

	context = {}
	return render(request, 'quotes/about.html', context)

def add_stock(request):
	import requests
	import json
	if request.method == 'POST':
		form = StockForm(request.POST or None)

		if form.is_valid():
			form.save()
			messages.success(request, ("Stock has been added"))
			return redirect('quotes:add_stock')
	else:
		stocks = Stock.objects.all()
		apis = []

		for ticker_item in stocks:
			api_request = requests.get("https://cloud.iexapis.com/stable/stock/" + str(ticker_item) + "/quote?token=pk_8e69579dfbab4b5ba539bfd4495ed048")
			
			errorFound = False
			error = ''
			try:
				api = json.loads(api_request.content)
				apis.append(api)
			except Exception as err:
				errorFound = True
				api = str(err)
				error = str(err)
				break

		context = {
			'apis':apis,
			'errorFound':errorFound,
			'errorMessage':error,
			'stocks': stocks
		}	

		return render(request, 'quotes/add_stock.html', context)

def delete(request, stock_id):
	item = Stock.objects.get(pk=stock_id)
	item.delete()
	messages.success(request, ("Stock has been deleted"))
	return redirect('quotes:delete_stock')

def delete_stock(request):
	stocks = Stock.objects.all()
	context = {'stocks' : stocks}
	return render(request, 'quotes/delete_stock.html', context)
	