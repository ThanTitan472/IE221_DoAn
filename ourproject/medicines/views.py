from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.decorators import user_passes_test
from .forms import *
from .models import *
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.forms import DateField
from django.urls import reverse
from django.http import HttpResponse
from django.contrib.auth.decorators import user_passes_test
from .utils import user_required_permission
from datetime import datetime

from django.shortcuts import render, redirect

def home_view(request):
    if not request.user or not request.user.is_authenticated:
        return redirect("/login")

    if request.user.is_superuser:
        text = 'Chào mừng admin'
    else:
        text = f'Chào mừng {request.user.username}'

    return render(request, 'home.html', {'text': text})
class LoginView:
  def register_view(response):
    if response.method =="POST":
      form =  RegisterForm(response.POST)
      if form.is_valid():

        user = form.save(commit=False)  # Chưa lưu vào database
        user.is_superuser = False       # Không phải admin
        user.is_staff = False           # Không có quyền staff
        user.save()
        return redirect("/login")

    else:
      form =  RegisterForm()
    print(form)
    return render(response, "register.html", {"form":form})

  def login_view(request):
    if request.method == 'POST':
      form = LoginForm(request.POST)
      if form.is_valid():
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        
        user = authenticate(request, username=username, password=password)
          
        if user is not None:
          login(request, user)
          messages.success(request, "Đăng nhập thành công.")
          return redirect('/profile')  # Chuyển hướng sau khi đăng nhập thành công
        else:
          messages.error(request, "Tài khoản hoặc mật khẩu không chính xác.")  # Thông báo khi đăng nhập thất bại
      else:
          messages.error(request, "Vui lòng kiểm tra lại thông tin đăng nhập.")  # Khi form không hợp lệ
    else:
      form = LoginForm()
    
    return render(request, 'login.html', {'form': form})

  def logout_view(response):
    logout(response)
    return redirect("/login")
class UserView:
  def view_profile(request):
    return render(request, 'profile.html', {'user': request.user})
  def edit_profile(request):
    if request.method == 'POST':
      form = ProfilePasswordChangeForm(data=request.POST, user=request.user)
      if form.is_valid():
          form.save()
          messages.success(request, "Thông tin của bạn đã được cập nhật thành công.")
          return redirect('/login')
    else:
      form = ProfilePasswordChangeForm(user=request.user)

    return render(request, 'edit_profile.html', {'form': form})
  @user_required_permission(allowed_roles=['admin'], message="Bạn không có quyền truy cập.")
  def user_list(request):
    users = User.objects.all()  # Lấy toàn bộ User từ database
    return render(request, 'user_list.html', {'users': users})
  @user_required_permission(allowed_roles=['admin'], message="Bạn không có quyền truy cập.")
  def delete_user(request, pk):
    user = get_object_or_404(User, pk=pk)
    if request.method == "POST":
        if user.is_superuser:
            messages.error(request, "Không thể xóa tài khoản admin.")
            return redirect('/users')
        user.delete()
        messages.success(request, 'Tài khoản đã được xóa thành công.')
        return redirect('/users')
    return render(request, 'confirm_delete_user.html', {'user': user})


class MedicineView:
  def show_medicine(request):
    medicines = Medicine.objects.all()
    
    form_list = []
    
    for medicine in medicines:
        form = MedicineForm(instance=medicine)
        
        for field in form:
            field.is_date = isinstance(field.field, DateField)
        
        url_update = reverse("medicines:update-medicine", kwargs={'key_id': medicine.pk})
        url_delete = reverse("medicines:delete-medicine", kwargs={'key_id': medicine.pk})
        url_cart = reverse("medicines:add-cart", kwargs={'key_id': medicine.pk})
        form_list.append({
            'form': form,
            'url_update': url_update,
            'url_delete': url_delete,
            'url_cart': url_cart
        })
    
    return render(request, 'show_medicine.html', {
        'form_list': form_list,
        'url_add': reverse("medicines:add-medicine")
    })
  @user_required_permission(allowed_roles=['admin'], message="Bạn không có quyền truy cập.")
  def add_medicine(request):
    if request.method == 'POST':
      form = MedicineForm(request.POST)
      if form.is_valid():
        form.save()
        form = MedicineForm()
    else:
        form = MedicineForm()
    return render(request, 'add_medicine.html', {'form': form})
  @user_required_permission(allowed_roles=['admin'], message="Bạn không có quyền truy cập.")
  def update_medicine(request, key_id):
    if request.method == 'POST':
      row = get_object_or_404(Medicine, pk=key_id)
      form = MedicineForm(request.POST,instance=row)
      if form.is_valid():
        form.save()
      return redirect('../../')
    else:
      row = get_object_or_404(Medicine, pk=key_id)
      form = MedicineForm(instance=row)
    return render(request,'update_medicine.html',{'form':form})
  @user_required_permission(allowed_roles=['admin'], message="Bạn không có quyền truy cập.")
  def delete_medicine(request,key_id):
    row = get_object_or_404(Medicine, pk=key_id)
    if request.method == 'POST':
      row.delete()
      return redirect('../../')
    return render(request, 'delete_medicine.html',{'object':row})
