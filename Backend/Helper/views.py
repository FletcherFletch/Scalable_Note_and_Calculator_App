import stripe
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
from users.models import Notes
from django.views.decorators.csrf import csrf_exempt
from Helper.billing import start_checkout_session 
from django.shortcuts import render
from Helper.billing import create_customer, create_product, create_stripe_price
from .models import Product 
from django.shortcuts import get_object_or_404

DOMAIN = "http://127.0.0.1:8000"
success_url = f"{DOMAIN}/home/?success=1"
cancel_url = f"{DOMAIN}/notes/?canceled=true"
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
                return redirect("home")
    return render(request, "Login.html", {})

def register_view(request):
    if request.method == "POST":

        username = request.POST.get("username") or None
        email = request.POST.get("email") or None
        password = request.POST.get("password") or None

        try:
            user = User.objects.create_user(username, email=email, password=password)
            user.save()

            try:

                stripe_id = create_customer(name=username, email=email)
            

                user.user_stripe_id = stripe_id
                user.save()
            except Exception as stripe_error:
                print(f"stripe customer creation failed: {stripe_error}")
            
            return redirect("Login")   
        except Exception as e:
            print(f"Error: {e}")

    
    return render(request, "auth/register.html", {})

@login_required
def home_view(request, *args, **kwargs):
    if request.user.is_authenticated:
        print(request.user.username)
    return about_view(request, *args, **kwargs)

#def homepage(request):
   # products = Product.objects.all()
   # return render(request, 'home.html', {'user': request.user, 'products': products})

def about_view(request, *args, **kwargs):
    products = Product.objects.all()
    my_title = "My Page"
    html_template = "home.html"
    my_context = {
        "page_title": my_title,
        'products': products,
    }
    for product in products:
        print(f"Product: {product.name}, stripe price id: {product.stripe_price_id}")

    return render(request, html_template, my_context)

def placeholder_view(request):
    return HttpResponse("temp for test")
@csrf_exempt
def create_price(request, django_product_id):
    product = get_object_or_404(Product, id=django_product_id,)
        #this is safer than  doing something like 
       # try:
      #      product = Product.objects.get(id=django_product_id)
      #  except Product.DoesNotExist:
      #      raise Http404("Product does not exist ")

    #this is saying find the product who id equals to the django_product_id passed into the view
    #so it looks up a product by matching values 

      #this view is being passed product_id - this refers to my own Django product in my own database
      
      #product - > buy flow
      #user clicks buy on product, this product has a django id of 5
      #use above get object
      #we now have internal product
      #then get a stripe product id if not already made 

    if not product.stripe_product_id:
        stripe_product = create_product(
            name=product.name,        
        )
        product.stripe_product_id = stripe_product
        product.save()

    
    if not product.stripe_price_id:
        stripe_price_id = create_stripe_price(
            currency = "usd",
            product = product.stripe_product_id,
            unit_amount= "0",
        )

        product.stripe_price_id = stripe_price_id
        product.save()

    user_stripe_id = request.POST.get('customer_id')    

    if not user_stripe_id:
        return JsonResponse({"error": "missing customer"}, status=400)
    
    line_items = [{"price": product.stripe_price_id, "quantity": 1}]
    session = start_checkout_session(
        customer_id=user_stripe_id,
        line_items=line_items,
        success_url=success_url,
        cancel_url=cancel_url,
        raw=False
    )

    return redirect(session, code=303)

def back_login(request):
    #if request.method == 'POST':

    return redirect(request, 'Login.html')


def payment_cancel(request, *args, **kwargs):
    canceled = request.GET.get('canceled') == 'true'
    all_notes = Notes.objects.filter(user=request.user)

    if request.method == 'POST':
        content = request.POST.get('Note')
        title = request.POST.get('Note')
        if content:
            notes = Notes.objects.create(user=request.user, content=content, title=title)          
            print(f"Note_check: {notes.content}, Title_Check: {notes.title}")            
            return redirect('display_notes')
   
    return render(request, 'NoteDisplay.html', {'canceled': canceled, 'notes': all_notes,})

def delete_note(request, note_id):
    if request.method == 'POST':
        note = get_object_or_404(Notes, id=note_id)
        note.delete()
    return redirect('display_notes')

def note_display(request, *args, **kwargs):
    notes = Notes.objects.all()
    my_title = "note"
    html_template = "NoteDisplay"
    my_context = {
        "page_title": my_title,
        "notes": notes,
    }

    return render(request, html_template, my_context)


#dont use session.url just session because session returns session.url in the helper function 
#redirect sends GET request, checkout view want the POST request 

# @csrf_exempt
# def create_checkout_view(request, django_product_id):
#     if request.method == 'GET':
#         try:
#            # print(request.body)
#            # data = json.loads(request.body)
#            # this is not for typical form request, this expects the reuqest body to be JSONstring 
#            #but here using templates i am sending regular html form submnission 

#             #This parses the raw HTTP request body (this is JSON-formatted string sent from frontend)
#             #This turns it into a python dictionary that can be worked with 
#             #request.body - this is the raw HTTP request body as bytes  (what the client frontend sends in a POST request)
#             #json.loads(..) this function decodes a JSON string into a python dict 
#             #since request.body is bytes it much be decoded (json.loads)
#             #now data has a dictionary stored 
#             #Ex data.get('customer_id') -- > 'cus_1234'



#             #extract parameters from request
#             #user_stripe_id = data.get('customer_id')
#            # stripe_price_id = data.get('stripe_price_id')

#            #these would be used for a request from a JSON string from a frontent submission
#            #but in typical form POST you should use request.POST

#             customer_id = request.POST.get('customer_id')
#             stripe_price_id = request.POST.get('price_id')
#             #success_url = data.get('succes_url', '')
#             #cancel_url  = data.get('cancel_url', '')

#             #call helper 

#             line_items = [{"price": stripe_price_id, "quantity": 2}]

#             print(f"customer_id: {customer_id}")
#             print(f"price_id: {stripe_price_id}")
#             #print(f"db_entry: {Product.name}" )

#             if not stripe_price_id:
#                 return JsonResponse({'error': 'missing price'}, status=400)

#             session = start_checkout_session(
#                 customer_id=customer_id,
#                 #price_id=stripe_price_id,
#                 success_url=success_url,
#                 cancel_url=cancel_url,
#                 line_items=line_items,
#                 raw=False #because just want to return url isntead of full response
#             )

#             return redirect(session.url, code=303)

#           #  return JsonResponse({'checkout_url': session})
#         except Exception as e:
#            return JsonResponse({'error': str(e)}, status=500)
        
#         #This view falls under using traditional form submission and server-rendered views 
#         #lets you redirect directly from Django 
#     return JsonResponse({'error': 'Invalid request method'}, status=405)

    #Checkout view works with helper function
    #View receives request, extracts parameters from request (customer_id, price_id, success_url)
    #calls the start_checkout_session() function with those arguments
    #returns a JsonResponse to the frontend (containing either the full session object or just the URL)



