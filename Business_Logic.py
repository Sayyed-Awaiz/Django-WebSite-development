from django.shortcuts import render, redirect, get_object_or_404
from dappx.forms import UserForm, UserUpdateForm,StaffForm,ProfileForm,ProfileUpdateForm,StaffUpdateForm,AppointmentForm,DmitvalForm,DmitvalUpdateForm
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.db.models import Q
from django.conf import settings
from dappx.models import Profile, DMIT, Appointment,DMITVAL
from django.core.mail import send_mail
import matplotlib.pyplot as plt
from django_xhtml2pdf.utils import generate_pdf


# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.forms.utils import ErrorList
from django.http import HttpResponse
from .forms import LoginForm, SignUpForm

def login_view(request):
    form = LoginForm(request.POST or None)

    msg = None

    if request.method == "POST":

        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("/")
            else:    
                msg = 'Invalid credentials'    
        else:
            msg = 'Error validating the form'    

    return render(request, "dappx/login.html", {"form": form, "msg" : msg})

def register_user(request):

    msg     = None
    success = False

    if request.method == "POST":
        form = SignUpForm(request.POST)
        profile_form = ProfileForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()
            profile = profile_form.save(commit=False)
            username = form.cleaned_data.get("username")
            raw_password = form.cleaned_data.get("password1")
            confirm_password = form.cleaned_data.get("password2")
            email = form.cleaned_data.get("email")
            user = authenticate(username=username, password=raw_password)
            user.profile.full_name=profile_form.cleaned_data.get('full_name')
            user.profile.father_or_husband_name=profile_form.cleaned_data.get('father_or_husband_name')
            user.profile.dob=profile_form.cleaned_data.get('dob')
            user.profile.mobile_no=profile_form.cleaned_data.get('mobile_no')
            user.profile.city=profile_form.cleaned_data.get('city')
            user.profile.state=profile_form.cleaned_data.get('state')
            user.profile.country=profile_form.cleaned_data.get('country')

            user.save()
            registered=True            

            msg     = 'User created - please login.'
            success = True
            
            #return redirect("/login/")

        else:
            msg = 'Form is not valid'    
    else:
        form = SignUpForm()
        profile_form = ProfileForm()

    return render(request, "dappx/registration.html", {"form": form, "p_form" : profile_form, "msg" : msg, "success" : success })


def index(request):
    totalDMITprofiles = len(Profile.objects.all()) - 1
    totalDMITcompleted = len(DMITVAL.objects.all())
    totalDMITpending = totalDMITprofiles - totalDMITcompleted
    totalAppointments = len(Appointment.objects.all())
    context = {"totalDMITprofiles":totalDMITprofiles, "totalDMITcompleted":totalDMITcompleted, "totalDMITpending":totalDMITpending, "totalAppointments":totalAppointments}
    return render(request,'dappx/index.html', context)

@login_required
def user_logout(request):
    logout(request)
    messages.success(request, 'You\'ve logged out successfully')
    return HttpResponseRedirect(reverse('index'))

@login_required
def edit_profile(request):       
    if request.method == 'POST':
        p_form=ProfileUpdateForm(request.POST,
                            request.FILES,
                            instance=request.user.profile)
        if p_form.is_valid():
            profile = p_form.save(commit=False)
            p_form.save()
            messages.success(request, 'Your Profile has been updated successfully')
            return redirect('edit_profile')
    else:        
        p_form=ProfileUpdateForm(instance=request.user.profile)
        context={
            'p_form':p_form,
            }
        
    return render(request,'dappx/edit_profile.html',context)

@login_required
def staff(request, pk=None):
    if request.user.is_staff or request.user.is_superuser:
        dmit_exists=False
        if pk:
            all_users_profile = Profile.objects.get(pk=pk)
            all_users=User.objects.get(pk=pk)
            staff_form = ''
            staff_form = StaffForm(request.POST, request.FILES)
            y=""
            y=User.objects.get(pk=pk)
    
            if request.method == 'POST':
                # messages.success(request, 'Dmit images saved Successfully')    
                if staff_form.is_valid():            
                    dmit= staff_form.save(commit=False)
                    dmit.user_id = all_users_profile.user_id
                    dmit.l1l = staff_form.cleaned_data.get('l1l')
                    dmit.l1c = staff_form.cleaned_data.get('l1c')
                    dmit.l1r = staff_form.cleaned_data.get('l1r')
                   
                    dmit.l2l = staff_form.cleaned_data.get('l2l')
                    dmit.l2c = staff_form.cleaned_data.get('l2c')
                    dmit.l2r = staff_form.cleaned_data.get('l2r')
                   
                    dmit.l3l = staff_form.cleaned_data.get('l3l')
                    dmit.l3c = staff_form.cleaned_data.get('l3c')
                    dmit.l3r = staff_form.cleaned_data.get('l3r')
                    
                    dmit.l4l = staff_form.cleaned_data.get('l4l')
                    dmit.l4c = staff_form.cleaned_data.get('l4c')
                    dmit.l4r = staff_form.cleaned_data.get('l4r')
                   
                    dmit.l5l = staff_form.cleaned_data.get('l5l')
                    dmit.l5c = staff_form.cleaned_data.get('l5c')
                    dmit.l5r = staff_form.cleaned_data.get('l5r')
                    
                    dmit.r1l = staff_form.cleaned_data.get('r1l')
                    dmit.r1c = staff_form.cleaned_data.get('r1c')
                    dmit.r1r = staff_form.cleaned_data.get('r1r')
                   
                    dmit.r2l = staff_form.cleaned_data.get('r2l')
                    dmit.r2c = staff_form.cleaned_data.get('r2c')
                    dmit.r2r = staff_form.cleaned_data.get('r2r')
                    
                    dmit.r3l = staff_form.cleaned_data.get('r3l')
                    dmit.r3c = staff_form.cleaned_data.get('r3c')
                    dmit.r3r = staff_form.cleaned_data.get('r3r')
                    
                    dmit.r4l = staff_form.cleaned_data.get('r4l')
                    dmit.r4c = staff_form.cleaned_data.get('r4c')
                    dmit.r4r = staff_form.cleaned_data.get('r4r')
                   
                    dmit.r5l = staff_form.cleaned_data.get('r5l')
                    dmit.r5c = staff_form.cleaned_data.get('r5c')
                    dmit.r5r = staff_form.cleaned_data.get('r5r')

                    dmit.confirm = staff_form.cleaned_data.get('confirm')

                    confirm = request.POST['confirm']
                    if confirm == 'confirm':
                        dmit_exists=True
                        messages.success(request, 'Dmit images saved Successfully now click on input value to fill the pattern and RC')
                        staff_form.save()
                        # return HttpResponseRedirect('/dappx/dmitval.html')
                        all_users=[]
                        all_users_profile=[]
                        all_users_appointment=[]   
                        context={} 
                        all_users= User.objects.all()
                        all_users_profile=Profile.objects.all()
                        
                        all_users_appointment=Appointment.objects.all()
                        context= {'all_users': all_users,'all_users_profile': all_users_profile,'all_users_appointment':all_users_appointment}
                        # args={'value_form':DmitvalForm}
                        return render(request,'dappx/users.html', context)
        else:
            staff_form = StaffForm(data=request.POST or None)
            all_users = request.user
            all_users_profile=request.user.profile
            
    else:
        messages.success(request,"You don't have access to it!")
        return render(request,'dappx/login.html')
    args = {'all_users': all_users,'all_users_profile':all_users_profile, 'staff_form':staff_form }
  

    return render(request,'dappx/staff.html',args)




@login_required
def value(request, pk=None):
    if request.user.is_staff or request.user.is_superuser:
        dmit_exists=False
       
        if pk:
            all_users_profile = Profile.objects.get(pk=pk)
            all_users=User.objects.get(pk=pk)
            value_form = ''
            value_form = DmitvalForm(request.POST)
            y=""
            y=User.objects.get(pk=pk)
    
            if request.method == 'POST':

                    
                if value_form.is_valid():
            
                    dmit= value_form.save(commit=False)
                    dmit.user_id = all_users_profile.user_id
                    dmit.l1 = value_form.cleaned_data.get('l1')
                    dmit.lrc1 = value_form.cleaned_data.get('lrc1')
                    

                    
                    dmit.l2 = value_form.cleaned_data.get('l2')
                    dmit.lrc2 = value_form.cleaned_data.get('lrc2')


                    dmit.l3 = value_form.cleaned_data.get('l3')
                    dmit.lrc3 = value_form.cleaned_data.get('lrc3')

                   

                    dmit.l4 = value_form.cleaned_data.get('l4')
                    dmit.lrc4 = value_form.cleaned_data.get('lrc4')
                    

                    

                    dmit.l5 = value_form.cleaned_data.get('l5')
                    dmit.lrc5 = value_form.cleaned_data.get('lrc5')

                   

                    dmit.r1 = value_form.cleaned_data.get('r1')
                    dmit.rrc1 = value_form.cleaned_data.get('rrc1')


                    dmit.r2 = value_form.cleaned_data.get('r2')
                    dmit.rrc2 = value_form.cleaned_data.get('rrc2')

                    

                    dmit.r3 = value_form.cleaned_data.get('r3')
                    dmit.rrc3 = value_form.cleaned_data.get('rrc3')


                    dmit.r4 = value_form.cleaned_data.get('r4')
                    dmit.rrc4 = value_form.cleaned_data.get('rrc4')

                   

                    dmit.r5 = value_form.cleaned_data.get('r5')
                    dmit.rrc5 = value_form.cleaned_data.get('rrc5')

                    dmit.latd = value_form.cleaned_data.get('latd')
                    dmit.ratd = value_form.cleaned_data.get('ratd')
                    dmit_exists=True
                    value_form.save()
                    messages.success(request, 'Dmit data saved reports have generated successfully ')

                    return HttpResponseRedirect('/dappx/staff')
           
        else:
            value_form = DmitvalForm(data=request.POST or None)
            all_users = request.user
            all_users_profile=request.user.profile
            
    else:
        messages.success(request,"You don't have access to it!")
        return render(request,'dappx/login.html')
    args = {'all_users': all_users,'all_users_profile':all_users_profile,'value_form':value_form, }
  

    return render(request,'dappx/dmitval.html',args)












        
@login_required
def users(request):
    all_users=[]
    all_users_profile=[]
    all_users_appointment=[]
    context={}
    if request.user.is_staff or request.user.is_superuser:
        all_users= User.objects.all()
        all_users_profile=Profile.objects.all()
        
        all_users_appointment=Appointment.objects.all()
        
        
        context= {'all_users': all_users,'all_users_profile': all_users_profile,'all_users_appointment':all_users_appointment }
    else:
        messages.success(request,"You don't have the access to do this!")
        return render(request,'dappx/login.html')    
    return render(request, 'dappx/users.html', context)
        
@login_required        
def search(request):
    if request.method=='POST':
        srch=request.POST['srh']

        if srch:
            match=User.objects.filter(Q(username__icontains=srch)|
                                         Q(email__icontains=srch)
                                         )

            if match:
                return render(request,'dappx/search.html', {'sr':match})
            else:
                messages.error(request,'no result found')

        else:
            return HttpResponseRedirect('/search/')

                        
    return render(request, 'dappx/search.html')

@login_required    
def cadmin(request):
    all_users=[]
    context={}
    if request.user.is_superuser:
        all_users= User.objects.all()
    else:
         messages.success(request,"You don't have the access to it!")
         return render(request,'dappx/login.html')
    context= {'all_users': all_users}
        
    return render(request, 'dappx/cadmin.html', context)

@login_required
def authmembers(request,pk=None):
    all_users=[]
    if request.user.is_superuser:
        if pk:
            all_user = User.objects.get(pk=pk)
    else:
         messages.success(request,"You don't have the access to it!")
         return render(request,'dappx/login.html')
    return render(request, 'dappx/authmembers.html',{'all_user':all_user})

@login_required                 
def adminsearch(request):
    if request.user.is_superuser:
        if request.method=='POST':
            srch=request.POST['srh']

            if srch:
                match=User.objects.filter(Q(username__icontains=srch)|
                                         Q(email__icontains=srch)
                                         )

                if match:
                    return render(request,'dappx/adminsearch.html', {'sr':match})
                else:
                    messages.error(request,'no result found')

            else:
                return HttpResponseRedirect('/search/')
    else:
        messages.success(request,"You don't have the access to it!")
        return render(request,'dappx/login.html')
                        
    return render(request, 'dappx/adminsearch.html')

    # return render(request, 'dappx/staff_list.html',{'superusers':superusers,'all_user':all_user})
@login_required


def staff_list(request,pk=None):
    
    if pk:
        all_user=User.objects.get(pk=pk)
        all_user.is_staff=True
        all_user.save()
    superusers=User.objects.filter(is_staff=True)
    return redirect('cadmin')
    # return render(request, 'dappx/staff_list.html',{'superusers':superusers,'all_user':all_user})

@login_required
def staff_listno(request,pk=None):
    if request.user.is_superuser:
        if pk:
            all_user=User.objects.get(pk=pk)
            all_user.is_staff=False
            all_user.save()
    else:
        messages.success(request,"You don't have access to it!")
        return redirect('index')
    return redirect('cadmin')
@login_required    
def update_dmit(request, pk):
    if request.user.is_staff or request.user.is_superuser: 
        instance = get_object_or_404(DMIT, user_id=pk)
        staff_form = StaffUpdateForm(request.POST,request.FILES,instance=instance)
        instancev = get_object_or_404(DMITVAL, user_id=pk)
        value_form = DmitvalUpdateForm(request.POST,request.FILES,instance=instancev)
        msg= "update data"
        if staff_form.is_valid() and value_form.is_valid():
            
            staff_form.save()
            instance.refresh_from_db()
            value_form.save()
            instancev.refresh_from_db()
            messages.success(request,'DMIT updated successfully')
            msg = "DMIT updated successfully"
        else:
            staff_form = StaffUpdateForm(instance=instance)
            value_form = DmitvalUpdateForm(instance=instancev)
            
    else:
        messages.success(request,"You don't have access to it!")
        return render(request,'dappx/login.html')
    return render(request, 'dappx/update_dmit.html', {'staff_form': staff_form,'value_form':value_form, 'instance': instance, "msg" : msg,})  



def staffsearch(request):
    if request.method=='POST':
        srch=request.POST['srh']

        if srch:
            match=User.objects.filter(Q(username__icontains=srch)|
                                         Q(email__icontains=srch)
                                         )

            if match:
                return render(request,'dappx/staffsr.html', {'sr':match})
            else:
                messages.error(request,'no result found')

        else:
            return HttpResponseRedirect('/staffsr/')

                        
    return render(request, 'dappx/staffsr.html')

@login_required
def appointment(request):
    if request.method=='POST':
        a_form=''
        a_form=AppointmentForm(data=request.POST)
        if a_form.is_valid():
            user=request.user
            profile=request.user.profile
            appointment=a_form.save()
            appointment.user_id=profile.user_id
            appointment.appointment_date=a_form.cleaned_data.get('appointment_date')
            appointment.appointment_slot=a_form.cleaned_data.get('appointment_slot')
            appointment.save()
            # messages.success(request,"You've booked your appointment successfully!")
            send_mail(
                'Hi '+user.username,
                'Hi '+str(user.username)+'!'+' A reminder from CloudAge about your DMIT appointment on '+str(user.appointment.appointment_date)+' at '+str(user.appointment.appointment_slot)+' If you need to reschedule login to our portal or contact us on +91 8087201590 . Thanks',
                settings.EMAIL_HOST_USER,
                [user.email],
                fail_silently=False,
            )
            return redirect('index')
    else:
        a_form = AppointmentForm(data=request.POST or None)
    args={'a_form':a_form}         
    return render(request,'dappx/appointment.html',args)

@login_required
def cancel_appointment(request):
    profile=request.user.profile
    user_id=profile.user_id
    user=request.user
    appointment = request.user.appointment
    instance=Appointment.objects.get(user_id=user_id)
    instance.delete()
    messages.success(request,"You cancelled your appointment successfully!")
    send_mail(
        'DMIT slot cancel of '+user.username,
        'your Appointment for date '+str(user.appointment.appointment_date)+' time '+str(user.appointment.appointment_slot)+' is canceled',
        settings.EMAIL_HOST_USER,
        [user.email],
        fail_silently=False,
     )

    return redirect('index')

def contact(request):
    return render(request, 'dappx/contact.html')








