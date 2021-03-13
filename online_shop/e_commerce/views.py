from django.contrib.auth.decorators import login_required
from django.shortcuts import render,redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import login,logout,authenticate,login
from django.contrib.auth.forms import UserCreationForm
from .forms import createUserForm
from django.contrib import messages
from .models import product,cartItem
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
    item=cartItem(user_id=request.user.username,id=id,name=item1[0].name,brand=item1[0].brand,price=item1[0].price,size=item1[0].size,img=item1[0].img,units=1)
    item.save()
    products = product.objects.filter(gender=item1[0].gender)
    return render(request, 'e_commerce/products.html', {'products': products})


def showCart(request):
    current_user = request.user
    cartItems=cartItem.objects.filter(user_id=current_user.username)
    return render(request, 'e_commerce/cart.html', {'products':cartItems})

def deleteItemFromCart(request,id):
    if request.method=='GET':
        print(id)
        item = cartItem.objects.filter(id=id)
        item.delete()
        cartItems = cartItem.objects.filter(user_id=request.user.username)
    return render(request, 'e_commerce/cart.html', {'products':cartItems})

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
    current_user = request.user
    cartItems = cartItem.objects.filter(user_id=current_user.username)
    for item in cartItems:
        total=total+item.price*item.units

    return render(request, 'e_commerce/Bill.html', {'items': cartItems,'total_amount':total})

def filter(request):
    if request.method=='GET':
        brand = request.GET['brandSelect']
        products = product.objects.filter(brand=brand)
        print(products[0])
    return render(request, 'e_commerce/products.html', {'products': products})







