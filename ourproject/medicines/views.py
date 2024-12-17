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

# def is_admin(user):
#     return user.is_superuser

# def is_registered_user(user):
#     return not user.is_superuser and not user.is_staff
def home_view(request):
  text = ''
  if request.user.is_superuser:
    text = 'Chào mừng admin'
  else:
    text = f'Chào mừng {request.user.username}'
  return render(request,'home.html',{'text':text})
# # Create your views here.
# class HomeView:
#   # @user_passes_test(is_admin)
#   # def home_view_admin(request):
#   #   return render(request, 'home_admin.html')
#   # @user_passes_test(is_registered_user)
#   # def home_view_user(request):
#   #   return render(request, 'home_user.html')
#   def home_view(request):
#     message = ''
#     if request.user.is_superuser:
#       message = 'Chào Admin! Đây là nội dung dành riêng cho bạn.'
#     else:
#       message = f'Chào {request.user.username}! Đây là nội dung dành riêng cho bạn.'
#     return render(request, 'home.html',{'message':message})

# class LoginView:
# # Create your views here.
#   def register_view(response):
#     if response.method =="POST":
#       form =  RegisterForm(response.POST)
#       if form.is_valid():
#         # form.save()

#         user = form.save(commit=False)  # Chưa lưu vào database
#         user.is_superuser = False       # Không phải admin
#         user.is_staff = False           # Không có quyền staff
#         user.save()
#         return redirect("/login")

#     else:
#       form =  RegisterForm()
#     print(form)
#     return render(response, "register.html", {"form":form})

#   def login_view(request):
#     if request.method == 'POST':
#       form = LoginForm(request.POST)
#       if form.is_valid():
#         username = form.cleaned_data['username']
#         password = form.cleaned_data['password']
        
#         user = authenticate(request, username=username, password=password)
          
#         if user is not None:
#           login(request, user)
#           messages.success(request, "Đăng nhập thành công.")
#           if user.is_superuser:
#             return redirect('/admin')  # Chuyển hướng sau khi đăng nhập thành công
#           else:
#             return redirect('/user')
#         else:
#           messages.error(request, "Tài khoản hoặc mật khẩu không chính xác.")  # Thông báo khi đăng nhập thất bại
#       else:
#           messages.error(request, "Vui lòng kiểm tra lại thông tin đăng nhập.")  # Khi form không hợp lệ
#     else:
#       form = LoginForm()
    
#     return render(request, 'login.html', {'form': form})

#   def logout_view(response):
#     logout(response)
#     return redirect("/login")
# class UserView:
#   def view_profile(request):
#     return render(request, 'profile.html', {'user': request.user})
#   def edit_profile(request):
#     if request.method == 'POST':
#       form = ProfilePasswordChangeForm(request.POST, user=request.user)
#       if form.is_valid():
#           form.save()
#           messages.success(request, "Thông tin của bạn đã được cập nhật thành công.")
#           return redirect('../')
#     else:
#       form = ProfilePasswordChangeForm(user=request.user)

#     return render(request, 'edit_profile.html', {'form': form})
#   @user_passes_test(is_admin)
#   def user_list(request):
#     users = User.objects.all()  # Lấy toàn bộ User từ database
#     return render(request, 'user_list.html', {'users': users})
#   @user_passes_test(is_admin)
#   def delete_user(request, pk):
#     user = get_object_or_404(User, pk=pk)
#     if request.method == "POST":
#         if user.is_superuser:
#             messages.error(request, "Không thể xóa tài khoản admin.")
#             return redirect('../')
#         user.delete()
#         messages.success(request, 'Tài khoản đã được xóa thành công.')
#         return redirect('/../users')
#     return render(request, 'confirm_delete_user.html', {'user': user})


#////////////////////////
class LoginView:
# Create your views here.
  def register_view(response):
    if response.method =="POST":
      form =  RegisterForm(response.POST)
      if form.is_valid():
        # form.save()

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
  # def edit_user(request,pk):
  #   user = get_object_or_404(User, pk=pk)
  #   if request.method == "POST":
  #       form = PasswordChangeForm(user, request.POST)
  #       if form.is_valid():
  #           form.save()
  #           messages.success(request, 'Mật khẩu đã được cập nhật thành công.')
  #           return redirect('user_list')
  #   else:
  #       form = PasswordChangeForm(user)
  #   return render(request, 'edit_user.html', {'form': form, 'user': user})
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
  
