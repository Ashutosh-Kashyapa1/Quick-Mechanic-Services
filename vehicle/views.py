from django.shortcuts import render,redirect,reverse
from . import forms,models
from datetime import datetime
from vehicle.models import Contact
from django.db.models import Sum
from django.contrib.auth.models import Group
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required,user_passes_test
from django.conf import settings
from django.db.models import Q

#ABOUT US

def aboutus(request):
    return render(request, 'vehicle/about.html')

#SERVICES

def onspot_service(request):
    return render(request, 'vehicle/onspot_service.html')

def doorstep_service(request):
    return render(request, 'vehicle/doorstep_service.html')

def pre_booking_service(request):
    return render(request, 'vehicle/pre_booking_service.html')

#USER

def home_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request,'vehicle/index.html')

#ADMIN

def adminclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return HttpResponseRedirect('adminlogin')

#for checking user customer, Garage or admin
def is_customer(user):
    return user.groups.filter(name='CUSTOMER').exists()
def is_garage(user):
    return user.groups.filter(name='GARAGE').exists()

def afterlogin_view(request):
    if is_customer(request.user):
        return redirect('customer-dashboard')
    elif is_garage(request.user):
        accountapproval=models.Garage.objects.all().filter(user_id=request.user.id,status=True)
        if accountapproval:
            return redirect('garage-dashboard')
        else:
            return render(request,'vehicle/garage_wait_for_approval.html')
    else:
        return redirect('admin-dashboard')

@login_required(login_url='adminlogin')
def admin_dashboard_view(request):
    enquiry=models.Request.objects.all().order_by('-id')
    customers=[]
    for enq in enquiry:
        customer=models.Customer.objects.get(id=enq.customer_id)
        customers.append(customer)
    dict={
    'total_customer':models.Customer.objects.all().count(),
    'total_garage':models.Garage.objects.all().count(),
    'total_request':models.Request.objects.all().count(),
    'total_feedback':models.Feedback.objects.all().count(),
    'data':zip(customers,enquiry),
    }
    return render(request,'vehicle/admin_dashboard.html',context=dict)

@login_required(login_url='adminlogin')
def admin_customer_view(request):
    return render(request,'vehicle/admin_customer.html')

@login_required(login_url='adminlogin')
def admin_view_customer_view(request):
    customers=models.Customer.objects.all()
    return render(request,'vehicle/admin_view_customer.html',{'customers':customers})

@login_required(login_url='adminlogin')
def delete_customer_view(request,pk):
    customer=models.Customer.objects.get(id=pk)
    user=models.User.objects.get(id=customer.user_id)
    user.delete()
    customer.delete()
    return redirect('admin-view-customer')

@login_required(login_url='adminlogin')
def update_customer_view(request,pk):
    customer=models.Customer.objects.get(id=pk)
    user=models.User.objects.get(id=customer.user_id)
    userForm=forms.CustomerUserForm(instance=user)
    customerForm=forms.CustomerForm(request.FILES,instance=customer)
    mydict={'userForm':userForm,'customerForm':customerForm}
    if request.method=='POST':
        userForm=forms.CustomerUserForm(request.POST,instance=user)
        customerForm=forms.CustomerForm(request.POST,request.FILES,instance=customer)
        if userForm.is_valid() and customerForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            customerForm.save()
            return redirect('admin-view-customer')
    return render(request,'vehicle/update_customer.html',context=mydict)

@login_required(login_url='adminlogin')
def admin_add_customer_view(request):
    userForm=forms.CustomerUserForm()
    customerForm=forms.CustomerForm()
    mydict={'userForm':userForm,'customerForm':customerForm}
    if request.method=='POST':
        userForm=forms.CustomerUserForm(request.POST)
        customerForm=forms.CustomerForm(request.POST,request.FILES)
        if userForm.is_valid() and customerForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            customer=customerForm.save(commit=False)
            customer.user=user
            customer.save()
            my_customer_group = Group.objects.get_or_create(name='CUSTOMER')
            my_customer_group[0].user_set.add(user)
        return HttpResponseRedirect('/admin-view-customer')
    return render(request,'vehicle/admin_add_customer.html',context=mydict)

