from django.contrib.auth.models import User
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=50)
    parent = models.ForeignKey('Category', null=True, blank=True, on_delete=models.CASCADE,
                               related_name='parent_field')

    def __str__(self):
        if not self.parent:
            type_ = "Category"
        else:
            type_ = "SubCategory"
        return "{0} ({1})".format(self.name, type_)


class Company(models.Model):
    TYPES = (
        ('m', 'Maker'),
        ('i', 'Importer'),
    )
    type = models.CharField(max_length=1, choices=TYPES)
    name = models.CharField(max_length=150)
    address = models.CharField(max_length=150)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=150)
    category = models.ForeignKey(Category, null=True, on_delete=models.SET_NULL)
    serial_number = models.CharField(max_length=150, unique=True)
    photo = models.URLField(max_length=300)
    maker = models.ForeignKey(Company, null=True, on_delete=models.SET_NULL, related_name='maker_field')
    importer = models.ForeignKey(Company, null=True, on_delete=models.SET_NULL)
    country = models.CharField(max_length=40)
    barcode = models.CharField(max_length=100, unique=True, null=True, blank=True)
    certificate = models.CharField(max_length=100, null=True, blank=True)
    cost = models.DecimalField(decimal_places=2, max_digits=10)
    delivery_date = models.DateField(null=True, blank=True)
    description = models.TextField(null=True)

    def __str__(self):
        return self.name

    def get_instance_count(self):
        return self.productinstance_set.filter(status='s').count()


class ProductInstance(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    STATUS = (
        ('s', 'In stock'),
        ('b', 'Booked'),
    )
    status = models.CharField(choices=STATUS, max_length=1, default='s')

    def __str__(self):
        return "{0} ({1})".format(self.product.name, self.get_status_display())


class Comments(models.Model):
    sender = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    text = models.TextField(max_length=2000)
    send_data_time = models.DateTimeField(auto_now=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)


class Basket(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product, blank=True)


class Order(models.Model):
    cost = models.DecimalField(decimal_places=2, max_digits=10)
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    data_time = models.DateTimeField(auto_now=True)
    address = models.CharField(max_length=300)
    phone_number = PhoneNumberField()
    STATUS = (
        ('n', 'Not confirmed'),
        ('c', 'Confirmed'),
        ('s', 'Submitted'),
        ('r', 'Received'),
    )
    status = models.CharField(choices=STATUS, max_length=1, default='n')
    product_name = models.CharField(max_length=150)

    def get_status(self):
        return self.get_status_display()

    def __str__(self):
        return "{0}, {1}, {2} BYN, {3}".format(self.product_name, self.get_status(), self.cost, self.phone_number)
