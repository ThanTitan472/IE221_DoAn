from django.urls import path
from .views import *
app_name = 'medicines'

urlpatterns = [
  path('',home_view,name='home'),
  path('home/',home_view,name='home'),
  path('profile/', UserView.view_profile, name='view_profile'),  # Xem thông tin cá nhân
  path('profile/edit/', UserView.edit_profile, name='edit_profile'),
  path('users/', UserView.user_list, name='user_list'),  # Hiển thị danh sách User
  path('users/<int:pk>/delete/', UserView.delete_user, name='delete_user'),
  path('register/', LoginView.register_view, name='register'),
  path('login/', LoginView.login_view, name='login'),
  path('logout/', LoginView.logout_view, name='logout'),
  path('medicine/', MedicineView.show_medicine, name='show-medicine'),
  path('medicine/add/', MedicineView.add_medicine, name='add-medicine'),
  path('medicine/<str:key_id>/update/', MedicineView.update_medicine, name='update-medicine'),
  path('medicine/<str:key_id>/delete/', MedicineView.delete_medicine, name='delete-medicine'),
  path('category/', CategoryView.show_medicine, name='show-category'),
  path('category/add/', CategoryView.add_medicine, name='add-category'),
  path('category/<str:key_id>/update/', CategoryView.update_medicine, name='update-category'),
  path('category/<str:key_id>/delete/', CategoryView.delete_medicine, name='delete-category'),
  path('supplier/', SupplierView.show_medicine, name='show-supplier'),
  path('supplier/add/', SupplierView.add_medicine, name='add-supplier'),
  path('supplier/<str:key_id>/update/', SupplierView.update_medicine, name='update-supplier'),
  path('supplier/<str:key_id>/delete/', SupplierView.delete_medicine, name='delete-supplier'),
  path('customer/', CustomerView.show_medicine, name='show-customer'),
  path('customer/add/', CustomerView.add_medicine, name='add-customer'),
  path('customer/<str:key_id>/update/', CustomerView.update_medicine, name='update-customer'),
  path('customer/<str:key_id>/delete/', CustomerView.delete_medicine, name='delete-customer'),
  path('employee/', EmployeeView.show_medicine, name='show-employee'),
  path('employee/add/', EmployeeView.add_medicine, name='add-employee'),
  path('employee/<str:key_id>/update/', EmployeeView.update_medicine, name='update-employee'),
  path('employee/<str:key_id>/delete/', EmployeeView.delete_medicine, name='delete-employee'),
  path('sale/', SaleView.show_medicine, name='show-sale'),
  path('cart/',CartView.show_medicine,name='show-cart'),
  path('cart/<str:key_id>/add',CartView.add_medicine,name='add-cart'),
  path('cart/<int:id>/update',CartView.update_medicine,name='update-cart'),
  path('cart/<int:id>/delete',CartView.delete_medicine,name='delete-cart'),
  path('cart/pay_medicine',CartView.pay_medicine, name='pay-cart'),
  path('order/',OrderView.show_medicine,name='show-order'),
]