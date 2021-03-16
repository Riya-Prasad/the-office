from django.shortcuts import render, redirect
from django.forms import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group


from .models import *
from .forms import OrderForm, CreateUserForm, CustomerForm
from .filters import OrderFilter
from .decorators import unauthenticated_user, allowed_users, admin_only

# Create your views here.

@unauthenticated_user
def registerPage(request):
	form = CreateUserForm()
	if request.method == 'POST':
		form = CreateUserForm(request.POST)
		if form.is_valid():
			user = form.save()
			username = form.cleaned_data.get('username')

			messages.success(request, f'Account has been created for ' + username + '! You are now able to log in.')
			return redirect('login')

	context = {'form':form}
	return render(request, 'customer/register.html', context)


@unauthenticated_user
def loginPage(request):
	if request.method == 'POST':
		username = request.POST.get('username')
		password = request.POST.get('password')

		user = authenticate(request, username=username, password=password)

		if user is not None:
			login(request, user)
			return redirect('home')
		else:
			messages.info(request, f'Username or Password is incorrect!')

	context = {}
	return render(request, 'customer/login.html', context)


def logoutUser(request):
	logout(request)
	return redirect('login')
	

@login_required(login_url='login')
@admin_only
def home(request):
	orders = Order.objects.all()
	customers = Customer.objects.all()

	total_customer = customers.count()
	total_orders = orders.count()
	delivered = orders.filter(status='Delivered').count()
	pending = orders.filter(status='Pending').count()

	context = {
		'orders':orders,
		'customers':customers,
		'total_customer':total_customer,
		'total_orders':total_orders,
		'delivered':delivered,
		'pending':pending
	}

	return render(request, 'customer/home.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def userPage(request):
	orders = request.user.customer.order_set.all()

	total_orders = orders.count()
	delivered = orders.filter(status='Delivered').count()
	pending = orders.filter(status='Pending').count()

	context = {
		'orders':orders,
		'total_orders':total_orders,
		'delivered':delivered,
		'pending':pending
	}
	return render(request, 'customer/user.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def accountSetting(request):
	customer = request.user.customer
	form = CustomerForm(instance=customer)

	if request.method == 'POST':
		form = CustomerForm(request.POST, instance=customer)

		if form.is_valid():
			form.save()

	context = {'form': form}
	return render(request, 'customer/account_setting.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def products(request):
	products = Product.objects.all()
	return render(request, 'customer/products.html', {'products': products})


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def customers(request, pk):
	customer = Customer.objects.get(id=pk)

	orders = customer.order_set.all()
	order_count = orders.count()

	myFilter = OrderFilter(request.GET, queryset=orders)
	orders = myFilter.qs

	context = {'customer':customer, 'orders':orders, 'order_count':order_count, 'myFilter':myFilter}

	return render(request, 'customer/customers.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def delete_customer(request, pk):
	customer = Customer.objects.get(id=pk)
	
	if request.method == 'POST':
		customer.delete()
		return redirect('/')

	context = {'customer':customer}
	return render(request, 'customer/delete_customer.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def create_order(request, pk):
	orderFormSet = inlineformset_factory(Customer, Order, fields=('product', 'status'), extra=10) 
	customer = Customer.objects.get(id=pk)
	formset = orderFormSet(queryset=Order.objects.none(), instance=customer)

	if request.method == 'POST':
		formset = orderFormSet(request.POST, instance=customer)

		if formset.is_valid():
			formset.save()
			return redirect('/')

	context = {'formset':formset}
	return render(request, 'customer/order_form.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def update_order(request, pk):

	order = Order.objects.get(id=pk)
	form = OrderForm(instance=order)

	if request.method == 'POST':
		form = OrderForm(request.POST, instance=order)
		if form.is_valid():
			form.save()
			return redirect('/')

	context = {'form':form}
	return render(request, 'customer/update_order.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def delete_order(request, pk):
	order = Order.objects.get(id=pk)
	
	if request.method == 'POST':
		order.delete()
		return redirect('/')

	context = {'order':order}
	return render(request, 'customer/delete_order.html', context)

