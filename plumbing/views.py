from django.contrib.auth import login, authenticate
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import ListView, CreateView, FormView

from .forms import OrderForm, RegistrationForm
from plumbing import services
from .models import Product, Comments
from plumbing_rest import services as rest_services


class ProductsListView(ListView):
    model = Product
    context_object_name = 'products'
    template_name = 'plumbing/home_page.html'
    paginate_by = 10

    def get_queryset(self):
        if not self.kwargs.get('category_id', None):
            # If the category_id is not passed then we return all products
            return rest_services.get_all_products()
        if self.kwargs.get('subcategory_id', None):
            # If the subcategory_id is passed, we return the products related to this subcategory
            return services.get_product_with_subcategory(self.kwargs.get('subcategory_id', None))
        else:
            # If you passed category_id, we return products related to this category
            return services.get_product_with_category(self.kwargs.get('category_id', None))

    def get_context_data(self, *, object_list=None, **kwargs):
        categories_ = services.get_subcategories(self.kwargs.get('category_id', None))
        context = super().get_context_data(**kwargs)
        context['categories'] = categories_
        return context


class ProductDetail(CreateView):
    model = Comments
    fields = ['text', ]
    template_name = 'plumbing/product_view.html'

    def get_success_url(self):
        """Redirect after successfully submitting a comment"""
        return reverse('show_product', kwargs={'serial_number': self.kwargs['serial_number']})

    def form_valid(self, form):
        """Adding product id and sender id to a comment"""
        product_ = services.get_product(self.kwargs.get('serial_number', None))
        form.instance.product_id = product_.id
        form.instance.sender_id = self.request.user.id
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        """We return all information about the product and comments to it"""
        context = super(ProductDetail, self).get_context_data()
        product_ = services.get_product(self.kwargs.get('serial_number', None))
        if not product_:
            return redirect('index')
        comments = services.get_comments(product_)
        context['product'] = product_
        context['comments'] = comments
        return context


class RegistrationView(FormView):
    model = User
    form_class = RegistrationForm
    template_name = 'registration/registration.html'
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        form.save()
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password1')
        email = form.cleaned_data.get('email')
        user = authenticate(username=username, password=password, email=email)
        login(self.request, user)
        services.create_basket(username)
        services.send_email_successful_registration(email)
        return super(RegistrationView, self).form_valid(form)


class BasketView(LoginRequiredMixin, ListView):
    template_name = 'plumbing/basket.html'
    context_object_name = 'products'

    def get_queryset(self):
        return services.get_user_products(self.kwargs.get('user_id', None))

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(BasketView, self).get_context_data()
        products = services.get_user_products(self.kwargs.get('user_id', None))
        cost = 0
        for product_ in products:
            cost += product_.cost
        context.update({'cost': cost})
        return context


class AddToCard(LoginRequiredMixin, View):
    @staticmethod
    def get(request, serial_number):
        services.add_to_card(request.user, serial_number)
        return redirect('basket', user_id=request.user.id)


class RemoveFromCard(LoginRequiredMixin, View):
    @staticmethod
    def get(request, serial_number):
        services.remove_from_card(request.user, serial_number)
        return redirect('basket', user_id=request.user.id)


class CreateOrder(LoginRequiredMixin, FormView):
    form_class = OrderForm
    template_name = 'plumbing/create_order.html'

    def get_success_url(self):
        return reverse('orders', kwargs={'user_id': self.request.user.id})

    def get_context_data(self, **kwargs):
        context = super(CreateOrder, self).get_context_data()
        product_ = services.get_product(self.kwargs.get('serial_number', None))
        context['product'] = product_
        return context

    def form_valid(self, form):
        if services.change_instance_status(self.kwargs.get('serial_number', None)):
            product_ = services.get_product(self.kwargs.get('serial_number', None))
            offer = form.save(commit=False)
            offer.customer = self.request.user
            offer.cost = product_.cost
            offer.product_name = product_.name
            offer.save()
            services.send_email_create_order(
                offer.customer.email,
                offer.product_name,
                offer.cost
            )
            return super(CreateOrder, self).form_valid(offer)
        else:
            return redirect('index')


class OrdersList(LoginRequiredMixin, ListView):
    template_name = 'plumbing/orders.html'
    context_object_name = 'orders'

    def get_queryset(self):
        return services.get_orders(self.kwargs.get('user_id', None))

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(OrdersList, self).get_context_data()
        context.update({'user_id': self.request.user.id})
        return context