@login_required(login_url='adminlogin')
def admin_view_customer_enquiry_view(request):
    enquiry=models.Request.objects.all().order_by('-id')
    customers=[]
    for enq in enquiry:
        customer=models.Customer.objects.get(id=enq.customer_id)
        customers.append(customer)
    return render(request,'vehicle/admin_view_customer_enquiry.html',{'data':zip(customers,enquiry)})

@login_required(login_url='adminlogin')
def admin_view_customer_invoice_view(request):
    enquiry=models.Request.objects.values('customer_id').annotate(Sum('cost'))
    print(enquiry)
    customers=[]
    for enq in enquiry:
        print(enq)
        customer=models.Customer.objects.get(id=enq['customer_id'])
        customers.append(customer)
    return render(request,'vehicle/admin_view_customer_invoice.html',{'data':zip(customers,enquiry)})

@login_required(login_url='adminlogin')
def admin_garage_view(request):
    return render(request,'vehicle/admin_garage.html')

@login_required(login_url='adminlogin')
def admin_approve_garage_view(request):
    garages=models.Garage.objects.all().filter(status=False)
    return render(request,'vehicle/admin_approve_garage.html',{'garages':garages})

@login_required(login_url='adminlogin')
def approve_garage_view(request,pk):
    garageSalary=forms.GarageSalaryForm()
    if request.method=='POST':
        garageSalary=forms.GarageSalaryForm(request.POST)
        if garageSalary.is_valid():
            garage=models.Garage.objects.get(id=pk)
            garage.salary=garageSalary.cleaned_data['salary']
            garage.status=True
            garage.save()
        else:
            print("form is invalid")
        return HttpResponseRedirect('/admin-approve-garage')
    return render(request,'vehicle/admin_approve_garage_details.html',{'garageSalary':garageSalary})

@login_required(login_url='adminlogin')
def delete_garage_view(request,pk):
    garage=models.Garage.objects.get(id=pk)
    user=models.User.objects.get(id=garage.user_id)
    user.delete()
    garage.delete()
    return redirect('admin-approve-garage')

@login_required(login_url='adminlogin')
def admin_add_garage_view(request):
    userForm=forms.GarageUserForm()
    garageForm=forms.GarageForm()
    garageSalary=forms.GarageSalaryForm()
    mydict={'userForm':userForm,'garageForm':garageForm,'garageSalary':garageSalary}
    if request.method=='POST':
        userForm=forms.GarageUserForm(request.POST)
        garageForm=forms.GarageForm(request.POST,request.FILES)
        garageSalary=forms.GarageSalaryForm(request.POST)
        if userForm.is_valid() and garageForm.is_valid() and garageSalary.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            garage=garageForm.save(commit=False)
            garage.user=user
            garage.status=True
            garage.salary=garageSalary.cleaned_data['salary']
            garage.save()
            my_garage_group = Group.objects.get_or_create(name='GARAGE')
            my_garage_group[0].user_set.add(user)
            return HttpResponseRedirect('admin-view-garage')
        else:
            print('problem in form')
    return render(request,'vehicle/admin_add_garage.html',context=mydict)

@login_required(login_url='adminlogin')
def admin_view_garage_view(request):
    garages=models.Garage.objects.all()
    return render(request,'vehicle/admin_view_garage.html',{'garages':garages})

@login_required(login_url='adminlogin')
def delete_garage_view(request,pk):
    garage=models.Garage.objects.get(id=pk)
    user=models.User.objects.get(id=garage.user_id)
    user.delete()
    garage.delete()
    return redirect('admin-view-garage')


@login_required(login_url='adminlogin')
def update_garage_view(request,pk):
    garage=models.Garage.objects.get(id=pk)
    user=models.User.objects.get(id=garage.user_id)
    userForm=forms.GarageUserForm(instance=user)
    garageForm=forms.GarageForm(request.FILES,instance=garage)
    mydict={'userForm':userForm,'garageForm':garageForm}
    if request.method=='POST':
        userForm=forms.GarageUserForm(request.POST,instance=user)
        garageForm=forms.GarageForm(request.POST,request.FILES,instance=garage)
        if userForm.is_valid() and garageForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            garageForm.save()
            return redirect('admin-view-garage')
    return render(request,'vehicle/update_garage.html',context=mydict)