# class BaseView:
#   model = None
#   form_class = None
#   template_prefix = ""

#   def show_list(self, request):
#     obj_list = self.model.objects.all()
#     form_list = []
#     for obj in obj_list:
#       form = self.form_class(instance=obj)
#       for field in form:
#           field.is_date = isinstance(field.field, DateField)
        
#       url_update = reverse(f"medicines:update-{self.template_prefix}", kwargs={'key_id': obj.pk})
#       url_delete = reverse(f"medicines:delete-{self.template_prefix}", kwargs={'key_id': obj.pk})
        
        
#       form_list.append({
#           'form': form,
#           'url_update': url_update,
#           'url_delete': url_delete
#       })
    
    
#     return render(request,'show_medicine.html', {'form_list': form_list})

#   def add_object(self, request):
#     if request.method == 'POST':
#       form = self.form_class(request.POST)
#       if form.is_valid():
#         form.save()
#         form = self.form_class()
#     else:
#       form = self.form_class()
#     return render(request, 'add_medicine.html', {'form': form})

#   def update_object(self, request, key_id):
#     row = get_object_or_404(self.model, pk=key_id)
#     if request.method == 'POST':
#       form = self.form_class(request.POST, instance=row)
#       if form.is_valid():
#         form.save()
#         return redirect('../../')
#     else:
#       form = self.form_class(instance=row)
#     return render(request,'update_medicine.html',{'form':form})

#   def delete_object(self, request, key_id):
#       row = get_object_or_404(self.model, pk=key_id)
#       if request.method == 'POST':
#           row.delete()
#           return redirect('../../')
#       return render(request, 'delete_medicine.html',{'object':row})

# class MedicineView(BaseView):
#     model = Medicine
#     form_class = MedicineForm
#     template_prefix = "medicine"


class MedicineView:
  def show_medicine(request):
    # return render(request, 'show_medicine.html',{'object_list':Medicine.objects.all()})
    medicines = Medicine.objects.all()
    
    # Danh sách để lưu các form đã được khởi tạo cho mỗi Category
    form_list = []
    
    # Tạo form cho từng Category
    for medicine in medicines:
        form = MedicineForm(instance=medicine)
        
        # Xử lý các trường để kiểm tra kiểu dữ liệu, ví dụ như trường DateField
        for field in form:
            field.is_date = isinstance(field.field, DateField)
        
        # Tạo URL cho các nút update và delete
        url_update = reverse("medicines:update-medicine", kwargs={'key_id': medicine.pk})
        url_delete = reverse("medicines:delete-medicine", kwargs={'key_id': medicine.pk})
        url_cart = reverse("medicines:add-cart", kwargs={'key_id': medicine.pk})
        # Thêm form và các URL vào trong danh sách
        form_list.append({
            'form': form,
            'url_update': url_update,
            'url_delete': url_delete,
            'url_cart': url_cart
        })
    
    # Trả về view với tất cả các form và nút update, delete
    return render(request, 'show_medicine.html', {
        'form_list': form_list
    })
  # def show_detail(request,key_id):
  #   row = get_object_or_404(Medicine, pk=key_id)
  #   form = MedicineForm(instance=row)
  #   for field in form:
  #     field.is_date = isinstance(field.field, DateField)
  #   url_update = reverse("medicines:update-medicine", kwargs={'key_id': key_id})
  #   url_delete = reverse("medicines:delete-medicine", kwargs={'key_id': key_id})
  #   return render(request,'show_detail.html',{'form':form,'url_update': url_update,'url_delete':url_delete})
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
      # return redirect('/medicine/')
    return render(request, 'delete_medicine.html',{'object':row})
