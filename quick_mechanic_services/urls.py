"""quick_mechanic_services URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from vehicle import views
from django.contrib.auth.views import LoginView,LogoutView
from django.views.generic import RedirectView
from django.conf.urls import url


urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.home_view,name=''),
    path('contact',views.contact, name='contact'),
    path('about/',views.aboutus),
    path('onspot-service/',views.onspot_service, name='onspot-service'),
    path('doorstep-service/',views.doorstep_service, name='doorstep-service'),
    path('pre-booking-service/',views.pre_booking_service, name='pre-booking-service'),

    path('adminclick', views.adminclick_view),
    path('customerclick', views.customerclick_view),
    path('garageclick', views.garageclick_view),

    path('customersignup', views.customer_signup_view,name='customersignup'),
    path('garagesignup', views.garage_signup_view,name='garagesignup'),

    path('customerlogin', LoginView.as_view(template_name='vehicle/customerlogin.html'),name='customerlogin'),
    path('garagelogin', LoginView.as_view(template_name='vehicle/garagelogin.html'),name='garagelogin'),
    path('adminlogin', LoginView.as_view(template_name='vehicle/adminlogin.html'),name='adminlogin'),



    path('admin-dashboard', views.admin_dashboard_view,name='admin-dashboard'),

    path('admin-customer', views.admin_customer_view,name='admin-customer'),
    path('admin-view-customer',views.admin_view_customer_view,name='admin-view-customer'),
    path('delete-customer/<int:pk>', views.delete_customer_view,name='delete-customer'),
    path('update-customer/<int:pk>', views.update_customer_view,name='update-customer'),
    path('admin-add-customer', views.admin_add_customer_view,name='admin-add-customer'),
    path('admin-view-customer-enquiry', views.admin_view_customer_enquiry_view,name='admin-view-customer-enquiry'),
    path('admin-view-customer-invoice', views.admin_view_customer_invoice_view,name='admin-view-customer-invoice'),


    path('admin-request', views.admin_request_view,name='admin-request'),
    path('admin-view-request',views.admin_view_request_view,name='admin-view-request'),
    path('change-status/<int:pk>', views.change_status_view,name='change-status'),
    path('admin-delete-request/<int:pk>', views.admin_delete_request_view,name='admin-delete-request'),
    path('admin-add-request',views.admin_add_request_view,name='admin-add-request'),
    path('admin-approve-request',views.admin_approve_request_view,name='admin-approve-request'),
    path('approve-request/<int:pk>', views.approve_request_view,name='approve-request'),
    
    path('admin-view-service-cost',views.admin_view_service_cost_view,name='admin-view-service-cost'),
    path('update-cost/<int:pk>', views.update_cost_view,name='update-cost'),

    path('admin-garage', views.admin_garage_view,name='admin-garage'),
    path('admin-view-garage',views.admin_view_garage_view,name='admin-view-garage'),
    path('delete-garage/<int:pk>', views.delete_garage_view,name='delete-garage'),
    path('update-garage/<int:pk>', views.update_garage_view,name='update-garage'),
    path('admin-add-garage',views.admin_add_garage_view,name='admin-add-garage'),
    path('admin-approve-garage',views.admin_approve_garage_view,name='admin-approve-garage'),
    path('approve-garage/<int:pk>', views.approve_garage_view,name='approve-garage'),
    path('delete-garage/<int:pk>', views.delete_garage_view,name='delete-garage'),
    path('admin-view-garage-salary',views.admin_view_garage_salary_view,name='admin-view-garage-salary'),
    path('update-salary/<int:pk>', views.update_salary_view,name='update-salary'),

    
    path('admin-feedback', views.admin_feedback_view,name='admin-feedback'),

    path('admin-report', views.admin_report_view,name='admin-report'),

    path('garage-dashboard', views.garage_dashboard_view,name='garage-dashboard'),
    path('garage-work-assigned', views.garage_work_assigned_view,name='garage-work-assigned'),
    path('garage-update-status/<int:pk>', views.garage_update_status_view,name='garage-update-status'),
    path('garage-feedback', views.garage_feedback_view,name='garage-feedback'),
    path('garage-salary', views.garage_salary_view,name='garage-salary'),
    path('garage-profile', views.garage_profile_view,name='garage-profile'),
    path('edit-garage-profile', views.edit_garage_profile_view,name='edit-garage-profile'),

    


    path('customer-dashboard', views.customer_dashboard_view,name='customer-dashboard'),
    path('customer-request', views.customer_request_view,name='customer-request'),
    path('customer-add-request',views.customer_add_request_view,name='customer-add-request'),

    path('customer-profile', views.customer_profile_view,name='customer-profile'),
    path('edit-customer-profile', views.edit_customer_profile_view,name='edit-customer-profile'),
    path('customer-feedback', views.customer_feedback_view,name='customer-feedback'),
    path('customer-invoice', views.customer_invoice_view,name='customer-invoice'),
    path('customer-view-request',views.customer_view_request_view,name='customer-view-request'),
    path('customer-delete-request/<int:pk>', views.customer_delete_request_view,name='customer-delete-request'),
    path('customer-view-approved-request',views.customer_view_approved_request_view,name='customer-view-approved-request'),
    path('customer-view-approved-request-invoice',views.customer_view_approved_request_invoice_view,name='customer-view-approved-request-invoice'),

    path('afterlogin', views.afterlogin_view,name='afterlogin'),
    path('logout', LogoutView.as_view(template_name='vehicle/index.html'),name='logout'),
    url(r'^favicon\.ico$',RedirectView.as_view(url='/static/images/favicon.ico')),
]

    





   

