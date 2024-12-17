from django.db import models
from django.urls import reverse
# Create your models here.
class Category(models.Model):
  # CategoryID,CategoryName,Description
  category_id = models.CharField(max_length=5, unique=True, primary_key=True)
  name = models.CharField(max_length=20)
  description = models.TextField(null=True,blank=True)

  def get_absolute_url(self):
    return reverse("medicines:show-detail-category", kwargs={'key_id': self.pk})
  # def __init__(self):
  #   return f'Mã phân lọai thuốc: {self.category_id}\nTên phân loại thuốc: {self.name}\nMô tả: {self.description}\n'

class Supplier(models.Model):
  supplier_id = models.CharField(max_length=5, unique=True, primary_key=True)
  name = models.CharField(max_length=50)
  contact_info = models.CharField(max_length=10)
  address = models.CharField(max_length=30)

  def get_absolute_url(self):
    return reverse("medicines:show-detail-supplier", kwargs={'key_id': self.pk})
  # def __str__(self):
  #   return f'Mã nhà cung cấp thuốc: {self.supplier_id}\nTên nhà cung cấp thuốc: {self.name}\nSố điện thoại liên hệ: {self.contact_info}\nĐịa chỉ nhà cung cấp: {self.address}\n'

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

  # def __str__(self):
  #    return f'{self.medicine_id}{self.name}{self.category_id}{self.dosage_form}{self.strength}{self.quantity_in_stock}{self.price}{datetime.strptime(self.expiry_date, "%B %d, %Y").strftime("%d/%m/%Y")}{self.supplier_id}'
  def get_absolute_url(self):
    return reverse("medicines:show-detail-medicine", kwargs={'key_id': self.pk})

#/////////////////////////////////////////////
# CustomerID,Name,ContactNumber,Address,DateOfBirth
class Customer(models.Model):
  customer_id = models.CharField(max_length=5,unique= True, primary_key=True)
  name = models.CharField(max_length=50)
  contact_number = models.CharField(max_length=10,blank=True, null=True)
  address = models.CharField(max_length=30,blank=True, null=True)
  date_of_birth = models.DateField(blank=True, null=True)
  
  def get_absolute_url(self):
    return reverse("medicines:show-detail-customer", kwargs={'key_id': self.pk})
#EmployeeID,Name,Position,ContactNumber,HireDate,Salary,DateOfBirth
class Employee(models.Model):
  employee_id = models.CharField(max_length=5,unique=True,primary_key=True)
  name = models.CharField(max_length=50)
  position = models.CharField(max_length=50)
  contact_number = models.CharField(max_length=10)
  hire_date = models.DateField()
  salary = models.IntegerField()
  date_of_birth = models.DateField()
  def get_absolute_url(self):
    return reverse("medicines:show-detail-employee", kwargs={'key_id': self.pk})
# SaleID,MedicineID,CustomerID,QuantitySold,SaleDate,TotalPrice
class Sale(models.Model):
  sale_id = models.CharField(max_length=5,unique=True, primary_key=True)
  # medicine_id = models.ForeignKey(Medicine, on_delete=models.CASCADE,to_field='medicine_id')
  customer_id = models.ForeignKey(Customer, on_delete=models.CASCADE, to_field='customer_id')
  # quantity_sold = models.IntegerField()
  sale_date = models.DateField(blank=True, null=True)
  status = models.BooleanField(default=False)
  # total = models.IntegerField(editable=False)
  total = models.IntegerField(blank=True, null=True)

  # def save(self, *args, **kwargs):
  #   self.total = self.quantity_sold * self.medicine_id.price
  #   super().save(*args, **kwargs)

  def get_absolute_url(self):
    return reverse("medicines:show-detail-sale", kwargs={'key_id': self.pk})
class Order(models.Model):
  sale_id = models.ForeignKey(Sale, on_delete=models.CASCADE, to_field='sale_id')
  medicine_id = models.ForeignKey(Medicine, on_delete=models.CASCADE, to_field='medicine_id')
  count = models.IntegerField()
class Cart(models.Model):
  sale_id = models.ForeignKey(Sale, on_delete=models.CASCADE, to_field='sale_id')
  medicine_id = models.ForeignKey(Medicine, on_delete=models.CASCADE, to_field='medicine_id')
  count = models.IntegerField()
    