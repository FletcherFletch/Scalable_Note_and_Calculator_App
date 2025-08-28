import json
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.conf import settings
from django.http import HttpResponseBadRequest, JsonResponse, HttpResponse
from .models import Product
from django.views.decorators.csrf import csrf_exempt
from Helper.billing import start_checkout_session 

User = get_user_model()

BASE_URL = settings.BASE_URL

def product_price_redirect_view(request, price_id=None, *args, **kwargs):
    request.session[''] = price_id
    return redirect("")

def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username") or None
        password = request.POST.get("password") or None

        if all([username, password]):
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                print("Login here")
                return redirect("/Home")
    return render(request, "Login.html", {})

def register_view(request):
    if request.method == "POST":

        username = request.POST.get("username") or None
        email = request.POST.get("email") or None
        password = request.POST.get("password") or None

        try:
            User.objects.create_user(username, email=email, password=password)
        except:
            pass
    return render(request, "auth/register.html", {})

@login_required
def home_view(request, *args, **kwargs):
    if request.user.is_authenticated:
        print(request.user.username)
    return about_view(request, *args, **kwargs)

def about_view(request, *args, **kwargs):

    my_title = "My Page"
    html_template = "home.html"
    my_context = {
        "page_title": my_title,
    }

    return render(request, html_template, my_context)

def placeholder_view(request):
    return HttpResponse("temp for test")

@csrf_exempt
def create_checkout_view(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)

            #This parses the raw HTTP request body (this is JSON-formatted string sent from frontend)
            #This turns it into a python dictionary that can be worked with 
            #request.body - this is the raw HTTP request body as bytes  (what the client frontend sends in a POST request)
            #json.loads(..) this function decodes a JSON string into a python dict 
            #since request.body is bytes it much be decoded (json.loads)
            #now data has a dictionary stored 
            #Ex data.get('customer_id') -- > 'cus_1234'



            #extract parameters from request
            customer_id = data.get('customer_id')
            price_id = data.get('price_id')
            success_url = data.get('succes_url', '')
            cancel_url  = data.get('cancel_url', '')

            #call helper 

            session = start_checkout_session(
                customer_id=customer_id,
                price_id=price_id,
                success_url=success_url,
                cancel_url=cancel_url,
                raw=False #because just want to return url isntead of full response
            )

            return JsonResponse({'checkout_url': session})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)


    #Checkout view works with helper function
    #View receives request, extracts parameters from request (customer_id, price_id, success_url)
    #calls the start_checkout_session() function with those arguments
    #returns a JsonResponse to the frontend (containing either the full session object or just the URL)