class CategoryView:
  @user_required_permission(allowed_roles=['admin'], message="Bạn không có quyền truy cập.")
  def show_medicine(request):
    categorys = Category.objects.all()
    
    # Danh sách để lưu các form đã được khởi tạo cho mỗi Category
    form_list = []
    
    # Tạo form cho từng Category
    for category in categorys:
        form = CategoryForm(instance=category)
        
        # Xử lý các trường để kiểm tra kiểu dữ liệu, ví dụ như trường DateField
        for field in form:
            field.is_date = isinstance(field.field, DateField)
        
        # Tạo URL cho các nút update và delete
        url_update = reverse("medicines:update-category", kwargs={'key_id': category.pk})
        url_delete = reverse("medicines:delete-category", kwargs={'key_id': category.pk})
        
        # Thêm form và các URL vào trong danh sách
        form_list.append({
            'form': form,
            'url_update': url_update,
            'url_delete': url_delete
        })
    
    # Trả về view với tất cả các form và nút update, delete
    return render(request, 'show_medicine.html', {
        'form_list': form_list
    })
  # def show_detail(request,key_id):
  #   row = get_object_or_404(Category, pk=key_id)
  #   form = CategoryForm(instance=row)
  #   for field in form:
  #     field.is_date = isinstance(field.field, DateField)
  #   url_update = reverse("medicines:update-category", kwargs={'key_id': key_id})
  #   url_delete = reverse("medicines:delete-category", kwargs={'key_id': key_id})
  #   return render(request,'show_detail.html',{'form':form,'url_update': url_update,'url_delete':url_delete})
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
      # return redirect('/medicine/')
    return render(request, 'delete_medicine.html',{'object':row})
class SupplierView:
  @user_required_permission(allowed_roles=['admin'], message="Bạn không có quyền truy cập.")
  def show_medicine(request):
    suppliers = Supplier.objects.all()
    
    # Danh sách để lưu các form đã được khởi tạo cho mỗi Category
    form_list = []
    
    # Tạo form cho từng Category
    for supplier in suppliers:
        form = SupplierForm(instance=supplier)
        
        # Xử lý các trường để kiểm tra kiểu dữ liệu, ví dụ như trường DateField
        for field in form:
            field.is_date = isinstance(field.field, DateField)
        
        # Tạo URL cho các nút update và delete
        url_update = reverse("medicines:update-supplier", kwargs={'key_id': supplier.pk})
        url_delete = reverse("medicines:delete-supplier", kwargs={'key_id': supplier.pk})
        
        # Thêm form và các URL vào trong danh sách
        form_list.append({
            'form': form,
            'url_update': url_update,
            'url_delete': url_delete
        })
    
    # Trả về view với tất cả các form và nút update, delete
    return render(request, 'show_medicine.html', {
        'form_list': form_list
    })
  # def show_detail(request,key_id):
  #   row = get_object_or_404(Supplier, pk=key_id)
  #   form = SupplierForm(instance=row)
  #   for field in form:
  #     field.is_date = isinstance(field.field, DateField)
  #   url_update = reverse("medicines:update-supplier", kwargs={'key_id': key_id})
  #   url_delete = reverse("medicines:delete-supplier", kwargs={'key_id': key_id})
  #   return render(request,'show_detail.html',{'form':form,'url_update': url_update,'url_delete':url_delete})
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
    
    # Danh sách để lưu các form đã được khởi tạo cho mỗi Category
    form_list = []
    
    # Tạo form cho từng Category
    for customer in customers:
        form = CustomerForm(instance=customer)
        
        # Xử lý các trường để kiểm tra kiểu dữ liệu, ví dụ như trường DateField
        for field in form:
            field.is_date = isinstance(field.field, DateField)
        
        # Tạo URL cho các nút update và delete
        url_update = reverse("medicines:update-customer", kwargs={'key_id': customer.pk})
        url_delete = reverse("medicines:delete-customer", kwargs={'key_id': customer.pk})
        
        # Thêm form và các URL vào trong danh sách
        form_list.append({
            'form': form,
            'url_update': url_update,
            'url_delete': url_delete
        })
    
    # Trả về view với tất cả các form và nút update, delete
    return render(request, 'show_medicine.html', {
        'form_list': form_list
    })
  # def show_detail(request,key_id):
  #   row = get_object_or_404(Customer, pk=key_id)
  #   form = CustomerForm(instance=row)
  #   for field in form:
  #     field.is_date = isinstance(field.field, DateField)
  #   url_update = reverse("medicines:update-customer", kwargs={'key_id': key_id})
  #   url_delete = reverse("medicines:delete-customer", kwargs={'key_id': key_id})
  #   return render(request,'show_detail.html',{'form':form,'url_update': url_update,'url_delete':url_delete})
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
    
    # Danh sách để lưu các form đã được khởi tạo cho mỗi Category
    form_list = []
    
    # Tạo form cho từng Category
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
            'url_delete': url_delete
        })
    
    # Trả về view với tất cả các form và nút update, delete
    return render(request, 'show_medicine.html', {
        'form_list': form_list
    })
  # def show_detail(request,key_id):
  #   row = get_object_or_404(Employee, pk=key_id)
  #   form = EmployeeForm(instance=row)
  #   for field in form:
  #     field.is_date = isinstance(field.field, DateField)
  #   url_update = reverse("medicines:update-employee", kwargs={'key_id': key_id})
  #   url_delete = reverse("medicines:delete-employee", kwargs={'key_id': key_id})
  #   return render(request,'show_detail.html',{'form':form,'url_update': url_update,'url_delete':url_delete})
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
      # return redirect('/medicine/')
    return render(request, 'delete_medicine.html',{'object':row})
