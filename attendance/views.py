from django.shortcuts import render
from django.http import  HttpResponseRedirect
from .forms import LoginForm , RegisterForm,LeaveRequestForm
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User
from django.shortcuts import redirect
from .models import leave
from .models import staff
from .models import rec ,dept
from .models import leave_request as lrequest
from django.urls import reverse
from django.views.generic.edit import UpdateView
from django.contrib.auth.decorators import user_passes_test
from django.db import connections
from django import forms
import datetime







#view for a user dashboard
# url = 127.0.0.1:8000/dashboard

def dashboard(request):

    current_user=request.user
    current_staff=staff.objects.get(user=current_user)

    casual_leaves_taken_object = leave.objects.get(emp_id=current_staff)
    casual_leaves_taken=casual_leaves_taken_object.casual_leave
    max_casual_leaves = current_staff.category.max_casual_leave
    casual_leaves_remaining = max_casual_leaves-casual_leaves_taken

    department_hods = dept.objects.all()

    if department_hods.filter(emp=current_staff).exists():
        hod={ 'hod' : current_staff, 'principal':None,'name':current_staff.name,'rem_leave':casual_leaves_remaining}
    else:
        hod={ 'hod' : None, 'principal':None,'name':current_staff.name,'rem_leave':casual_leaves_remaining}



    return render(request,'attendance/user_dashboard.html',hod)




#view for the admin dashboard
# url = 127.0.0.1:8000/admin_user

def admin_dashboard(request):
        if request.user.is_superuser:
            staffs=staff.objects.all().order_by('staff_id')
            query=request.GET.get("q")
            if query:
                staffs=staffs.filter(staff_id__icontains=query)
            paginator=Paginator(staffs,15)
            
            page=request.GET.get('page')
            staff_list=paginator.get_page(page)
            return render(request,'attendance/admin_dashboard.html',{'staffs':staff_list})
        else:
            return redirect('attendance:login')



#login for a user
# url = 127.0.0.1:8000/login

def login_user(request):
    form=LoginForm(request.POST or None)
    if request.POST and form.is_valid():
        user=form.login(request)
        if user:
            login(request,user)
            if not user.is_superuser:
                return redirect('attendance:dash_board')
            else:
                return redirect('attendance:admin_user')
    
    return render(request,'attendance/login.html',{'form':form})




#logout

def logout_user(request):
    logout(request)
    return HttpResponseRedirect(reverse('attendance:login'))




#register a user ( a facility for a superuser (admin))
# url = 127.0.0.1:8000/admin_user/register/

def  register(request):
    if request.user.is_superuser:
        if request.method=='POST':
            form=RegisterForm(request.POST)
            if form.is_valid():
                staff=form.save(commit=False)
                id = form.cleaned_data['staff_id']
                user = User.objects.create_user(username=str(form.cleaned_data['staff_id'])
                                                     , password='user'+str(form.cleaned_data['staff_id']))

                staff.user=user
                staff.save()

                leave_rec=leave(emp_id=staff)
                leave_rec.save()




                return redirect('attendance:admin_user')

        else:
            form=RegisterForm()
        return render(request,'attendance/register.html',{'form':form})
    else:
        return redirect('attendance:login')









#performs the delete operation (functionality ) and redirects back to  staffs list

@user_passes_test(lambda u : u.is_superuser)
def delete(request,id):
    userfield=User.objects.get(username=id)
    userfield.delete()
    return HttpResponseRedirect(reverse('attendance:admin_user'))






#updating a user (functionality)

class Update_view(UpdateView):
    model = staff
    fields = ['staff_id','name','category','department','qualification'
                ,'joining_date','termination_date']
  

    template_name_suffix = '_update_form'

    def get_success_url(self):
        return reverse('attendance:admin_user')




#method to list out the leaves taken by the current user
#  url = 127.0.0.1:8000/dashboard/leave

def leaves(request):

    recs=rec.objects.filter(status=0  , emp_id=staff.objects.get(staff_id=request.user.username))
    return render(request,'attendance/leaves_table_list.html',{'recs':recs})



#method which displays a form for submitting leave request
#  url = 127.0.0.1:8000/dashboard/leave/id/<leave_id>/