class DFormula:   
    def __init__(self, pk):
        self.pk = pk
        self.userDetail = ""
        self.userDetail = User.objects.get(pk=self.pk)
        self.username = ""
        self.username = self.userDetail.username 
        self.userDetail = ""
        self.userDetail = User.objects.get(pk=self.pk)
        self.username = ""
        self.username = self.userDetail.username
        self.userProfileDetail = Profile.objects.get(pk=self.pk)
        self.dmitDetail = DMITVAL.objects.get(user_id=self.pk)
        
        self.k=self.userProfileDetail.mobile_no
        
        w = [int(i) for i in str(self.k)]
        s = (w[-4:])
        self.mobileno= ''.join([str(elem) for elem in s])
        self.clientcode = 'CGS' + str(self.mobileno)        

        self.l1 = self.dmitDetail.l1
        self.r1 = self.dmitDetail.r1
        
            #### HR
    BD4 = {
    'W1' : "Dominant",
    'W2' : "Dominant",
    'W3' : "Dominant",
    'W4' : "Dominant",
    'W5' : "Compliant",
    'W6' : "Compliant",
    'W7' : "Compliant",
    'W8' : "Dominant",
    'W9' : "Dominant",
    'W10' : "Dominant",
    'W11' : "Dominant",
    'L' : "Steady" ,
    'R' : "Steady" ,
    'L1' : "Steady" ,
    'R1' : "Steady" ,
    'X1' : "Influential", 
    'X2' : "Influential" ,
    'X3' : "Influential" ,
    'X4' : "Influential" ,
    'W' : "Dominant"
    }

    AN4 = {
    "W1":   1.43,
    "W2":   1.287,
    "W3":   1.4872,
    "W4":   1.3013,
    "W5":   1.3871,
    "W6":   1.4014,
    "W7":   1.4157,
    "W8":   1.6445,
    "W9":   1.5587,
    "W10":  1.9448,
    "W11":  1.8876,
    "L" :   1.2441,
    "R" :   1.6731,
    "L1":   1.3442,
    "R1":   1.7875,
    "X1":   0,
    "X2":   0,
    "X3":   0,
    "X4":   0,
    "W" :   1.43,
    }

    Y4 = {
    "W1":   1.33,
    "W2":   1.197,
    "W3":   1.3832,
    "W4":   1.2103,
    "W5":   1.2901,
    "W6":   1.3034,
    "W7":   1.3167,
    "W8":   1.5295,
    'W9':   1.4497,
    "W10":  1.8088,
    "W11":  1.7556,
    "L" :   1.1571,
    'R' :   1.5561,
    "L1":   1.2502,
    'R1':   1.6625,
    "X1":   0,
    "X2":   0,
    "X3":   0,
    "X4":   0,
    "W":    1.33
    }

    AB4 = {
    "W1":   1.19,
    "W2":   1.071,
    "W3":   1.2376,
    "W4":   1.0829,
    "W5":   1.1543,
    "W6":   1.1662,
    "W7":   1.1781,
    "W8":   1.3685,
    "W9":   1.2971,
    "W10":  1.6184,
    "W11":  1.5708,
    "L" :   1.0353,
    "R" :   1.3923,
    "L1":   1.1186,
    "R1":   1.4875,
    "X1":   0,
    "X2":   0,
    "X3":   0,
    "X4":   0,
    "W":    1.19

    }

    AE4 = {
    "W1":   1.31,
    "W2":   1.179,
    "W3":   1.3624,
    "W4":   1.1921,
    "W5":   1.2707,
    "W6":   1.2838,
    "W7":   1.2969,
    "W8":   1.5065,
    "W9":   1.4279,
    "W10":  1.7816,
    "W11":  1.7292,
    "L" :   1.1397,
    "R" :   1.5327,
    "L1":   1.2314,
    "R1":   1.6375,
    "X1":   0,
    "X2":   0,
    "X3":   0,
    "X4":   0,
    "W":    1.31

    }

    AH4 = {
    "W1":   1.35,
    "W2":   1.215,
    "W3":   1.404,
    "W4":   1.2285,
    "W5":   1.3095,
    "W6":   1.323,
    "W7":   1.3365,
    "W8":   1.5525,
    "W9":   1.4715,
    "W10":  1.836,
    "W11":  1.782,
    "L" :   1.1745,
    "R" :   1.5795,
    "L1":   1.269,
    "R1":   1.6875,
    "X1":   0,
    "X2":   0,
    "X3":   0,
    "X4":   0,
    "W":    1.35

    }

    AK4 = {
    "W1":   1.57,
    "W2":   1.413,
    "W3":   1.6328,
    "W4":   1.4287,
    "W5":   1.5229,
    "W6":   1.5386,
    "W7":   1.5543,
    "W8":   1.8055,
    "W9":   1.7113,
    "W10":  2.1352,
    "W11":  2.0724,
    "L" :   1.3659,
    "R" :   1.8369,
    "L1":   1.4758,
    "R1":   1.9625,
    "X1":   0,
    "X2":   0,
    "X3":   0,
    "X4":   0,
    "W":    1.57

    }

    AQ4 = {
    "W1":   1.22,
    "W2":   1.098,
    "W3":   1.2688,
    "W4":   1.1102,
    "W5":   1.1834,
    "W6":   1.1956,
    "W7":   1.2078,
    "W8":   1.403,
    "W9":   1.3298,
    "W10":  1.6592,
    "W11":  1.6104,
    "L" :   1.0614,
    "R" :   1.4274,
    "L1":   1.1468,
    "R1":   1.525,
    "X1":   0,
    "X2":   0,
    "X3":   0,
    "X4":   0,
    "W":    1.22

    }

    AT4 = {
    "W1":   1.35,
    "W2":   1.215,
    "W3":   1.404,
    "W4":   1.2285,
    "W5":   1.3095,
    "W6":   1.323,
    "W7":   1.3365,
    "W8":   1.5525,
    "W9":   1.4715,
    "W10":  1.836,
    "W11":  1.782,
    "L" :   1.1745,
    "R" :   1.5795,
    "L1":   1.269,
    "R1":   1.6875,
    "X1":   0,
    "X2":   0,
    "X3":   0,
    "X4":   0,
    "W":    1.35

    }

    AW4 = {
    "W1":   1.4,
    "W2":   1.26,
    "W3":   1.456,
    "W4":   1.274,
    "W5":   1.358,
    "W6":   1.372,
    "W7":   1.386,
    "W8":   1.61,
    "W9":   1.526,
    "W10":  1.904,
    "W11":  1.848,
    "L" :   1.218,
    "R" :   1.638,
    "L1":   1.316,
    "R1":   1.75,
    "X1":   0,
    "X2":   0,
    "X3":   0,
    "X4":   0,
    "W":    1.4

    }

    AZ4 = {
    "W1":   1.61,
    "W2":   1.449,
    "W3":   1.6744,
    "W4":   1.4651,
    "W5":   1.5617,
    "W6":   1.5778,
    "W7":   1.5939,
    "W8":   1.8515,
    "W9":   1.7549,
    "W10":  2.1896,
    "W11":  2.1252,
    "L" :   1.4007,
    "R" :   1.8837,
    "L1":   1.5134,
    "R1":   2.0125,
    "X1":   0,
    "X2":   0,
    "X3":   0,
    "X4":   0,
    "W":    1.61

    }

    def D19func(self):
        return self.dmitDetail.latd

    def D21func(self):
        return self.dmitDetail.ratd


    def BD4func(self, l1):
        for pattern in DFormula.BD4:
            if l1 == pattern:
                return DFormula.BD4[pattern]
                break

    def BD18func(self, r1):
        for pattern in DFormula.BD4:
            if r1 == pattern:
                return DFormula.BD4[pattern]
                break

    def D44func(self):                 
        return self.dmitDetail.r2    

    def D43func(self):                
        return self.dmitDetail.rrc1

    def AN4func(r1):
        for pattern in DFormula.AN4:
            if r1 == pattern:
                return DFormula.AN4[pattern]
                break

    def D32func(self):
        return self.dmitDetail.l1

    def D33func(self):              
        return self.dmitDetail.lrc1

    def Y4func(l1):
        for pattern in DFormula.Y4:
            if l1 == pattern:
                return DFormula.Y4[pattern]
                break

    def Y11func(self):
        return self.D33func() * DFormula.Y4func(self.dmitDetail.l1)

    def D35func(self):
        return self.dmitDetail.lrc2

    def AB4func(l2):
        for pattern in DFormula.AB4:
            if l2 == pattern:
                return DFormula.AB4[pattern]
                break

    def AB11func(self):
        return self.D35func() * DFormula.AB4func(self.dmitDetail.l2)

    def D38func(self):
        return self.dmitDetail.l4
    
    
    def D37func(self):
        return self.dmitDetail.lrc3
    
    def AE4func(l3):
        for pattern in DFormula.AE4:
            if l3 == pattern:
                return DFormula.AE4[pattern]
                break

    def AE11func(self):
        return self.D37func() * DFormula.AE4func(self.dmitDetail.l3)

    def D39func(self):
        return self.dmitDetail.lrc4

    def AH4func(l4):
        for pattern in DFormula.AH4:
            if l4 == pattern:
                return DFormula.AH4[pattern]
                break

    def AH11func(self):
        return self.D39func() * DFormula.AH4func(self.dmitDetail.l4)

    def D42func(self):
        return self.dmitDetail.r1

    def D41func(self):
        return self.dmitDetail.lrc5

    def AK4func(self, l5):
        for pattern in DFormula.AK4:
            if l5 == pattern:
                return DFormula.AK4[pattern]
                break

    def AK11func(self):
        return self.D41func() * DFormula.AK4func(self.dmitDetail.l5)

    def Z30func(self):
        return self.Y11func() + self.AB11func() + self.AE11func() + self.AH11func() + self.AK11func()

    def D45func(self):             
        return self.dmitDetail.rrc2

    def AQ4func(r2):
        for pattern in DFormula.AQ4:
            if r2 == pattern:
                return DFormula.AQ4[pattern]
                break

    def AQ11func(self):
        return self.D45func() * DFormula.AQ4func(self.dmitDetail.r2)

    def D48func(self):
        return self.dmitDetail.r4
    
    def D47func(self):
        return self.dmitDetail.rrc3
       
    def AT4func(r3):
        for pattern in DFormula.AT4:
            if r3 == pattern:
                return DFormula.AT4[pattern]
                break

    def AT11func(self):
        return self.D47func() * DFormula.AT4func(self.dmitDetail.r3)
    
    def D49func(self):
        return self.dmitDetail.rrc4

    def AW4func(r4):
        for pattern in DFormula.AW4:
            if r4 == pattern:
                return DFormula.AW4[pattern]
                break

    def AW11func(self):
        return self.D49func() * DFormula.AW4func(self.dmitDetail.r4)
    
    def D51func(self):
        return self.dmitDetail.rrc5

    def AZ4func(r5):
        for pattern in DFormula.AZ4:
            if r5 == pattern:
                return DFormula.AZ4[pattern]
                break
    
    def D46func(self):
        return self.dmitDetail.r3
    
    def D50func(self):
        return self.dmitDetail.r5

    def D34func(self):
        return self.dmitDetail.l2

    def D36func(self):
        return self.dmitDetail.l3

    def D40func(self):
        return self.dmitDetail.l5

    def AZ11func(self):
        return self.D51func() * DFormula.AZ4func(self.dmitDetail.r5)
    
    def AA30func(self):
        return self.AN11func() + self.AQ11func() + self.AT11func() + self.AW11func() + self.AZ11func()

    def AB30func(self):
        return self.Z30func() + self.AA30func()

    def AN11func(self):
        return self.D43func() * DFormula.AN4func(self.dmitDetail.r1)

    def AC33func(self):
        return (self.AN11func() / self.AB30func()) * 100
    
    def AC34func(self):
        return (self.AQ11func() / self.AB30func()) * 100 

    def AC35func(self):
        return (self.AT11func() / self.AB30func()) * 100

    def AC36func(self):
        return (self.AW11func() / self.AB30func()) * 100

    def AC37func(self):
        return (self.AZ11func() / self.AB30func()) * 100

    def AC38func(self):
        return self.AC33func() + self.AC34func() + self.AC35func() + self.AC36func() + self.AC37func()

    def AA35func(self):
        return (self.AE11func() / self.AB30func()) * 100

    def Y52func(self):
        return ((self.AC37func()) + (self.AC35func() + self.AA35func())/2)/2

    def Z52func(self):
        return (self.AZ11func() / self.AB30func()) * 100

    def AA52func(self):
        return (self.AC37func() + self.AC35func()) / 2
    
    def AA36func(self):
        return (self.AH11func() / self.AB30func()) * 100
    
    def AB52func(self):
        return (self.AC37func() + self.AA36func()) / 2

    def AA37func(self):
        return (self.AK11func() / self.AB30func()) * 100

    def AC52func(self):
        return (self.AC37func() + self.AA37func()) / 2

    def AD52func(self):                
        return self.Y52func() + self.Z52func() + self.AA52func() + self.AB52func() + self.AC52func()

    def Y51func(self):
        return (self.Y52func() / self.AD52func()) * 100

    def Z51func(self):
        return (self.Z52func() / self.AD52func()) * 100

    def AA51func(self):
        return (self.AA52func() / self.AD52func()) * 100
    
    def AB51func(self):
        return (self.AB52func() / self.AD52func()) * 100

    def AC51func(self):
        return (self.AC52func() / self.AD52func()) * 100

    def AJ37func(self):
        return (self.AC34func() + self.AC33func()) / 2

    def AA34func(self):
        return (self.AB11func() / self.AB30func()) * 100

    def AA33func(self):
        return ((self.Y11func() / self.AB30func()) * 100)

    def AK37func(self):
        return (self.AA37func() + self.AA34func() + self.AA33func()) / 3

    def AL37func(self):
        return self.AJ37func() + self.AK37func()

    def AM37func(self):
        return (self.AJ37func() / self.AL37func()) * 100

    def AN37func(self):
        return (self.AK37func() / self.AL37func()) * 100

    def AO37func(self):
        return (self.AA33func() + self.AC33func()) / 2

    def AP37func(self):
        return (self.AC34func() + self.AC37func()) / 2

    def AQ37func(self):
        return self.AO37func() + self.AP37func()

    def AR37func(self):
        return (self.AO37func() / self.AQ37func()) * 100

    def AS37func(self):
        return (self.AP37func() / self.AQ37func()) * 100
    
    def AQ24func(self):
        return self.AQ11func()
    
    def AW24func(self):
        return self.AW11func()

    def AE39func(self):
        return (((self.AQ24func() + self.AW24func())/2)/2)*10

    def Y24func(self):
        return self.Y11func()

    def AN24func(self):
        return self.AN11func()

    def AF39func(self):
        return (((self.Y24func() + self.AN24func())/2)/2)*10

    def AE24func(self):
        return (self.AE11func() + self.AT11func()) / 2

    def AZ24func(self):
        return self.AZ11func()

    def AH39func(self):
        return (((self.AE24func() + self.AZ24func())/2)/2)*10

    def AK11func(self):
        return self.D41func() * self.AK4func(self.dmitDetail.l5)
    
    def AB24func(self):
        return (self.AB11func() + self.AK11func()) / 2

    def AH24func(self):
        return self.AH11func()

    def AG39func(self):
        return (((self.AB24func() + self.AH24func())/2)/2)*10

    def AG34func(self):
        return (self.AA37func() + self.AC37func()) / 2

    def AE34func(self):
        return (self.AA35func() + self.AC35func()) / 2

    def AF34func(self):
        return (self.AA36func() + self.AC36func()) / 2

    def AH34func(self):
        return self.AE34func() + self.AF34func() + self.AG34func()

    def AG35func(self):
        return (self.AG34func() / self.AH34func()) * 100
    
    def AF35func(self):
        return (self.AF34func() / self.AH34func()) * 100

    def AE35func(self):
        return (self.AE34func() / self.AH34func()) * 100

    def AJ39func(self, l1):
        if l1 == 'W' or l1 == 'W10' or l1 == 'W1' or l1 == 'W2' or l1 == 'W3' or l1 == 'W4' or l1 == 'W11' or l1 == 'W5' or l1 == 'W6' or l1 == 'W7' or l1 == 'W8' or l1 == 'W9':
            return 10
        else :
            return 0

    def AJ40func(self, l2):
        if l2 == 'W' or l2 == 'W10' or l2 == 'W1' or l2 == 'W2' or l2 == 'W3' or l2 == 'W4' or l2 == 'W11' or l2 == 'W5' or l2 == 'W6' or l2 == 'W7' or l2 == 'W8' or l2 == 'W9':
            return 10
        else :
            return 0

    def AJ41func(self, l3):
        if l3 == 'W' or l3 == 'W10' or l3 == 'W1' or l3 == 'W2' or l3 == 'W3' or l3 == 'W4' or l3 == 'W11' or l3 == 'W5' or l3 == 'W6' or l3 == 'W7' or l3 == 'W8' or l3 == 'W9':
            return 10
        else :
            return 0
    
    def AJ42func(self, l4):
        if l4 == 'W' or l4 == 'W10' or l4 == 'W1' or l4 == 'W2' or l4 == 'W3' or l4 == 'W4' or l4 == 'W11' or l4 == 'W5' or l4 == 'W6' or l4 == 'W7' or l4 == 'W8' or l4 == 'W9':
            return 10
        else :
            return 0

    def AJ43func(self, l5):
        if l5 == 'W' or l5 == 'W10' or l5 == 'W1' or l5 == 'W2' or l5 == 'W3' or l5 == 'W4' or l5 == 'W11' or l5 == 'W5' or l5 == 'W6' or l5 == 'W7' or l5 == 'W8' or l5 == 'W9':
            return 10
        else :
            return 0

    def AJ44func(self, r1):
        if r1 == 'W' or r1 == 'W10' or r1 == 'W1' or r1 == 'W2' or r1 == 'W3' or r1 == 'W4' or r1 == 'W11' or r1 == 'W5' or r1 == 'W6' or r1 == 'W7' or r1 == 'W8' or r1 == 'W9':
            return 10
        else :
            return 0

    def AJ45func(self, r2):
        if r2 == 'W' or r2 == 'W10' or r2 == 'W1' or r2 == 'W2' or r2 == 'W3' or r2 == 'W4' or r2 == 'W11' or r2 == 'W5' or r2 == 'W6' or r2 == 'W7' or r2 == 'W8' or r2 == 'W9':
            return 10
        else :
            return 0

    def AJ46func(self, r3):
        if r3 == 'W' or r3 == 'W10' or r3 == 'W1' or r3 == 'W2' or r3 == 'W3' or r3 == 'W4' or r3 == 'W11' or r3 == 'W5' or r3 == 'W6' or r3 == 'W7' or r3 == 'W8' or r3 == 'W9':
            return 10
        else :
            return 0

    def AJ47func(self, r4):
        if r4 == 'W' or r4 == 'W10' or r4 == 'W1' or r4 == 'W2' or r4 == 'W3' or r4 == 'W4' or r4 == 'W11' or r4 == 'W5' or r4 == 'W6' or r4 == 'W7' or r4 == 'W8' or r4 == 'W9':
            return 10
        else :
            return 0

    def AJ48func(self, r5):
        if r5 == 'W' or r5 == 'W10' or r5 == 'W1' or r5 == 'W2' or r5 == 'W3' or r5 == 'W4' or r5 == 'W11' or r5 == 'W5' or r5 == 'W6' or r5 == 'W7' or r5 == 'W8' or r5 == 'W9':
            return 10
        else :
            return 0

    def AJ49func(self):
        return (self.AJ39func(self.dmitDetail.l1) + self.AJ40func(self.dmitDetail.l2) + self.AJ41func(self.dmitDetail.l3) + self.AJ42func(self.dmitDetail.l4) + self.AJ43func(self.dmitDetail.l5) + self.AJ44func(self.dmitDetail.r1) + self.AJ45func(self.dmitDetail.r2) + self.AJ46func(self.dmitDetail.r3) + self.AJ47func(self.dmitDetail.r4) + self.AJ48func(self.dmitDetail.r5)) / 100

    def AJ52func(self):
        return self.AJ49func() * 100

    def AK39func(self, l1):
        if l1 == "L" or l1 == "L1":
            return 10
        else:
            return 0

    def AK40func(self, l2):
        if l2 == "L" or l2 == "L1":
            return 10
        else:
            return 0

    def AK41func(self, l3):
        if l3 == "L" or l3 == "L1":
            return 10
        else:
            return 0

    def AK42func(self, l4):
        if l4 == "L" or l4 == "L1":
            return 10
        else:
            return 0
    
    def AK43func(self, l5):
        if l5 == "L" or l5 == "L1":
            return 10
        else:
            return 0

    def AK44func(self, r1):
        if r1 == "L" or r1 == "L1":
            return 10
        else:
            return 0
        
    def AK45func(self, r2):
        if r2 == "L" or r2 == "L1":
            return 10
        else:
            return 0

    def AK46func(self, r3):
        if r3 == "L" or r3 == "L1":
            return 10
        else:
            return 0

    def AK47func(self, r4):
        if r4 == "L" or r4 == "L1":
            return 10
        else:
            return 0

    def AK48func(self, r5):
        if r5 == "L" or r5 == "L1":
            return 10
        else:
            return 0
    
    def AK49func(self):
        return (self.AK39func(self.dmitDetail.l1) + self.AK40func(self.dmitDetail.l2) + self.AK41func(self.dmitDetail.l3) + self.AK42func(self.dmitDetail.l4) + self.AK43func(self.dmitDetail.l5) + self.AK44func(self.dmitDetail.r1) + self.AK45func(self.dmitDetail.r2) + self.AK46func(self.dmitDetail.r3) + self.AK47func(self.dmitDetail.r4) + self.AK48func(self.dmitDetail.r5)) / 100

    def AL39func(self, l1):
        if l1 == "R" or l1 == "R1":
            return 10
        else:
            return 0
    
    def AL40func(self, l2):
        if l2 == "R" or l2 == "R1":
            return 10
        else:
            return 0

    def AL41func(self, l3):
        if l3 == "R" or l3 == "R1":
            return 10
        else:
            return 0
    
    def AL42func(self, l4):
        if l4 == "R" or l4 == "R1":
            return 10
        else:
            return 0
    
    def AL43func(self, l5):
        if l5 == "R" or l5 == "R1":
            return 10
        else:
            return 0
    
    def AL44func(self, r1):
        if r1 == "R" or r1 == "R1":
            return 10
        else:
            return 0
    
    def AL45func(self, r2):
        if r2 == "R" or r2 == "R1":
            return 10
        else:
            return 0
    
    def AL46func(self, r3):
        if r3 == "R" or r3 == "R1":
            return 10
        else:
            return 0
    
    def AL47func(self, r4):
        if r4 == "R" or r4 == "R1":
            return 10
        else:
            return 0
    
    def AL48func(self, r5):
        if r5 == "R" or r5 == "R1":
            return 10
        else:
            return 0
        
    def AL49func(self):
        return (self.AL39func(self.dmitDetail.l1) + self.AL40func(self.dmitDetail.l2) + self.AL41func(self.dmitDetail.l3) + self.AL42func(self.dmitDetail.l4) + self.AL43func(self.dmitDetail.l5) + self.AL44func(self.dmitDetail.r1) + self.AL45func(self.dmitDetail.r2) + self.AL46func(self.dmitDetail.r3) + self.AL47func(self.dmitDetail.r4) + self.AL48func(self.dmitDetail.r5)) / 100

    def AM39func(self, l1):
        if l1 == "X1" or l1 == "X2" or l1 == "X3" or l1 == "X4":
            return 10
        else:
            return 0

    def AM40func(self, l2):
        if l2 == "X1" or l2 == "X2" or l2 == "X3" or l2 == "X4":
            return 10
        else:
            return 0

    def AM41func(self, l3):
        if l3 == "X1" or l3 == "X2" or l3 == "X3" or l3 == "X4":
            return 10
        else:
            return 0

    def AM42func(self, l4):
        if l4 == "X1" or l4 == "X2" or l4 == "X3" or l4 == "X4":
            return 10
        else:
            return 0

    def AM43func(self, l5):
        if l5 == "X1" or l5 == "X2" or l5 == "X3" or l5 == "X4":
            return 10
        else:
            return 0

    def AM44func(self, r1):
        if r1 == "X1" or r1 == "X2" or r1 == "X3" or r1 == "X4":
            return 10
        else:
            return 0

    def AM45func(self, r2):
        if r2 == "X1" or r2 == "X2" or r2 == "X3" or r2 == "X4":
            return 10
        else:
            return 0

    def AM46func(self, r3):
        if r3 == "X1" or r3 == "X2" or r3 == "X3" or r3 == "X4":
            return 10
        else:
            return 0

    def AM47func(self, r4):
        if r4 == "X1" or r4 == "X2" or r4 == "X3" or r4 == "X4":
            return 10
        else:
            return 0

    def AM48func(self, r5):
        if r5 == "X1" or r5 == "X2" or r5 == "X3" or r5 == "X4":
            return 10
        else:
            return 0

    def AM49func(self):
        return (self.AM39func(self.dmitDetail.l1) + self.AM40func(self.dmitDetail.l2) + self.AM41func(self.dmitDetail.l3) + self.AM42func(self.dmitDetail.l4) + self.AM43func(self.dmitDetail.l5) + self.AM44func(self.dmitDetail.r1) + self.AM45func(self.dmitDetail.r2) + self.AM46func(self.dmitDetail.r3) + self.AM47func(self.dmitDetail.r4) + self.AM48func(self.dmitDetail.r5)) / 100

    def AK52func(self):
        return (self.AK49func() + self.AL49func() + self.AM49func()) * 100
    
    # RIGHT BRAIN DOMINANCE
    def AA38func(self):
        return self.AA33func() + self.AA34func() + self.AA35func() + self.AA36func() + self.AA37func()

        #Realistic page29 
        # 
    def AD57func(self):
        return (self.AC35func() + self.AA35func() + self.AC34func()) / 3                                                

    def AE57func(self):
        #=(AC34+AC37+AC33)/3
        return (self.AC34func() + self.AC37func() + self.AC33func()) / 3

    def AF57func(self):
        #=(AA34+AA37+AA36+AA35+AC35)/5
        return (self.AA34func() + self.AA37func() + self.AA36func() + self.AA35func() + self.AC35func()) / 5

    def AG57func(self):
        #=(AA33+AC36+AC34)/3
        return (self.AA33func() + self.AC36func() + self.AC34func()) / 3

    def AH57func(self):
        #=(AA33+AC36+AA34+AA37)/4
        return (self.AA33func() + self.AC36func() + self.AA34func() + self.AA37func()) / 4

    def AI57func(self):
        #=(AC34+AC36+AC35)/3
        return (self.AC34func() + self.AC36func() + self.AC35func()) / 3

    def AJ57func(self):
        return (self.AD57func() + self.AE57func() + self.AF57func() + self.AG57func() + self.AH57func() + self.AI57func())

    def AD56func(self):
        return (self.AD57func() / self.AJ57func()) * 100

        #Investigative page 29                         

    def AE56func(self):
        #=AE57/AJ57
        return (self.AE57func() / self.AJ57func()) * 100


        #Conventional
    def AI56func(self):
        #=AI57/AJ57
        return (self.AI57func() / self.AJ57func()) * 100

        #Artistic
    def AF56func(self):
        #=AF57/AJ57
        return (self.AF57func() / self.AJ57func()) * 100

    #enterprising
    def AH56func(self):
        #=AH57/AJ57
        return (self.AH57func() / self.AJ57func()) * 100

        #Social
    def AG56func(self):
        #=AG57/AJ57
        return (self.AG57func() / self.AJ57func()) * 100

        #page 33

    def AH73func(self):
        return self.AC37func()

    def AH70func(self):
        return self.AC34func()

    def AH72func(self):
        return self.AC36func()

    def AD60func(self):
        #=(AH73+AH70+AH72)/3
        return (self.AH73func() + self.AH70func() + self.AH72func()) / 3

    #Doctor
    def AC60func(self):
        #IF(AD60>=11%,"*****",IF(AD60>=10%,"****",IF(AD60>=9%,"***",IF(AD60>=8%,"**","*"))))
        if self.AD60func() >= 11:
            return "*****"
        else:
            if self.AD60func() >= 10:
                return "****"
            else:
                if self.AD60func() >= 9:
                    return "***"
                else:
                    if self.AD60func() >= 8:
                        return "**"
                    else:
                        return "*"

    #Pharmacist 
    def AH107func(self):
        return self.AC37func()
    
    def AH104func(self):
        return self.AC34func()

    def AD121func(self):
        #=(AH107+AH104)/2
        return (self.AH107func() + self.AH104func()) / 2

    def AC121func(self):
        # =IF(AD121>=11%,"*****",IF(AD121>=10%,"****",IF(AD121>=9%,"***",IF(AD121>=8%,"**","*"))))
        if self.AD121func() >= 11:
            return "*****"
        else:
            if self.AD121func() >= 10:
                return "****"
            else:
                if self.AD121func() >= 9:
                    return "***"
                else:
                    if self.AD121func() >= 8:
                        return "**"
                    else:
                        return "*"

    #nutritionist
    def AD61func(self):
        #=(AH73+AH70)/2
        return (self.AH73func() + self.AH70func()) / 2

    def AC61func(self):
        #=IF(AD61>=11%,"*****",IF(AD61>=10%,"****",IF(AD61>=9%,"***",IF(AD61>=8%,"**","*"))))
        if self.AD61func() >= 11:
            return "*****"
        else:
            if self.AD61func() >= 10:
                return "****"
            else:
                if self.AD61func() >= 9:
                    return "***"
                else:
                    if self.AD61func() >= 8:
                        return "**"
                    else:
                        return "*"

        #Medical Officer
    def AD62func(self):
        #=(AH73+AH70+AF71)/3
        return (self.AH73func() + self.AH70func() + self.AF71func()) / 3

    def AC62func(self):
        #=IF(AD62>=11%,"*****",IF(AD62>=10%,"****",IF(AD62>=9%,"***",IF(AD62>=8%,"**","*"))))
        if self.AD62func() >= 11:
            return "*****"
        else:
            if self.AD62func() >= 10:
                return "****"
            else:
                if self.AD62func() >= 9:
                    return "***"
                else:
                    if self.AD62func() >= 8:
                        return "**"
                    else:
                        return "*"

        # Chemist
    def AD63func(self):
        #=(AH73+AH70+AF71)/3
        return (self.AH73func() + self.AH70func()) / 2

    def AC63func(self):
        #=IF(AD63>=11%,"*****",IF(AD63>=10%,"****",IF(AD63>=9%,"***",IF(AD63>=8%,"**","*"))))
        if self.AD63func() >= 11:
            return "*****"
        else:
            if self.AD63func() >= 10:
                return "****"
            else:
                if self.AD63func() >= 9:
                    return "***"
                else:
                    if self.AD63func() >= 8:
                        return "**"
                    else:
                        return "*"

    #Drug Officer
    def AD122func(self):
        #=(AH107+AH104+AF105)/3
        return ( self.AH107func() + self.AH104func() + self.AF105func() ) / 3

    def AC122func(self):
        #=IF(AD122>=11%,"*****",IF(AD122>=10%,"****",IF(AD122>=9%,"***",IF(AD122>=8%,"**","*"))))
        if self.AD122func() >= 11:
            return "*****"
        else:
            if self.AD122func() >= 10:
                return "****"
            else:
                if self.AD122func() >= 9:
                    return "***"
                else:
                    if self.AD122func() >= 8:
                        return "**"
                    else:
                        return "*"

    # Surgeon
    def AD123func(self):
        return ( self.AH107func() + self.AH104func() + self.AH105func() ) / 3

    def AC123func(self):
        #=IF(AD123>=11%,"*****",IF(AD123>=10%,"****",IF(AD123>=9%,"***",IF(AD123>=8%,"**","*"))))
        if self.AD123func() >= 11:
            return "*****"
        else:
            if self.AD123func() >= 10:
                return "****"
            else:
                if self.AD123func() >= 9:
                    return "***"
                else:
                    if self.AD123func() >= 8:
                        return "**"
                    else:
                        return "*"

    # Food Inspector
    def AD124func(self):
        return ( self.AH107func() + self.AH104func() ) / 2

    def AC124func(self):
        #=IF(AD124>=11%,"*****",IF(AD124>=10%,"****",IF(AD124>=9%,"***",IF(AD124>=8%,"**","*"))))
        if self.AD124func() >= 11:
            return "*****"
        else:
            if self.AD124func() >= 10:
                return "****"
            else:
                if self.AD124func() >= 9:
                    return "***"
                else:
                    if self.AD124func() >= 8:
                        return "**"
                    else:
                        return "*"

    # Chemical Engineering R1635
    def AH71func(self):
        return self.AC35func()

    def AD64func(self):
        return (self.AH73func() + self.AH70func() + self.AH71func()) 

    def AC64func(self):
        #=IF(AD64>=11%,"*****",IF(AD64>=10%,"****",IF(AD64>=9%,"***",IF(AD64>=8%,"**","*"))))
        if self.AD64func() >= 11:
            return "*****"
        else:
            if self.AD64func() >= 10:
                return "****"
            else:
                if self.AD64func() >= 9:
                    return "***"
                else:
                    if self.AD64func() >= 8:
                        return "**"
                    else:
                        return "*"
        
    # Mechanical Engineering
    def AF105func(self):
        return self.AA35func()

    def AF107func(self):
        return self.AA37func()

    def AD125func(self):
        return (self.AF105func() + self.AH104func() + self.AF107func()) / 3

    def AC125func(self):
        #=IF(AD125>=11%,"*****",IF(AD125>=10%,"****",IF(AD125>=9%,"***",IF(AD125>=8%,"**","*"))))
        if self.AD125func() >= 11:
            return "*****"
        else:
            if self.AD125func() >= 10:
                return "****"
            else:
                if self.AD125func() >= 9:
                    return "***"
                else:
                    if self.AD125func() >= 8:
                        return "**"
                    else:
                        return "*"
        
    # Electronics Engineering
    def AF73func(self):
        return self.AA37func()

    def AF70func(self):
        return self.AA34func()

    def AD65func(self):
        return (self.AH70func() + self.AF73func() + self.AF70func() + self.AH71func()) / 4

    def AC65func(self):
        #=IF(AD65>=11%,"*****",IF(AD65>=10%,"****",IF(AD65>=9%,"***",IF(AD65>=8%,"**","*"))))
        if self.AD65func() >= 11:
            return "*****"
        else:
            if self.AD65func() >= 10:
                return "****"
            else:
                if self.AD65func() >= 9:
                    return "***"
                else:
                    if self.AD65func() >= 8:
                        return "**"
                    else:
                        return "*"

        # Electrical Engineering
    def AF71func(self):
        return self.AA35func()

    def AD66func(self):
        return (self.AH70func() + self.AH71func() + self.AF71func()) / 3

    def AC66func(self):
        #=IF(AD66>=11%,"*****",IF(AD66>=10%,"****",IF(AD66>=9%,"***",IF(AD66>=8%,"**","*"))))
        if self.AD66func() >= 11:
            return "*****"
        else:
            if self.AD66func() >= 10:
                return "****"
            else:
                if self.AD66func() >= 9:
                    return "***"
                else:
                    if self.AD66func() >= 8:
                        return "**"
                    else:
                        return "*"

    # Aviation Engineering
    def AD67func(self):
        return (self.AH70func() + self.AF73func() + self.AF70func() + self.AH73func())

    def AC67func(self):
        # =IF(AD67>=11%,"*****",IF(AD67>=10%,"****",IF(AD67>=9%,"***",IF(AD67>=8%,"**","*"))))
        if self.AD67func() >= 11:
            return "*****"
        else:
            if self.AD67func() >= 10:
                return "****"
            else:
                if self.AD67func() >= 9:
                    return "***"
                else:
                    if self.AD67func() >= 8:
                        return "**"
                    else:
                        return "*"

        # Computer Engineering
    def AH106func(self):
        return self.AC36func()

    def AD126func(self):
        return (self.AH104func() + self.AH107func() + self.AH106func()) / 3

    def AC126func(self):
        #=IF(AD126>=11%,"*****",IF(AD126>=10%,"****",IF(AD126>=9%,"***",IF(AD126>=8%,"**","*"))))
        if self.AD126func() >= 11:
            return "*****"
        else:
            if self.AD126func() >= 10:
                return "****"
            else:
                if self.AD126func() >= 9:
                    return "***"
                else:
                    if self.AD126func() >= 8:
                        return "**"
                    else:
                        return "*"

    # Production Engineering
    def AF148func(self):
        return self.AA33func()

    def AH149func(self):
        return self.AC34func()

    def AF152func(self):
        return self.AA37func()

    def AH152func(self):
        return self.AC37func()

    def AD127func(self):
        return (self.AF148func() + self.AH149func() + self.AF152func() + self.AH152func()) / 4

    def AC127func(self):
        if self.AD127func() >= 11:
            return "*****"
        else:
            if self.AD127func() >= 10:
                return "****"
            else:
                if self.AD127func() >= 9:
                    return "***"
                else:
                    if self.AD127func() >= 8:
                        return "**"
                    else:
                        return "*"

    # Sound Engineering
    def AF151func(self):
        return self.AA36func()

    def AD128func(self):
        return (self.AF151func() + self.AH149func()) / 2

    def AC128func(self):
        #=IF(AD128>=11%,"*****",IF(AD128>=10%,"****",IF(AD128>=9%,"***",IF(AD128>=8%,"**","*"))))
        if self.AD128func() >= 11:
            return "*****"
        else:
            if self.AD128func() >= 10:
                return "****"
            else:
                if self.AD128func() >= 9:
                    return "***"
                else:
                    if self.AD128func() >= 8:
                        return "**"
                    else:
                        return "*"

    # Biology Engineering
    def AF69func(self):
        return self.AA33func()

    def AD73func(self):
        return (self.AH73func() + self.AF69func() + self.AH72func()) / 3

    def AC73func(self):
        #=IF(AD73>=11%,"*****",IF(AD73>=10%,"****",IF(AD73>=9%,"***",IF(AD73>=8%,"**","*"))))
        if self.AD73func() >= 11:
            return "*****"
        else:
            if self.AD73func() >= 10:
                return "****"
            else:
                if self.AD73func() >= 9:
                    return "***"
                else:
                    if self.AD73func() >= 8:
                        return "**"
                    else:
                        return "*"

    # Biotechnology Engineering
    def AH69func(self):
        return self.AC33func()

    def AD74func(self):
        return (self.AH73func() + self.AH70func() + self.AH69func()) / 3

    # =IF(AD74>=11%,"*****",IF(AD74>=10%,"****",IF(AD74>=9%,"***",IF(AD74>=8%,"**","*"))))
    def AC74func(self):
        if self.AD74func() >= 11:
            return "*****"
        else:
            if self.AD74func() >= 10:
                return "****"
            else:
                if self.AD74func() >= 9:
                    return "***"
                else:
                    if self.AD74func() >= 8:
                        return "**"
                    else:
                        return "*"

    # Botony Engineering
    def AD75func(self):
        return (self.AH73func() + self.AF69func() + self.AH72func()) / 3
        
    #=IF(AD75>=11%,"*****",IF(AD75>=10%,"****",IF(AD75>=9%,"***",IF(AD75>=8%,"**","*"))))
    def AC75func(self):
        if self.AD75func() >= 11:
            return "*****"
        else:
            if self.AD75func() >= 10:
                return "****"
            else:
                if self.AD75func() >= 9:
                    return "***"
                else:
                    if self.AD75func() >= 8:
                        return "**"
                    else:
                        return "*"

    # Fashion Designer
    def AD76func(self):
        return (self.AF73func() + self.AF70func() + self.AH71func()) / 3
        
    #=IF(AD76>=11%,"*****",IF(AD76>=10%,"****",IF(AD76>=9%,"***",IF(AD76>=8%,"**","*"))))
    def AC76func(self):
        if self.AD76func() >= 11:
            return "*****"
        else:
            if self.AD76func() >= 10:
                return "****"
            else:
                if self.AD76func() >= 9:
                    return "***"
                else:
                    if self.AD76func() >= 8:
                        return "**"
                    else:
                        return "*"

        # Architect
    def AD77func(self):
        return (self.AF73func() + self.AF70func() + self.AH71func()) / 3
        
    #=IF(AD77>=11%,"*****",IF(AD77>=10%,"****",IF(AD77>=9%,"***",IF(AD77>=8%,"**","*"))))
    def AC77func(self):
        if self.AD77func() >= 11:
            return "*****"
        else:
            if self.AD77func() >= 10:
                return "****"
            else:
                if self.AD77func() >= 9:
                    return "***"
                else:
                    if self.AD77func() >= 8:
                        return "**"
                    else:
                        return "*"
    
    # Web Designer
    def AD78func(self):
        return (self.AF73func() + self.AF70func() + self.AH70func()) / 3
        
    #=IF(AD78>=11%,"*****",IF(AD78>=10%,"****",IF(AD78>=9%,"***",IF(AD78>=8%,"**","*"))))
    def AC78func(self):
        if self.AD78func() >= 11:
            return "*****"
        else:
            if self.AD78func() >= 10:
                return "****"
            else:
                if self.AD78func() >= 9:
                    return "***"
                else:
                    if self.AD78func() >= 8:
                        return "**"
                    else:
                        return "*"
    
        # Software Developer
    def AD79func(self):
        return (self.AF70func() + self.AH70func()) / 2
        
    #=IF(AD79>=11%,"*****",IF(AD79>=10%,"****",IF(AD79>=9%,"***",IF(AD79>=8%,"**","*"))))
    def AC79func(self):
        if self.AD79func() >= 11:
            return "*****"
        else:
            if self.AD79func() >= 10:
                return "****"
            else:
                if self.AD79func() >= 9:
                    return "***"
                else:
                    if self.AD79func() >= 8:
                        return "**"
                    else:
                        return "*"

    # Geography Professor
    def AD80func(self):
        return (self.AH73func() + self.AF69func() + self.AH72func()) / 3
        
    #=IF(AD80>=11%,"*****",IF(AD80>=10%,"****",IF(AD80>=9%,"***",IF(AD80>=8%,"**","*"))))
    def AC80func(self):
        if self.AD80func() >= 11:
            return "*****"
        else:
            if self.AD80func() >= 10:
                return "****"
            else:
                if self.AD80func() >= 9:
                    return "***"
                else:
                    if self.AD80func() >= 8:
                        return "**"
                    else:
                        return "*"

        # Environment Researcher
    def AD81func(self):
        return (self.AH73func() + self.AH70func()) / 2
        
    #=IF(AD81>=11%,"*****",IF(AD81>=10%,"****",IF(AD81>=9%,"***",IF(AD81>=8%,"**","*"))))
    def AC81func(self):
        if self.AD81func() >= 11:
            return "*****"
        else:
            if self.AD81func() >= 10:
                return "****"
            else:
                if self.AD81func() >= 9:
                    return "***"
                else:
                    if self.AD81func() >= 8:
                        return "**"
                    else:
                        return "*"

    # Soil Researcher
    def AD82func(self):
        return (self.AH73func() + self.AH70func()) / 2
        
    #=IF(AD82>=11%,"*****",IF(AD82>=10%,"****",IF(AD82>=9%,"***",IF(AD82>=8%,"**","*"))))
    def AC82func(self):
        if self.AD82func() >= 11:
            return "*****"
        else:
            if self.AD82func() >= 10:
                return "****"
            else:
                if self.AD82func() >= 9:
                    return "***"
                else:
                    if self.AD82func() >= 8:
                        return "**"
                    else:
                        return "*"
    
    # Agriculturist
    # Agriculturist doesn't have any formula so assigned to AC79func

    # Chartered Accounted
    def AD83func(self):
        return self.AH70func()
        
    #=IF(AD83>=11%,"*****",IF(AD83>=10%,"****",IF(AD83>=9%,"***",IF(AD83>=8%,"**","*"))))
    def AC83func(self):
        if self.AD83func() >= 11:
            return "*****"
        else:
            if self.AD83func() >= 10:
                return "****"
            else:
                if self.AD83func() >= 9:
                    return "***"
                else:
                    if self.AD83func() >= 8:
                        return "**"
                    else:
                        return "*"

    # Mutual Fund / Insurance
    def AD84func(self):
        return (self.AH70func() + self.AF69func() + self.AH72func()) / 3
        
    #=IF(AD84>=11%,"*****",IF(AD84>=10%,"****",IF(AD84>=9%,"***",IF(AD84>=8%,"**","*"))))
    def AC84func(self):
        if self.AD84func() >= 11:
            return "*****"
        else:
            if self.AD84func() >= 10:
                return "****"
            else:
                if self.AD84func() >= 9:
                    return "***"
                else:
                    if self.AD84func() >= 8:
                        return "**"
                    else:
                        return "*"

    # Investment Banker
    def AD85func(self):
        return (self.AH70func() + self.AF69func() + self.AH72func()) / 3
        
    #=IF(AD85>=11%,"*****",IF(AD85>=10%,"****",IF(AD85>=9%,"***",IF(AD85>=8%,"**","*"))))
    def AC85func(self):
        if self.AD85func() >= 11:
            return "*****"
        else:
            if self.AD85func() >= 10:
                return "****"
            else:
                if self.AD85func() >= 9:
                    return "***"
                else:
                    if self.AD85func() >= 8:
                        return "**"
                    else:
                        return "*"

        # Wealth Manager
    def AD86func(self):
        return (self.AH70func() + self.AF69func() + self.AH72func()) / 3
        
    #=IF(AD86>=11%,"*****",IF(AD86>=10%,"****",IF(AD86>=9%,"***",IF(AD86>=8%,"**","*"))))
    def AC86func(self):
        if self.AD86func() >= 11:
            return "*****"
        else:
            if self.AD86func() >= 10:
                return "****"
            else:
                if self.AD86func() >= 9:
                    return "***"
                else:
                    if self.AD86func() >= 8:
                        return "**"
                    else:
                        return "*"

    # Language Expert
    def AD87func(self):
        return self.AH106func()
        
    #=IF(AD87>=11%,"*****",IF(AD87>=10%,"****",IF(AD87>=9%,"***",IF(AD87>=8%,"**","*"))))
    def AC87func(self):
        if self.AD87func() >= 11:
            return "*****"
        else:
            if self.AD87func() >= 10:
                return "****"
            else:
                if self.AD87func() >= 9:
                    return "***"
                else:
                    if self.AD87func() >= 8:
                        return "**"
                    else:
                        return "*"

        # Anchor/ Radio Jockey
    def AF103func(self):
        return self.AA33func()

    def AD88func(self):
        return (self.AH106func() + self.AF103func()) / 2
        
    #=IF(AD88>=11%,"*****",IF(AD88>=10%,"****",IF(AD88>=9%,"***",IF(AD88>=8%,"**","*"))))
    def AC88func(self):
        if self.AD88func() >= 11:
            return "*****"
        else:
            if self.AD88func() >= 10:
                return "****"
            else:
                if self.AD88func() >= 9:
                    return "***"
                else:
                    if self.AD88func() >= 8:
                        return "**"
                    else:
                        return "*"

    # Writer / Author
    def AF104func(self):
        return self.AA34func()

    def AH103func(self):
        return self.AC33func()

    def AD89func(self):
        return (self.AH106func() + self.AF104func() + self.AH103func()) / 3
        
    #=IF(AD89>=11%,"*****",IF(AD89>=10%,"****",IF(AD89>=9%,"***",IF(AD89>=8%,"**","*"))))
    def AC89func(self):
        if self.AD89func() >= 11:
            return "*****"
        else:
            if self.AD89func() >= 10:
                return "****"
            else:
                if self.AD89func() >= 9:
                    return "***"
                else:
                    if self.AD89func() >= 8:
                        return "**"
                    else:
                        return "*"

    # News Editor
    def AD90func(self):
        return (self.AH106func() + self.AF103func() + self.AH104func()) / 3
        
    #=IF(AD90>=11%,"*****",IF(AD90>=10%,"****",IF(AD90>=9%,"***",IF(AD90>=8%,"**","*"))))
    def AC90func(self):
        if self.AD90func() >= 11:
            return "*****"
        else:
            if self.AD90func() >= 10:
                return "****"
            else:
                if self.AD90func() >= 9:
                    return "***"
                else:
                    if self.AD90func() >= 8:
                        return "**"
                    else:
                        return "*"

    # Hindi / English Teacher
    def AD91func(self):
        return (self.AH106func() + self.AF103func()) / 2
        
    #=IF(AD91>=11%,"*****",IF(AD91>=10%,"****",IF(AD91>=9%,"***",IF(AD91>=8%,"**","*"))))
    def AC91func(self):
        if self.AD91func() >= 11:
            return "*****"
        else:
            if self.AD91func() >= 10:
                return "****"
            else:
                if self.AD91func() >= 9:
                    return "***"
                else:
                    if self.AD91func() >= 8:
                        return "**"
                    else:
                        return "*"

    # Philosopher
    def AD92func(self):
        return (self.AH106func() + self.AF103func() + self.AH103func()) / 3
        
    #=IF(AD92>=11%,"*****",IF(AD92>=10%,"****",IF(AD92>=9%,"***",IF(AD92>=8%,"**","*"))))
    def AC92func(self):
        if self.AD92func() >= 11:
            return "*****"
        else:
            if self.AD92func() >= 10:
                return "****"
            else:
                if self.AD92func() >= 9:
                    return "***"
                else:
                    if self.AD92func() >= 8:
                        return "**"
                    else:
                        return "*"

    # Mathematician
    def AD93func(self):
        return self.AH104func()
        
    #=IF(AD93>=11%,"*****",IF(AD93>=10%,"****",IF(AD93>=9%,"***",IF(AD93>=8%,"**","*"))))
    def AC93func(self):
        if self.AD93func() >= 11:
            return "*****"
        else:
            if self.AD93func() >= 10:
                return "****"
            else:
                if self.AD93func() >= 9:
                    return "***"
                else:
                    if self.AD93func() >= 8:
                        return "**"
                    else:
                        return "*"

    # Chemical Expert
    def AD94func(self):
        return (self.AH104func() + self.AH107func()) / 2
        
    #=IF(AD94>=11%,"*****",IF(AD94>=10%,"****",IF(AD94>=9%,"***",IF(AD94>=8%,"**","*"))))
    def AC94func(self):
        if self.AD94func() >= 11:
            return "*****"
        else:
            if self.AD94func() >= 10:
                return "****"
            else:
                if self.AD94func() >= 9:
                    return "***"
                else:
                    if self.AD94func() >= 8:
                        return "**"
                    else:
                        return "*"

    # Accountant
    def AD95func(self):
        return (self.AH104func() + self.AH103func()) / 2
        
    #=IF(AD95>=11%,"*****",IF(AD95>=10%,"****",IF(AD95>=9%,"***",IF(AD95>=8%,"**","*"))))
    def AC95func(self):
        if self.AD95func() >= 11:
            return "*****"
        else:
            if self.AD95func() >= 10:
                return "****"
            else:
                if self.AD95func() >= 9:
                    return "***"
                else:
                    if self.AD95func() >= 8:
                        return "**"
                    else:
                        return "*"

    # Actuary
    def AD96func(self):
        return self.AH104func() 
        
    #=IF(AD96>=11%,"*****",IF(AD96>=10%,"****",IF(AD96>=9%,"***",IF(AD96>=8%,"**","*"))))
    def AC96func(self):
        if self.AD96func() >= 11:
            return "*****"
        else:
            if self.AD96func() >= 10:
                return "****"
            else:
                if self.AD96func() >= 9:
                    return "***"
                else:
                    if self.AD96func() >= 8:
                        return "**"
                    else:
                        return "*"

    # Charted Accountant
    def AD97func(self):
        return self.AH104func() 
        
    #=IF(AD97>=11%,"*****",IF(AD97>=10%,"****",IF(AD97>=9%,"***",IF(AD97>=8%,"**","*"))))
    def AC97func(self):
        if self.AD97func() >= 11:
            return "*****"
        else:
            if self.AD97func() >= 10:
                return "****"
            else:
                if self.AD97func() >= 9:
                    return "***"
                else:
                    if self.AD97func() >= 8:
                        return "**"
                    else:
                        return "*"

    # HR Management
    def AD98func(self):
        return (self.AH103func() + self.AF103func() + self.AH106func()) / 3
        
    #=IF(AD98>=11%,"*****",IF(AD98>=10%,"****",IF(AD98>=9%,"***",IF(AD98>=8%,"**","*"))))
    def AC98func(self):
        if self.AD98func() >= 11:
            return "*****"
        else:
            if self.AD98func() >= 10:
                return "****"
            else:
                if self.AD98func() >= 9:
                    return "***"
                else:
                    if self.AD98func() >= 8:
                        return "**"
                    else:
                        return "*"

    # HR Management
    def AD99func(self):
        return (self.AH103func() + self.AF103func() + self.AH106func() + self.AH104func()) / 4
        
    #=IF(AD99>=11%,"*****",IF(AD99>=10%,"****",IF(AD99>=9%,"***",IF(AD99>=8%,"**","*"))))
    def AC99func(self):
        if self.AD99func() >= 11:
            return "*****"
        else:
            if self.AD99func() >= 10:
                return "****"
            else:
                if self.AD99func() >= 9:
                    return "***"
                else:
                    if self.AD99func() >= 8:
                        return "**"
                    else:
                        return "*"

    # Tourism Management
    def AD100func(self):
        return (self.AH106func() + self.AF107func() + self.AH107func() + self.AF105func()) / 4
        
    #=IF(AD100>=11%,"*****",IF(AD100>=10%,"****",IF(AD100>=9%,"***",IF(AD100>=8%,"**","*"))))
    def AC100func(self):
        if self.AD100func() >= 11:
            return "*****"
        else:
            if self.AD100func() >= 10:
                return "****"
            else:
                if self.AD100func() >= 9:
                    return "***"
                else:
                    if self.AD100func() >= 8:
                        return "**"
                    else:
                        return "*"

    # Politician
    def AD101func(self):
        return (self.AH106func() + self.AF103func()) / 2
        
    #=IF(AD101>=11%,"*****",IF(AD101>=10%,"****",IF(AD101>=9%,"***",IF(AD101>=8%,"**","*"))))
    def AC101func(self):
        if self.AD101func() >= 11:
            return "*****"
        else:
            if self.AD101func() >= 10:
                return "****"
            else:
                if self.AD101func() >= 9:
                    return "***"
                else:
                    if self.AD101func() >= 8:
                        return "**"
                    else:
                        return "*"

    # Politician
    def AD102func(self):
        return (self.AH106func() + self.AF103func() + self.AH107func()) / 3
        
    #=IF(AD102>=11%,"*****",IF(AD102>=10%,"****",IF(AD102>=9%,"***",IF(AD102>=8%,"**","*"))))
    def AC102func(self):
        if self.AD102func() >= 11:
            return "*****"
        else:
            if self.AD102func() >= 10:
                return "****"
            else:
                if self.AD102func() >= 9:
                    return "***"
                else:
                    if self.AD102func() >= 8:
                        return "**"
                    else:
                        return "*"

    # Judge
    def AF106func(self):
        return self.AA36func()

    def AD103func(self):
        return (self.AH106func() + self.AH107func() + self.AF106func() + self.AH104func()) / 4
        
    #=IF(AD103>=11%,"*****",IF(AD103>=10%,"****",IF(AD103>=9%,"***",IF(AD103>=8%,"**","*"))))
    def AC103func(self):
        if self.AD103func() >= 11:
            return "*****"
        else:
            if self.AD103func() >= 10:
                return "****"
            else:
                if self.AD103func() >= 9:
                    return "***"
                else:
                    if self.AD103func() >= 8:
                        return "**"
                    else:
                        return "*"

    # Public Relation Officer
    def AD104func(self):
        return (self.AF103func() + self.AH106func()) / 2
        
    #=IF(AD104>=11%,"*****",IF(AD104>=10%,"****",IF(AD104>=9%,"***",IF(AD104>=8%,"**","*"))))
    def AC104func(self):
        if self.AD104func() >= 11:
            return "*****"
        else:
            if self.AD104func() >= 10:
                return "****"
            else:
                if self.AD104func() >= 9:
                    return "***"
                else:
                    if self.AD104func() >= 8:
                        return "**"
                    else:
                        return "*"

    # Psychologist
    def AD105func(self):
        return (self.AF103func() + self.AH106func() + self.AH103func() + self.AF106func()) / 4
        
    #=IF(AD105>=11%,"*****",IF(AD105>=10%,"****",IF(AD105>=9%,"***",IF(AD105>=8%,"**","*"))))
    def AC105func(self):
        if self.AD105func() >= 11:
            return "*****"
        else:
            if self.AD105func() >= 10:
                return "****"
            else:
                if self.AD105func() >= 9:
                    return "***"
                else:
                    if self.AD105func() >= 8:
                        return "**"
                    else:
                        return "*"

    # Career Counselor
    def AD106func(self):
        return (self.AF103func() + self.AH106func() + self.AH103func() + self.AF106func()) / 4
        
    #=IF(AD106>=11%,"*****",IF(AD106>=10%,"****",IF(AD106>=9%,"***",IF(AD106>=8%,"**","*"))))
    def AC106func(self):
        if self.AD106func() >= 11:
            return "*****"
        else:
            if self.AD106func() >= 10:
                return "****"
            else:
                if self.AD106func() >= 9:
                    return "***"
                else:
                    if self.AD106func() >= 8:
                        return "**"
                    else:
                        return "*"

    # Mediator
    def AD107func(self):
        return (self.AF103func() + self.AH106func() + self.AF106func()) / 3
        
    #=IF(AD107>=11%,"*****",IF(AD107>=10%,"****",IF(AD107>=9%,"***",IF(AD107>=8%,"**","*"))))
    def AC107func(self):
        if self.AD107func() >= 11:
            return "*****"
        else:
            if self.AD107func() >= 10:
                return "****"
            else:
                if self.AD107func() >= 9:
                    return "***"
                else:
                    if self.AD107func() >= 8:
                        return "**"
                    else:
                        return "*"

    # Translator
    def AD108func(self):
        return (self.AF103func() + self.AH106func() ) / 2
        
    #=IF(AD108>=11%,"*****",IF(AD108>=10%,"****",IF(AD108>=9%,"***",IF(AD108>=8%,"**","*"))))
    def AC108func(self):
        if self.AD108func() >= 11:
            return "*****"
        else:
            if self.AD108func() >= 10:
                return "****"
            else:
                if self.AD108func() >= 9:
                    return "***"
                else:
                    if self.AD108func() >= 8:
                        return "**"
                    else:
                        return "*"

    # Intrepreter
    def AD109func(self):
        return (self.AF103func() + self.AH106func() +self.AF106func()) / 3
        
    #=IF(AD109>=11%,"*****",IF(AD109>=10%,"****",IF(AD109>=9%,"***",IF(AD109>=8%,"**","*"))))
    def AC109func(self):
        if self.AD109func() >= 11:
            return "*****"
        else:
            if self.AD109func() >= 10:
                return "****"
            else:
                if self.AD109func() >= 9:
                    return "***"
                else:
                    if self.AD109func() >= 8:
                        return "**"
                    else:
                        return "*"

    # News Reader
    def AD110func(self):
        return (self.AH106func() +self.AF107func() + self.AH107func()) / 3
        
    #=IF(AD109>=11%,"*****",IF(AD109>=10%,"****",IF(AD109>=9%,"***",IF(AD109>=8%,"**","*"))))
    def AC110func(self):
        if self.AD110func() >= 11:
            return "*****"
        else:
            if self.AD110func() >= 10:
                return "****"
            else:
                if self.AD110func() >= 9:
                    return "***"
                else:
                    if self.AD110func() >= 8:
                        return "**"
                    else:
                        return "*"

    # Trainer
    def AD111func(self):
        return (self.AH106func() + self.AF105func() + self.AF103func()) / 3
        
    #=IF(AD111>=11%,"*****",IF(AD111>=10%,"****",IF(AD111>=9%,"***",IF(AD111>=8%,"**","*"))))
    def AC111func(self):
        if self.AD111func() >= 11:
            return "*****"
        else:
            if self.AD111func() >= 10:
                return "****"
            else:
                if self.AD111func() >= 9:
                    return "***"
                else:
                    if self.AD111func() >= 8:
                        return "**"
                    else:
                        return "*"

    # Language Researcher
    def AD112func(self):
        return (self.AH106func() + self.AH107func()) / 2
        
    #=IF(AD111>=11%,"*****",IF(AD111>=10%,"****",IF(AD111>=9%,"***",IF(AD111>=8%,"**","*"))))
    def AC112func(self):
        if self.AD112func() >= 11:
            return "*****"
        else:
            if self.AD112func() >= 10:
                return "****"
            else:
                if self.AD112func() >= 9:
                    return "***"
                else:
                    if self.AD112func() >= 8:
                        return "**"
                    else:
                        return "*"

    # Cricket
    def AH105func(self):
        return self.AC35func()
        
    def AD113func(self):
        return (self.AF107func() + self.AF104func() +self.AH104func() + self.AF105func() + self.AH105func()) / 5
        
    #=IF(AD112>=11%,"*****",IF(AD112>=10%,"****",IF(AD112>=9%,"***",IF(AD112>=8%,"**","*"))))
    def AC113func(self):
        if self.AD113func() >= 11:
            return "*****"
        else:
            if self.AD113func() >= 10:
                return "****"
            else:
                if self.AD113func() >= 9:
                    return "***"
                else:
                    if self.AD113func() >= 8:
                        return "**"
                    else:
                        return "*"

    # Tennis
    def AD114func(self):
        return (self.AF105func() + self.AH105func() +self.AF107func()) / 3
        
    #=IF(AD114>=11%,"*****",IF(AD114>=10%,"****",IF(AD114>=9%,"***",IF(AD114>=8%,"**","*"))))
    def AC114func(self):
        if self.AD114func() >= 11:
            return "*****"
        else:
            if self.AD114func() >= 10:
                return "****"
            else:
                if self.AD114func() >= 9:
                    return "***"
                else:
                    if self.AD114func() >= 8:
                        return "**"
                    else:
                        return "*"

    # Snooker
    def AD115func(self):
        return (self.AF105func() + self.AH104func() +self.AF107func() + self.AF104func()) / 4
        
    #=IF(AD115>=11%,"*****",IF(AD115>=10%,"****",IF(AD115>=9%,"***",IF(AD115>=8%,"**","*"))))
    def AC115func(self):
        if self.AD115func() >= 11:
            return "*****"
        else:
            if self.AD115func() >= 10:
                return "****"
            else:
                if self.AD115func() >= 9:
                    return "***"
                else:
                    if self.AD115func() >= 8:
                        return "**"
                    else:
                        return "*"

    # Army
    def AD116func(self):
        return (self.AH104func() + self.AH107func() + self.AF105func()) / 3
        
    #=IF(AD116>=11%,"*****",IF(AD116>=10%,"****",IF(AD116>=9%,"***",IF(AD116>=8%,"**","*"))))
    def AC116func(self):
        if self.AD116func() >= 11:
            return "*****"
        else:
            if self.AD116func() >= 10:
                return "****"
            else:
                if self.AD116func() >= 9:
                    return "***"
                else:
                    if self.AD116func() >= 8:
                        return "**"
                    else:
                        return "*"

    # Police
    def AD117func(self):
        return (self.AF105func() + self.AH104func() + self.AH106func() + self.AF103func()) / 4
        
    #=IF(AD117>=11%,"*****",IF(AD117>=10%,"****",IF(AD117>=9%,"***",IF(AD117>=8%,"**","*"))))
    def AC117func(self):
        if self.AD117func() >= 11:
            return "*****"
        else:
            if self.AD117func() >= 10:
                return "****"
            else:
                if self.AD117func() >= 9:
                    return "***"
                else:
                    if self.AD117func() >= 8:
                        return "**"
                    else:
                        return "*"

    # Fire Brigade Officer
    def AD118func(self):
        return (self.AF105func() + self.AF107func() + self.AH104func()) / 3
        
    #=IF(AD118>=11%,"*****",IF(AD118>=10%,"****",IF(AD118>=9%,"***",IF(AD118>=8%,"**","*"))))
    def AC118func(self):
        if self.AD118func() >= 11:
            return "*****"
        else:
            if self.AD118func() >= 10:
                return "****"
            else:
                if self.AD118func() >= 9:
                    return "***"
                else:
                    if self.AD118func() >= 8:
                        return "**"
                    else:
                        return "*"

    # Fire Brigade Officer
    def AD119func(self):
        return (self.AF105func() + self.AF103func() + self.AH103func() + self.AH106func()) / 4
        
    #=IF(AD119>=11%,"*****",IF(AD119>=10%,"****",IF(AD119>=9%,"***",IF(AD119>=8%,"**","*"))))
    def AC119func(self):
        if self.AD119func() >= 11:
            return "*****"
        else:
            if self.AD119func() >= 10:
                return "****"
            else:
                if self.AD119func() >= 9:
                    return "***"
                else:
                    if self.AD119func() >= 8:
                        return "**"
                    else:
                        return "*"

    # Athelete
    def AD120func(self):
        return (self.AF105func() + self.AH105func() + self.AF107func()) / 3
        
    #=IF(AD120>=11%,"*****",IF(AD120>=10%,"****",IF(AD120>=9%,"***",IF(AD120>=8%,"**","*"))))
    def AC120func(self):
        if self.AD120func() >= 11:
            return "*****"
        else:
            if self.AD120func() >= 10:
                return "****"
            else:
                if self.AD120func() >= 9:
                    return "***"
                else:
                    if self.AD120func() >= 8:
                        return "**"
                    else:
                        return "*"

    #### LifeTime
    def P45func(self):
        return self.AC33func() + self.AA36func()

    def P47func(self):
        #=AA36/P45
        return (self.AA36func() / self.P45func()) * 100

    def Q44func(self):
        return (self.AC34func() + self.AC36func()) / 2

    def R44func(self):
        return self.AC34func()

    def S44func(self):    
        # // =(AC34+AA34+AA37)/3
        return (self.AC34func() + self.AA34func() + self.AA37func()) / 3

    def R45func(self):
        return self.Q44func() + self.R44func() + self.S44func()

    def Q47func(self):
        return (self.Q44func() / self.R45func()) * 100

    def R47func(self):  
        # //=R44/R45
        return (self.R44func() / self.R45func()) * 100

    def S47func(self):  
        # //=S44/R45
        return (self.S44func() / self.R45func()) * 100

    def V44func(self): 
        # //(AA35+AC35)/2
        return (self.AA35func() + self.AC35func()) / 2

    def W44func(self):
        return self.AC36func()

    def X44func(self): 
        # //=(AC36+AC35)/2
        return (self.AC36func() + self.AC35func()) / 2

    def W45func(self): 
        # //V44+W44+X44
        return self.V44func() + self.W44func() + self.X44func()

    def V47func(self): 
        # //V44/W45
        return (self.V44func() / self.W45func()) * 100

    def AG41func(self):
        #=D33+D35+D37+D39+D41+D43+D45+D47+D49+D51
        return self.D33func() + self.D35func() + self.D37func() + self.D39func() + self.D41func() + self.D43func() + self.D45func() + self.D47func() + self.D49func() + self.D51func()

    def W47func(self): 
        # //=W44/W45
        return  (self.W44func() / self.W45func()) * 100

    def X47func(self): 
        # //X44/W45
        return (self.X44func() / self.W45func()) * 100

    def Y44func(self):  
        # //(AC37+AA37)/2
        return (self.AC37func() + self.AA37func()) / 2

    def Z44func(self):
        return self.AC37func()

    def Z45func(self): 
        # //Y44+Z44
        return self.Y44func() + self.Z44func()

    def Y47func(self): 
        # //=Y44/Z45
        return (self.Y44func() / self.Z45func()) * 100

    def Z47func(self): 
        # //Z44/Z45
        return (self.Z44func() / self.Z45func()) * 100

    def AA44func(self):  
        # //(AA33+AC36)/2
        return (self.AA33func() + self.AC36func()) / 2

    def AB44func(self):  
        # //=(AC33+AA33)/2
        return (self.AC33func() + self.AA33func()) / 2

    def AB45func(self): 
        # //AA44+AB44
        return self.AA44func() + self.AB44func()

    def AA47func(self):  
        # //AA44/AB45
        return (self.AA44func() / self.AB45func()) * 100

    def AB47func(self):  
        # //AB44/AB45
        return (self.AB44func() / self.AB45func()) * 100

    def AC44func(self):
        # =(AA34+AA37)/2
        return (self.AA34func() + self.AA37func()) / 2

    def AD44func(self):
        # =(AA34+AC33)/2
        return (self.AA34func() + self.AC33func()) / 2

    def AD45func(self):
        # =AC44+AD44
        return self.AC44func() + self.AD44func()

    def AC47func(self):
        # =AC44/AD45
        return (self.AC44func() / self.AD45func()) * 100

    def AD47func(self):
        # =AD44/AD45
        return (self.AD44func() / self.AD45func()) * 100

    def AE44func(self):  
        #=(AC36+AA36)/2
        return (self.AC36func() + self.AA36func()) / 2

    def AG44func(self): 
        # //=(AA36+AC33)/2
        return (self.AA36func() + self.AC33func()) / 2

    def AF44func(self): 
        # //=(AA36+AC34)/2
        return (self.AA36func() + self.AC34func()) / 2

    def AG45func(self): 
        #  //AE44+AF44+AG44
        return self.AE44func() + self.AF44func() + self.AG44func()

    def AE47func(self): 
        # //AE44/AG45
        return (self.AE44func() / self.AG45func()) * 100

    def AF47func(self): 
        #  //AF44/AG45
        return (self.AF44func() / self.AG45func()) * 100

    def AG47func(self):  
    # =AG44/AG45
        return (self.AG44func() / self.AG45func()) * 100

    def AH44func(self):
        return self.AA37func()

    def AI44func(self):  
        # //(AA37+AC34)/2
        return (self.AA37func() + self.AC34func()) / 2

    def AI45func(self):  
        # //=AH44+AI44
        return self.AH44func() + self.AI44func()

    def AH47func(self): 
        # //AH44/AI45
        return (self.AH44func() / self.AI45func()) * 100

    def AI47func(self):  
        # //AI44/AI45
        return (self.AI44func() / self.AI45func()) * 100

    # Intrapersonal
    def AE29func(self):
        return (self.AA33func() + self.AA36func() + self.AC33func() + self.AC34func() + self.AC36func() + self.AC37func() + (self.AA34func() + self.AA37func()) / 2 + (self.AA35func() + self.AC35func()) / 2)

    #Intrapersonal Intelligence
    def AH31func(self):
        # =AC33/AE29
        return (self.AC33func() / self.AE29func()) * 100
    
    #Planning, Intuitive, judgement & Execution
    def O47func(self):
        #=AC33/P45
        return (self.AC33func() / self.P45func()) * 100

        # LIFETIME (25)
    def AI31func(self):
        return (self.AC34func() / self.AE29func()) * 100

        # Lifetime(27)
    def AJ31func(self): 
        #  //AC36/AE29
        return (self.AC36func() / self.AE29func()) * 100

    # Lifetime (29)
    def AK31func(self): 
        # //=AC37/AE29
        return (self.AC37func() / self.AE29func()) * 100

    def AD31func(self): 
        # //AA33/AE29
        return (self.AA33func() / self.AE29func()) * 100

    def AE31func(self):  
        # //((AA34+AA37)/2)/AE29
        return (((self.AA34func() + self.AA37func()) / 2) / self.AE29func()) * 100

    def AG31func(self): 
        # //AA36/AE29
        return (self.AA36func() / self.AE29func()) * 100

    def Z41func(self):
        # =AA33+AC33
        return (self.AA33func() + self.AC33func())    

    def AA41func(self):
        #=AA34+AC34
        return (self.AA34func() + self.AC34func())

    def AB41func(self):
        #=AA35+AC35
        return (self.AA35func() + self.AC35func())

    def AC41func(self):
        #=AA36+AC36
        return (self.AA36func() + self.AC36func())

    def AD41func(self):
        #=AA37+AC37
        return (self.AA37func() + self.AC37func())

    def AF31func(self):  
        # //((AA35+AC35)/2)/AE29
        return (((self.AA35func() + self.AC35func()) / 2) / self.AE29func()) * 100

    def T44func(self):
        return self.AC35func()

    def U45func(self):  
        # //AA35+AC35
        return self.AA35func() + self.AC35func()

    def T47func(self):  
        # //=T44/U45
        return  (self.T44func() / self.U45func()) * 100

    def U44func(self):
        return self.AA35func()

    def U47func(self):
        #  //U44/U45
        return (self.U44func() / self.U45func()) * 100
    
    def AF53func(self):
        return (self.AC34func() + self.AC36func() + self.AC37func()) / 3

    def AG53func(self):
        #=(AC34+AC36)/2
        return (self.AC34func() + self.AC36func()) / 2

    def Y38func(self):
        return 0

    def AH53func(self):
        #=(AA36+AC36+Y38+AC35+AA37+AA34)/6
        return (self.AA36func() + self.AC36func() + self.Y38func() + self.AC35func() + self.AA37func() + self.AA34func()) / 6

    def AI53func(self):  
        # //=SUM(AF53:AH53)
        return (self.AF53func() + self.AG53func() + self.AH53func())    

    def AF52func(self):  
        # //=AF53/AI53
        return (self.AF53func() / self.AI53func()) * 100

        #stream selection(commerce)
    def AG52func(self):  
        # //=AG53/AI53
        return (self.AG53func() / self.AI53func()) * 100

    #stream selection(arts)
    def AH52func(self):  
        #  //=AH53/AI53
        return (self.AH53func() / self.AI53func()) * 100

    #Pathology Researcher   
    def AH150func(self):
        return self.AC35func()

    def AD134func(self):
        #=(AH152+AH149+AH150)/3
        return (self.AH152func()  + self.AH149func() + self.AH150func()) / 3

    def AC134func(self):
        if self.AD134func() >= 11:
            return "*****"
        else:
            if self.AD134func() >= 10:
                return "****"
            else:
                if self.AD134func() >= 9:
                    return "***"
                else:
                    if self.AD134func() >=8:
                        return "**"
                    else:
                        return "*"

    #veterinary doctor
    def AD135func(self):
        #=(AH152+AH150+AH149)/3
        return (self.AH152func() + self.AH150func() + self.AH149func()) / 3

    def AC135func(self):
        if self.AD135func() >= 11:
            return "*****"
        else:
            if self.AD135func() >= 10:
                return "****"
            else:
                if self.AD135func() >= 9:
                    return "***"
                else:
                    if self.AD135func() >=8:
                        return "**"
                    else:
                        return "*"

    #animal and plant researcher
    def AD136func(self):
        #(AH152+AH149)/2
        return (self.AH152func() + self.AH149func()) / 2

    def AC136func(self):
        if self.AD136func() >= 11:
            return "*****"
        else:
            if self.AD136func() >= 10:
                return "****"
            else:
                if self.AD136func() >= 9:
                    return "***"
                else:
                    if self.AD136func() >=8:
                        return "**"
                    else:
                        return "*"

    # Map Designer
    def AF149func(self):
        return self.AA34func()

    def AD137func(self):
        #(AH152+AH149)/2
        return (self.AF152func() + self.AF149func() + self.AH149func()) / 3
        
    def AC137func(self):
        # =IF(AD137>=11%,"*****",IF(AD137>=10%,"****",IF(AD137>=9%,"***",IF(AD137>=8%,"**","*"))))
        if self.AD137func() >= 11:
            return "*****"
        else:
            if self.AD137func() >= 10:
                return "****"
            else:
                if self.AD137func() >= 9:
                    return "***"
                else:
                    if self.AD137func() >=8:
                        return "**"
                    else:
                        return "*"

        #interior designer AC1710 
    def AD138func(self):
        #=(AF149+AF152+AH149)/3
        return (self.AF149func() + self.AF152func() + self.AH149func()) / 3

    #=IF(AD138>=11%,"*****",IF(AD138>=10%,"****",IF(AD138>=9%,"***",IF(AD138>=8%,"**","*"))))
    def AC138func(self):
        if self.AD138func() >= 11:
            return "*****"
        else:
            if self.AD138func() >= 10:
                return "****"
            else:
                if self.AD138func() >= 9:
                    return "***"
                else:
                    if self.AD138func() >= 8:
                        return "**"
                    else:
                        return "*"

    #car / bike designer AS1713
    def AD139func(self):
        #=(AF152+AF149+AH150)/3
        return (self.AF152func() + self.AF149func() + self.AH150func()) / 3

    #   IF(AD139>=11%,"*****",IF(AD139>=10%,"****",IF(AD139>=9%,"***",IF(AD139>=8%,"**","*"))))                     
    def AC139func(self):
        if self.AD139func() >= 11:
            return "*****"
        else:
            if self.AD139func() >= 10:
                return "****"
            else:
                if self.AD139func() >= 9:
                    return "***"
                else:
                    if self.AD139func() >= 8:
                        return "**"
                    else:
                        return "*"

    #Wedding planner AS1716
    def AF150func(self):
        return (self.AA35func())

    def AD140func(self):
        #(AF149+AF152+AF150)/3
        return (self.AF149func() + self.AF152func() + self.AF150func()) / 3

    #IF(AD140>=11%,"*****",IF(AD140>=10%,"****",IF(AD140>=9%,"***",IF(AD140>=8%,"**","*"))))
    def AC140func(self):
        if self.AD140func() >= 11:
            return "*****"
        else:
            if self.AD140func() >= 10:
                return "****"
            else:
                if self.AD140func() >= 9:
                    return "***"
                else:
                    if self.AD140func() >= 8:
                        return "**"
                    else:
                        return "*"

    #35 Geo-science
    def AD141func(self):
        #=(AH152+AH149)/2
        return (self.AH152func() + self.AH149func()) / 2

    def AC141func(self):
        if self.AD141func() >= 11:
            return "*****" 
        else:
            if self.AD141func() >= 10:
                return "****"
            else:
                if self.AD141func() >= 9:
                    return "***"
                else:
                    if self.AD141func() >= 8:
                        return "**"
                    else:
                        return "*"

    #Archeologist AS1726
    def AD142func(self):
        #(AH152+AH149+AF150)/3
        return (self.AH152func() + self.AH149func() + self.AF150func()) / 3

    def AC142func(self):
        #F(AD142>=11%,"*****",IF(AD142>=10%,"****",IF(AD142>=9%,"***",IF(AD142>=8%,"**","*"))))
        if self.AD142func() >= 11:
            return "*****"
        else:
            if self.AD142func() >= 10:
                return "****"
            else:
                if self.AD142func() >= 9:
                    return "***"
                else:
                    if self.AD142func() >= 8:
                        return "**"
                    else:
                        return "*"

    #Water Harvest AS1729
    def AD143func(self):
        #=(AH152+AH149)/2
        return (self.AH152func() + self.AH149func()) / 2

    def AC143func(self):
        #=IF(AD143>=11%,"*****",IF(AD143>=10%,"****",IF(AD143>=9%,"***",IF(AD143>=8%,"**","*"))))
        if self.AD143func() >= 11:
            return "*****"
        else:
            if self.AD143func() >= 10:
                return "****"
            else:
                if self.AD143func() >= 9:
                    return "***"
                else:
                    if self.AD143func() >= 8:
                        return "**"
                    else:
                        return "*"

    #Forest officer AS1732
    def AD144func(self):
        #(AH152+AF150)/2
        return (self.AH152func() + self.AF150func()) / 2

    def AC144func(self):
        #=IF(AD144>=11%,"*****",IF(AD144>=10%,"****",IF(AD144>=9%,"***",IF(AD144>=8%,"**","*"))))
        if self.AD144func() >= 11:
            return "*****"
        else:
            if self.AD144func() >= 10:
                return "****"
            else:
                if self.AD144func() >= 9:
                    return "***"
                else:
                    if self.AD144func() >= 8:
                        return "**"
                    else:
                        return "*"

    #pg36 Financial Planner AS1760
    def AD145func(self):
        return self.AH149func()

    def AC145func(self):
        #=IF(AD145>=11%,"*****",IF(AD145>=10%,"****",IF(AD145>=9%,"***",IF(AD145>=8%,"**","*"))))
        if self.AD145func() >= 11:
            return "*****"
        else:
            if self.AD145func() >= 10:
                return "****"
            else:
                if self.AD145func() >= 9:
                    return "***"
                else:
                    if self.AD145func() >= 8:
                        return "**"
                    else:
                        return "*"

    #Tax consultant AS1763
    def AH151func(self):
        return self.AC36func()

    def AD146func(self):
        #=(AH149+AF148+AH151)/3
        return (self.AH149func() + self.AF148func() + self.AH151func()) / 3

    def AC146func(self):
        #=IF(AD146>=11%,"*****",IF(AD146>=10%,"****",IF(AD146>=9%,"***",IF(AD146>=8%,"**","*"))))
        if self.AD146func() >= 11:
            return "*****"
        else:
            if self.AD146func() >= 10:
                return "****"
            else:
                if self.AD146func() >= 9:
                    return "***"
                else:
                    if self.AD146func() >= 8:
                        return "**"
                    else:
                        return "*"

    #equity researcher AS1766
    def AD147func(self):
        #=(AH149+AH152)/2
        return (self.AH149func() + self.AH152func()) / 2

    def AC147func(self):
        #=IF(AD147>=11%,"*****",IF(AD147>=10%,"****",IF(AD147>=9%,"***",IF(AD147>=8%,"**","*"))))
        if self.AD147func() >= 11:
            return "*****"
        else:
            if self.AD147func() >= 10:
                return "****"
            else:
                if self.AD147func() >= 9:
                    return "***"
                else:
                    if self.AD147func() >= 8:
                        return "**"
                    else:
                        return "*"

    #Bank Teller AS1769
    def AD148func(self):
        #(AH149+AF148+AH151)/3
        return (self.AH149func() + self.AF148func() + self.AH151func()) / 3    

    def AC148func(self):
        #=IF(AD148>=11%,"*****",IF(AD148>=10%,"****",IF(AD148>=9%,"***",IF(AD148>=8%,"**","*"))))
        if self.AD148func() >= 11:
            return "*****"
        else:
            if self.AD148func() >= 10:
                return "****"
            else:
                if self.AD148func() >= 9:
                    return "***"
                else:
                    if self.AD148func() >= 8:
                        return "**"
                    else:
                        return "*"

    # masss media >> News reader AS1775
    def AD110func(self):
        #=(AH106+AF107+AH107)/3
        return (self.AH106func() + self.AF107func() + self.AH107func()) / 3

    def AD149func(self):
        return self.AD110func()

    def AC149func(self):
        ##=IF(AD149>=11%,"*****",IF(AD149>=10%,"****",IF(AD149>=9%,"***",IF(AD149>=8%,"**","*"))))
        if self.AD149func() >= 11:
            return "*****"
        else:
            if self.AD149func() >= 10:
                return "****"
            else:
                if self.AD149func() >= 9:
                    return "***"
                else:
                    if self.AD149func() >= 8:
                        return "**"
                    else:
                        return "*"

    #Poet AS1778
    def AD150func(self):
        #=(AF149+AH151)/2
        return (self.AF149func() + self.AH151func()) / 2

    def AC150func(self):
        #=IF(AD150>=11%,"*****",IF(AD150>=10%,"****",IF(AD150>=9%,"***",IF(AD150>=8%,"**","*"))))
        if self.AD150func() >= 11:
            return "*****"
        else:
            if self.AD150func() >= 10:
                return "****"
            else:
                if self.AD150func() >= 9:
                    return "***"
                else:
                    if self.AD150func() >= 8:
                        return "**"
                    else:
                        return "*"

    #Journalist AS1781
    def AD151func(self):
        #=(AH151+AH149+AF150+AF148)/4
        return (self.AH151func() + self.AH149func() + self.AF150func() + self.AF148func()) / 4

    def AC151func(self):
        #IF(AD151>=11%,"*****",IF(AD151>=10%,"****",IF(AD151>=9%,"***",IF(AD151>=8%,"**","*"))))
        if self.AD151func() >= 11:
            return "*****"
        else:
            if self.AD151func() >= 10:
                return "****"
            else:
                if self.AD151func() >= 9:
                    return "***"
                else:
                    if self.AD151func() >= 8:
                        return "**"
                    else:
                        return "*"

    #Public Relation officer AS1784    
    def AD152func(self):
        #=(AF148+AH151)/2
        return (self.AF148func() + self.AH151func()) / 2

    def AC152func(self):
        #IF(AD152>=11%,"*****",IF(AD152>=10%,"****",IF(AD152>=9%,"***",IF(AD152>=8%,"**","*"))))
        if self.AD152func() >= 11:
            return "*****"
        else:
            if self.AD152func() >= 10:
                return "****"
            else:
                if self.AD152func() >= 9:
                    return "***"
                else:
                    if self.AD152func() >= 8:
                        return "**"
                    else:
                        return "*"

    # pg 137 poet AS1812
    def AD153func(self):
        return self.AD150func()

    def AC153func(self):
        #=IF(AD153>=11%,"*****",IF(AD153>=10%,"****",IF(AD153>=9%,"***",IF(AD153>=8%,"**","*"))))
        if self.AD153func() >= 11:
            return "*****"
        else:
            if self.AD153func() >= 10:
                return "****"
            else:
                if self.AD153func() >= 9:
                    return "***"
                else:
                    if self.AD153func() >= 8:
                        return "**"
                    else:
                        return "*"

    #Grammer expert AS115
    def AD154func(self):
        #=(AH149+AH151+AH152)/3
        return (self.AH149func() + self.AH151func() + self.AH152func()) / 3

    def AC154func(self):
        if self.AD154func() >= 11:
            return "*****"
        else:
            if self.AD154func() >= 10:
                return "****"
            else:
                if self.AD154func() >= 9:
                    return "***"
                else:
                    if self.AD154func() >=8:
                        return "**"
                    else:
                        return "*"

    #Physicist AS1822
    def AD155func(self):
        #=(AH152+AH149)/2
        return (self.AH152func() + self.AH149func()) / 2

    def AC155func(self):
        ##=IF(AD155>=11%,"*****",IF(AD155>=10%,"****",IF(AD155>=9%,"***",IF(AD155>=8%,"**","*"))))
        if self.AD155func() >= 11:
            return "*****"
        else:
            if self.AD155func() >= 10:
                return "****"
            else:
                if self.AD155func() >= 9:
                    return "***"
                else:
                    if self.AD155func() >= 8:
                        return "**"
                    else:
                        return "*"

    #Buiness Analyst AS1825
    def AD156func(self):
        #=(AH149+AH151)/2
        return (self.AH149func() + self.AH151func()) / 2

    def AC156func(self):
        #IF(AD156>=11%,"*****",IF(AD156>=10%,"****",IF(AD156>=9%,"***",IF(AD156>=8%,"**","*"))))
        if self.AD156func() >= 11:
            return "*****"
        else:
            if self.AD156func() >= 10:
                return "****"
            else:
                if self.AD156func() >= 9:
                    return "***"
                else:
                    if self.AD156func() >= 8:
                        return "**"
                    else:
                        return "*"

    #Statistician AS1828
    def AD157func(self):
        #=(AH149+AH152)/2
        return (self.AH149func() + self.AH152func()) / 2

    def AC157func(self):
        #IF(AD157>=11%,"*****",IF(AD157>=10%,"****",IF(AD157>=9%,"***",IF(AD157>=8%,"**","*"))))
        if self.AD157func() >= 11:
            return "*****"
        else:
            if self.AD157func() >= 10:
                return "****"
            else:
                if self.AD157func() >= 9:
                    return "***"
                else:
                    if self.AD157func() >= 8:
                        return "**"
                    else:
                        return "*"

    #Economist AS1831
    def AD158func(self):
        return self.AH149func()

    def AC158func(self):
        #IF(AD158>=11%,"*****",IF(AD158>=10%,"****",IF(AD158>=9%,"***",IF(AD158>=8%,"**","*"))))
        if self.AD158func() >= 11:
            return "*****"
        else:
            if self.AD158func() >= 10:
                return "****"
            else:
                if self.AD158func() >= 9:
                    return "***"
                else:
                    if self.AD158func() >= 8:
                        return "**"
                    else:
                        return "*"

    #Company secratary AS1834
    def AD159func(self):
        #=(AH149+AF148+AH151)/3
        return (self.AH149func() + self.AF148func() + self.AH151func()) / 3 

    def AC159func(self):
        #IF(AD159>=11%,"*****",IF(AD159>=10%,"****",IF(AD159>=9%,"***",IF(AD158>=8%,"**","*"))))
        if self.AD159func() >= 11:
            return "*****"
        else:
            if self.AD159func() >= 10:
                return "****"
            else:
                if self.AD159func() >= 9:
                    return "***"
                else:
                    if self.AD159func() >= 8:
                        return "**"
                    else:
                        return "*"

    # pg 37 Marketing management AS1865
    def AD160func(self):
        #=(AF152+AF149+AH149+AH152)/4
        return (self.AF152func() + self.AF149func() + self.AH152func() + self.AH149func()) / 4

    def AC160func(self):
        #IF(AD160>=11%,"*****",IF(AD160>=10%,"****",IF(AD160>=9%,"***",IF(AD160>=8%,"**","*"))))
        if self.AD160func() >= 11:
            return "*****"
        else:
            if self.AD160func() >= 10:
                return "****"
            else:
                if self.AD160func() >= 9:
                    return "***"
                else:
                    if self.AD160func() >= 8:
                        return "**"
                    else:
                        return "*"

    #production management  AS1868
    def AD161func(self):
        #=(AF148+AH149+AF150)/3
        return (self.AF148func() + self.AH149func() + self.AF150func()) / 3

    def AC161func(self):
        #IF(AD161>=11%,"*****",IF(AD161>=10%,"****",IF(AD161>=9%,"***",IF(AD161>=8%,"**","*"))))
        if self.AD161func() >= 11:
            return "*****"
        else:
            if self.AD161func() >= 10:
                return "****"
            else:
                if self.AD161func() >= 9:
                    return "***"
                else:
                    if self.AD161func() >= 8:
                        return "**"
                    else:
                        return "*"

    #Sales Management AS1871
    def AH148func(self):
        return self.AC33func()

    def AD162func(self):
        #=(AF148+AH148+AH151)/3
        return (self.AF148func() + self.AH148func() + self.AH151func()) / 3

    def AC162func(self):
        ##IF(AD162>=11%,"*****",IF(AD162>=10%,"****",IF(AD162>=9%,"***",IF(AD162>=8%,"**","*"))))
        if self.AD162func() >= 11:
            return "*****"
        else:
            if self.AD162func() >= 10:
                return "****"
            else:
                if self.AD162func() >= 9:
                    return "***"
                else:
                    if self.AD162func() >=8:
                        return "**"
                    else:
                        return "*"

    #IAS/IPS AS1878
    def AD163func(self):
        #=(AH149+AH151)/2
        return (self.AH149func() + self.AH151func()) / 2

    def AC163func(self):
        ##IF(AD163>=11%,"*****",IF(AD163>=10%,"****",IF(AD163>=9%,"***",IF(AD163>=8%,"**","*"))))
        if self.AD163func() >= 11:
            return "*****"
        else:
            if self.AD163func() >= 10:
                return "****"
            else:
                if self.AD163func() >= 9:
                    return "***"
                else:
                    if self.AD163func() >= 8:
                        return "**"
                    else:
                        return "*"

    #Teacher/Professor AS1881
    def AD164func(self):
        #=(AH151+AH149+AF148)/3
        return (self.AH151func() + self.AH149func() + self.AF148func()) / 3

    def AC164func(self):
        ##IF(AD164>=11%,"*****",IF(AD164>=10%,"****",IF(AD164>=9%,"***",IF(AD164>=8%,"**","*"))))
        if self.AD164func() >= 11:
            return "*****"
        else:
            if self.AD164func() >= 10:
                return "****"
            else:
                if self.AD164func() >= 9:
                    return "***"
                else:
                    if self.AD164func() >= 8:
                        return "**"
                    else:
                        return "*"                        

    #Administration AS1884
    def AD165func(self):
        #=(AF148+AH151+AH148)/3
        return (self.AF148func() + self.AH151func() + self.AH148func()) / 3

    def AC165func(self):
        ##IF(AD165>=11%,"*****",IF(AD165>=10%,"****",IF(AD165>=9%,"***",IF(AD165>=8%,"**","*"))))
        if self.AD165func() >= 11:
            return "*****"
        else:
            if self.AD165func() >= 10:
                return "****"
            else:
                if self.AD165func() >= 9:
                    return "***"
                else:
                    if self.AD165func() >= 8:
                        return "**"
                    else:
                        return "*"

    #Counselor AS1887
    def AD166func(self):
        #=(AF148+AH148+AF151+AH151+AH149)/5
        return (self.AF148func() + self.AH148func() + self.AF151func() + self.AH149func() + self.AH151func()) / 5

    def AC166func(self):
        #IF(AD166>=11%,"*****",IF(AD166>=10%,"****",IF(AD166>=9%,"***",IF(AD166=8%,"**","*"))))
        if self.AD166func() >= 11:
            return "*****"
        else:
            if self.AD166func() >= 10:
                return "****"
            else:
                if self.AD166func() >= 9:
                    return "***"
                else:
                    if self.AD166func() >= 8:
                        return "**"
                    else:
                        return "*"

    ##pg 39
    #Marriage counselor AS1918
    def AD167func(self):
        return self.AD166func()

    def AC167func(self):
        #IF(AD167>=11%,"*****",IF(AD167>=10%,"****",IF(AD167>=9%,"***",IF(AD167>=8%,"**","*"))))
        if self.AD167func() >= 11:
            return "*****"
        else:
            if self.AD167func() >= 10:
                return "****"
            else:
                if self.AD167func() >= 9:
                    return "***"
                else:
                    if self.AD167func() >= 8:
                        return "**"
                    else:
                        return "*"

    #Parenting Counselor AS1921
    def AD168func(self):
        return self.AD167func()

    def AC168func(self):
        #IF(AD168>=11%,"*****",IF(AD167>=10%,"****",IF(AD167>=9%,"***",IF(AD167>=8%,"**","*"))))
        if self.AD168func() >= 11:
            return "*****"
        else:
            if self.AD168func() >= 10:
                return "****"
            else:
                if self.AD168func() >= 9:
                    return "***"
                else:
                    if self.AD168func() >= 8:
                        return "**"
                    else:
                        return "*"

    #Spirutual behaviour AS1924 
    def AF171func(self):
        return self.AA33func()

    def AH171func(self):
        return self.AC33func()

    def AH174func(self):
            return self.AC36func()

    def AD169func(self):
        #=(AF171+AH171+AH174)/3
        return (self.AF171func() + self.AH171func() + self.AH174func()) / 3

    def AC169func(self):
        #IF(AD169>=11%,"*****",IF(AD169>=10%,"****",IF(AD169>=9%,"***",IF(AD169>=8%,"**","*"))))
        if self.AD169func() >= 11:
            return "*****"
        else:
            if self.AD169func() >= 10:
                return "****"
            else:
                if self.AD169func() >= 9:
                    return "***"
                else:
                    if self.AD169func() >= 8:
                        return "**"
                    else:
                        return "*"                    

    #Language Teacher AS1931
    def AD170func(self):
        #=(AH174+AF171)/2
        return (self.AH174func() + self.AF171func()) / 2

    def AC170func(self):
        #IF(AD170>=11%,"*****",IF(AD170>=10%,"****",IF(AD170>=9%,"***",IF(AD170>=8%,"**","*"))))
        if self.AD170func() >= 11:
            return "*****"
        else:
            if self.AD170func() >= 10:
                return "****"
            else:
                if self.AD170func() >= 9:
                    return "***"
                else:
                    if self.AD170func() >= 8:
                        return "**"
                    else:
                        return "*"

    #Grammar expert AS1934
    def AH172func(self):
        return (self.AC34func())

    def AD171func(self):
        #=(AH172+AH174)/2
        return (self.AH172func() + self.AH174func()) / 2

    def AC171func(self):
        #IF(AD171>=11%,"*****",IF(AD171>=10%,"****",IF(AD171>=9%,"***",IF(AD171>=8%,"**","*"))))
        if self.AD171func() >= 11:
            return "*****"
        else:
            if self.AD171func() >= 10:
                return "****"
            else:
                if self.AD171func() >= 9:
                    return "***"
                else:
                    if self.AD171func() >= 8:
                        return "**"
                    else:
                        return "*"

    #Anchor AS1937
    def AD172func(self):
        #=(AF171+AH174)/2
        return (self.AF171func() + self.AH174func()) / 2 

    def AC172func(self):
        #IF(AD172>=11%,"*****",IF(AD172>=10%,"****",IF(AD172>=9%,"***",IF(AD172>=8%,"**","*"))))
        if self.AD172func() >= 11:
            return "*****"
        else:
            if self.AD172func() >= 10:
                return "****"
            else:
                if self.AD172func() >= 9:
                    return "***"
                else:
                    if self.AD172func() >= 8:
                        return "**"
                    else:
                        return "*"

    #Motivational Speaker AS1940
    def AD173func(self):
        #=(AH174+AH171+AF171)/3
        return (self.AH174func() + self.AH171func() + self.AF171func()) / 3

    def AC173func(self):
        #IF(AD173>=11%,"*****",IF(AD173>=10%,"****",IF(AD173>=9%,"***",IF(AD173>=8%,"**","*"))))
        if self.AD173func() >= 11:
            return "*****"
        else:
            if self.AD173func() >= 10:
                return "****"
            else:
                if self.AD173func() >= 9:
                    return "***"
                else:
                    if self.AD173func() >= 8:
                        return "**"
                    else:
                        return "*"

    #Speech Therapist AS1943
    def AD174func(self):
        #=(AF171+AH174)/4
        return (self.AF171func() + self.AH174func()) / 4

    def AC174func(self):
        #IF(AD174>=11%,"*****",IF(AD174>=10%,"****",IF(AD174>=9%,"***",IF(AD174>=8%,"**","*"))))
        if self.AD174func() >= 11:
            return "*****"
        else:
            if self.AD174func() >= 10:
                return "****"
            else:
                if self.AD174func() >= 9:
                    return "***"
                else:
                    if self.AD174func() >= 8:
                        return "**"
                    else:
                        return "*"

    #pg 40
    #Football AS1971
    def AF173func(self):
        #=AA35
        return self.AA35func()

    def AF172func(self):
        return self.AA34func()

    def AF175func(self):
        return self.AA37func()

    def AD175func(self):
        #=(AF173+AF175+AF172+AH172)/4
        return (self.AF173func() + self.AF172func() + self.AH172func() + self.AF175func()) / 4

    def AC175func(self):
        #IF(AD175>=11%,"*****",IF(AD175>=10%,"****",IF(AD175>=9%,"***",IF(AD175>=8%,"**","*"))))
        if self.AD175func() >= 11:
            return "*****"
        else:
            if self.AD175func() >= 10:
                return "****"
            else:
                if self.AD175func() >= 9:
                    return "***"
                else:
                    if self.AD175func() >= 8:
                        return "**"
                    else:
                        return "*"

    #Swimming AS1974
    def AD176func(self):
        #=(AF173+AF175)/2
        return (self.AF173func() + self.AF175func()) / 2

    def AC176func(self):
        if self.AD176func() >= 11:
            return "*****"
        else:
            if self.AD176func() >= 10:
                return "****"
            else:
                if self.AD176func() >= 9:
                    return "***"
                else:
                    if self.AD176func() >= 8:
                        return "**"
                    else:
                        return "*"

    #Carrom AS1977
    def AH173func(self):
        return self.AC35func()

    def AD177func(self):
        #=(AF172+AH173+AH172)/3
        return (self.AF172func() + self.AH173func() + self.AH172func()) / 3

    def AC177func(self):
        if self.AD177func() >= 11:
            return "*****"
        else:
            if self.AD177func() >= 10:
                return "****"
            else:
                if self.AD177func() >= 9:
                    return "***"
                else:
                    if self.AD177func() >= 8:
                        return "**"
                    else:
                        return "*"

    #Air Force AS1984
    def AD178func(self):
        #=(AF173+AF172+AF175+AH172)/4
        return (self.AF173func() + self.AF172func() + self.AF175func() + self.AH172func()) / 4

    def AC178func(self):
        if self.AD178func() >= 11:
            return "*****"
        else:
            if self.AD178func() >= 10:
                return "****"
            else:
                if self.AD178func() >= 9:
                    return "***"
                else:
                    if self.AD178func() >= 8:
                        return "**"
                    else:
                        return "*"

    #CRPF AS1987
    def AD179func(self):
        #=(AF173+AH172)/2
        return (self.AF173func() + self.AH172func()) / 2

    def AC179func(self):
        #IF(AD179>=11%,"*****",IF(AD179>=10%,"****",IF(AD179>=9%,"***",IF(AD179>=8%,"**","*"))))
        if self.AD179func() >= 11:
            return "*****"
        else:
            if self.AD179func() >= 10:
                return "****"
            else:
                if self.AD179func() >= 9:
                    return "***"
                else:
                    if self.AD179func() >= 8:
                        return "**"
                    else:
                        return "*"

    #Navy AS1990
    def AD180func(self):
        #=(AF173+AH172)/2
        return (self.AF173func() + self.AH172func()) / 2

    def AC180func(self):
        if self.AD180func() >= 11:
            return "*****"
        else:
            if self.AD180func() >= 10:
                return "****"
            else:
                if self.AD180func() >= 9:
                    return "***"
                else:
                    if self.AD180func() >= 8:
                        return "**"
                    else:
                        return "*"

    #Nurse AS1993
    def AD181func(self):
        #=(AF173+AH173+AF171+AH174)/4
        return (self.AF173func() + self.AH173func() + self.AF171func() + self.AH174func()) / 4

    def AC181func(self):
        #IF(AD181>=11%,"*****",IF(AD181>=10%,"****",IF(AD181>=9%,"***",IF(AD181>=8%,"**","*"))))
        if self.AD181func() >= 11:
            return "*****"
        else:
            if self.AD181func() >= 10:
                return "****"
            else:
                if self.AD181func() >= 9:
                    return "***"
                else:
                    if self.AD181func() >= 8:
                        return "**"
                    else:
                        return "*"

        #Shooter AS1996
    def AH175func(self):
        return self.AC37func()

    def AD182func(self):
        #=(AH175+AH173)/2
        return (self.AH175func() + self.AH173func()) / 2

    def AC182func(self):
        #IF(AD182>=11%,"*****",IF(AD182>=10%,"****",IF(AD182>=9%,"***",IF(AD182>=8%,"**","*"))))
        if self.AD182func() >= 11:
            return "*****"
        else:
            if self.AD182func() >= 10:
                return "****"
            else:
                if self.AD182func() >= 9:
                    return "***"
                else:
                    if self.AD182func() >= 8:
                        return "**"
                    else:
                        return "*"
    
    def senseFunc(self):
        labels = ['Taste', "Smell", "Touch", "Listen", "See"]
        values = [round(self.Y51func(), 2), round(self.Z51func(), 2), round(self.AA51func(), 2), round(self.AB51func(), 2), round(self.AC51func(), 2)]
        colors = ['green','blue','purple','brown','teal']
        plt.barh(labels, values, color=colors)
        for index, value in enumerate(values):
            plt.text(value + 0.25, index, str(value) + ' %')
        # plt.xlim([min(values) - 2, max(values) + 2])
        # plt.title("Making Sense", fontsize=14)
        # plt.xlabel('Values', fontsize=14)
        # plt.ylabel("Senses", fontsize=14)
        plt.yticks(fontsize=16)
        plt.savefig('media/{}/senseImg.png'.format(self.username), dpi=400, bbox_inches = "tight")
        plt.clf()
        plt.cla()
    
    def processFunc(self):
        labels = ['Action', "Thinking", "Tactile", "Auditory", "Visual"]
        values = [round(self.Z41func(), 2), round(self.AA41func(), 2), round(self.AB41func(), 2), round(self.AC41func(), 2), round(self.AD41func(), 2)]
        colors = ['green','blue','purple','brown','teal']
        plt.barh(labels, values, color=colors)
        for index, value in enumerate(values):
            plt.text(value + 0.25, index, str(value)+ ' %')
        # plt.title("Making Sense", fontsize=14)
        # plt.xlabel('Values', fontsize=14)
        # plt.ylabel("Senses", fontsize=14)
        plt.yticks(fontsize=16)        
        plt.savefig('media/{}/processImg.png'.format(self.username), dpi=400, bbox_inches = "tight")
        plt.clf()
        plt.cla()
    
    def quotientsFunc(self):
        labels = ['IQ', "EQ", "CQ", "AQ"]
        values = [round(self.AE39func()), round(self.AF39func()), round(self.AG39func()), round(self.AH39func())]
        colors = ['green','blue','purple','brown','teal']
        plt.bar(labels, values, color=colors)
        for index, value in enumerate(values):
            plt.text(index, value + 0.25, str(value), ha='center')
        # plt.title("Making Sense", fontsize=14)
        # plt.xlabel('Values', fontsize=14)
        # plt.ylabel("Senses", fontsize=14)
        plt.xticks(fontsize=15)
        plt.yticks(fontsize=16)
        plt.savefig('media/{}/quotientsImg.png'.format(self.username), dpi=400, bbox_inches = "tight")
        plt.clf()
        plt.cla()
    
    def learningFunc(self):
        fig = plt.figure()
        ax = fig.add_axes([0,0,1,1])
        ax.axis('equal')                
        labels = ['Visual', "Auditory", "Kinesthetic"]
        values = [round(self.AG35func(), 2), round(self.AF35func(), 2), round(self.AE35func(), 2)]
        # colors = ['green','blue','purple','brown','teal']
        # plt.bar(labels, values, color=colors)
        ax.pie(values, labels=labels, autopct='%1.2f%%')
        # plt.title("Making Sense", fontsize=14)
        # plt.xlabel('Values', fontsize=14)
        # plt.ylabel("Senses", fontsize=14)
        plt.yticks(fontsize=16)
        plt.savefig('media/{}/learningImg.png'.format(self.username), dpi=400, bbox_inches = "tight")
        plt.clf()
        plt.cla()
    
    def leaderFunc(self):
        labels = ['Task', "Relationship"]
        values = [round(self.AJ52func(), 2), round(self.AK52func(), 2)]
        colors = ['green','blue','purple','brown','teal']
        plt.bar(labels, values, color=colors)
        for index, value in enumerate(values):
            plt.text(index, value + 0.25, str(value)+ ' %', ha='center')
        # plt.title("Making Sense", fontsize=14)
        # plt.xlabel('Values', fontsize=14)
        # plt.ylabel("Senses", fontsize=14)
        plt.yticks(fontsize=16)
        plt.savefig('media/{}/leaderImg.png'.format(self.username), dpi=400, bbox_inches = "tight")
        plt.clf()
        plt.cla()
    
    def hollandFunc(self):
        labels = ['Realistic', "Coventional", "Enterprising", "Investigative", "Artistic", "Social"]
        values = [round(self.AD56func(), 2), round(self.AI56func(), 2), round(self.AH56func(), 2), round(self.AE56func(), 2), round(self.AF56func(), 2), round(self.AG56func(), 2)]
        colors = ['green','blue','purple','brown','teal', 'red']
        plt.bar(labels, values, color=colors)
        for index, value in enumerate(values):
            plt.text(index, value + 0.25, str(value)+ ' %', ha='center')
        # plt.title("Making Sense", fontsize=14)
        # plt.xlabel('Values', fontsize=14)
        # plt.ylabel("Senses", fontsize=14)
        plt.xticks(rotation=70)
        plt.xticks(fontsize=16)
        plt.yticks(fontsize=16)
        plt.savefig('media/{}/hollandImg.png'.format(self.username), dpi=400, bbox_inches = "tight")
        plt.clf()
        plt.cla()
    
    def Z57func(self):
        #=(AC34+AA36+AC37)/3
        return ((self.AC34func() + self.AA36func() + self.AC37func()) / 3)
    
    def AA57func(self):
        #=(AC33+AA34+AA37)/3
        return ((self.AC33func() + self.AA34func() + self.AA37func()) / 3)
    
    def AB57func(self):
        #=(AC36+AA33+AA35+AC35)/4
        return ((self.AC36func() + self.AA33func() + self.AA35func() + self.AC35func()) / 4 )

    def AC57func(self):
        #=SUM(Z57:AB57)
        return (self.Z57func() + self.AA57func() + self.AB57func())
    
    def Z56func(self):
        #=Z57/AC57
        return (self.Z57func() / self.AC57func()) * 100
    
    def AA56func(self):
        #=AA57/AC57
        return (self.AA57func() / self.AC57func()) * 100
    
    def AB56func(self):
        #=AB57/AC57
        return (self.AB57func() / self.AC57func()) * 100
    
    def mckenzieFunc(self):
        labels = ['Analytical', "Introspective", "Interactive"]
        values = [round(self.Z56func(), 2), round(self.AA56func(), 2), round(self.AB56func(), 2)]
        colors = ['green','blue','purple','brown','teal']
        plt.bar(labels, values, color=colors)
        for index, value in enumerate(values):
            plt.text(index, value + 0.25, str(value)+ ' %', ha='center')
        # plt.title("Making Sense", fontsize=14)
        # plt.xlabel('Values', fontsize=14)
        # plt.ylabel("Senses", fontsize=14)
        plt.xticks(fontsize=16)
        plt.yticks(fontsize=16)
        plt.savefig('media/{}/mckenzieImg.png'.format(self.username), dpi=400, bbox_inches = "tight")
        plt.clf()
        plt.cla()
    
    def AG62func(self):
        #=(AH73+AH70)/2
        return ((self.AH73func() + self.AH70func()) / 2)
    
    def AH62func(self):
        #=(AH70+AF73+AF70+AF71+AH71)/5
        return ((self.AH70func() + self.AF73func() + self.AF70func() + self.AF71func() + self.AH71func()) / 5)
    
    def AI62func(self):
        #=AF72
        return self.AF72func()

    def AF72func(self):
        return self.AA36func()
    
    def AJ62func(self):
        #=(AH73+AH70)/2
        return ((self.AH73func() + self.AH70func()) / 2)

    def AK62func(self): 
        #=(AF70+AF73)/2
        return ((self.AF70func() + self.AF73func()) / 2)
    
    def AL62func(self):
        #=(AH73+AH70)/2
        return ((self.AH73func() + self.AH70func()) / 2)

    def AM62func(self):
        #=AH70
        return self.AH70func()

    def AN62func(self):
        #=(AH72+AF69)/2
        return ((self.AH72func() + self.AF69func()) / 2)

    def AO62func(self):
        #=AH72
        return self.AH72func()

    def AP62func(self):
        #=AH70
        return self.AH70func()
    
    def AQ62func(self):
        #=(AF69+AH69+AH70+AH72)/4
        return ((self.AF69func() + self.AH69func() + self.AH70func() + self.AH72func()) / 4)

    def AR62func(self):
        #=(AH72+AF69)/2
        return ((self.AH72func() + self.AF69func()) / 2)
    
    def AS62func(self):
        #=(AF69+AH69+AF72+AH72)/4
        return ((self.AF69func() + self.AH69func() + self.AF72func() + self.AH72func()) / 4)
    
    def AT62func(self):
        #=AH72
        return self.AH72func()
        
    def AU62func(self):
        #=(AF71+AF73+AF70+AH71)/4
        return ((self.AF71func() + self.AF73func() + self.AF70func() + self.AH71func()) / 4)
    
    def AV62func(self):
        #=(AF71+AH71+AH70)/3
        return((self.AF71func() + self.AH71func() + self.AH70func()) / 3)

    def careerFunc(self):
        labels = ['Medical' , "Engineering", "Melody", "Life Science", "Designing", "Weather & Environment Science", "Banking & Finance", "Mass & Media Communication", "Literature", "Mathematics", "Management", "Public & Political Affairs", "Psychology", "Foreign Language", "Sports", "Defense"]
        values = [round(self.AG62func(), 2), round(self.AH62func(), 2), round(self.AI62func(), 2), round(self.AJ62func(), 2), round(self.AK62func(), 2), round(self.AL62func(), 2), round(self.AM62func(), 2), round(self.AN62func(), 2), round(self.AO62func(), 2), round(self.AP62func(), 2), round(self.AQ62func(), 2), round(self.AR62func(), 2), round(self.AS62func(), 2), round(self.AT62func(), 2), round(self.AU62func(), 2), round(self.AV62func(), 2)]
        colors = ['Aquamarine','brown','teal', 'Blue', 'BlueViolet', 'Chocolate','Coral', 'DarkBlue', 'DarkGrey', 'DarkGreen', 'DarkMagenta', 'DarkKhaki', 'DarkOrange', 'DarkSlateGray', 'DarkViolet', 'FireBrick', 'ForestGreen', 'DeepSkyBlue', 'DodgerBlue', 'Indigo']
        plt.barh(labels, values, color=colors)
        # for index, value in enumerate(values):
        #     plt.text(value, index, str(value)+ ' %')
        # plt.title("Making Sense", fontsize=14)
        # plt.xlabel('Values', fontsize=14)
        # plt.ylabel("Senses", fontsize=14)
        plt.savefig('media/{}/careerImg.png'.format(self.username), bbox_inches = "tight", dpi=400)
        plt.clf()
        plt.cla()
    
    def intrapersonalFunc(self):
        labels = ['Planning', "Emotion"]
        values = [round(self.O47func(), 2), round(self.P47func(), 2)]
        colors = ['green','blue']
        plt.bar(labels, values, color=colors)
        for index, value in enumerate(values):
            plt.text(index, value + 0.25, str(value)+ ' %', ha='center')
        # plt.title("Making Sense", fontsize=14)
        # plt.xlabel('Values', fontsize=14)
        # plt.ylabel("Senses", fontsize=14)
        # plt.xticks(rotation=70)
        plt.xticks(fontsize=16)
        plt.yticks(fontsize=16)
        plt.savefig('media/{}/intrapersonalImg.png'.format(self.username), dpi=400, bbox_inches = "tight")
        plt.clf()
        plt.cla()    

    def intrapersonalintelFunc(self):
        labels = ['Inter', "Visual","Kinesthetic","Melody","Intra","Logical","Language","Naturalist"]
        values = [round(self.AD31func(), 2), round(self.AE31func(), 2), round(self.AF31func(), 2),round(self.AG31func(), 2),round(self.AH31func(), 2),round(self.AI31func(), 2),round(self.AJ31func(), 2),round(self.AK31func(), 2) ]
        colors = ['green','blue','Red','yellow','Aquamarine','brown','teal','Coral' ]
        plt.bar(labels, values, color=colors)
        for index, value in enumerate(values):
            plt.text(index, value + 0.25, str(value)+ ' %', ha='center')
        # plt.title("Making Sense", fontsize=14)
        # plt.xlabel('Values', fontsize=14)
        # plt.ylabel("Senses", fontsize=14)
        plt.xticks(rotation=70)
        plt.xticks(fontsize=16)
        plt.yticks(fontsize=16)
        plt.savefig('media/{}/intrapersonalintelImg.png'.format(self.username), dpi=400, bbox_inches = "tight")
        plt.clf()
        plt.cla()    
    
    def logicalFunc(self):
        labels = ['Reasoning', "Numerical","Geometry"]
        values = [round(self.Q47func(), 2), round(self.R47func(), 2),round(self.S47func(), 2),]
        colors = ['green','blue','red']
        plt.bar(labels, values, color=colors)
        for index, value in enumerate(values):
            plt.text(index, value + 0.25, str(value)+ ' %', ha='center')
        # plt.title("Making Sense", fontsize=14)
        # plt.xlabel('Values', fontsize=14)
        # plt.ylabel("Senses", fontsize=14)
        # plt.xticks(rotation=70)
        plt.xticks(fontsize=16)
        plt.yticks(fontsize=16)
        plt.savefig('media/{}/logicalImg.png'.format(self.username), dpi=400, bbox_inches = "tight")
        plt.clf()
        plt.cla()    

    def linguisticFunc(self):
        labels = ["Non-Verbal", "Verbal","Writing"]
        values = [round(self.V47func(), 2), round(self.W47func(), 2),round(self.X47func(), 2)]
        colors = ['green','blue','red']
        plt.bar(labels, values, color=colors)
        for index, value in enumerate(values):
            plt.text(index, value + 0.25, str(value)+ ' %', ha='center')
        # plt.title("Making Sense", fontsize=14)
        # plt.xlabel('Values', fontsize=14)
        # plt.ylabel("Senses", fontsize=14)
        # plt.xticks(rotation=70)
        plt.xticks(fontsize=16)
        plt.yticks(fontsize=16)
        plt.savefig('media/{}/linguisticImg.png'.format(self.username), dpi=400, bbox_inches = "tight")
        plt.clf()
        plt.cla()    

    def naturalistFunc(self):
        labels = ["Observation","Senses"]
        values = [round(self.Y47func(), 2), round(self.Z47func(), 2)]
        colors = ['green','blue']
        plt.bar(labels, values, color=colors)
        for index, value in enumerate(values):
            plt.text(index, value + 0.25, str(value)+ ' %', ha='center')
        # plt.title("Making Sense", fontsize=14)
        # plt.xlabel('Values', fontsize=14)
        # plt.ylabel("Senses", fontsize=14)
        # plt.xticks(rotation=70)
        plt.xticks(fontsize=16)
        plt.yticks(fontsize=16)
        plt.savefig('media/{}/naturalistImg.png'.format(self.username), dpi=400, bbox_inches = "tight")
        plt.clf()
        plt.cla()    

    def interpersonalFunc(self):
        labels = ["Social","Motivation"]
        values = [round(self.AA47func(), 2), round(self.AB47func(), 2)]
        colors = ['green','blue']
        plt.bar(labels, values, color=colors)
        for index, value in enumerate(values):
            plt.text(index, value + 0.25, str(value)+ ' %', ha='center')
        # plt.title("Making Sense", fontsize=14)
        # plt.xlabel('Values', fontsize=14)
        # plt.ylabel("Senses", fontsize=14)
        # plt.xticks(rotation=70)
        plt.xticks(fontsize=16)
        plt.yticks(fontsize=16)
        plt.savefig('media/{}/interpersonalImg.png'.format(self.username), dpi=400, bbox_inches = "tight")
        plt.clf()
        plt.cla() 

    def visualFunc(self):
        labels = ["Social","Spiritual"]
        values = [round(self.AH47func(), 2), round(self.AI47func(), 2)]
        colors = ['green','blue']
        plt.bar(labels, values, color=colors)
        for index, value in enumerate(values):
            plt.text(index, value + 0.25, str(value)+ ' %', ha='center')
        # plt.title("Making Sense", fontsize=14)
        # plt.xlabel('Values', fontsize=14)
        # plt.ylabel("Senses", fontsize=14)
        # plt.xticks(rotation=70)
        plt.xticks(fontsize=16)
        plt.yticks(fontsize=16)
        plt.savefig('media/{}/visualImg.png'.format(self.username), dpi=400, bbox_inches = "tight")
        plt.clf()
        plt.cla()        
        
    def melodyalFunc(self):
        labels = ["Voice-Tone", "Processing","Auditory"]
        values = [round(self.AE47func(), 2), round(self.AF47func(), 2),round(self.AG47func(), 2)]
        colors = ['green','blue','red']
        plt.bar(labels, values, color=colors)
        for index, value in enumerate(values):
            plt.text(index, value + 0.25, str(value)+ ' %', ha='center')
        # plt.title("Making Sense", fontsize=14)
        # plt.xlabel('Values', fontsize=14)
        # plt.ylabel("Senses", fontsize=14)
        # plt.xticks(rotation=70)
        plt.xticks(fontsize=16)
        plt.yticks(fontsize=16)
        plt.savefig('media/{}/melodyalImg.png'.format(self.username), dpi=400, bbox_inches = "tight")
        plt.clf()
        plt.cla()    

    def kinestheticFunc(self):
        labels = ["Fine-Motor", "Gross-Motor"]
        values = [round(self.T47func(), 2), round(self.U47func(), 2)]
        colors = ['green','blue']
        plt.bar(labels, values, color=colors)
        for index, value in enumerate(values):
            plt.text(index, value + 0.25, str(value)+ ' %', ha='center')
        # plt.title("Making Sense", fontsize=14)
        # plt.xlabel('Values', fontsize=14)
        # plt.ylabel("Senses", fontsize=14)
        # plt.xticks(rotation=70)
        plt.xticks(fontsize=16)
        plt.yticks(fontsize=16)
        plt.savefig('media/{}/kinestheticImg.png'.format(self.username), dpi=400, bbox_inches = "tight")
        plt.clf()
        plt.cla()  
    
    def streamFunc(self):
        fig = plt.figure()
        ax = fig.add_axes([0,0,1,1])
        ax.axis('equal')                
        labels = ['Arts', "Commerce", "Science"]
        values = [round(self.AH52func(), 2), round(self.AG35func(), 2), round(self.AF35func(), 2)]
        # colors = ['green','blue','purple','brown','teal']
        # plt.bar(labels, values, color=colors)
        ax.pie(values, labels=labels, autopct='%1.2f%%')
        # plt.title("Making Sense", fontsize=14)
        # plt.xlabel('Values', fontsize=14)
        # plt.ylabel("Senses", fontsize=14)
        plt.yticks(fontsize=16)
        plt.savefig('media/{}/streamImg.png'.format(self.username), dpi=400, bbox_inches = "tight")
        plt.clf()
        plt.cla()

    def AJ35func(self):
        return (self.AA36func() + self.AA35func()) /2

    def AK35func(self):
        return (self.AA36func() + self.AC35func()) / 2

    def AL35func(self):
        return (self.AA36func() + self.AC36func()) / 2

    def AM35func(self):
        return (self.AC36func() + self.AA35func()) / 2

    def AN35func(self):
        return (self.AA37func() + self.AA35func()) / 2 

    def AO35func(self):
        return (self.AA35func() + self.AA37func() + self.AA34func()) / 3

    def AP35func(self):
        return self.AC34func()

    def AQ35func(self):
        return (self.AC35func() + self.AA37func() + self.AA34func() + self.AC34func()) / 4

    def AR35func(self):
        return self.AC36func()

    def AS35func(self):
        return (self.AC35func() + self.AA34func() + self.AA37func()) / 3

    def activityFunc(self):
        labels = ["1", "2","3","4","5","6","7","8","9","10"]
        values = [round(self.AJ35func(), 2), round(self.AK35func(), 2), round(self.AL35func(), 2),round(self.AM35func(), 2),round(self.AN35func(), 2),round(self.AO35func(), 2),round(self.AP35func(), 2),round(self.AQ35func(), 2), round(self.AR35func(), 2), round(self.AS35func(), 2) ]
        colors = ['green','blue','Red','yellow','Aquamarine','brown','teal','Coral','pink','grey']
        plt.bar(labels, values, color=colors)
        for index, value in enumerate(values):
            plt.text(index, value + 0.25, str(value)+ ' %', ha='center')
        # plt.title("Making Sense", fontsize=14)
        # plt.xlabel('Values', fontsize=14)
        # plt.ylabel("Senses", fontsize=14)
        # plt.xticks(rotation=70)
        plt.xticks(fontsize=16)
        plt.yticks(fontsize=16)
        plt.savefig('media/{}/activityImg.png'.format(self.username), dpi=400, bbox_inches = "tight")
        plt.clf()
        plt.cla()  

    def info(self):
        # Graph Charts
        
        self.senseFunc()
        self.processFunc()
        self.quotientsFunc()
        self.leaderFunc()
        self.learningFunc()
        self.hollandFunc()
        self.mckenzieFunc()
        self.careerFunc()
        self.intrapersonalFunc()
        self.intrapersonalintelFunc()
        self.logicalFunc()
        self.linguisticFunc()
        self.naturalistFunc()
        self.interpersonalFunc()
        self.visualFunc()
        self.melodyalFunc()
        self.kinestheticFunc()
        self.streamFunc()
        self.activityFunc()


        self.data = {
            "username" : self.username,
            "clientcode" : self.clientcode,
            "BD4rp" : self.BD4func(self.dmitDetail.l1),
            "BD18rp" : self.BD18func(self.dmitDetail.r1),
            "AG41rp" : self.AG41func(),
            "AC38rp" : round(self.AC38func(), 2),
            "AA38rp" : round(self.AA38func(), 2),
            "Y51rp" : round(self.Y51func(), 2),
            "Z51rp" : round(self.Z51func(), 2),
            "AA51rp" : round(self.AA51func(), 2),
            "AB51rp" : round(self.AB51func(), 2),
            "AC51rp" : round(self.AC51func(), 2),
            "AM37rp" : round(self.AM37func(), 2),
            "AN37rp" : round(self.AN37func(), 2),
            "AR37rp" : round(self.AR37func(), 2),
            "AS37rp" : round(self.AS37func(), 2),
            "AE39rp" : round(self.AE39func()),
            "AH39rp" : round(self.AH39func()),
            "AF39rp" : round(self.AF39func()),
            "AG39rp" : round(self.AG39func()),
            "AG35rp" : round(self.AG35func(), 2),
            "AF35rp" : round(self.AF35func(), 2),
            "AE35rp" : round(self.AE35func(), 2),
            "AJ52rp" : round(self.AJ52func(), 2),
            "AK52rp" : round(self.AK52func(), 2),
            "AD56rp" : round(self.AD56func(), 2),
            "AI56rp" : round(self.AI56func(), 2),
            "AH56rp" : round(self.AH56func(), 2),
            "AE56rp" : round(self.AE56func(), 2),
            "AF56rp" : round(self.AF56func(), 2),
            "AG56rp" : round(self.AG56func(), 2),
            "AJ49rp" : round(self.AJ49func() * 100, 2),
            "AK49rp" : round(self.AK49func() * 100, 2),
            "AL49rp" : round(self.AL49func() * 100, 2),
            "AM49rp" : round(self.AM49func() * 100, 2),
            "AC60rp" : self.AC60func(),
            "AC61rp" : self.AC61func(),
            "AC62rp" : self.AC62func(),
            "AC63rp" : self.AC63func(),
            "AC64rp" : self.AC64func(),
            "AC65rp" : self.AC65func(),
            "AC66rp" : self.AC66func(),
            "AC67rp" : self.AC67func(),
            "AC121rp" : self.AC121func(),
            "AC122rp" : self.AC122func(),
            "AC123rp" : self.AC123func(),
            "AC124rp" : self.AC124func(),
            'AC125rp' : self.AC125func(),
            "AC126rp" : self.AC126func(),
            "AC127rp" : self.AC127func(),
            "AC128rp" : self.AC128func(),
            "AC73rp" : self.AC73func(),
            'AC74rp' : self.AC74func(),
            'AC75rp' : self.AC75func(),
            'AC134rp' : self.AC134func(),
            'AC135rp' : self.AC135func(),
            'AC136rp' : self.AC136func(),
            "AC76rp" : self.AC76func(),
            'AC77rp' : self.AC77func(),
            'AC78rp' : self.AC78func(),
            'AC79rp' : self.AC79func(),
            'AC80rp' : self.AC80func(),
            'AC81rp' : self.AC81func(),
            'AC82rp' : self.AC82func(),
            'Agrirp' : self.AC79func(),
            'AC137rp' : self.AC137func(),
            "AC138rp" : self.AC138func(),
            'AC139rp' : self.AC139func(),
            'AC140rp' : self.AC140func(),
            'AC141rp' : self.AC141func(),
            'AC142rp' : self.AC142func(),
            'AC143rp' : self.AC143func(),
            'AC144rp' : self.AC144func(),
            "AC83rp" : self.AC83func(),
            'AC84rp' : self.AC84func(),
            "AC85rp" : self.AC85func(),
            'AC86rp' : self.AC86func(),
            'AC87rp' : self.AC87func(),
            'AC88rp' : self.AC88func(),
            'AC89rp' : self.AC89func(),
            'AC90rp' : self.AC90func(),
            'AC145rp' : self.AC145func(),
            'AC146rp' : self.AC146func(),
            'AC147rp' : self.AC147func(),
            'AC148rp' : self.AC148func(),
            'AC149rp' : self.AC149func(),
            'AC150rp' : self.AC150func(),
            'AC151rp' : self.AC151func(),
            'AC152rp' : self.AC152func(),
            "AC91rp" : self.AC91func(),
            'AC92rp' : self.AC92func(),
            'AC93rp' : self.AC93func(),
            'AC94rp' : self.AC94func(),
            'AC95rp' : self.AC95func(),
            'AC96rp' : self.AC96func(),
            'AC97rp' : self.AC97func(),
            'AC153rp' : self.AC153func(),
            'AC154rp' : self.AC154func(),
            'AC155rp' : self.AC155func(),
            'AC156rp' : self.AC156func(),
            'AC157rp' : self.AC157func(),
            'AC158rp' : self.AC158func(),
            'AC159rp' : self.AC159func(),
            "AC98rp" : self.AC98func(),
            'AC99rp' : self.AC99func(),
            'AC100rp' : self.AC100func(),
            "AC101rp" : self.AC101func(),
            "AC102rp" : self.AC102func(),
            'AC103rp' : self.AC103func(),
            "AC104rp" : self.AC104func(),
            "AC160rp" : self.AC160func(),
            "AC161rp" : self.AC161func(),
            "AC162rp" : self.AC162func(),
            "AC163rp" : self.AC163func(),
            "AC164rp" : self.AC164func(),
            "AC165rp" : self.AC165func(),
            'AC166rp' : self.AC166func(),
            "AC105rp" : self.AC105func(),
            'AC106rp' : self.AC106func(),
            'AC107rp' : self.AC107func(),
            'AC108rp' : self.AC108func(),
            'AC109rp' : self.AC109func(),
            'AC110rp' : self.AC110func(),
            'AC111rp' : self.AC111func(),
            'AC112rp' : self.AC112func(),
            'AC167rp' : self.AC167func(),
            'AC168rp' : self.AC168func(),
            'AC169rp' : self.AC169func(),
            'AC170rp' : self.AC170func(),
            'AC171rp' : self.AC171func(),
            'AC172rp' : self.AC172func(),
            'AC173rp' : self.AC173func(),
            'AC174rp' : self.AC174func(),
            'AC113rp' : self.AC113func(),
            'AC114rp' : self.AC114func(),
            'AC115rp' : self.AC115func(),
            'AC116rp' : self.AC116func(),
            'AC117rp' : self.AC117func(),
            'AC118rp' : self.AC118func(),
            'AC119rp' : self.AC119func(),
            'AC120rp' : self.AC120func(),
            'AC175rp' : self.AC175func(),
            'AC176rp' : self.AC176func(),
            'AC177rp' : self.AC177func(),
            'AC178rp' : self.AC178func(),
            'AC179rp' : self.AC179func(),
            'AC180rp' : self.AC180func(),
            'AC181rp' : self.AC181func(),
            'AC182rp' : self.AC182func(),
            'Z41rp' : round(self.Z41func(), 2),
            'AA41rp' : round(self.AA41func(), 2),
            'AB41rp' : round(self.AB41func(), 2),
            'AC41rp' : round(self.AC41func(), 2),
            'AD41rp' : round(self.AD41func(), 2),
            'Z56rp' : round(self.Z56func(), 2),
            'AA56rp' : round(self.AA56func(), 2),
            'AB56rp' : round(self.AB56func(), 2),
            'AG62rp' : round(self.AG62func(), 2),
            'AH62rp' : round(self.AH62func(), 2),
            'AI62rp' : round(self.AI62func(), 2),
            'AJ62rp' : round(self.AJ62func(), 2),
            'AK62rp' : round(self.AK62func(), 2),
            'AL62rp' : round(self.AL62func(), 2),
            'AM62rp' : round(self.AM62func(), 2),
            'AN62rp' : round(self.AN62func(), 2),
            'AO62rp' : round(self.AO62func(), 2),
            'AP62rp' : round(self.AP62func(), 2),
            'AQ62rp' : round(self.AQ62func(), 2),
            'AR62rp' : round(self.AR62func(), 2),
            'AS62rp' : round(self.AS62func(), 2),
            'AT62rp' : round(self.AT62func(), 2),
            'AU62rp' : round(self.AU62func(), 2),
            'AV62rp' : round(self.AV62func(), 2),
            'AH31rp' : round(self.AH31func(), 2),
            'O47rp' : round(self.O47func(), 2),
            'P47rp' : round(self.P47func(), 2),
            'AI31rp' : round(self.AI31func(), 2),
            'Q47rp' : round(self.Q47func(), 2),
            'R47rp' : round(self.R47func(), 2),
            'S47rp' : round(self.S47func(), 2),
            'AJ31rp' : round(self.AJ31func(), 2),
            'V47rp' : round(self.V47func(), 2),
            'W47rp' : round(self.W47func(), 2),
            'X47rp' : round(self.X47func(), 2),
            'AK31rp' : round(self.AK31func(), 2),
            'Y47rp' : round(self.Y47func(), 2),
            'Z47rp' : round(self.Z47func(), 2),
            'AD31rp' : round(self.AD31func(), 2),
            'AA47rp' : round(self.AA47func(), 2),
            'AB47rp' : round(self.AB47func(), 2),
            'AE31rp' : round(self.AE31func(), 2),
            'AH47rp' : round(self.AH47func(), 2),
            'AI47rp' : round(self.AI47func(), 2),
            'AG31rp' : round(self.AG31func(), 2),
            'AE47rp' : round(self.AE47func(), 2),
            'AF47rp' : round(self.AF47func(), 2),
            'AG47rp' : round(self.AG47func(), 2),
            'AF31rp' : round(self.AF31func(), 2),
            'T47rp' : round(self.T47func(), 2),
            'U47rp' : round(self.U47func(), 2),
            'AF52rp' : round(self.AF52func(), 2),
            'AG52rp' : round(self.AG52func(), 2),
            'AH52rp' : round(self.AH52func(), 2),
            'AC33rp' : round(self.AC33func(), 2),
            'D32rp' : self.D32func(),
            'AA33rp' : round(self.AA33func(), 2),
            'D33rp' : self.D33func(),
            'D44rp' : self.D44func(),
            'AC34rp' : round(self.AC34func(), 2),
            'D45rp' : self.D45func(),
            'AC47rp' : round(self.AC47func(), 2),
            'AD47rp' : round(self.AD47func(), 2),
            'D34rp' : self.D34func(),
            'AA34rp' : round(self.AA34func(), 2),
            'D35rp' : self.D35func(),
            'AC35rp' : round(self.AC35func(), 2),
            'D36rp' : self.D36func(),
            'AA35rp' : round(self.AA35func(), 2),
            'D37rp' : self.D37func(),
            'AC36rp' : round(self.AC36func(), 2),
            'D38rp' : self.D38func(),
            'AA36rp' : round(self.AA36func(), 2),
            'D39rp' : self.D39func(),
            'AC37rp' : round(self.AC37func(), 2),
            'AA37rp' : round(self.AA37func(), 2),
            'D42rp' : self.D42func(),
            'D43rp' : self.D43func(),
            'D46rp' : self.D46func(),
            'D47rp' : self.D47func(),
            'D48rp' : self.D48func(),
            'D49rp' : self.D49func(),
            'D50rp' : self.D50func(),
            'D51rp' : self.D51func(),
            'D40rp' : self.D40func(),
            'D41rp' : self.D41func(),
            'D19rp' : self.D19func(),
            'D21rp' : self.D19func(),
        }
        return self.data



def report(request ,pk=None):
    if pk:        
        hrReport = DFormula(pk)
        info = hrReport.info()       
        resp = HttpResponse(content_type='application/pdf')
        result = generate_pdf('dappx/report.html',context=info, file_object=resp)    
        return result
    else:
        user=request.user
        x=user.username
        context={'username':x}
        resp = HttpResponse(content_type='application/pdf')
        result = generate_pdf('dappx/report.html', file_object=resp)

def lifetimeReport(request ,pk=None):
    if pk:        
        hrReport = DFormula(pk)
        info = hrReport.info()       
        resp = HttpResponse(content_type='application/pdf')
        result = generate_pdf('dappx/lifetimeReport.html',context=info, file_object=resp)    
        return result
    else:
        user=request.user
        x=user.username
        context={'username':x}
        resp = HttpResponse(content_type='application/pdf')
        result = generate_pdf('dappx/lifetimeReport.html', file_object=resp)