# class SaleView:
#   def show_medicine(request):
#     sales = Sale.objects.all()
    
#     # Danh sách để lưu các form đã được khởi tạo cho mỗi Category
#     form_list = []
    
#     # Tạo form cho từng Category
#     for sale in sales:
#         form = SaleForm(instance=sale)
        
#         # Xử lý các trường để kiểm tra kiểu dữ liệu, ví dụ như trường DateField
#         for field in form:
#             field.is_date = isinstance(field.field, DateField)
        
#         # Tạo URL cho các nút update và delete
#         url_update = reverse("medicines:update-sale", kwargs={'key_id': sale.pk})
#         url_delete = reverse("medicines:delete-sale", kwargs={'key_id': sale.pk})
        
#         # Thêm form và các URL vào trong danh sách
#         form_list.append({
#             'form': form,
#             'url_update': url_update,
#             'url_delete': url_delete
#         })
    
#     # Trả về view với tất cả các form và nút update, delete
#     return render(request, 'show_medicine.html', {
#         'form_list': form_list
#     })
#   # def show_detail(request,key_id):
#   #   row = get_object_or_404(Sale, pk=key_id)
#   #   form = SaleForm(instance=row)
#   #   for field in form:
#   #     field.is_date = isinstance(field.field, DateField)
#   #   url_update = reverse("medicines:update-sale", kwargs={'key_id': key_id})
#   #   url_delete = reverse("medicines:delete-sale", kwargs={'key_id': key_id})
#   #   return render(request,'show_detail.html',{'form':form,'url_update': url_update,'url_delete':url_delete})
#   def add_medicine(request):
#     # if request.method == 'POST':
#     #   form = SaleForm(request.POST)
#     #   if form.is_valid():
#     #     form.save()
#     #     form = SaleForm()
#     # else:
#     #   form = SaleForm()
#     # return render(request, 'add_medicine.html', {'form': form})
#     if request.method == 'POST':
#       # Kiểm tra nếu đang ở bước "Calculate"
#       if 'calculate' in request.POST:
#         form = SaleForm(request.POST)
#         if form.is_valid():
#           # sale = form.cleaned_data['sale_id']
#           medicine = form.cleaned_data['medicine_id']
#           # customer = form.cleaned_data['customer_id']
#           quantity = form.cleaned_data['quantity_sold']
#           # date = form.cleaned_data['sale_date']
          
#           # Tính toán total_price
#           total = medicine.price * quantity

#           # Gắn giá trị total_price vào form (chưa lưu vào database)
#           form.initial['total'] = total
#           form.data = form.data.copy()  # Tạo bản sao POST data để sửa dữ liệu
#           form.data['total'] = total

#           return render(request, 'add_sale.html', {'form': form, 'step': 'calculate'})

#       # Nếu đang ở bước "Save"
#       elif 'save' in request.POST:
#         form = SaleForm(request.POST)
#         if form.is_valid():
#           medicine = form.cleaned_data['medicine_id']
#           quantity = form.cleaned_data['quantity_sold']
#           try:
#             medicine.reduce_stock(quantity)
#           except ValueError as e:
#             return render(request, 'add_sale.html', {
#                 'form': form,
#                 'step': 'initial',
#                 'error': str(e)
#             })
#           form.save()  # Lưu vào cơ sở dữ liệu

#           # Tạo form mới sau khi lưu
#           form = SaleForm()
#           return render(request, 'add_sale.html', {'form': form, 'step': 'initial', 'message': 'Saved successfully!'})

#     else:
#       # Hiển thị form ban đầu
#       form = SaleForm()

