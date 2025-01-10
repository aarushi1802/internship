from pyexpat.errors import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Order, Product
from .forms import OrderForm, AuthenticationForm
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout
from django.core.paginator import Paginator


def home(request):
    return render(request, 'home.html')

def profile_view(request):
    return render(request, 'account/profile.html')

def dashboard(request):
    return render(request, 'account/dashboard.html')

def dashboard(request):
    try:
        orders = Order.objects.all()  # Fetch all orders
        print(f"Orders fetched: {orders}")  # Debugging
        return render(request, 'account/dashboard.html', {'orders': orders})
    except Exception as e:
        print(f"Error fetching orders: {e}")  # Debugging



def user_login(request):  
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            auth_login(request, form.get_user())
            return redirect('dashboard') 
    else:
        form = AuthenticationForm()
    
    return render(request, 'login.html', {'form': form})

@login_required
def dashboard(request):
    search_query = request.GET.get('search', '')
    
    # Use the correct field 'id' instead of 'order_id'
    items = Order.objects.filter(id__icontains=search_query)
    
    # Use 'id' for ordering as well
    orders = Order.objects.all().order_by('id')  # Assuming 'id' is the primary key
    
    paginator = Paginator(orders, 10)  # Show 10 orders per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    total_order_value = sum(order.order_value for order in orders)

    return render(request, 'account/dashboard.html', {
        'page_obj': page_obj,
        'total_order_value': total_order_value
    })



def search_orders(request):
    query = request.GET.get('q', '')  # Get the search query from the URL
    if query:
        orders = Order.objects.filter(customer_name__icontains=query)  # Filter orders by customer name
    else:
        orders = Order.objects.all()  # Show all orders if no query
    total_order_value = sum(order.order_value for order in orders)  # Recalculate total order value
    return render(request, 'account/dashboard.html', {'orders': orders, 'total_order_value': total_order_value, 'query': query})


    # Pagination logic
    page = int(request.GET.get('page', 1))
    per_page = 50
    start = (page - 1) * per_page
    end = start + per_page
    total_pages = (len(orders) + per_page - 1) // per_page

    context = {
        'orders': orders[start:end],
        'total_order_value': sum(order.order_value for order in orders),
        'current_page': page,
        'total_pages': total_pages,
        'search_query': search_query,
    }
    return render(request, 'dashboard.html', context)

# Create New Order View
@login_required
def create_order(request):
    if request.method == 'POST':
        form = OrderForm(request.POST)
        print("Form data:", request.POST)  # Debug: Print submitted form data
        if form.is_valid():
            order = form.save(commit=False)
            product = form.cleaned_data['product_name']
            order.order_value = product.price * order.quantity
            order.save()
            return redirect('dashboard')
        else:
            # Print form errors for debugging
            print(form.errors)
            return render(request, 'account/create_order.html', {'form': form})
    else:
        form = OrderForm()

    return render(request, 'account/create_order.html', {'form': form})


# Edit Order View
@login_required
def edit_order(request, order_id):
    # Get the order object by id
    order = get_object_or_404(Order, pk=order_id)

    if request.method == 'POST':
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()  # Save the updated order
            return redirect('dashboard')  # Redirect to the dashboard or wherever you need
    else:
        form = OrderForm(instance=order)  # Pre-populate the form with existing data

    return render(request, 'account/edit_order.html', {'form': form, 'order': order})

# Delete Order View
@login_required
def confirm_delete(request, order_id):
    order = get_object_or_404(Order, pk=order_id)

    if request.method == 'POST':
        order.delete()  # Delete the order
        return redirect('dashboard')  # Redirect after deletion

    return render(request, 'app/confirm_delete.html', {'order': order})

# API Endpoint for Orders (Bonus: JSON format)
@login_required
def orders_json(request):
    orders = Order.objects.all()
    data = [
        {
            'id': order.id,  # Use 'id' instead of 'order_id'
            'customer_name': order.customer_name,
            'customer_email': order.customer_email,
            'product': order.product_name,  # Use 'product_name' if that’s the correct field
            'quantity': order.quantity,
            'order_value': order.order_value,
        } for order in orders
    ]
    return JsonResponse({'orders': data})


def user_logout(request):
    logout(request)
    return redirect('login')