@login_required(login_url='adminlogin')
def admin_view_garage_salary_view(request):
    garages=models.Garage.objects.all()
    return render(request,'vehicle/admin_view_garage_salary.html',{'garages':garages})

@login_required(login_url='adminlogin')
def update_salary_view(request,pk):
    garageSalary=forms.GarageSalaryForm()
    if request.method=='POST':
        garageSalary=forms.GarageSalaryForm(request.POST)
        if garageSalary.is_valid():
            garage=models.Garage.objects.get(id=pk)
            garage.salary=garageSalary.cleaned_data['salary']
            garage.save()
        else:
            print("form is invalid")
        return HttpResponseRedirect('/admin-view-garage-salary')
    return render(request,'vehicle/admin_approve_garage_details.html',{'garageSalary':garageSalary})


@login_required(login_url='adminlogin')
def admin_request_view(request):
    return render(request,'vehicle/admin_request.html')

@login_required(login_url='adminlogin')
def admin_view_request_view(request):
    enquiry=models.Request.objects.all().order_by('-id')
    customers=[]
    for enq in enquiry:
        customer=models.Customer.objects.get(id=enq.customer_id)
        customers.append(customer)
    return render(request,'vehicle/admin_view_request.html',{'data':zip(customers,enquiry)})


@login_required(login_url='adminlogin')
def change_status_view(request,pk):
    adminenquiry=forms.AdminApproveRequestForm()
    if request.method=='POST':
        adminenquiry=forms.AdminApproveRequestForm(request.POST)
        if adminenquiry.is_valid():
            enquiry_x=models.Request.objects.get(id=pk)
            enquiry_x.garage=adminenquiry.cleaned_data['garage']
            enquiry_x.cost=adminenquiry.cleaned_data['cost']
            enquiry_x.status=adminenquiry.cleaned_data['status']
            enquiry_x.save()
        else:
            print("form is invalid")
        return HttpResponseRedirect('/admin-view-request')
    return render(request,'vehicle/admin_approve_request_details.html',{'adminenquiry':adminenquiry})

@login_required(login_url='adminlogin')
def admin_delete_request_view(request,pk):
    requests=models.Request.objects.get(id=pk)
    requests.delete()
    return redirect('admin-view-request')

@login_required(login_url='adminlogin')
def admin_add_request_view(request):
    enquiry=forms.RequestForm()
    adminenquiry=forms.AdminRequestForm()
    mydict={'enquiry':enquiry,'adminenquiry':adminenquiry}
    if request.method=='POST':
        enquiry=forms.RequestForm(request.POST)
        adminenquiry=forms.AdminRequestForm(request.POST)
        if enquiry.is_valid() and adminenquiry.is_valid():
            enquiry_x=enquiry.save(commit=False)
            enquiry_x.customer=adminenquiry.cleaned_data['customer']
            enquiry_x.garage=adminenquiry.cleaned_data['garage']
            enquiry_x.cost=adminenquiry.cleaned_data['cost']
            enquiry_x.status='Approved'
            enquiry_x.save()
        else:
            print("form is invalid")
        return HttpResponseRedirect('admin-view-request')
    return render(request,'vehicle/admin_add_request.html',context=mydict)

@login_required(login_url='adminlogin')
def admin_approve_request_view(request):
    enquiry=models.Request.objects.all().filter(status='Pending')
    return render(request,'vehicle/admin_approve_request.html',{'enquiry':enquiry})

@login_required(login_url='adminlogin')
def approve_request_view(request,pk):
    adminenquiry=forms.AdminApproveRequestForm()
    if request.method=='POST':
        adminenquiry=forms.AdminApproveRequestForm(request.POST)
        if adminenquiry.is_valid():
            enquiry_x=models.Request.objects.get(id=pk)
            enquiry_x.garage=adminenquiry.cleaned_data['garage']
            enquiry_x.cost=adminenquiry.cleaned_data['cost']
            enquiry_x.status=adminenquiry.cleaned_data['status']
            enquiry_x.save()
        else:
            print("form is invalid")
        return HttpResponseRedirect('/admin-approve-request')
    return render(request,'vehicle/admin_approve_request_details.html',{'adminenquiry':adminenquiry})