#     return render(request, 'add_sale.html', {'form': form, 'step': 'initial'})
#   def update_medicine(request, key_id):
#     if request.method == 'POST':
#       row = get_object_or_404(Sale, pk=key_id)
#       form = SaleForm(request.POST,instance=row)
#       if form.is_valid():
#         form.save()
#       return redirect('../../')
#     else:
#       row = get_object_or_404(Sale, pk=key_id)
#       form = SaleForm(instance=row)
#     return render(request,'update_medicine.html',{'form':form})
#   def delete_medicine(request,key_id):
#     row = get_object_or_404(Sale, pk=key_id)
#     if request.method == 'POST':
#       row.delete()
#       return redirect('../../')
#       # return redirect('/medicine/')
#     return render(request, 'delete_medicine.html',{'object':row})
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

        # Sau khi thực hiện thao tác, trả về redirect đến trang /medicine
    return redirect('/medicine')
    # if request.method == 'POST':
    #   customer_count = Customer.objects.count() +1
    #   customer_id = f'CU{customer_count:03d}'
      
    #   sale_count = Sale.objects.count() +1
    #   sale_id = f'SL{sale_count:03d}'
      
    #   customer_name = request.user.username
    #   find = Customer.objects.filter(name=customer_name)
    #   if find.exists() == False:
    #     cus = Customer.objects.create(customer_id=customer_id,name=customer_name)
    #     Sale.objects.create(sale_id=sale_id,customer_id=cus)
    #     Cart.objects.create(sale_id=sale_id,medicine_id=key_id,count=request.POST.get('count'))
    #   else:
    #     sale_in = Sale.objects.filter(customer_id=customer_id,status=True)
    #     if sale_in.exists() == False:
    #       Sale.objects.create(sale_id=sale_id,customer_id=find.customer_id)
    #       Cart.objects.create(sale_id=sale_id,medicine_id=key_id,count=request.POST.get('count'))
    #     else:
    #       check_cart = Cart.objects.filter(medicine_id=key_id)
    #       if check_cart.exists() == False:
    #         Cart.objects.create(sale_id=sale_in.sale_id,medicine_id=key_id,count=request.POST.get('count'))
    #       else:
    #         count_new = check_cart.count + request.POST.get('count')
    #         check_cart.count = count_new
    #         check_cart.save()
    # return redirect('/medicine')
  def show_medicine(request):
    carts = Cart.objects.all()
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
    # carts = Cart.objects.all()
    # form_list = []
    # sum_o = 0

    # if request.method == 'POST':
    #     # Duyệt qua các form đã gửi để cập nhật dữ liệu
    #     for item in form_list:
    #         form = item['form']
    #         if form.is_valid():
    #             # Lấy giá trị mới từ trường count và cập nhật
    #             new_count = form.cleaned_data['count']
    #             cart_instance = Cart.objects.get(id=item['form'].id)  # Lấy Cart theo id
    #             cart_instance.count = new_count
    #             cart_instance.save()

    # # Tạo form cho từng Cart
    # for cart in carts:
    #     sum_o += cart.medicine_id.price * cart.count
    #     form = CartForm(initial={
    #         'medicine_name': cart.medicine_id.name,
    #         'medicine_price': cart.medicine_id.price,
    #         'count': cart.count
    #     })
    #     form.id = cart.id  # Thêm id vào form để nhận diện khi update
    #     url_update = reverse("medicines:update-cart", kwargs={'id': cart.id})
    #     url_delete = reverse("medicines:delete-cart", kwargs={'id': cart.id})
    #     form_list.append({
    #         'form': form,
    #         'url_update': url_update,
    #         'url_delete': url_delete
    #     })

    # return render(request, 'show_cart.html', {
    #     'form_list': form_list,
    #     'sum_o': sum_o
    # })
  def update_medicine(request, id):
    # if request.method == 'POST':
    #   row = get_object_or_404(Cart,pk=id)
    #   form = CartForm(initial={
    #         'medicine_name': row.medicine_id.name,
    #         'medicine_price': row.medicine_id.price,
    #         'count': row.count
    #     })
    #   if form.is_valid():
    #     reg = Cart(sale_id=row.sale_id,medicine_id=row.medicine_id,count=form.cleaned_data['count'])
    #     reg.save()
    # return redirect('/cart')
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

#/////////////////////////




# class MedicineView:
#   def show_medicine(request):
#     return render(request, 'show_medicine.html',{'object_list':Medicine.objects.all()})
#   def show_detail(request,medicine_id):
#     # row = get_object_or_404(Medicine, medicine_id=medicine_id)
#     # # return render(request, 'show_detail.html',{'object':Medicine.objects.get(pk=id)})
#     # return render(request, 'show_detail.html',{'object':row})
    
