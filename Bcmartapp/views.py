from django.shortcuts import render,redirect
from django.http import JsonResponse
import json
import datetime
from .models import * 
from django.contrib.auth import login,logout,authenticate
from django.contrib import messages
from django import *

from django.contrib.auth.decorators import login_required

from django.core.mail import send_mail

@login_required(login_url="/register/")
def store(request):

	if request.user.is_authenticated:
		customer = request.user.customer
		order, created = Order.objects.get_or_create(customer=customer, complete=False)
		items = order.orderitem_set.all()
		cartItems = order.get_cart_items
	else:
		#Create empty cart for now for non-logged in user
		items = []
		order = {'get_cart_total':0, 'get_cart_items':0, 'shipping':False}
		cartItems = order['get_cart_items']

	products = Product.objects.all()
	context = {'pro':products, 'cartItems':cartItems}
	return render(request, 'store.html', context)



@login_required(login_url="/register/")
def Cat(request):
  if request.user.is_authenticated:
    customer = request.user.customer
    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    items = order.orderitem_set.all()
    cartItems = order.get_cart_items
  else:
    items = []
    order = {'get_cart_total':0, 'get_cart_items':0, 'shipping':False}
    cartItems = order['get_cart_items']

  li = Category.objects.all()
  return render(request,'categories.html',{'i':li,'cartItems':cartItems})





@login_required(login_url="/register/")
def Cat_det(request,name):
  if request.user.is_authenticated:
    customer = request.user.customer
    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    items = order.orderitem_set.all()
    cartItems = order.get_cart_items
  else:
    items = []
    order = {'get_cart_total':0, 'get_cart_items':0, 'shipping':False}
    cartItems = order['get_cart_items']
    
  det = Product.objects.filter(id=name)
  cat_name= Product.cat_name
  print(det,cat_name) 
  
  
  return render(request,'Cat_det.html',{'i':det,'cartItems':cartItems,'j':cat_name})
  
  
@login_required(login_url="/register/")
def cart(request):

	if request.user.is_authenticated:
		customer = request.user.customer
		order, created = Order.objects.get_or_create(customer=customer, complete=False)
		items = order.orderitem_set.all()
		cartItems = order.get_cart_items
	else:
		#Create empty cart for now for non-logged in user
		items = []
		order = {'get_cart_total':0, 'get_cart_items':0, 'shipping':False}
		cartItems = order['get_cart_items']

	context = {'items':items, 'order':order, 'cartItems':cartItems}
	return render(request, 'cart.html', context)




@login_required(login_url="/register/")
def checkout(request):
	if request.user.is_authenticated:
		customer = request.user.customer
		order, created = Order.objects.get_or_create(customer=customer, complete=False)
		items = order.orderitem_set.all()
		cartItems = order.get_cart_items
	else:
		#Create empty cart for now for non-logged in user
		items = []
		order = {'get_cart_total':0, 'get_cart_items':0, 'shipping':False}
		cartItems = order['get_cart_items']

	context = {'items':items, 'order':order, 'cartItems':cartItems}
	return render(request, 'checkout.html', context)


def register_main(request):
  if request.method=='POST':
    username= request.POST.get('Username')
    email= request.POST.get('email')
    password= request.POST.get('password')
    if User.objects.filter(username=username).exists():
      messages.info(request,'Username taken')
      return redirect('/')
    c=User.objects.create_user(username=username,email=email,password=password)
    v=Customer.objects.create(user=c,email=email,name=username)
    v.save()
    c.save()
    sub= "Account Confirmation"
    body=f"Dear{request.user} , Thank you for choosing our website to order your items"
    email=request.user.email
    send_mail(sub,body,"badhrinadh.g.v.s@gmail.com",[email],fail_silently=False)
    return render(request,'register.html')
  return render(request,'register.html')


def login_main(request):
  if request.method == 'POST':
    username=request.POST.get('Username')
    password=request.POST.get('password')
    if User.objects.filter(username=username) is None:
      messages.info(request,'User not exist')
      return redirect('/')
    user=authenticate(username=username,password=password)
    if user is None:
      messages.info(request,'User did not exist')
      return redirect('login')
    else:
      login(request,user)
      return redirect('store')
  return render(request,'login.html')
  
  
def logout_main(request):
  logout(request)
  return redirect('/register/')
    
@login_required(login_url="/register/")
def updateItem(request):
	data = json.loads(request.body)
	productId = data['productId']
	action = data['action']
	print('Action:', action)
	print('Product:', productId)

	customer = request.user.customer
	product = Product.objects.get(id=productId)
	order, created = Order.objects.get_or_create(customer=customer, complete=False)

	orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

	if action == 'add':
		orderItem.quantity = (orderItem.quantity + 1)
	elif action == 'remove':
		orderItem.quantity = (orderItem.quantity - 1)

	orderItem.save()

	if orderItem.quantity <= 0:
		orderItem.delete()

	return JsonResponse('Item was added', safe=False)







@login_required(login_url="/register/")
def processOrder(request):
	transaction_id = datetime.datetime.now().timestamp()
	data = json.loads(request.body)

	if request.user.is_authenticated:
		customer = request.user.customer
		order, created = Order.objects.get_or_create(customer=customer, complete=False)
		total = float(data['form']['total'])
		order.transaction_id = transaction_id

		if total == order.get_cart_total:
			order.complete = True
		order.save()

		if order.shipping == True:
			ShippingAddress.objects.create(
			customer=customer,
			order=order,
			address=data['shipping']['address'],
			city=data['shipping']['city'],
			state=data['shipping']['state'],
			zipcode=data['shipping']['zipcode'],
			)
	else:
		print('User is not logged in')

	return JsonResponse('Payment submitted..', safe=False)


def detview(request,det):
  if request.user.is_authenticated:
    customer = request.user.customer
    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    items = order.orderitem_set.all()
    cartItems = order.get_cart_items
  else:
    items = []
    order = {'get_cart_total':0, 'get_cart_items':0, 'shipping':False}
    cartItems = order['get_cart_items']

  li = Product.objects.filter(name=det).first()
  # im=Product.objects.image()
  return render(request,'view.html',{'item':li,'cartItems':cartItems})  