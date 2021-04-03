from django.contrib.auth.decorators import login_required
from django.shortcuts import render,redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import login,logout,authenticate,login
from django.contrib.auth.forms import UserCreationForm
from .forms import createUserForm
from django.contrib import messages
from .models import product,cartItem,Review
import datetime
from django.forms.models import model_to_dict
from .forms import *
import random
# Create your views here.
def home(request):
    if request.method=='POST':
        uname=request.POST.get('username')
        password=request.POST.get('password')
        user=authenticate(request,username=uname,password=password)
        if user is not None:
            login(request,user)
            return redirect('shop')
        else:
            messages.info(request,"Username or password is incorrect")
    return render(request,'e_commerce/login.html')

def logOutUser(request):
    logout(request)
    return redirect('e_commerce-home')

@login_required(login_url='e_commerce-home')
def showHome(request):
    return render(request, 'e_commerce/home.html')

def register(request):
    form=createUserForm()
    context={'form':form}
    if request.method == "POST":
        form = createUserForm(request.POST)
        if form.is_valid():
            form.save()
            user = form.cleaned_data.get('username')
            messages.success(request, f"account created for {user}")
            return redirect('e_commerce-home')

            #messages.success(request, f"account created for {user}")

    return render(request,'e_commerce/register.html',context)

def showProducts(request,gender):
    products = product.objects.filter(gender=gender)
    return render(request,'e_commerce/products.html',{'products':products})

def addToCart(request,id):
    item1=product.objects.filter(id=id)
    item=cartItem(removed=False,ordered=True,user_id=request.user.username,id=id,name=item1[0].name,brand=item1[0].brand,price=item1[0].price,size=item1[0].size,img=item1[0].img,units=1)
    item.save()
    products = product.objects.filter(gender=item1[0].gender)
    return render(request, 'e_commerce/products.html', {'products': products})


def showCart(request):
    not_empty=False
    current_user = request.user
    cartItems=cartItem.objects.filter(user_id=current_user.username).filter(ordered=True,removed=False)
    count=cartItems.count()
    if count>0:
        not_empty=True
    return render(request, 'e_commerce/cart.html', {'products':cartItems,'empty':not_empty})

def deleteItemFromCart(request,id):
    not_empty=False

    if request.method=='GET':
        print(id)
        item = cartItem.objects.filter(id=id)[0]
        item.removed=True
        item.ordered=False
        item.save()
        cartItems = cartItem.objects.filter(user_id=request.user.username,removed=False)
    count=cartItems.count()
    if count>0:
        not_empty=True
    return render(request, 'e_commerce/cart.html', {'products':cartItems,'empty':not_empty})

def updateItemFromCart(request,id):
    item = cartItem.objects.filter(id=id)
    print(item)

    print(item.values())
    if request.method=='POST':
        cartItem.objects.filter(id=id).update(size=request.POST['size'])
        cartItem.objects.filter(id=id).update(units=request.POST['units'])
        item.size=request.POST['size']
        item.units = request.POST['units']
        #item.save()
    return render(request, 'e_commerce/update.html', {'item':item[0]})

def generateBill(request):
    total=0
    type_list=[]
    current_user = request.user
    cartItem.objects.filter(user_id=current_user.username).update(status='Ordered')
    orderedItems = cartItem.objects.filter(user_id=current_user.username).filter(ordered=True, removed=False)
    #types=orderedItems.objects.values_list('name', flat=True)
    types=['top','jacket','shrug','jeans']
    for item in orderedItems:
        for type in types:
            if type in item.name.lower():
                type_list.append(type)
                break
    unique_types=list(set(type_list))
    type_freq_list={x:type_list.count(x) for x in unique_types}
    max_type = max(type_freq_list, key=type_freq_list.get)
    rec_products=product.objects.filter(name__contains=max_type)
    order_ids=[item.id for item in orderedItems]
    rec_ids=[item.id for item in rec_products]
    print(order_ids)
    print(rec_ids)
    to_rec=set(rec_ids)-set(order_ids)
    print(to_rec)
    rec_products=product.objects.filter(name__contains=max_type,id__in=to_rec)
    print(rec_products)
    cartItems = cartItem.objects.filter(user_id=current_user.username).filter(ordered=True,removed=False)
    for item in cartItems:
        total=total+item.price*item.units

    return render(request, 'e_commerce/Bill.html', {'items': cartItems,'total_amount':total,'rec':rec_products})

def filter(request):
    if request.method=='GET':
        brand = request.GET['brandSelect']
        products = product.objects.filter(brand=brand)
        print(products[0])
    return render(request, 'e_commerce/products.html', {'products': products})

def savePastOrder(request):
    current_user = request.user
    cartItems = cartItem.objects.filter(user_id=current_user.username)
    for item in cartItems:
        item.ordered=True
        item.save()
    address=Profile.objects.filter(user_id=current_user.username)[0].address
    print(ProfileForm)
    return render(request, 'e_commerce/confirm.html',{'address':address})

def OrderReview(request):
    current_user = request.user
    orderedItems = cartItem.objects.filter(user_id=current_user.username).filter(ordered=True,removed=False)
    return render(request, 'e_commerce/review.html', {'products': orderedItems})

def recommendProducts(request):
    current_user = request.user
    orderedItems = cartItem.objects.filter(user_id=current_user.username).filter(ordered=True, removed=False)
    types=orderedItems.objects.values_list('name', flat=True)
    print(types)

def profileSetUp(request):
    """Process images uploaded by users"""
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES)
        if form.is_valid():

            form.save()
            profile=Profile(user_id=request.user.username,address=request.POST['address'],image=request.FILES['image'])
            profile.save()
            # Get the current instance object to display in the template
            img_obj = form.instance
            return render(request, 'e_commerce/profile.html', {'form': form, 'img_obj': img_obj})
    else:
        form = ProfileForm()
    return render(request, 'e_commerce/profile.html', {'form': form})

def productReview(request,id):

    if request.method=='GET':
        #id = request.GET['item_id']
        items=list(request.GET.items())

        print(type(items[1][0]))
        for i in range(1,len(items)):
            form = Review(item_id=int(items[i][0]), review=items[i][1], user_id=request.user.username, review_id=random.randint(0, 1000))
            form.save()
        #review=request.GET[str(id)]
        #print(request)
        #print(review)

        #user_review=Review()
    current_user = request.user
    orderedItems = cartItem.objects.filter(user_id=current_user.username).filter(ordered=True, removed=False)
    return render(request, 'e_commerce/review.html', {'products': orderedItems})

def productDetails(request,id):
    item=product.objects.filter(id=id)
    reviews=Review.objects.filter(item_id=id)
    return render(request, 'e_commerce/product_details.html', {'product': item[0],'reviews':reviews})