#     # <!-- <td>
#     #     {% if field.field.__class__.__name__ == "DateField" %}
#     #         {{ field.value|date:"d/m/Y" }}
#     #     {% else %}
#     #         {{ field.value }}
#     #     {% endif %}
#     #   </td> -->

#     # <!-- <button onclick="location.href='{% url 'medicines:update-medicine' object.medicine_id %}';">Update</button>
#     # <button onclick="location.href='{% url 'medicines:delete-medicine' object.medicine_id %}';">Delete</button> -->

#     row = get_object_or_404(Medicine, pk=medicine_id)
#     form = MedicineForm(instance=row)
#     for field in form:
#         field.is_date = isinstance(field.field, DateField)
#     return render(request,'show_detail.html',{'form':form})

#   # def is_admin(user):
#   #   return user.is_superuser
#   # @user_passes_test(is_admin)
  # def add_medicine(request):
  #   if request.method == 'POST':
  #     form = MedicineForm(request.POST)
  #     if form.is_valid():
  #       # m_id = form.cleaned_data['medicine_id']
  #       # nm = form.cleaned_data['name']
  #       # c_id = form.cleaned_data['category_id']
  #       # df = form.cleaned_data['dosage_form']
  #       # sth = form.cleaned_data['strength']
  #       # qis = form.cleaned_data['quantity_in_stock']
  #       # pr = form.cleaned_data['price']
  #       # ed = form.cleaned_data['expiry_date']
  #       # s_id = form.cleaned_data['supplier_id']
  #       # # Category.objects.get(categoty_id=c_id)
  #       # # Supplier.objects.get(supplier_id=s_id)
  #       # reg = Medicine(medicine_id=m_id,name=nm,category_id=c_id,dosage_form=df,strength=sth,quantity_in_stock=qis,price=pr,expiry_date=ed,supplier_id=s_id)
  #       # reg.save()
  #       form.save()
  #       form = MedicineForm()
  #   else:
  #     form = MedicineForm()
  #   return render(request, 'add_medicine.html', {'form': form})
#   # @user_passes_test(is_admin)
#   def update_medicine(request, medicine_id):
#     # update: form ra id cua cac class khac chu khong hien ra ..._id cua class
#     if request.method == 'POST':
#       row = get_object_or_404(Medicine, medicine_id=medicine_id)
#       form = MedicineForm(request.POST,instance=row)
#       if form.is_valid():
#         form.save()
#       return redirect('../')
#     else:
#       row = get_object_or_404(Medicine, medicine_id=medicine_id)
#       form = MedicineForm(instance=row)
#     return render(request,'update_medicine.html',{'form':form})
#   # @user_passes_test(is_admin)
#   def delete_medicine(request,medicine_id):
#     row = get_object_or_404(Medicine, medicine_id=medicine_id)
#     if request.method == 'POST':
#       row.delete()
#       return redirect('../../')
#       # return redirect('/medicine/')
#     return render(request, 'delete_medicine.html',{'object':row})

# class CategoryView:
#   def show_category(request):
#     return render(request, 'show_medicine.html',{'object_list':Category.objects.all()})
#   def show_detail(request, category_id):
#     row = get_object_or_404(Category, category_id=category_id)
#     return render(request, 'show_detail_category.html', {'object': row})
#   def add_category(request):
#     if request.method =='POST':
#       form = CategoryForm(request.POST)
#       if form.is_valid():
#         form.save()
#         form = CategoryForm()
#     else:
#       form = CategoryForm()
#     return render(request, 'add_medicine.html', {'form': form})
#   def update_category(request, category_id):
#     if request.method == 'POST':
#       row = get_object_or_404(Category, category_id=category_id)
#       form = CategoryForm(request.POST, instance=row)
#       if form.is_valid():
#         form.save()
#       return redirect('../')
#     else:
#       row = get_object_or_404(Category, category_id=category_id)
#       form = CategoryForm(instance=row)
#     return render(request, 'update_medicine.html', {'form':form})
#   def delete_category(request, category_id):
#     row = get_object_or_404(Category, category_id=category_id)
#     if request.method == 'POST':
#       row.delete()
#       return redirect('../../')
#     return render(request, 'delete_medicine.html', {'object':row})
# class SupplierView:
#   def show_supplier(request):
#     return render(request, 'show_medicine.html', {'object_list':Supplier.objects.all()})
  