def leave_request(request,pk):
    current_user=request.user
    current_staff=staff.objects.get(user=current_user)

    requested_leave = rec.objects.get(id=pk)

    if request.method=='POST':
        form=LeaveRequestForm(request.POST)
        if form.is_valid():

            leave_req=form.save(commit=False)

            leave_req.is_accepted_by_hod=leave_req.is_accepted_by_princi=False
            if (dept.objects.filter(emp=current_staff).exists()):
                leave_req.is_accepted_by_hod=True

            leave_req.emp=requested_leave.emp_id
            leave_req.date=requested_leave.date
            leave_req.department=requested_leave.emp_id.department



            leave_req.save()


            return redirect('attendance:leaves')
    else:

        form=LeaveRequestForm(initial={'date':requested_leave.date})
    return render(request,'attendance/leave_request.html',{'form':form})



# shows all the leave requests which needs to be approved by the HOD
def available_leave_request(request):



    current_user=request.user
    current_staff=staff.objects.get(user=current_user)

    department_hods = dept.objects.all()



    if department_hods.filter(emp=current_staff).exists():



        empobject=dept.objects.get(emp=current_staff)

        if empobject.designation=='H':

            leaverequests=lrequest.objects.filter(is_accepted_by_hod=False,department=current_staff.department).exclude(emp=current_staff)

            return render(request, 'attendance/leave_requests_list.html',{'requests':leaverequests})
        elif empobject.designation=='P':
            leaverequests=lrequest.objects.filter(is_accepted_by_princi=False)
            return render(request, 'attendance/leave_requests_list.html',{'requests':leaverequests})

    else:
        return redirect('attendance:dash_board')




#helper method for incrementing the leave of the person from the leave type
def increment_leave_count(staff_leave_record , leave_id):

    if leave_id==1:
        staff_leave_record.casual_leave+=1
    elif leave_id==2:
        staff_leave_record.compensation_leave+=1
    elif leave_id==3:
        staff_leave_record.earned_leave+=1
    elif leave_id==4:
        staff_leave_record.half_pay_leave+=1
    elif leave_id==5:
        staff_leave_record. leave_allowance+=1
    elif leave_id==6:
        staff_leave_record.duty_leave +=1
    staff_leave_record.save()




#method whhich approves the leave request does the functionality
def approve_leave_requests(request,pk):
    current_user=request.user
    current_staff=staff.objects.get(user=current_user)
    hod_or_principal=dept.objects.get(emp=current_staff)


    current_request=lrequest.objects.get(pk=pk)
    if(hod_or_principal.designation=='H'):
        current_request.is_accepted_by_hod=True
    elif (hod_or_principal.designation=='P'):
        current_request.is_accepted_by_princi = True
    current_request.save()

    if(current_request.is_accepted_by_hod==True and current_request.is_accepted_by_princi==True):

        leave_id=current_request.type

        staff_leave_record=leave.objects.get(emp_id=current_request.emp)
        increment_leave_count(staff_leave_record,leave_id)


    return HttpResponseRedirect(reverse('attendance:pendingleaverequests'))




#view for showing the detailed attendance

def detailed_attendance(request ,year=2018 ,month=6):
    current_user_id=request.user.username
    cursor=connections['attlog'].cursor()
    prev_year,prev_month=fun_prev(year,month)
    nxt_year,nxt_month=fun_next(year,month)
    

    offset=datetime.datetime(year,month,1).weekday()
    
    
    cursor.execute("SELECT * FROM attlog WHERE eid = %s AND attdate >= '%s-%s-01' AND attdate  < '%s-%s-01'",[current_user_id,year,month,nxt_year,nxt_month] )
    
    loglist=dictfetchall(cursor)
    

    return render(request,'attendance/detailed_attendance.html',{'records':loglist,
    'current_year':year,
    'current_month':month,
    'nxt_year':nxt_year,
    'nxt_month':nxt_month,
    'prev_year':prev_year,
    'prev_month':prev_month ,
    'offset':range(offset+1) })


#@user_passes_test(lambda u : u.is_superuser)
class UpdateLeave(UpdateView):
    model = leave
    fields = ['present_days','casual_leave' , 'compensation_leave' ,'earned_leave'
    ,'half_pay_leave','leave_allowance' ,'duty_leave',
    ]
  

    template_name_suffix = '_update_form'

    def get_success_url(self):
        return reverse('attendance:admin_user')







################################################### UTILITY FUNCTIONS ##########################



 # Returning the queryset for iteration in html page
def dictfetchall(cursor):
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]



# Function for returning the next month and year
def fun_next(year,month):

    if month==12:
        nxt_month=1
        nxt_year=year+1
    else:
        nxt_month=month+1
        nxt_year=year
    
    return nxt_year,nxt_month

# Function for returning the previous month and year
def fun_prev(year,month):
    if month==1:
        prev_month=12
        prev_year=year-1
    
    else:
        prev_month=month-1
        prev_year=year
    return prev_year,prev_month