class CategoryView:
  @user_required_permission(allowed_roles=['admin'], message="Bạn không có quyền truy cập.")
  def show_medicine(request):
    categorys = Category.objects.all()
    
    form_list = []
    
    for category in categorys:
        form = CategoryForm(instance=category)
        
        for field in form:
            field.is_date = isinstance(field.field, DateField)
        
        url_update = reverse("medicines:update-category", kwargs={'key_id': category.pk})
        url_delete = reverse("medicines:delete-category", kwargs={'key_id': category.pk})
        form_list.append({
            'form': form,
            'url_update': url_update,
            'url_delete': url_delete,
        })
        return render(request, 'show_medicine.html', {
        'form_list': form_list,
        'url_add': reverse("medicines:add-category")
    })
  @user_required_permission(allowed_roles=['admin'], message="Bạn không có quyền truy cập.")
  def add_medicine(request):
    if request.method == 'POST':
      form = CategoryForm(request.POST)
      if form.is_valid():
        form.save()
        form = CategoryForm()
    else:
        form = CategoryForm()
    return render(request, 'add_medicine.html', {'form': form})
  @user_required_permission(allowed_roles=['admin'], message="Bạn không có quyền truy cập.")
  def update_medicine(request, key_id):
    if request.method == 'POST':
      row = get_object_or_404(Category, pk=key_id)
      form = CategoryForm(request.POST,instance=row)
      if form.is_valid():
        form.save()
      return redirect('../../')
    else:
      row = get_object_or_404(Category, pk=key_id)
      form = CategoryForm(instance=row)
    return render(request,'update_medicine.html',{'form':form})
  @user_required_permission(allowed_roles=['admin'], message="Bạn không có quyền truy cập.")
  def delete_medicine(request,key_id):
    row = get_object_or_404(Category, pk=key_id)
    if request.method == 'POST':
      row.delete()
      return redirect('../../')
    return render(request, 'delete_medicine.html',{'object':row})
class SupplierView:
  @user_required_permission(allowed_roles=['admin'], message="Bạn không có quyền truy cập.")
  def show_medicine(request):
    suppliers = Supplier.objects.all()
    
    form_list = []
    
    for supplier in suppliers:
        form = SupplierForm(instance=supplier)
        
        for field in form:
            field.is_date = isinstance(field.field, DateField)
        
        url_update = reverse("medicines:update-supplier", kwargs={'key_id': supplier.pk})
        url_delete = reverse("medicines:delete-supplier", kwargs={'key_id': supplier.pk})
        form_list.append({
            'form': form,
            'url_update': url_update,
            'url_delete': url_delete,
        })
    
    return render(request, 'show_medicine.html', {
        'form_list': form_list,
        'url_add': reverse("medicines:add-supplier")
    })
  @user_required_permission(allowed_roles=['admin'], message="Bạn không có quyền truy cập.")
  def add_medicine(request):
    if request.method == 'POST':
      form = SupplierForm(request.POST)
      if form.is_valid():
        form.save()
        form = SupplierForm()
    else:
        form = SupplierForm()
    return render(request, 'add_medicine.html', {'form': form})
  @user_required_permission(allowed_roles=['admin'], message="Bạn không có quyền truy cập.")
  def update_medicine(request, key_id):
    if request.method == 'POST':
      row = get_object_or_404(Supplier, pk=key_id)
      form = SupplierForm(request.POST,instance=row)
      if form.is_valid():
        form.save()
      return redirect('../../')
    else:
      row = get_object_or_404(Supplier, pk=key_id)
      form = SupplierForm(instance=row)
    return render(request,'update_medicine.html',{'form':form})
  @user_required_permission(allowed_roles=['admin'], message="Bạn không có quyền truy cập.")
  def delete_medicine(request,key_id):
    row = get_object_or_404(Supplier, pk=key_id)
    if request.method == 'POST':
      row.delete()
      return redirect('../../')
      # return redirect('/medicine/')
    return render(request, 'delete_medicine.html',{'object':row})