@login_required(login_url='adminlogin')
def admin_view_service_cost_view(request):
    enquiry=models.Request.objects.all().order_by('-id')
    customers=[]
    for enq in enquiry:
        customer=models.Customer.objects.get(id=enq.customer_id)
        customers.append(customer)
    print(customers)
    return render(request,'vehicle/admin_view_service_cost.html',{'data':zip(customers,enquiry)})

@login_required(login_url='adminlogin')
def update_cost_view(request,pk):
    updateCostForm=forms.UpdateCostForm()
    if request.method=='POST':
        updateCostForm=forms.UpdateCostForm(request.POST)
        if updateCostForm.is_valid():
            enquiry_x=models.Request.objects.get(id=pk)
            enquiry_x.cost=updateCostForm.cleaned_data['cost']
            enquiry_x.save()
        else:
            print("form is invalid")
        return HttpResponseRedirect('/admin-view-service-cost')
    return render(request,'vehicle/update_cost.html',{'updateCostForm':updateCostForm})

@login_required(login_url='adminlogin')
def admin_mechanic_attendance_view(request):
    return render(request,'vehicle/admin_mechanic_attendance.html')

@login_required(login_url='adminlogin')
def admin_report_view(request):
    reports=models.Request.objects.all().filter(Q(status="Repairing Done") | Q(status="Released"))
    dict={
        'reports':reports,
    }
    return render(request,'vehicle/admin_report.html',context=dict)

@login_required(login_url='adminlogin')
def admin_feedback_view(request):
    feedback=models.Feedback.objects.all().order_by('-id')
    return render(request,'vehicle/admin_feedback.html',{'feedback':feedback})

#CUSTOMER

def customerclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request,'vehicle/customerclick.html')

def customer_signup_view(request):
    userForm=forms.CustomerUserForm()
    customerForm=forms.CustomerForm()
    mydict={'userForm':userForm,'customerForm':customerForm}
    if request.method=='POST':
        userForm=forms.CustomerUserForm(request.POST)
        customerForm=forms.CustomerForm(request.POST,request.FILES)
        if userForm.is_valid() and customerForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            customer=customerForm.save(commit=False)
            customer.user=user
            customer.save()
            my_customer_group = Group.objects.get_or_create(name='CUSTOMER')
            my_customer_group[0].user_set.add(user)
        return HttpResponseRedirect('customerlogin')
    return render(request,'vehicle/customersignup.html',context=mydict)

@login_required(login_url='customerlogin')
@user_passes_test(is_customer)
def customer_dashboard_view(request):
    customer=models.Customer.objects.get(user_id=request.user.id)
    work_in_progress=models.Request.objects.all().filter(customer_id=customer.id,status='Repairing').count()
    work_completed=models.Request.objects.all().filter(customer_id=customer.id).filter(Q(status="Repairing Done") | Q(status="Released")).count()
    new_request_made=models.Request.objects.all().filter(customer_id=customer.id).filter(Q(status="Pending") | Q(status="Approved")).count()
    bill=models.Request.objects.all().filter(customer_id=customer.id).filter(Q(status="Repairing Done") | Q(status="Released")).aggregate(Sum('cost'))
    print(bill)
    dict={
    'work_in_progress':work_in_progress,
    'work_completed':work_completed,
    'new_request_made':new_request_made,
    'bill':bill['cost__sum'],
    'customer':customer,
    }
    return render(request,'vehicle/customer_dashboard.html',context=dict)

@login_required(login_url='customerlogin')
@user_passes_test(is_customer)
def customer_request_view(request):
    customer=models.Customer.objects.get(user_id=request.user.id)
    return render(request,'vehicle/customer_request.html',{'customer':customer})

@login_required(login_url='customerlogin')
@user_passes_test(is_customer)
def customer_view_request_view(request):
    customer=models.Customer.objects.get(user_id=request.user.id)
    enquiries=models.Request.objects.all().filter(customer_id=customer.id , status="Pending")
    return render(request,'vehicle/customer_view_request.html',{'customer':customer,'enquiries':enquiries})

@login_required(login_url='customerlogin')
@user_passes_test(is_customer)
def customer_delete_request_view(request,pk):
    customer=models.Customer.objects.get(user_id=request.user.id)
    enquiry=models.Request.objects.get(id=pk)
    enquiry.delete()
    return redirect('customer-view-request')

