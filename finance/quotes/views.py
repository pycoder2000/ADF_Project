from django.shortcuts import render, redirect
from .models import Stock
from .forms import StockForm,NewUserForm
from django.contrib import messages
import requests
import json
from .api import *
from datetime import datetime
from django.views.generic.base import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import login
import requests
import json

def home(request):
    import requests
    import json
    if request.method == 'POST':
        ticker = request.POST['ticker']
        api_request = requests.get("https://sandbox.iexapis.com/stable/stock/" + ticker + "/quote?token=Tpk_c46f4087296c43358402984f3b26ed2f")
    
        # for error handling
        try:
            api = json.loads(api_request.content)
        #create an exception
        except Exception as e:
            api = "Sorry there is an error"
        return render(request, 'home.html', {'api': api} )
    else:
        return render(request, 'home.html', {'ticker': "Enter Ticker Symbol"} )
    
def register_request(request):
    if (request.method == "POST"):
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful." )
            return redirect("home")
        messages.error(request, "Unsuccessful registration. Invalid information.")
    form = NewUserForm()
    return render (request=request, template_name="register.html", context={"register_form":form})

def about(request):
    return render(request, 'about.html', {})

class ProfileView(LoginRequiredMixin ,TemplateView):
    template_name = 'profile.html'

def add_stock(request):
    if request.method == 'POST':
        form = StockForm(request.POST or None)
        
        if form.is_valid():
            form.save()
            messages.success(request, ("Stock ticker has been added to your Portfolio!"))
            return redirect('add_stock')
    else:
        ticker = Stock.objects.all()
        output = []
        for ticker_item in ticker:
            api_request = requests.get("https://sandbox.iexapis.com/stable/stock/" + str(ticker_item) + "/quote?token=Tpk_c46f4087296c43358402984f3b26ed2f")
            
            # for error handling
            try:
                api = json.loads(api_request.content)
                output.append(api)
            except Exception as e:
                api = "Sorry there is an error"
        return render(request, 'add_stock.html', {'ticker': ticker, 'output': output})
    
def list_stock(request):
    ticker = Stock.objects.filter(user=request.user)
    output = []
    tickerList = " ".join([t.ticker for t in ticker])
    print(tickerList)
    tickerData = GetAllStocks(tickerList)
    #tickerData = tickerData.summary_detail.update(tickerData.price)
    #print(tickerData.summary_detail)
    return render(request, 'stockList.html', {'ticker':tickerData.summary_detail|tickerData.price, 'output':output})


def delete(request, stock_id):
    item = Stock.objects.get(pk=stock_id)
    item.delete()
    messages.success(request, ("Stock ticker has been removed from your Portfolio!"))
    return redirect(delete_stock)


def delete_stock(request):
    ticker = Stock.objects.all()
    return render(request, 'delete_stock.html', {'ticker': ticker})