class CustomerView:
  @user_required_permission(allowed_roles=['admin'], message="Bạn không có quyền truy cập.")
  def show_medicine(request):
    customers = Customer.objects.all()
    
    form_list = []
    
    for customer in customers:
        form = CustomerForm(instance=customer)
        
        for field in form:
            field.is_date = isinstance(field.field, DateField)
        
        url_update = reverse("medicines:update-customer", kwargs={'key_id': customer.pk})
        url_delete = reverse("medicines:delete-customer", kwargs={'key_id': customer.pk})
        form_list.append({
            'form': form,
            'url_update': url_update,
            'url_delete': url_delete,
        })
    
    return render(request, 'show_medicine.html', {
        'form_list': form_list,
        'url_add': reverse("medicines:add-customer")
    })
  @user_required_permission(allowed_roles=['admin'], message="Bạn không có quyền truy cập.")
  def add_medicine(request):
    if request.method == 'POST':
      form = CustomerForm(request.POST)
      if form.is_valid():
        form.save()
        form = CustomerForm()
    else:
        form = CustomerForm()
    return render(request, 'add_medicine.html', {'form': form})
  @user_required_permission(allowed_roles=['admin'], message="Bạn không có quyền truy cập.")
  def update_medicine(request, key_id):
    if request.method == 'POST':
      row = get_object_or_404(Customer, pk=key_id)
      form = CustomerForm(request.POST,instance=row)
      if form.is_valid():
        form.save()
      return redirect('../../')
    else:
      row = get_object_or_404(Customer, pk=key_id)
      form = CustomerForm(instance=row)
    return render(request,'update_medicine.html',{'form':form})
  @user_required_permission(allowed_roles=['admin'], message="Bạn không có quyền truy cập.")
  def delete_medicine(request,key_id):
    row = get_object_or_404(Customer, pk=key_id)
    if request.method == 'POST':
      row.delete()
      return redirect('../../')
      # return redirect('/medicine/')
    return render(request, 'delete_medicine.html',{'object':row})
class EmployeeView:
  @user_required_permission(allowed_roles=['admin'], message="Bạn không có quyền truy cập.")
  def show_medicine(request):
    employees = Employee.objects.all()
    
    form_list = []
    
    for employee in employees:
        form = EmployeeForm(instance=employee)
        
        # Xử lý các trường để kiểm tra kiểu dữ liệu, ví dụ như trường DateField
        for field in form:
            field.is_date = isinstance(field.field, DateField)
        
        # Tạo URL cho các nút update và delete
        url_update = reverse("medicines:update-employee", kwargs={'key_id': employee.pk})
        url_delete = reverse("medicines:delete-employee", kwargs={'key_id': employee.pk})
        # Thêm form và các URL vào trong danh sách
        form_list.append({
            'form': form,
            'url_update': url_update,
            'url_delete': url_delete,
        })
    
    return render(request, 'show_medicine.html', {
        'form_list': form_list,
        'url_add': reverse("medicines:add-employee")
    })
  @user_required_permission(allowed_roles=['admin'], message="Bạn không có quyền truy cập.")
  def add_medicine(request):
    if request.method == 'POST':
      form = EmployeeForm(request.POST)
      if form.is_valid():
        form.save()
        form = EmployeeForm()
    else:
        form = EmployeeForm()
    return render(request, 'add_medicine.html', {'form': form})
  @user_required_permission(allowed_roles=['admin'], message="Bạn không có quyền truy cập.")
  def update_medicine(request, key_id):
    if request.method == 'POST':
      row = get_object_or_404(Employee, pk=key_id)
      form = EmployeeForm(request.POST,instance=row)
      if form.is_valid():
        form.save()
      return redirect('../../')
    else:
      row = get_object_or_404(Employee, pk=key_id)
      form = EmployeeForm(instance=row)
    return render(request,'update_medicine.html',{'form':form})
  @user_required_permission(allowed_roles=['admin'], message="Bạn không có quyền truy cập.")
  def delete_medicine(request,key_id):
    row = get_object_or_404(Employee, pk=key_id)
    if request.method == 'POST':
      row.delete()
      return redirect('../../')
    return render(request, 'delete_medicine.html',{'object':row})
