from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.models import User
from django.http import HttpResponse

import pymongo

from adoptionsite.models import CartItem, Animal

conn_str = "mongodb://cosmos-panda-taa-sea-dev:MNoNom1AQMPUI4CUmUypOM3MYCd3VhDaWyNnMJLV6vxhFzJm3lcmAm85bZpZLeD73PTlBi8N7JuYcbcucb2iPQ==@cosmos-panda-taa-sea-dev.mongo.cosmos.azure.com:10255/?ssl=true&replicaSet=globaldb&retrywrites=false&maxIdleTimeMS=120000&appName=@cosmos-panda-taa-sea-dev@"

client = pymongo.MongoClient(conn_str, serverSelectionTimeoutMS=5000)

available_animals = []

try:
    print(client.server_info())
    db = client['TAA_Portal']
    collection = db['AvailableAnimals']

    print(collection.count_documents({}))
    
    # Initial load of animals
    for animal in collection.find():
        print(animal)
        available_animals.append(Animal(id=animal['Id'], name=animal['Name'], description=animal['Description'], age=animal['Age']))
except Exception as e:
    print(e)

login_ids = [ 'pencil', 'flower', 'icecream', 'basketball', 'orange', 'placeholder' ]


for animal in available_animals:
    print(animal.__dict__)

cart_items = []

for animal in available_animals:
    cart_items.append(CartItem(id=1, quantity=0, name=animal.name))


def index(request):
    context = {
        'available_animals': available_animals
    }

    return render(request, 'adoptionsite/index.html', context)

def cart(request):
    context = {
        'cart_items': cart_items
    }

    return render(request, 'adoptionsite/cart.html', context)

def login(request):
    context = {
        'login_ids': login_ids
    }

    return render(request, 'adoptionsite/login.html', context)

def logout(request):
    return render(request, 'adoptionsite/logout.html')

def perform_login(request):
    provided_username = request.POST['AvatarId']
    provided_password = request.POST.get('password')

    user = authenticate(request, username=provided_username, password=provided_password)

    if user is not None:
        auth_login(request, user)

        return redirect('Index')
    else:
        context = {
            'login_ids': login_ids,
            'error_message': 'Invalid username or password.'
        }

        return render(request, 'adoptionsite/login.html', context)

def adjust_cart_item_quantity(request, item_id):
    cart_item = next((item for item in cart_items if item.id == item_id))
    action = request.POST['action']

    if action == "increment":
        cart_item.increment()
    else:
        cart_item.decrement()

    return redirect('Cart')