@login_required(login_url='customerlogin')
@user_passes_test(is_customer)
def customer_view_approved_request_view(request):
    customer=models.Customer.objects.get(user_id=request.user.id)
    enquiries=models.Request.objects.all().filter(customer_id=customer.id).exclude(status='Pending')
    return render(request,'vehicle/customer_view_approved_request.html',{'customer':customer,'enquiries':enquiries})

@login_required(login_url='customerlogin')
@user_passes_test(is_customer)
def customer_view_approved_request_invoice_view(request):
    customer=models.Customer.objects.get(user_id=request.user.id)
    enquiries=models.Request.objects.all().filter(customer_id=customer.id).exclude(status='Pending')
    return render(request,'vehicle/customer_view_approved_request_invoice.html',{'customer':customer,'enquiries':enquiries})

@login_required(login_url='customerlogin')
@user_passes_test(is_customer)
def customer_add_request_view(request):
    customer=models.Customer.objects.get(user_id=request.user.id)
    enquiry=forms.RequestForm()
    if request.method=='POST':
        enquiry=forms.RequestForm(request.POST)
        if enquiry.is_valid():
            customer=models.Customer.objects.get(user_id=request.user.id)
            enquiry_x=enquiry.save(commit=False)
            enquiry_x.customer=customer
            enquiry_x.save()
        else:
            print("form is invalid")
        return HttpResponseRedirect('customer-dashboard')
    return render(request,'vehicle/customer_add_request.html',{'enquiry':enquiry,'customer':customer})


@login_required(login_url='customerlogin')
@user_passes_test(is_customer)
def customer_profile_view(request):
    customer=models.Customer.objects.get(user_id=request.user.id)
    return render(request,'vehicle/customer_profile.html',{'customer':customer})


@login_required(login_url='customerlogin')
@user_passes_test(is_customer)
def edit_customer_profile_view(request):
    customer=models.Customer.objects.get(user_id=request.user.id)
    user=models.User.objects.get(id=customer.user_id)
    userForm=forms.CustomerUserForm(instance=user)
    customerForm=forms.CustomerForm(request.FILES,instance=customer)
    mydict={'userForm':userForm,'customerForm':customerForm,'customer':customer}
    if request.method=='POST':
        userForm=forms.CustomerUserForm(request.POST,instance=user)
        customerForm=forms.CustomerForm(request.POST,instance=customer)
        if userForm.is_valid() and customerForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            customerForm.save()
            return HttpResponseRedirect('customer-profile')
    return render(request,'vehicle/edit_customer_profile.html',context=mydict)


@login_required(login_url='customerlogin')
@user_passes_test(is_customer)
def customer_invoice_view(request):
    customer=models.Customer.objects.get(user_id=request.user.id)
    enquiries=models.Request.objects.all().filter(customer_id=customer.id).exclude(status='Pending')
    return render(request,'vehicle/customer_invoice.html',{'customer':customer,'enquiries':enquiries})


@login_required(login_url='customerlogin')
@user_passes_test(is_customer)
def customer_feedback_view(request):
    customer=models.Customer.objects.get(user_id=request.user.id)
    feedback=forms.FeedbackForm()
    if request.method=='POST':
        feedback=forms.FeedbackForm(request.POST)
        if feedback.is_valid():
            feedback.save()
        else:
            print("form is invalid")
        return render(request,'vehicle/feedback_sent_by_customer.html',{'customer':customer})
    return render(request,'vehicle/customer_feedback.html',{'feedback':feedback,'customer':customer})

#GARAGE

def garageclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request,'vehicle/garageclick.html')

def garage_signup_view(request):
    userForm=forms.GarageUserForm()
    garageForm=forms.GarageForm()
    mydict={'userForm':userForm,'garageForm':garageForm}
    if request.method=='POST':
        userForm=forms.GarageUserForm(request.POST)
        garageForm=forms.GarageForm(request.POST,request.FILES)
        if userForm.is_valid() and garageForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            garage=garageForm.save(commit=False)
            garage.user=user
            garage.save()
            my_garage_group = Group.objects.get_or_create(name='GARAGE')
            my_garage_group[0].user_set.add(user)
        return HttpResponseRedirect('garagelogin')
    return render(request,'vehicle/garagesignup.html',context=mydict)