class CartView():
  def add_medicine(request, key_id):
    if request.method == 'POST':
        customer_count = Customer.objects.count() + 1
        customer_id = f'CU{customer_count:03d}'

        sale_count = Sale.objects.count() + 1
        sale_id = f'SL{sale_count:03d}'

        customer_name = request.user.username
        find = Customer.objects.filter(name=customer_name).first()  # Lấy khách hàng đầu tiên
        
        if not find:  # Nếu khách hàng chưa tồn tại
            cus = Customer.objects.create(customer_id=customer_id, name=customer_name)
            sale_in = Sale.objects.create(sale_id=sale_id, customer_id=cus)
            medicine = Medicine.objects.get(medicine_id=key_id)  # Lấy đối tượng Medicine
            Cart.objects.create(sale_id=sale_in, medicine_id=medicine, count=request.POST.get('count'))
        else:
            sale_in = Sale.objects.filter(customer_id=find.customer_id, status=False).first()
            
            if not sale_in:  # Nếu chưa có Sale nào chưa hoàn thành
                sale_in = Sale.objects.create(sale_id=sale_id, customer_id=find)
                medicine = Medicine.objects.get(medicine_id=key_id)  # Lấy đối tượng Medicine
                Cart.objects.create(sale_id=sale_in, medicine_id=medicine, count=request.POST.get('count'))
            else:
                check_cart = Cart.objects.filter(medicine_id=key_id, sale_id=sale_in).first()
                if not check_cart:  # Nếu không có Cart cho medicine_id này
                    medicine = Medicine.objects.get(medicine_id=key_id)  # Lấy đối tượng Medicine
                    Cart.objects.create(sale_id=sale_in, medicine_id=medicine, count=request.POST.get('count'))
                else:
                    # Cập nhật số lượng mới
                    count_new = check_cart.count + int(request.POST.get('count'))
                    check_cart.count = count_new
                    check_cart.save()

    return redirect('/medicine')
  def show_medicine(request):
    try:
        customer = Customer.objects.get(name=request.user.username)
    except Customer.DoesNotExist:
        messages.error(request, "Không tìm thấy khách hàng tương ứng với tài khoản của bạn!")
        return render(request, 'show_cart.html', {
            'form_list': [],
            'sum_o': 0
        })
    # carts = Cart.objects.all()
    sales = Sale.objects.filter(customer_id=customer)

    # Lấy tất cả các Cart liên quan đến Sale của khách hàng
    carts = Cart.objects.filter(sale_id__in=sales)
    form_list = []
    sum_o = 0
    for cart in carts:
        sum_o += cart.medicine_id.price * cart.count
        form = CartForm(initial={
            'medicine_name': cart.medicine_id.name,
            'medicine_price': cart.medicine_id.price,
            'count': cart.count
        })
        url_update = reverse("medicines:update-cart", kwargs={'id':cart.id})
        url_delete = reverse("medicines:delete-cart", kwargs={'id': cart.id})
        form_list.append({
            'form': form,
            'url_update': url_update,
            'url_delete': url_delete
        })
    if not form_list:
        messages.error(request, "Giỏ hàng của bạn hiện tại trống!")
    return render(request, 'show_cart.html', {
        'form_list': form_list,
        'sum_o': sum_o
    })
  def update_medicine(request, id):
    row = get_object_or_404(Cart, pk=id)  # Lấy Cart hiện tại
    if request.method == 'POST':
        form = CartForm(request.POST)  # Khởi tạo form với dữ liệu POST
        if form.is_valid():  # Kiểm tra form có hợp lệ không
            row.count = form.cleaned_data['count']  # Cập nhật số lượng
            row.save()  # Lưu lại đối tượng đã được cập nhật
            return redirect('/cart')  # Điều hướng lại trang cart sau khi cập nhật thành công
    else:
        form = CartForm(initial={
            'medicine_name': row.medicine_id.name,
            'medicine_price': row.medicine_id.price,
            'count': row.count
        })
  def delete_medicine(request, id):
    row = get_object_or_404(Cart, pk=id)
    if request.method == 'POST':
      row.delete()
      return redirect('/cart')
  def pay_medicine(request):
    if request.method == 'POST':
      carts = Cart.objects.all()
      for cart in carts:
        medicine = cart.medicine_id
        quantity = cart.count
        try:
          medicine.check_stock(quantity)
        except ValueError as e:
          messages.error(request, str(e))
      for cart in carts:
        Order.objects.create(
          sale_id = cart.sale_id,
          medicine_id = cart.medicine_id,
          count = cart.count,
        )
        medicine = cart.medicine_id
        quantity = cart.count
        medicine.reduce_stock(quantity)
        sale = cart.sale_id
        sale.total = request.POST.get('sum_o')
        sale.status =True 
        sale.sale_date = datetime.now().strftime('%Y-%m-%d')
        sale.save()
      Cart.objects.all().delete()
    return redirect('/cart')
class OrderView():
  def show_medicine(request):
    orders = Order.objects.all()
    form_list = []
    for order in orders:
        form = CartForm(initial={
            'medicine_name': order.medicine_id.name,
            'medicine_price': order.medicine_id.price,
            'count': order.count
        })
        form_list.append({
            'form': form
        })
    return render(request, 'show_order.html', {'form_list': form_list})
class SaleView:
  @user_required_permission(allowed_roles=['admin'], message="Bạn không có quyền truy cập.")
  def show_medicine(request):
    sales = Sale.objects.all()
    form_list = []
    for sale in sales:
        form = SaleForm(instance=sale)
        form_list.append({
            'form': form
        })
    return render(request, 'show_order.html', {'form_list': form_list})

