from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
import requests
from .models import *
import urllib.parse
# Create your views here.
def signUp(request):
    try:   
        context = {} 
        if request.method == 'POST':
            username = request.POST.get('username')
            email = request.POST.get('email')
            password = request.POST.get('password')
            password1 = request.POST.get('password1')
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')

            if password != password1:
                context = {
                    'error':True,
                    'message':'Both passwords didn\'t match'
                }
                return render(request, 'TrackerApp/signup.html', context)

            user = User.objects.create(username=username, email=email, first_name=first_name, last_name=last_name)
            user.set_password(password)
            user.save()
            context = {
                'error':False,
                'message':'Your account has been created succcesfully. Please vist the login page to login to your account.'
            }

    except Exception as e:
        context = {
            'error':True,
            'message': str(e)
        }
    return render(request, 'TrackerApp/signup.html', context)

def signIn(request):
    context = {}
    context['error'] = False
    try:
        if request.method == 'POST':
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                context['message'] = 'You have successfully signed in!'
                return redirect(dashboard, page=1)
            else:
                context['error'] = True
                context['message'] = 'Incorrect Username or Password'
                return render(request, 'TrackerApp/signin.html', context)
    except Exception as e:
        context['error'] = True
        context['message'] = str(e)
    return render(request, 'TrackerApp/signin.html', context)

@login_required
def dashboard(request, page):
    context = {}
    try:
        if request.method == 'POST':
            watchlist_id = request.POST.get('watchlist_id')
            stock_symbol = request.POST.get('stock_symbol')
            print('watchlist:',watchlist_id, 'stock_symbol:', stock_symbol)
            stock = Stock.objects.filter(symbol=stock_symbol).first()
            watchlist = WatchList.objects.filter(owner=request.user).filter(id=watchlist_id).first()
            if not stock:
                stock = Stock.objects.create(symbol=stock_symbol)
                stock.save()
            watchlist.stocks.add(stock)
            watchlist.save()
            return redirect('dashboard', page=1)

        response = requests.get('https://cloud.iexapis.com/stable/tops?token=pk_aee9f5a22c404b45a8230642120370e9')
        # print(response.json()[:10])
        stocks = response.json()
        context['stocks'] = stocks[page*10-10:10*page]
        watchlists = WatchList.objects.filter(owner=request.user).values_list('id','title')
        context['watchlists'] = watchlists
    except Exception as e:
        context['error'] = True
        context['message'] = str(e)
    # print(context)
    return render(request, 'TrackerApp/dashboard.html', context)

@login_required
def signOut(request):
    logout(request)
    return redirect('sign_in')

@login_required
def watchLists(request):
    context = {}
    context['error'] = False
    try:
        if request.method == 'POST':
            request_type = request.POST.get('request_type')
            if request_type == 'post':
                title = request.POST.get('title')
                desc = request.POST.get('desc')
                watchlist = WatchList.objects.create(title=title, desc=desc, owner=request.user)
                watchlist.save()
                context['message'] = "Your watchlist has been created successfully."
                return redirect('watch_lists')
            elif request_type == 'delete':
                watchlist_id = request.POST.get('watchlist_id')
                print(watchlist_id)
                watchlist = WatchList.objects.get(id=watchlist_id)
                watchlist.delete()
                return redirect('watch_lists')
        watchlist = WatchList.objects.filter(owner=request.user)
        context['watchlist'] = watchlist
    except Exception as e:
        context['error'] = True
        context['message'] = str(e)
    return render(request, 'TrackerApp/watchlists.html', context)

@login_required
def watchList(request, pk):
    context = {}
    context['error'] = False
    context['watchlist_id'] = pk
    try:
        watchlist = WatchList.objects.get(id=pk)
        if request.method == 'POST':
            stock_id = request.POST.get('stock_id')
            print(stock_id)
            stock = Stock.objects.get(id=stock_id)
            print(stock, watchlist)
            watchlist.stocks.remove(stock)
            watchlist.save()
            return redirect('watch_list', pk)
        context['title'] = watchlist.title
        stocks = watchlist.stocks.values()
        # print(stocks)
        data = []
        url = 'https://cloud.iexapis.com/stable/tops?token=pk_aee9f5a22c404b45a8230642120370e9&symbols='
        for stock in stocks:
            # if stock[0][len(stock[0])-1] == '+': url_new = url + stock[0][:-1] + '%2b'
            symbol = urllib.parse.quote_plus(stock['symbol'])
            url_new = url + symbol
            # print(url_new)
            response = requests.get(url_new)
            # print(response.json())
            data.append(response.json()[0])
            data[len(data)-1]['id'] = stock['id']
        # print(data)
        context['stocks'] = data
    except Exception as e:
        context['error'] = True
        context['message'] = str(e)
    # print(context)
    return render(request, 'TrackerApp/watchlist.html', context)

@login_required
def stock(request, sym):
    context = {}
    context['error'] = False
    try:
        print(1)
        stock = Stock.objects.get(symbol=sym)
        response = requests.get(f'https://cloud.iexapis.com/stable/stock/{stock.symbol}/quote?token=pk_aee9f5a22c404b45a8230642120370e9')
        data = response.json()
        response = requests.get(f'https://cloud.iexapis.com/stable/stock/{stock.symbol}/company?token=pk_aee9f5a22c404b45a8230642120370e9')
        context['company'] = response.json()
        print(response.json())
        context['stock'] = []
        for item in data:
            context['stock'].append([item,data[item]])
        print(context)
    except Exception as e:
        context['error'] = True
        context['message'] = str(e)
        print(str(e))
    return render(request, 'TrackerApp/stock.html', context)

