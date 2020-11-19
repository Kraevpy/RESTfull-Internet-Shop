from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm

from .forms import CommentForm, OrderForm
from plumbing import services


def index(request):
    categories_ = services.get_all_categories()
    products_list = services.get_all_products()

    return render(request, 'plumbing/home_page.html', context={
        'categories': categories_,
        'products': products_list,
    })


def categories(request, category_id, subcategory_id=None):
    categories_ = services.get_subcategories(category_id)

    if not categories_:
        return redirect('index')

    if subcategory_id:
        products_list = services.get_product_with_category(subcategory_id)

    else:
        products_list = services.get_product_with_subcategory(category_id)

    return render(request, 'plumbing/home_page.html', context={
        'categories': categories_,
        'products': products_list,
    })


def product(request, serial_number):
    product_ = services.get_product(serial_number)
    if not product_:
        return redirect('index')
    comments = services.get_comments(product_)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.sender_id = request.user.id
            comment.product_id = product_.id
            comment.save()
            return redirect('show_product', serial_number=product_.serial_number)

        else:
            return redirect('show_product', serial_number=product_.serial_number)
    else:
        form = CommentForm()
        return render(request, 'plumbing/product_view.html', context={
            'product': product_,
            'comments': comments,
            'form': form,
        })


def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            services.create_basket(username)
            return redirect('login')
        else:
            return render(request, 'registration/registration.html', {
                'form': form,
                'errors': form.error_messages,
            })
    elif request.method == "GET":
        form = UserCreationForm()
        return render(request, 'registration/registration.html', {'form': form})


def basket(request, user_id):
    products = services.get_user_products(user_id)
    cost = 0
    for product_ in products:
        cost += product_.cost
    return render(request, 'plumbing/basket.html', context={
        'products': products,
        'cost': cost,
    })


def add_to_card(request, serial_number):
    services.add_to_card(request.user, serial_number)
    return redirect('basket', user_id=request.user.id)


def remove_from_card(request, serial_number):
    services.remove_from_card(request.user, serial_number)
    return redirect('basket', user_id=request.user.id)


def order(request, serial_number):
    product_ = services.get_product(serial_number)
    if request.method == "POST":
        form = OrderForm(request.POST)
        if form.is_valid():
            if services.change_instance_status(serial_number):
                offer = form.save(commit=False)
                offer.customer = request.user
                offer.cost = product_.cost
                offer.product_name = product_.name
                offer.save()
                return redirect('index')
            else:
                return redirect('index')
        else:
            return render(request, 'plumbing/create_order.html', context={
                'form': form,
                'errors': form.errors,
                'product': product_,
            })
    elif request.method == "GET":
        form = OrderForm()
        return render(request, 'plumbing/create_order.html', context={
            'form': form,
            'product': product_,
        })


def orders(request, user_id):
    return render(request, 'plumbing/orders.html', context={
        'orders': services.get_orders(user_id),
        'user_id': user_id,
    })
