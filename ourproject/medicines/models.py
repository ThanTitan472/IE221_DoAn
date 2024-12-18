from django.db import models
from django.urls import reverse

class Category(models.Model):
  category_id = models.CharField(max_length=5, unique=True, primary_key=True)
  name = models.CharField(max_length=20)
  description = models.TextField(null=True, blank=True)


class Supplier(models.Model):
  supplier_id = models.CharField(max_length=5, unique=True, primary_key=True)
  name = models.CharField(max_length=50)
  contact_info = models.CharField(max_length=10)
  address = models.CharField(max_length=30)


class Medicine(models.Model):
  medicine_id = models.CharField(max_length=5, unique=True, primary_key=True)
  name = models.CharField(max_length=20)
  category_id = models.ForeignKey(Category, on_delete=models.CASCADE, to_field='category_id')
  dosage_form = models.CharField(max_length=10)
  strength = models.CharField(max_length=10)
  quantity_in_stock = models.IntegerField()
  price = models.IntegerField()
  expiry_date = models.DateField()
  supplier_id = models.ForeignKey(Supplier, on_delete=models.CASCADE, to_field='supplier_id')

  def check_stock(self, quantity):
    if self.quantity_in_stock < quantity:
        raise ValueError("Không đủ thuốc có sẵn")

  def reduce_stock(self, quantity):
    self.quantity_in_stock -= quantity
    self.save()


class Customer(models.Model):
  customer_id = models.CharField(max_length=5, unique=True, primary_key=True)
  name = models.CharField(max_length=50)
  contact_number = models.CharField(max_length=10, blank=True, null=True)
  address = models.CharField(max_length=30, blank=True, null=True)
  date_of_birth = models.DateField(blank=True, null=True)


class Employee(models.Model):
  employee_id = models.CharField(max_length=5, unique=True, primary_key=True)
  name = models.CharField(max_length=50)
  position = models.CharField(max_length=50)
  contact_number = models.CharField(max_length=10)
  hire_date = models.DateField()
  salary = models.IntegerField()
  date_of_birth = models.DateField()


class Sale(models.Model):
  sale_id = models.CharField(max_length=5, unique=True, primary_key=True)
  customer_id = models.ForeignKey(Customer, on_delete=models.CASCADE, to_field='customer_id')
  sale_date = models.DateField(blank=True, null=True)
  status = models.BooleanField(default=False)
  total = models.IntegerField(blank=True, null=True)


class Order(models.Model):
  sale_id = models.ForeignKey(Sale, on_delete=models.CASCADE, to_field='sale_id')
  medicine_id = models.ForeignKey(Medicine, on_delete=models.CASCADE, to_field='medicine_id')
  count = models.IntegerField()

class Cart(models.Model):
  sale_id = models.ForeignKey(Sale, on_delete=models.CASCADE, to_field='sale_id')
  medicine_id = models.ForeignKey(Medicine, on_delete=models.CASCADE, to_field='medicine_id')
  count = models.IntegerField()