@login_required(login_url='garagelogin')
@user_passes_test(is_garage)
def garage_dashboard_view(request):
    garage=models.Garage.objects.get(user_id=request.user.id)
    work_in_progress=models.Request.objects.all().filter(mechanic_id=garage.id,status='Repairing').count()
    work_completed=models.Request.objects.all().filter(mechanic_id=garage.id,status='Repairing Done').count()
    new_work_assigned=models.Request.objects.all().filter(mechanic_id=garage.id,status='Approved').count()
    dict={
    'work_in_progress':work_in_progress,
    'work_completed':work_completed,
    'new_work_assigned':new_work_assigned,
    'salary':garage.salary,
    'garage':garage,
    }
    return render(request,'vehicle/garage_dashboard.html',context=dict)

@login_required(login_url='garagelogin')
@user_passes_test(is_garage)
def garage_work_assigned_view(request):
    garage=models.Garage.objects.get(user_id=request.user.id)
    works=models.Request.objects.all().filter(garage_id=garage.id)
    return render(request,'vehicle/garage_work_assigned.html',{'works':works,'garage':garage})


@login_required(login_url='garagelogin')
@user_passes_test(is_garage)
def garage_update_status_view(request,pk):
    garage=models.Garage.objects.get(user_id=request.user.id)
    updateStatus=forms.GarageUpdateStatusForm()
    if request.method=='POST':
        updateStatus=forms.GarageUpdateStatusForm(request.POST)
        if updateStatus.is_valid():
            enquiry_x=models.Request.objects.get(id=pk)
            enquiry_x.status=updateStatus.cleaned_data['status']
            enquiry_x.save()
        else:
            print("form is invalid")
        return HttpResponseRedirect('/garage-work-assigned')
    return render(request,'vehicle/garage_update_status.html',{'updateStatus':updateStatus,'garage':garage})



@login_required(login_url='garagelogin')
@user_passes_test(is_garage)
def garage_feedback_view(request):
    garage=models.Garage.objects.get(user_id=request.user.id)
    feedback=forms.FeedbackForm()
    if request.method=='POST':
        feedback=forms.FeedbackForm(request.POST)
        if feedback.is_valid():
            feedback.save()
        else:
            print("form is invalid")
        return render(request,'vehicle/feedback_sent.html',{'garage':garage})
    return render(request,'vehicle/garage_feedback.html',{'feedback':feedback,'garage':garage})

@login_required(login_url='garagelogin')
@user_passes_test(is_garage)
def garage_salary_view(request):
    garage=models.Garage.objects.get(user_id=request.user.id)
    workdone=models.Request.objects.all().filter(garage_id=garage.id).filter(Q(status="Repairing Done") | Q(status="Released"))
    return render(request,'vehicle/garage_salary.html',{'workdone':workdone,'garage':garage})

@login_required(login_url='garagelogin')
@user_passes_test(is_garage)
def garage_profile_view(request):
    garage=models.Garage.objects.get(user_id=request.user.id)
    return render(request,'vehicle/garage_profile.html',{'garage':garage})

@login_required(login_url='garagelogin')
@user_passes_test(is_garage)
def edit_garage_profile_view(request):
    garage=models.garage.objects.get(user_id=request.user.id)
    user=models.User.objects.get(id=garage.user_id)
    userForm=forms.GarageUserForm(instance=user)
    garageForm=forms.GarageForm(request.FILES,instance=garage)
    mydict={'userForm':userForm,'garageForm':garageForm,'garage':garage}
    if request.method=='POST':
        userForm=forms.GarageUserForm(request.POST,instance=user)
        garageForm=forms.GarageForm(request.POST,request.FILES,instance=garage)
        if userForm.is_valid() and garageForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            garageForm.save()
            return redirect('garage-profile')
    return render(request,'vehicle/edit_garage_profile.html',context=mydict)

#CONTACT US
def contact(request):
    if request.method == "POST":
        name=request.POST.get('name')
        email=request.POST.get('email')
        phone=request.POST.get('phone')
        desc=request.POST.get('desc')
        contact= Contact(name=name, email=email, phone=phone, desc=desc, date=datetime.today())
        contact.save()
    return render(request, 'vehicle/contact.html')






