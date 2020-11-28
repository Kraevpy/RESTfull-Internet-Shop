from django.test import TestCase
from django.contrib.auth.models import User
from .models import Category, Company, Product, ProductInstance, Comments, Order
from . import services


class ServicesTest(TestCase):
    def setUp(self) -> None:
        self.first_category = Category.objects.create(
            name='a_test_category',
            parent=None
        )
        self.first_category.save()

        self.second_category = Category.objects.create(
            name='b_test_category',
            parent=None
        )
        self.second_category.save()

        self.first_subcategory = Category.objects.create(
            name='a_test_subcategory',
            parent=self.first_category
        )
        self.first_category.save()

        self.second_subcategory = Category.objects.create(
            name='b_test_subcategory',
            parent=self.second_category
        )
        self.second_subcategory.save()

        self.maker_company = Company.objects.create(
            type='m',
            name='maker_company',
            address='maker_address'
        )
        self.maker_company.save()

        self.importer_company = Company.objects.create(
            type='i',
            name='importer_company',
            address='importer_address'
        )
        self.importer_company.save()

        self.first_product = Product.objects.create(
            name='first_product',
            category=self.first_category,
            serial_number='first_serial',
            photo='first_photo',
            maker=self.maker_company,
            importer=self.importer_company,
            country='first_country',
            barcode='first_barcode',
            certificate='first_certificate',
            cost=10,
            description='first_description'
        )
        self.first_product.save()

        self.second_product = Product.objects.create(
            name='second_product',
            category=self.second_subcategory,
            serial_number='second_serial',
            photo='second_photo',
            maker=self.maker_company,
            importer=self.importer_company,
            country='second_country',
            barcode='second_barcode',
            certificate='second_certificate',
            cost=20,
            description='second_description'
        )
        self.second_product.save()

        self.first_instance = ProductInstance.objects.create(
            product=self.first_product,
            status='s'
        )
        self.first_instance.save()

        self.second_instance = ProductInstance.objects.create(
            product=self.second_product,
            status='b'
        )
        self.second_instance.save()

        self.user = User.objects.create(
            username='test_user',
            password='test_password',
            email='test_email@example.ex'
        )
        self.user.save()

        self.first_comment = Comments.objects.create(
            sender=self.user,
            text='first_comment_text',
            product=self.first_product
        )
        self.first_comment.save()

        self.second_comment = Comments.objects.create(
            sender=self.user,
            text='second_comment_text',
            product=self.second_product
        )
        self.second_comment.save()

        self.first_order = Order.objects.create(
            cost=10,
            customer=self.user,
            address='test_address',
            phone_number='+375333333333,',
            status='n',
            product_name='test_pr'
        )

    def tearDown(self) -> None:
        self.first_category.delete()
        self.second_category.delete()
        self.first_subcategory.delete()
        self.second_subcategory.delete()

    def test_get_all_categories(self):
        self.assertIn(self.first_category, services.get_all_categories())
        self.assertIn(self.second_category, services.get_all_categories())
        self.assertNotIn(self.first_subcategory, services.get_all_categories())
        self.assertEqual(services.get_all_categories()[0], self.first_category)
        self.assertEqual(services.get_all_categories()[1], self.second_category)

    def test_get_all_subcategories(self):
        self.assertIn(self.first_subcategory, services.get_all_subcategories())
        self.assertIn(self.second_subcategory, services.get_all_subcategories())
        self.assertNotIn(self.first_category, services.get_all_subcategories())
        self.assertEqual(services.get_all_subcategories()[0], self.first_subcategory)
        self.assertEqual(services.get_all_subcategories()[1], self.second_subcategory)

    def test_get_subcategories(self):
        self.assertEqual(services.get_subcategories(self.first_category.id)[0], self.first_subcategory)
        self.assertEqual(len(services.get_subcategories(self.first_category.id)), 1)

    def test_get_all_companies(self):
        self.assertIn(self.maker_company, services.get_all_companies())
        self.assertIn(self.importer_company, services.get_all_companies())

    def test_get_all_products(self):
        self.assertEqual(len(services.get_all_products()), 2)
        self.assertIn(self.first_product, services.get_all_products())
        self.assertIn(self.second_product, services.get_all_products())

    def test_get_product(self):
        self.assertEqual(self.first_product, services.get_product('first_serial'))
        self.assertIsNone(services.get_product('not exist serial'))

    def test_get_product_with_subcategory(self):
        self.assertIn(self.first_product, services.get_product_with_subcategory(self.first_category.id))
        self.assertEqual(1, len(services.get_product_with_subcategory(self.first_category.id)))

    def test_get_product_with_category(self):
        self.assertIn(self.second_product, services.get_product_with_category(self.second_category.id))
        self.assertEqual(1, len(services.get_product_with_category(self.second_category.id)))

    def test_get_all_instances(self):
        self.assertIn(self.first_instance, services.get_all_instances())
        self.assertIn(self.second_instance, services.get_all_instances())

    def test_change_instance_status(self):
        self.assertTrue(services.change_instance_status(self.first_instance.product.serial_number))
        self.assertEqual(ProductInstance.objects.get(id=self.first_instance.id).status, 'b')
        self.assertIsNone(services.change_instance_status(self.second_instance.product.serial_number))

    def test_get_all_comments(self):
        self.assertIn(self.first_comment, services.get_all_comments())
        self.assertIn(self.second_comment, services.get_all_comments())

    def test_get_comments(self):
        self.assertEqual(self.first_comment, services.get_comments(self.first_product)[0])
        self.assertEqual(self.second_comment, services.get_comments(self.second_product)[0])

    def test_create_basket(self):
        services.create_basket(self.user.username)
        self.user = User.objects.get(username=self.user.username)
        self.assertIsNotNone(self.user.basket)

    def test_add_to_card(self):
        services.create_basket(self.user.username)
        services.add_to_card(self.user, self.first_product.serial_number)
        services.add_to_card(self.user, self.second_product.serial_number)
        self.user = User.objects.get(username=self.user.username)
        self.assertIn(self.first_product, self.user.basket.products.all())
        self.assertIn(self.second_product, self.user.basket.products.all())

    def test_get_user_products(self):
        services.create_basket(self.user.username)
        services.add_to_card(self.user, self.first_product.serial_number)
        services.add_to_card(self.user, self.second_product.serial_number)
        self.assertIn(self.first_product, services.get_user_products(self.user.id))
        self.assertIn(self.second_product, services.get_user_products(self.user.id))

    def test_remove_from_card(self):
        services.create_basket(self.user.username)
        services.add_to_card(self.user, self.first_product.serial_number)
        services.add_to_card(self.user, self.second_product.serial_number)
        services.remove_from_card(self.user, self.first_product.serial_number)
        services.remove_from_card(self.user, self.second_product.serial_number)
        self.user = User.objects.get(username=self.user.username)
        self.assertEqual(len(self.user.basket.products.all()), 0)

    def test_get_all_orders(self):
        self.assertIn(self.first_order, services.get_all_orders())

    def test_user_orders(self):
        self.assertEqual(len(services.get_orders(self.user.id)), 1)
