import email
from multiprocessing import context
from django.shortcuts import render, redirect,get_object_or_404
from django.urls import reverse
from django.http import HttpResponse,HttpResponseRedirect, JsonResponse
from .models import *
from .forms import *
from datetime import datetime
from datetime import date, timedelta
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.db.models import Q
import random
from django.core.mail import send_mail
from io import BytesIO
from django.template.loader import get_template
import os
from django.conf import settings
from xhtml2pdf import pisa

def render_pdf_view(request):
    all = serviceHistory.objects.filter(is_deleted=False)
    context = {'all': all}
    # Create a Django response object, and specify content_type as pdf
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] =  'filename="Service_Invoice_Report.pdf"'
    # find the template and render it.
    template = get_template('for_render_pdf/try.html')
    html = template.render(context)

    # create a pdf
    pisa_status = pisa.CreatePDF(
       html, dest=response)
    # if error then show some funny view
    if pisa_status.err:
       return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response


def justtry(request):
    context ={'Hello':'Hello'}
    return render(request,'for_render_pdf/individual_chargeslip.html', context)


def index(request):
    return render(request, 'index.html')

def aboutUs(request):
    return render(request,'about.html')

def services1(request):
    return render(request,'services.html')

def contact_us(request):
    return render(request,'contact_us.html')

def forgot_pass_1(request):
    return render(request,'forgot_pass_1.html')

def forgot_pass_2(request):
    return render(request,'forgot_pass_2.html')

def forgot_pass_3(request):
    return render(request,'forgot_pass_3.html')

def loginPage(request):
    if request.user.is_authenticated and request.user.is_admin:
        return redirect('admin/')
    elif request.user.is_authenticated and request.user.is_headveterinarian:
        return redirect('headVetHome')
    elif request.user.is_authenticated and request.user.is_veterinarian:
        return redirect('veterinarianHome')
    elif request.user.is_authenticated and request.user.is_secretary:
        return redirect('secretaryHome')
    elif request.user.is_authenticated and request.user.is_petowner:
        return redirect('petOwnerHome')
    else:
        if request.method == 'POST':
            email = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
                users = request.user
                if user.is_authenticated and users.is_admin:
                    users.last_login = datetime.today()
                    users.save()
                    return redirect('admin/')
                elif user.is_authenticated and users.is_headveterinarian:
                    users.last_login = datetime.today()
                    users.save()
                    return redirect('headVetHome')
                elif user.is_authenticated and users.is_secretary:
                    users.last_login = datetime.today()
                    users.save()
                    return redirect('secretaryHome')
                elif user.is_authenticated and users.is_veterinarian:
                    users.last_login = datetime.today()
                    users.save()
                    return redirect('veterinarianHome')
                elif user.is_authenticated and users.is_petowner:
                    users.last_login = datetime.today()
                    users.save()
                    return redirect('petOwnerHome')
                else:
                    messages.error (request,'You have entered an invalid email or password.')
                    return render(request, 'login.html')
            else:
                    messages.error (request,'You have entered an invalid email or password.')
                    return render(request, 'login.html')
    return render(request,'login.html')


def OwnerChangePass(request):
    context={}
    if (request.method=='POST'):
        form = PasswordChangeForm(request.user,request.POST)
        if form.is_valid():
            user=form.save()
            update_session_auth_hash(request, user)
            messages.success(request,'Password Updated')
            context['form'] = form
            return render(request,'petowner/change_pass.html', context)
        else:
            pass
    else:
        form = PasswordChangeForm(request.user)

    context={'sideb':'OwnerChangePass','form':form}
    return render(request,'petowner/change_pass.html',context)

def SecChangePass(request):
    context={}
    if (request.method=='POST'):
        form = PasswordChangeForm(request.user,request.POST)
        if form.is_valid():
            user=form.save()
            update_session_auth_hash(request, user)
            messages.success(request,'Password Updated')
            context['form'] = form
            return render(request,'secretary/change_pass.html', context)
        else:
            pass
    else:
        form = PasswordChangeForm(request.user)

    context={'sideb':'SecChangePass','form':form}
    return render(request,'secretary/change_pass.html',context)

def headvetChangePass(request):
    context={}
    if (request.method=='POST'):
        form = PasswordChangeForm(request.user,request.POST)
        if form.is_valid():
            user=form.save()
            update_session_auth_hash(request, user)
            messages.success(request,'Password Updated')
            context['form'] = form
            return render(request,'headveterinarian/change_pass.html', context)
        else:
            pass
    else:
        form = PasswordChangeForm(request.user)

    context={'sideb':'headvetChangePass', 'form':form}
    return render(request,'headveterinarian/change_pass.html', context)

def vetChangePass(request):
    context={}
    if (request.method=='POST'):
        form = PasswordChangeForm(request.user,request.POST)
        if form.is_valid():
            user=form.save()
            update_session_auth_hash(request, user)
            messages.success(request,'Password Updated')
            context['form'] = form
            return render(request,'veterinarian/change_pass.html', context)
        else:
            pass
    else:
        form = PasswordChangeForm(request.user)

    context={'sideb':'vetChangePass','form':form}
    return render(request,'veterinarian/change_pass.html',context)

def logout_view(request):
    logout(request)
    
    return redirect('login')

#VIEWS FOR CRUD
#USER ACCOUNTS
def create_accounts(request): 
    id = request.user.id
    user = User.objects.get(pk=id)
    over_all = User.objects.filter(is_active=True)
    petowners = User.objects.filter(is_petowner=True,is_active=True)
    veterinarian = User.objects.filter(is_veterinarian=True,is_active=True)
    headvet = User.objects.filter(is_headveterinarian=True,is_active=True)
    secretary = User.objects.filter(is_secretary=True,is_active=True)
    searchthis_query = request.GET.get('searchthis1')
    if searchthis_query != " " and searchthis_query is not None:
        over_all = User.objects.filter(Q(email__icontains=searchthis_query)).distinct()    
    context = {'sideb':'create_accounts','petowners':petowners, 'veterinarian': veterinarian, 'headvet': headvet, 'secretary': secretary, 'user':user,'over_all':over_all}
    return render(request, 'secretary/create/create_accounts.html', context)

def add_users(request):
    context ={}
    alluser = User.objects.all
    if request.POST:
        form = CreateUserForm(request.POST,initial={'is_petowner': True})
        if form.is_valid():
            x = form.save()
            email = form.cleaned_data.get('email')
            raw_password = form.cleaned_data.get('password1')
            CustomUsers = authenticate(email=email,password=raw_password)
            CustomUsers.save
            subject = 'Dagupan Animal Clinic Activation'
            message = "You are now part of Dagupan Animal Clinic, to login please use the password: %s It is advisable to change you password immediatelty" %raw_password
            recipient = x.email
            send_mail(subject, message, settings.EMAIL_HOST_USER, [recipient], fail_silently=False)
            messages.success(request, "Pet Owner account has been successfully created.")

            return redirect('create_accounts')
        else:
            context['register'] = form
    else:
        form = CreateUserForm(initial={'is_petowner': True})
        context['register'] = form
    return render(request,'secretary/add_users.html', context)

def add_users_headvet(request):
    context ={}
    alluser = User.objects.all
    if request.POST:
        form = HeadVetUserForm(request.POST,initial={'is_headveterinarian': True})
        if form.is_valid():
            x = form.save()
            email = form.cleaned_data.get('email')
            raw_password = form.cleaned_data.get('password1')
            CustomUsers = authenticate(email=email,password=raw_password)
            CustomUsers.save
            subject = 'Dagupan Animal Clinic Activation'
            message = "You are now part of Dagupan Animal Clinic, to login please use the password: %s It is advisable to change you password immediatelty" %raw_password
            recipient = x.email
            send_mail(subject, message, settings.EMAIL_HOST_USER, [recipient], fail_silently=False)
            messages.success(request, "Head Veterinarian account has been successfully created.")
            return redirect('create_accounts')
        else:
            context['register'] = form
    else:
        form = HeadVetUserForm(initial={'is_headveterinarian': True})
        context['register'] = form
    return render(request,'secretary/add_users_headvet.html', context)

def add_users_vet(request):
    context ={}
    alluser = User.objects.all
    if request.POST:
        form = VeterinarianUserForm(request.POST,initial={'is_veterinarian': True})
        if form.is_valid():
            x = form.save()
            email = form.cleaned_data.get('email')
            raw_password = form.cleaned_data.get('password1')
            CustomUsers = authenticate(email=email,password=raw_password)
            CustomUsers.save
            subject = 'Dagupan Animal Clinic Activation'
            message = "You are now part of Dagupan Animal Clinic, to login please use the password: %s It is advisable to change you password immediatelty" %raw_password
            recipient = x.email
            send_mail(subject, message, settings.EMAIL_HOST_USER, [recipient], fail_silently=False)
            messages.success(request, "Veterinarian account has been successfully created.")
            return redirect('create_accounts')
        else:
            context['register'] = form
    else:
        form = VeterinarianUserForm(initial={'is_veterinarian': True})
        context['register'] = form
    return render(request,'secretary/add_users_vet.html', context)

def add_users_sec(request):
    context ={}
    alluser = User.objects.all
    if request.POST:
        form = SecretaryUserForm(request.POST,initial={'is_secretary': True})
        if form.is_valid():
            x = form.save()
            email = form.cleaned_data.get('email')
            raw_password = form.cleaned_data.get('password1')
            CustomUsers = authenticate(email=email,password=raw_password)
            CustomUsers.save
            subject = 'Dagupan Animal Clinic Activation'
            message = "You are now part of Dagupan Animal Clinic, to login please use the password: %s It is advisable to change you password immediatelty" %raw_password
            recipient = x.email
            send_mail(subject, message, settings.EMAIL_HOST_USER, [recipient], fail_silently=False)
            messages.success(request, "Secretary account has been successfully created.")
            return redirect('create_accounts')
        else:
            context['register'] = form
    else:
        form = SecretaryUserForm(initial={'is_secretary': True})
        context['register'] = form
    return render(request,'secretary/add_users_sec.html', context)

def delete_user(request,pk):
    id = request.user.id
    user = User.objects.get(pk=id)
    deleteuser = User.objects.get(id=pk)
    if request.method == "POST":
        if user == deleteuser:
            messages.error (request,'Cannot delete User Instance.')
            return render(request, 'secretary/delete_users.html')
        else:
            deleteuser.is_active = 0
            deleteuser.date_of_inactive = datetime.today()
            deleteuser.save()
            subject = 'Dagupan Animal Clinic: Account Deactivated'
            message = 'Your account has been deactivated.'
            recipient = user.email
            send_mail(subject, message, settings.EMAIL_HOST_USER, [recipient], fail_silently=False)
            messages.error (request,'User Account Deleted')
            return redirect('create_accounts')
    context ={'deleteuser':deleteuser, 'user':user}
    return render(request,'secretary/delete_users.html', context)

def update_user(request,pk):
    context = {}
    upduser = User.objects.get(id=pk)
    if request.POST:
        form =  UpdateUserForm(request.POST, instance=upduser)
        if form.is_valid():
            form.save()
            messages.success(request, "The email has been successfully updated")
            context['register'] = form
            return render(request, 'secretary/update_users.html', context)
        else:
            messages.error(request, "User with this Email already exists.")
            context['register'] = form
            return render(request, 'secretary/update_users.html', context)

    else:
        form =  UpdateUserForm(initial ={"email":upduser.email})
    context['register'] = form
    return render(request,'secretary/update_users.html', context)

#END OF USER ACOOUNTS

#USER PROFILE: PET OWNER

def add_petowner_profile(request):
    context = {}
    if request.POST:
        form = UpdateProfileForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('useracc')
            if email == None:
                form.save()
                return redirect('user_profile')
            else:
                form.save()
                used = User.objects.get(email=email)
                used.is_used=1
                used.save()
                messages.success(request, "Successfully Added")
                return redirect('user_profile')
        else:
            messages.error(request,  " ")
            context['form'] = form
    else:
        form = UpdateProfileForm()
        context['form'] = form
    return render(request,'secretary/add_petowner_profile.html', context)

def add_petowner_account(request):
    context ={}
    alluser = User.objects.all
    if request.POST:
        form = CreateUserForm(request.POST,initial={'is_petowner': True})
        if form.is_valid():
            x=form.save()
            messages.success(request, "Pet Owner account has been successfully Added.")
            email = form.cleaned_data.get('email')
            raw_password = form.cleaned_data.get('password1')
            CustomUsers = authenticate(email=email,password=raw_password)
            CustomUsers.save
            subject = 'Dagupan Animal Clinic Activation'
            message = "You are now part of Dagupan Animal Clinic, to login please use the password: %s It is advisable to change you password immediatelty" %raw_password
            recipient = x.email
            send_mail(subject, message, settings.EMAIL_HOST_USER, [recipient], fail_silently=False)
            return redirect('add_petowner_profile')
        else:
            context['register'] = form
    else:
        form = CreateUserForm(initial={'is_petowner': True})
        context['register'] = form
    return render(request,'secretary/add_users.html', context)

def add_petowner_account1(request,pk):
    context ={}
    alluser = User.objects.all
    if request.POST:
        form = CreateUserForm(request.POST,initial={'is_petowner': True})
        if form.is_valid():
            form.save()
            email = form.cleaned_data.get('email')
            raw_password = form.cleaned_data.get('password1')
            CustomUsers = authenticate(email=email,password=raw_password)
            CustomUsers.save
            return HttpResponseRedirect(reverse('update_profile', args=[str(pk)]))
        else:
            messages.error(request,  " ")
            context['register'] = form
    else:
        form = CreateUserForm(initial={'is_petowner': True})
        context['register'] = form
    return render(request,'secretary/add_users.html', context)

def update_profile(request,pk):
    context = {}
    updprofile = Profile.objects.get(id=pk)
    if request.POST:
        form = UpdateProfileForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('useracc')
            if email == None:
                form.save()
                messages.success(request, "Pet Owner account has been successfully Updated.")
                return redirect('user_profile')
            else:
                form.save()
                used = User.objects.get(email=email)
                used.is_used=1
                used.save()
                messages.success(request, "Pet Owner account has been successfully Updated.")
                return redirect('user_profile')
        else:
            
            context['form'] = form
            context['updprofile'] = updprofile
    else:
        form = UpdateProfileForm(initial ={"useracc":updprofile.useracc,"firstName":updprofile.firstName,"lastName":updprofile.lastName,"gender":updprofile.gender,"contactNum":updprofile.contactNum,"address":updprofile.address})
        context['form'] = form
        context['updprofile'] = updprofile
    return render(request,'secretary/no_acc_update_profile.html', context)

def update_petownerprofile(request,pk):
    context = {}
    updprofile = Profile.objects.get(id=pk)
    inuse = User.objects.get(email=updprofile.useracc)
    if request.POST:
        form = UpdatePetOwnerProfileForm(request.POST,instance=updprofile)
        if form.is_valid():
            email = form.cleaned_data.get('useracc')
            if email == None:
                inuse.is_used=0
                inuse.save()
                form.save()
                return redirect('user_profile')
            else:
                used = User.objects.get(email=email)
                if inuse == used:
                    p = 1
                else:
                    p = 0
                if used.is_petowner == 0 or Profile.objects.exclude(id=pk).filter(useracc=email).exists():
                    messages.error (request,'Account is already used or not compatible with this profile')
                    return HttpResponseRedirect(reverse('update_petownerprofile', args=[str(pk)]))
                elif used.is_active == 0:
                    messages.error (request,'Account is currently inactive.')
                    return HttpResponseRedirect(reverse('update_petownerprofile', args=[str(pk)]))
                elif used.is_used == 1 and p == 0:
                    messages.error (request,'Account is already used or not compatible with this profile')
                    return HttpResponseRedirect(reverse('update_petownerprofile', args=[str(pk)]))
                else:
                    inuse.is_used=0
                    inuse.save()
                    form.save()
                    email = form.cleaned_data.get('useracc')
                    used = User.objects.get(email=email)
                    used.is_used=1
                    used.save()
                    messages.success(request, "Pet Owner Profile has been successfully Updated.")
                    return redirect('user_profile')
        else:
            messages.error(request,  " ")
            context['form'] = form
            context['updprofile'] = updprofile
    else:
        form = UpdatePetOwnerProfileForm(initial ={"useracc":updprofile.useracc,"firstName":updprofile.firstName,"lastName":updprofile.lastName,"gender":updprofile.gender,"contactNum":updprofile.contactNum,"address":updprofile.address})
        context['form'] = form
        context['updprofile'] = updprofile
    return render(request,'secretary/updateprofile.html', context)

def direct_add_users(request,pk):
    context ={}
    alluser = User.objects.all
    if request.POST:
        form = CreateUserForm(request.POST,initial={'is_petowner': True})
        if form.is_valid():
            form.save()
            email = form.cleaned_data.get('email')
            raw_password = form.cleaned_data.get('password1')
            CustomUsers = authenticate(email=email,password=raw_password)
            CustomUsers.save
            return HttpResponseRedirect(reverse('update_petownerprofile', args=[str(pk)]))
        else:
            context['register'] = form
    else:
        form = CreateUserForm(initial={'is_petowner': True})
        context['register'] = form
    return render(request,'secretary/add_users.html', context)

def delete_profile(request,pk):
    id = request.user.id
    user = User.objects.get(pk=id)
    deleteprofile = Profile.objects.get(id=pk)
    if request.method == "POST":
        if user == deleteprofile.useracc:
            messages.error (request,'Cannot delete User Instance.')
            return render(request, 'secretary/delete_profile.html')
        else:
            deleteprofile.is_deleted = 1
            deleteprofile.date_of_inactive = datetime.today()
            deleteprofile.save()
            messages.error (request,'Successfully Deleted.')
            return redirect('user_profile')
    context ={'deleteprofile':deleteprofile, 'user':user}
    return render(request,'secretary/delete_profile.html', context)

#END USER PROFILE :PET OWNER

#USER PROFILE: VET

def add_veterinarian_profile(request):
    context = {}
    if request.POST:
        form = AddVetProfileForm(request.POST)
        if form.is_valid():
            form.save()
            email = form.cleaned_data.get('useracc')
            used = User.objects.get(email=email)
            used.is_used=1
            used.save()
            messages.success(request, "Successfully Added")
            return redirect('user_profile')
        else:
            messages.error(request,  " ")
            context['form'] = form
    else:
        form = AddVetProfileForm()
        context['form'] = form
    return render(request,'secretary/add_veterinarian_profile.html', context)

def add_veterinarian_account(request):
    context ={}
    alluser = User.objects.all
    if request.POST:
        form = VeterinarianUserForm(request.POST,initial={'is_veterinarian': True})
        if form.is_valid():
            form.save()
            email = form.cleaned_data.get('email')
            raw_password = form.cleaned_data.get('password1')
            CustomUsers = authenticate(email=email,password=raw_password)
            CustomUsers.save
            return redirect('add_veterinarian_profile')
        else:
            context['register'] = form
    else:
        form = VeterinarianUserForm(initial={'is_veterinarian': True})
        context['register'] = form
    return render(request,'secretary/add_users_vet.html', context)

def update_vet_profile(request,pk):
    context = {}
    updprofile = StaffProfile.objects.get(id=pk)
    if updprofile.useracc == None:
        if request.POST:
            form = UpdateVetProfileForm(request.POST,instance=updprofile)
            if form.is_valid():
                email = form.cleaned_data.get('useracc')
                if StaffProfile.objects.exclude(id=pk).filter(useracc=email).exists():
                    messages.error (request,'Account is already used.')
                    return HttpResponseRedirect(reverse('update_vet_profile', args=[str(pk)]))
                else:
                    form.save()
                    email = form.cleaned_data.get('useracc')
                    used = User.objects.get(email=email)
                    used.is_used=1
                    used.save()
                    messages.success(request, "Veterinarian Profile has been successfully Updated.")
                    return redirect('user_profile')
            else:
                context['form'] = form
                context['updprofile'] = updprofile
        else:
            form = UpdateVetProfileForm(initial ={"useracc":updprofile.useracc,"firstName":updprofile.firstName,"lastName":updprofile.lastName,"gender":updprofile.gender,"contactNum":updprofile.contactNum,"address":updprofile.address})
            context['form'] = form
            context['updprofile'] = updprofile
    else:
        inuse = User.objects.get(email=updprofile.useracc)
        if request.POST:
            form = UpdateVetProfileForm(request.POST,instance=updprofile)
            if form.is_valid():
                email = form.cleaned_data.get('useracc')
                if StaffProfile.objects.exclude(id=pk).filter(useracc=email).exists():
                    messages.error (request,'Account is already used.')
                    return HttpResponseRedirect(reverse('update_vet_profile', args=[str(pk)]))
                else:
                    inuse.is_used = 0
                    inuse.save()
                    form.save()
                    email = form.cleaned_data.get('useracc')
                    used = User.objects.get(email=email)
                    used.is_used=1
                    used.save()
                    messages.success(request,  "Veterinarian Profile has been successfully Updated.")
                    return redirect('user_profile')
            else:
                context['form'] = form
                context['updprofile'] = updprofile
        else:
            form = UpdateVetProfileForm(initial ={"useracc":updprofile.useracc,"firstName":updprofile.firstName,"lastName":updprofile.lastName,"gender":updprofile.gender,"contactNum":updprofile.contactNum,"address":updprofile.address})
            context['form'] = form
            context['updprofile'] = updprofile
    return render(request,'secretary/update_vet_profile.html', context)

def direct_add_users_vet(request,pk):
    context ={}
    alluser = User.objects.all
    if request.POST:
        form = VeterinarianUserForm(request.POST,initial={'is_veterinarian': True})
        if form.is_valid():
            form.save()
            email = form.cleaned_data.get('email')
            raw_password = form.cleaned_data.get('password1')
            CustomUsers = authenticate(email=email,password=raw_password)
            CustomUsers.save
            return HttpResponseRedirect(reverse('update_vet_profile', args=[str(pk)]))
        else:
            context['register'] = form
    else:
        form = VeterinarianUserForm(initial={'is_veterinarian': True})
        context['register'] = form
    return render(request,'secretary/add_users_vet.html', context)


#END USER PROFILE: VET

#USER PROFILE: HEAD VET
def add_headveterinarian_profile(request):
    context = {}
    if request.POST:
        form = AddHeadVetProfileForm(request.POST)
        if form.is_valid():
            form.save()
            email = form.cleaned_data.get('useracc')
            used = User.objects.get(email=email)
            used.is_used=1
            used.save()
            messages.success(request, "Successfully Added!")
            return redirect('user_profile')
        else:
            messages.error(request,  " ")
            context['form'] = form
    else:
        form = AddHeadVetProfileForm()
        context['form'] = form
    return render(request,'secretary/add_headveterinarian_profile.html', context)

def update_headvet_profile(request,pk):
    context = {}
    updprofile = StaffProfile.objects.get(id=pk)
    if updprofile.useracc == None:
        if request.POST:
            form = UpdateHeadVetProfileForm(request.POST,instance=updprofile)
            if form.is_valid():
                email = form.cleaned_data.get('useracc')
                if StaffProfile.objects.exclude(id=pk).filter(useracc=email).exists():
                    messages.error (request,'Account is already used.')
                    return HttpResponseRedirect(reverse('update_headvet_profile', args=[str(pk)]))
                else:
                    form.save()
                    email = form.cleaned_data.get('useracc')
                    used = User.objects.get(email=email)
                    used.is_used=1
                    used.save()
                    messages.success(request,  "Head Veterinarian Profile has been successfully Updated.")
                    return redirect('user_profile')
            else:
                context['form'] = form
                context['updprofile'] = updprofile
        else:
            form = UpdateHeadVetProfileForm(initial ={"useracc":updprofile.useracc,"firstName":updprofile.firstName,"lastName":updprofile.lastName,"gender":updprofile.gender,"contactNum":updprofile.contactNum,"address":updprofile.address})
            context['form'] = form
            context['updprofile'] = updprofile
    else:
        inuse = User.objects.get(email=updprofile.useracc)
        if request.POST:
            form = UpdateHeadVetProfileForm(request.POST,instance=updprofile)
            if form.is_valid():
                email = form.cleaned_data.get('useracc')
                if StaffProfile.objects.exclude(id=pk).filter(useracc=email).exists():
                    messages.error (request,'Account is already used.')
                    return HttpResponseRedirect(reverse('update_headvet_profile', args=[str(pk)]))
                else:
                    inuse.is_used = 0
                    inuse.save()
                    form.save()
                    email = form.cleaned_data.get('useracc')
                    used = User.objects.get(email=email)
                    used.is_used=1
                    used.save()
                    messages.success(request,  "Head Veterinarian Profile has been successfully Updated.")
                    return redirect('user_profile')
            else:
                context['form'] = form
                context['updprofile'] = updprofile
        else:
            form = UpdateHeadVetProfileForm(initial ={"useracc":updprofile.useracc,"firstName":updprofile.firstName,"lastName":updprofile.lastName,"gender":updprofile.gender,"contactNum":updprofile.contactNum,"address":updprofile.address})
            context['form'] = form
            context['updprofile'] = updprofile
    return render(request,'secretary/update_headvet_profile.html', context)

def add_headveterinarian_account(request):
    context ={}
    alluser = User.objects.all
    if request.POST:
        form = HeadVetUserForm(request.POST,initial={'is_headveterinarian': True})
        if form.is_valid():
            form.save()
            email = form.cleaned_data.get('email')
            raw_password = form.cleaned_data.get('password1')
            CustomUsers = authenticate(email=email,password=raw_password)
            CustomUsers.save
            
            return redirect('add_headveterinarian_profile')
        else:
            context['register'] = form
    else:
        form = HeadVetUserForm(initial={'is_headveterinarian': True})
        context['register'] = form
    return render(request,'secretary/add_users_headvet.html', context)

def direct_add_users_headvet(request,pk):
    context ={}
    alluser = User.objects.all
    if request.POST:
        form = HeadVetUserForm(request.POST,initial={'is_headveterinarian': True})
        if form.is_valid():
            form.save()
            email = form.cleaned_data.get('email')
            raw_password = form.cleaned_data.get('password1')
            CustomUsers = authenticate(email=email,password=raw_password)
            CustomUsers.save
            return HttpResponseRedirect(reverse('update_headvet_profile', args=[str(pk)]))
        else:
            context['register'] = form
    else:
        form = HeadVetUserForm(initial={'is_headveterinarian': True})
        context['register'] = form
    return render(request,'secretary/add_users_headvet.html', context)

def delete_vet_profile(request,pk):
    id = request.user.id
    user = User.objects.get(pk=id)
    deleteprofile = StaffProfile.objects.get(id=pk)
    if request.method == "POST":
        if user == deleteprofile.useracc:
            messages.error (request,'Cannot delete User Instance.')
            return render(request, 'secretary/delete_profile.html')
        else:
            deleteprofile.is_deleted = 1
            deleteprofile.date_of_inactive = datetime.today()
            deleteprofile.save()
            messages.error (request,'Successfully Deleted.')
            return redirect('user_profile')
    context ={'deleteprofile':deleteprofile, 'user':user}
    return render(request,'secretary/delete_profile.html', context)

#END USER PROFILE: HEAD VET

#USER PROFILE: SECRETARY
def add_sec_profile(request):
    context = {}
    if request.POST:
        form = AddSecProfileForm(request.POST)
        if form.is_valid():
            form.save()
            email = form.cleaned_data.get('useracc')
            used = User.objects.get(email=email)
            used.is_used=1
            used.save()
            messages.success(request, "Successfully Added")
            return redirect('user_profile')
        else:
            messages.error(request,  " ")
            context['form'] = form
    else:
        form = AddSecProfileForm()
        context['form'] = form
    return render(request,'secretary/add_sec_profile.html', context)

def update_sec_profile(request,pk):
    context = {}
    updprofile = StaffProfile.objects.get(id=pk)
    if updprofile.useracc == None:
        if request.POST:
            form = UpdateSecProfileForm(request.POST,instance=updprofile)
            if form.is_valid():
                email = form.cleaned_data.get('useracc')
                if StaffProfile.objects.exclude(id=pk).filter(useracc=email).exists():
                    messages.error (request,'Account is already used.')
                    return HttpResponseRedirect(reverse('update_sec_profile', args=[str(pk)]))
                else:
                    form.save()
                    email = form.cleaned_data.get('useracc')
                    used = User.objects.get(email=email)
                    used.is_used=1
                    used.save()
                    messages.success(request,  "Secretary Profile has been successfully Updated.")
                    return redirect('user_profile')
            else:
                context['form'] = form
                context['updprofile'] = updprofile
        else:
            form = UpdateSecProfileForm(initial ={"useracc":updprofile.useracc,"firstName":updprofile.firstName,"lastName":updprofile.lastName,"gender":updprofile.gender,"contactNum":updprofile.contactNum,"address":updprofile.address})
            context['form'] = form
            context['updprofile'] = updprofile
    else:
        inuse = User.objects.get(email=updprofile.useracc)
        if request.POST:
            form = UpdateSecProfileForm(request.POST,instance=updprofile)
            if form.is_valid():
                email = form.cleaned_data.get('useracc')
                if StaffProfile.objects.exclude(id=pk).filter(useracc=email).exists():
                    messages.error (request,'Account is already used.')
                    return HttpResponseRedirect(reverse('update_sec_profile', args=[str(pk)]))
                else:
                    inuse.is_used = 0
                    inuse.save()
                    form.save()
                    email = form.cleaned_data.get('useracc')
                    used = User.objects.get(email=email)
                    used.is_used=1
                    used.save()
                    messages.success(request,  "Secretary Profile has been successfully Updated.")
                    return redirect('user_profile')
            else:
                context['form'] = form
                context['updprofile'] = updprofile
        else:
            form = UpdateSecProfileForm(initial ={"useracc":updprofile.useracc,"firstName":updprofile.firstName,"lastName":updprofile.lastName,"gender":updprofile.gender,"contactNum":updprofile.contactNum,"address":updprofile.address})
            context['form'] = form
            context['updprofile'] = updprofile
    return render(request,'secretary/update_sec_profile.html', context)

def add_sec_account(request):
    context ={}
    alluser = User.objects.all
    if request.POST:
        form = SecretaryUserForm(request.POST,initial={'is_secretary': True})
        if form.is_valid():
            form.save()
            email = form.cleaned_data.get('email')
            raw_password = form.cleaned_data.get('password1')
            CustomUsers = authenticate(email=email,password=raw_password)
            CustomUsers.save
            return redirect('add_sec_profile')
        else:
            context['register'] = form
    else:
        form = SecretaryUserForm(initial={'is_secretary': True})
        context['register'] = form
    return render(request,'secretary/add_users_sec.html', context)

def direct_add_users_sec(request,pk):
    context ={}
    alluser = User.objects.all
    if request.POST:
        form = SecretaryUserForm(request.POST,initial={'is_secretary': True})
        if form.is_valid():
            form.save()
            email = form.cleaned_data.get('email')
            raw_password = form.cleaned_data.get('password1')
            CustomUsers = authenticate(email=email,password=raw_password)
            CustomUsers.save
            return HttpResponseRedirect(reverse('update_sec_profile', args=[str(pk)]))
        else:
            context['register'] = form
    else:
        form = SecretaryUserForm(initial={'is_secretary': True})
        context['register'] = form
    return render(request,'secretary/add_users_sec.html', context)

def delete_sec_profile(request,pk):
    id = request.user.id
    user = User.objects.get(pk=id)
    deleteprofile = StaffProfile.objects.get(id=pk)
    if request.method == "POST":
        if user == deleteprofile.useracc:
            messages.error (request,'Cannot delete User Instance.')
            return render(request, 'secretary/delete_profile.html')
        else:
            deleteprofile.is_deleted = 1
            deleteprofile.date_of_inactive = datetime.today()
            deleteprofile.save()
            messages.error (request,'Successfully Deleted.')
            return redirect('user_profile')
    context ={'deleteprofile':deleteprofile, 'user':user}
    return render(request,'secretary/delete_profile.html', context)

#END USER PROFILE: SECRETARY

# SECRETARY 
def secretaryHome(request):
    user = request.user.id
    getProfile = StaffProfile.objects.get(useracc=user)
    print(getProfile.firstName)
    context = {'getProfile':getProfile,'sideb' : 'secretaryHome'}
    return render(request,'secretary/secretaryHome.html',  context) 

def edit_sec_profile(request,pk):
  
    updprofile = StaffProfile.objects.get(id=pk)
    profile_pic = request.FILES.get('image') #bago toh
    context = {'sideb' : 'secretaryHome','profile_pic':profile_pic ,'updprofile':  updprofile}
    if request.POST:
        form = Edit_Staff_Profile(request.POST,instance=updprofile)
        if form.is_valid():
            if profile_pic:#bago toh
                updprofile.user_image = profile_pic #bago toh
            form.save()
            messages.success(request,'Successfully Updated')
            context['form'] = form
        
            return render(request,'secretary/edit_sec_profile.html', context)

        else:
            messages.error(request,' ')
            context['form'] = form
            context['updprofile'] = updprofile
    else:
        form = Edit_Staff_Profile(initial ={"useracc":updprofile.useracc,"firstName":updprofile.firstName,"lastName":updprofile.lastName,"gender":updprofile.gender,"contactNum":updprofile.contactNum,"address":updprofile.address, "user_image":profile_pic})
        context['form'] = form
        context['updprofile'] = updprofile
    return render(request,'secretary/edit_sec_profile.html',context)


def secretaryDashboard(request):
    user = request.user.id
    getProfile = StaffProfile.objects.get(useracc=user)
    today = date.today() 
    param = date.today() +  timedelta(14)
    print(today)
    getSchedToday = scheduling.objects.filter(status="Reserved",date=today)
    getSched = scheduling.objects.filter(date=today).exclude(status="Reserved")
    getSchedarrive = scheduling.objects.filter(date=today,status="Arrived")
    getScheddidnot = scheduling.objects.filter(date=today,status="Did Not Arrive")
    getSchedcancel = scheduling.objects.filter(date=today,status="Cancelled")
    getScheddone = scheduling.objects.filter(date=today,status="Done")
    schedCount = getSchedToday.count()
    arriveCount = getSchedarrive.count()
    didnotCount = getScheddidnot.count()
    cancelCount = getSchedcancel.count()
    doneCount = getScheddone.count()
    nostock = ProductInfo.objects.filter(status="No stock")
    lowstock = ProductInfo.objects.filter(status="Low in Stock")
    expire = Product.objects.filter(expireDate__lte=param)
    
    nostockCount = nostock.count()
    lowstockCount = lowstock.count
    expireCount = expire.count()
    context = {'expireCount':expireCount,'lowstockCount':lowstockCount,'nostockCount': nostockCount,'schedCount':schedCount,'getProfile':getProfile, 'getSched':getSched, 'sideb':'secretaryDashboard','getSchedToday':getSchedToday,'nostock':nostock,'lowstock':lowstock,'expire':expire}
    return render(request,'secretary/secretaryDashboard.html', context) 


def secretaryDashboard_one(request):
    user = request.user.id
    getProfile = StaffProfile.objects.get(useracc=user)
    today = date.today() 
    param = date.today() +  timedelta(14)
    print(today)
    getSchedToday = scheduling.objects.filter(status="Reserved",date=today)
    getSched = scheduling.objects.filter(date=today).exclude(status="Reserved")
    getSchedarrive = scheduling.objects.filter(date=today,status="Arrived")
    getScheddidnot = scheduling.objects.filter(date=today,status="Did Not Arrive")
    getSchedcancel = scheduling.objects.filter(date=today,status="Cancelled")
    getScheddone = scheduling.objects.filter(date=today,status="Done")
    schedCount = getSchedToday.count()
    arriveCount = getSchedarrive.count()
    didnotCount = getScheddidnot.count()
    cancelCount = getSchedcancel.count()
    doneCount = getScheddone.count()
    nostock = ProductInfo.objects.filter(status="No stock")
    lowstock = ProductInfo.objects.filter(status="Low in Stock")
    expire = Product.objects.filter(expireDate__lte=param)
    
    nostockCount = nostock.count()
    lowstockCount = lowstock.count
    expireCount = expire.count()
    context = {'expireCount':expireCount,'lowstockCount':lowstockCount,'nostockCount': nostockCount,'schedCount':schedCount,'getProfile':getProfile, 'getSched':getSched, 'sideb':'secretaryDashboard_one','getSchedToday':getSchedToday,'nostock':nostock,'lowstock':lowstock,'expire':expire}
    return render(request,'secretary/secretaryDashboard_one.html', context) 

def secretaryDashboard_low(request):
    user = request.user.id
    getProfile = StaffProfile.objects.get(useracc=user)
    today = date.today() 
    param = date.today() +  timedelta(14)
    print(today)
    getSchedToday = scheduling.objects.filter(status="Reserved",date=today)
    getSched = scheduling.objects.filter(date=today).exclude(status="Reserved")
    getSchedarrive = scheduling.objects.filter(date=today,status="Arrived")
    getScheddidnot = scheduling.objects.filter(date=today,status="Did Not Arrive")
    getSchedcancel = scheduling.objects.filter(date=today,status="Cancelled")
    getScheddone = scheduling.objects.filter(date=today,status="Done")
    schedCount = getSchedToday.count()
    arriveCount = getSchedarrive.count()
    didnotCount = getScheddidnot.count()
    cancelCount = getSchedcancel.count()
    doneCount = getScheddone.count()
    nostock = ProductInfo.objects.filter(status="No stock")
    lowstock = ProductInfo.objects.filter(status="Low in Stock")
    expire = Product.objects.filter(expireDate__lte=param)
    
    nostockCount = nostock.count()
    lowstockCount = lowstock.count
    expireCount = expire.count()
    context = {'expireCount':expireCount,'lowstockCount':lowstockCount,'nostockCount': nostockCount,'schedCount':schedCount,'getProfile':getProfile, 'getSched':getSched, 'sideb':'secretaryDashboard_low','getSchedToday':getSchedToday,'nostock':nostock,'lowstock':lowstock,'expire':expire}
    return render(request,'secretary/secretaryDashboard_low.html', context) 

def secretaryDashboard_no(request):
    user = request.user.id
    getProfile = StaffProfile.objects.get(useracc=user)
    today = date.today() 
    param = date.today() +  timedelta(14)
    print(today)
    getSchedToday = scheduling.objects.filter(status="Reserved",date=today)
    getSched = scheduling.objects.filter(date=today).exclude(status="Reserved")
    getSchedarrive = scheduling.objects.filter(date=today,status="Arrived")
    getScheddidnot = scheduling.objects.filter(date=today,status="Did Not Arrive")
    getSchedcancel = scheduling.objects.filter(date=today,status="Cancelled")
    getScheddone = scheduling.objects.filter(date=today,status="Done")
    schedCount = getSchedToday.count()
    arriveCount = getSchedarrive.count()
    didnotCount = getScheddidnot.count()
    cancelCount = getSchedcancel.count()
    doneCount = getScheddone.count()
    nostock = ProductInfo.objects.filter(status="No stock")
    lowstock = ProductInfo.objects.filter(status="Low in Stock")
    expire = Product.objects.filter(expireDate__lte=param)
    
    nostockCount = nostock.count()
    lowstockCount = lowstock.count
    expireCount = expire.count()
    context = {'expireCount':expireCount,'lowstockCount':lowstockCount,'nostockCount': nostockCount,'schedCount':schedCount,'getProfile':getProfile, 'getSched':getSched, 'sideb':'secretaryDashboard_no','getSchedToday':getSchedToday,'nostock':nostock,'lowstock':lowstock,'expire':expire}
    return render(request,'secretary/secretaryDashboard_no.html', context) 

def products_secretary(request):
    context={'sideb' : 'secretaryHome'}
    return render(request,'secretary/create/products_secretary.html',  context) 

def pet_record(request):
    id = request.user.id
    user = User.objects.get(pk=id)
    medical = MedicalHistory.objects.filter(is_deleted=False)
    pet = pets.objects.filter(is_deleted=False)
    searchthis_query = request.GET.get('searchthis')
    if searchthis_query != " " and searchthis_query is not None:
        pet = pets.objects.filter(Q(petOwner__firstName__icontains=searchthis_query) | Q(petOwner__lastName__icontains=searchthis_query)| Q(petName=searchthis_query)| Q(petOwner__useracc__email__icontains=searchthis_query)).distinct()
    context={'sideb':'pet_record','pet': pet,'medical':medical,'user':user}
    return render(request,'secretary/create/pet_record.html', context)

 

#def products(request):
  #return render(request, 'secretary/products/products.html', {'sideb': 'products'})

def  add_dropdown_details(request):
    id = request.user.id
    user = User.objects.get(pk=id)
    pet_species = petspecies.objects.filter(is_deleted=False)
    vaccType = vaxType.objects.filter(is_deleted=False)
    prodType = ProductType.objects.filter(is_deleted=False)
    genders= Gender.objects.filter(is_deleted=False)
    pet = pets.objects.filter(is_deleted=False)
    service = services.objects.filter(is_deleted=False)
    breeds = breed.objects.filter(is_deleted=False) 
    context= {'sideb':'add_dropdown_details','vaccType':vaccType,'pet_species':pet_species,'service':service,'prodType':prodType,'genders':genders,'breeds':breeds} 
   
    
    return render(request,'secretary/create/add_dropdown_details.html', context)

def  user_profile(request):
    id = request.user.id
    user = User.objects.get(pk=id)
    pet_species = petspecies.objects.filter(is_deleted=False)
    vaccType = vaxType.objects.filter(is_deleted=False)
    prodType = ProductType.objects.filter(is_deleted=False)
    genders= Gender.objects.filter(is_deleted=False)
    service = services.objects.filter(is_deleted=False)
    breeds = breed.objects.filter(is_deleted=False)
    petowners = User.objects.filter(is_petowner=True,is_active=True)
    veterinarian = User.objects.filter(is_veterinarian=True,is_active=True)
    headvet = User.objects.filter(is_headveterinarian=True,is_active=True)
    secretary = User.objects.filter(is_secretary=True,is_active=True)
    petowner_profile = Profile.objects.filter(useracc__in=petowners,is_deleted=False)   
    veterinarian_profile = StaffProfile.objects.filter(useracc__in=veterinarian,is_deleted=False)  
    head_profile = StaffProfile.objects.filter(useracc__in=headvet,is_deleted=False) 
    secretary_profile = StaffProfile.objects.filter(useracc__in=secretary,is_deleted=False) 
    unconnected_profile= Profile.objects.filter(useracc=None,is_deleted=False)
    medical = MedicalHistory.objects.filter(is_deleted=False)
    pet = pets.objects.filter(is_deleted=False)
    searchthis_query = request.GET.get('searchthis')
    if searchthis_query != " " and searchthis_query is not None:
        pet = pets.objects.filter(Q(petOwner__firstName__icontains=searchthis_query) | Q(petOwner__lastName__icontains=searchthis_query)| Q(petName=searchthis_query)| Q(petOwner__useracc__email__icontains=searchthis_query)).distinct()
    context={'sideb' : 'user_profile','petowners':petowners, 'veterinarian': veterinarian, 'headvet': headvet, 'secretary': secretary, 'user':user,'pet_species':pet_species,'vaccType':vaccType,'pet': pet,'service':service,'prodType':prodType,'genders':genders,'breeds':breeds,'petowner_profile':petowner_profile,'unconnected_profile':unconnected_profile,'veterinarian_profile':veterinarian_profile,'head_profile':head_profile,'secretary_profile':secretary_profile,'medical':medical}
    return render(request,'secretary/create/user_profile.html', context)

def direct_add_medical_history(request,pk):
    
    #all_meds = MedicalHistory.objects.get(is_deleted=False)
    all_meds = MedicalHistory.objects.all()
    addtopet = pets.objects.get(id=pk)
    if request.POST:
        form = SecMedHistory(request.POST,initial={'pet': addtopet})
        if form.is_valid():
            form.save()
            x = form.save()
            param = x.id
            codes= "PT" + "%x" % random.randint(0, 0xFFFFF)
            for med in all_meds:
                if med.code == codes:
                    codes= "PT" + "%x" % random.randint(0, 0xFFFFF)
            x.code=codes
            x.save()
            messages.success(request, "Pet Record has been successfully created.")
            return HttpResponseRedirect(reverse('add_medical_service', args=[str(param)]))
        else:
            context['form'] = form
    else:
        form = SecMedHistory(initial ={"pet":addtopet})
        

    context = {'sideb':'direct_add_medical_history', 'form':form}
    return render(request,'secretary/create/add_medical_history.html',context)

def add_medical_history(request):
    context = {'sideb':'add_medical_history'}
    all_meds = MedicalHistory.objects.get(is_deleted=False)
    if request.POST:
        form = SecMedHistory(request.POST)
        if form.is_valid():
            form.save()
            x = form.save()
            param = x.id
            codes= "PT" + "%x" % random.randint(0, 0xFFFFF)
            for med in all_meds:
                if med.code == codes:
                    codes= "PT" + "%x" % random.randint(0, 0xFFFFF)
            x.code=codes
            x.save()
            
            return HttpResponseRedirect(reverse('add_medical_service', args=[str(param)]))
        else:
            context['form'] = form
    else:
        form = SecMedHistory()
        context['form'] = form
    return render(request,'secretary/create/add_medical_history.html',context)

def update_medical_history(request,pk):
    context = {'sideb':'update_medical_history'}
    medHist = MedicalHistory.objects.get(id=pk)
    if request.POST:
        form = MedHistory(request.POST,instance=medHist)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('add_medical_service', args=[str(pk)]))
        else:
            context['form'] = form
    else:
        form = MedHistory(initial ={'code':medHist.code,'pet':medHist.pet,'date':medHist.date,'weight':medHist.weight,'symptoms':medHist.symptoms,'treatment':medHist.treatment,'prescription':medHist.prescription,'instruction':medHist.instruction,'dateofReturn':medHist.dateofReturn,'reason':medHist.reason,'vet':medHist.vet})
        context['form'] = form
    return render(request,'secretary/create/add_medical_history.html',context)

def view_all_medical_history(request,pk):
    param = pets.objects.get(id=pk)
    records = MedicalHistory.objects.filter(pet=param)
    context = {'sideb':'view_all_medical_history','records':records,'param':param}
    return render(request,'secretary/create/view_all_medical_history.html',context)

def view_medical_history(request,pk):
    medHist = MedicalHistory.objects.get(id=pk)
    vaccination =vaccineHistory.objects.filter(medHistory=medHist,is_deleted=False)
    labtest =labHistory.objects.filter(medHistory=medHist,is_deleted=False)
    availed = serviceHistory.objects.filter(medHistory=medHist,is_deleted=False)
    context={'sideb':'view_medical_history','vaccination':vaccination,'labtest':labtest,'availed':availed,'medHist':medHist}
    return render(request,'secretary/create/view_medical_history.html',context)

def delete_history(request,pk):
    med = MedicalHistory.objects.get(id=pk)
    if request.method == "POST":
        med.is_deleted = 1
        med.date_of_delete = datetime.today()
        med.save()
        return redirect('pet_record')
    context ={'sideb':'delete_history','med':med}
    return render(request,'secretary/create/delete_history.html',context)

def add_medical_service(request,pk):
    medHist = MedicalHistory.objects.get(id=pk)
    vaccination =vaccineHistory.objects.filter(medHistory=medHist,is_deleted=False)
    labtest =labHistory.objects.filter(medHistory=medHist,is_deleted=False)
    availed = serviceHistory.objects.filter(medHistory=medHist,is_deleted=False)
    context={'sideb':'add_medical_service', 'vaccination':vaccination,'labtest':labtest,'availed':availed,'medHist':medHist}
    return render(request,'secretary/create/add_medical_service.html',context)

def availed_service(request,pk):
    context = {'sideb':'availed_service',}
    all_service = serviceHistory.objects.all()
    medHist = MedicalHistory.objects.get(id=pk)
    if request.POST:
        form = AddAvailedService(request.POST,initial={'medHistory': medHist,'dateofService':medHist.date})
        if form.is_valid():
            services = form.cleaned_data.get('service')
            if serviceHistory.objects.filter(medHistory=medHist).filter(service=services).exists():
                messages.error(request,"Service is already added")
                return HttpResponseRedirect(reverse('availed_service', args=[str(pk)]))
            else:
                x = form.save()
                codes= "GS" + "%x" % random.randint(0, 0xFFFFF)
                for med in all_service:
                    if med.code == codes:
                        codes= "GS" + "%x" % random.randint(0, 0xFFFFF)
                x.code=codes
                x.save()
                messages.success(request,'Successfully Added')
                return HttpResponseRedirect(reverse('add_medical_service', args=[str(pk)]))
    else:
        form = AddAvailedService(initial ={"medHistory":medHist,'dateofService':medHist.date})
        context['form'] = form
        context['medHist'] = medHist
    return render(request,'secretary/create/availed_service.html',context)

def edit_availed_service(request,pk,pk2):
    context = {'sideb':'edit_availed_service',}
    medHist = MedicalHistory.objects.get(id=pk)
    serve= serviceHistory.objects.get(id=pk2)
    if request.POST:
        form = AvailedService(request.POST,instance=serve)
        if form.is_valid():
            services = form.cleaned_data.get('service')
            if serviceHistory.objects.filter(medHistory=medHist).exclude(id=pk2).filter(service=services).exists():
                messages.error(request,"Service is already added")
                return HttpResponseRedirect(reverse('add_medical_service', args=[str(pk)]))
            else:
                x = form.save()
                messages.success(request,'Successfully Updated!')
                return HttpResponseRedirect(reverse('add_medical_service', args=[str(pk)]))
    else:
        form = AvailedService(initial ={'code':serve.code,'medHistory':serve.medHistory,'dateofService':serve.dateofService,'service':serve.service,'interpretation':serve.interpretation,'vet':serve.vet})
        context['form'] = form
        context['medHist'] = medHist
        context['serve'] = serve
    return render(request,'secretary/create/availed_service.html',context)

def availed_labTest(request,pk):
    context = {'sideb':'availed_labTest',}
    all_lab = labHistory.objects.all()
    medHist = MedicalHistory.objects.get(id=pk)
    if request.POST:
        form = AddLabTestForm(request.POST,initial={'medHistory': medHist,'dateofService':medHist.date})
        if form.is_valid():
            services = form.cleaned_data.get('service')
            if labHistory.objects.filter(medHistory=medHist).filter(service=services).exists():
                messages.error(request,"Service is already added")
                return HttpResponseRedirect(reverse('add_medical_service', args=[str(pk)]))
            else:
                x = form.save()
                codes= "LT" + "%x" % random.randint(0, 0xFFFFF)
                for med in all_lab:
                    if med.code == codes:
                        codes= "LT" + "%x" % random.randint(0, 0xFFFFF)
                x.code=codes
                x.save()
                messages.success(request,'Successfully Added')
                return HttpResponseRedirect(reverse('add_medical_service', args=[str(pk)]))
    else:
        form = AddLabTestForm(initial ={"medHistory":medHist,'dateofService':medHist.date})
        context['form'] = form
        context['medHist'] = medHist
    return render(request,'secretary/create/availed_labTest.html',context)

def edit_lab_test(request,pk,pk2):
    context = {'sideb':'edit_lab_test',}
    medHist = MedicalHistory.objects.get(id=pk)
    serve= labHistory.objects.get(id=pk2)
    if request.POST:
        form = LabTestForm(request.POST,instance=serve)
        if form.is_valid():
            services = form.cleaned_data.get('service')
            if labHistory.objects.filter(medHistory=medHist).exclude(id=pk2).filter(service=services).exists():
                messages.error(request,"Service is already added")
                return HttpResponseRedirect(reverse('add_medical_service', args=[str(pk)]))
            else:
                x = form.save()
                messages.success(request,'Successfully Updated!')
                return HttpResponseRedirect(reverse('add_medical_service', args=[str(pk)]))
    else:
        form = LabTestForm(initial ={'code':serve.code,"medHistory":serve.medHistory,'dateofService':serve.dateofService,'service':serve.service,'interpretation':serve.interpretation,'vet':serve.vet,'dateofResult':serve.dateofResult})
        context['form'] = form
        context['medHist'] = medHist
        context['serve'] = serve
    return render(request,'secretary/create/availed_labTest.html',context)


def availed_vaccination(request,pk):
    context = {'sideb':'availed_vaccination',}
    all_vacc = vaccineHistory.objects.all()
    medHist = MedicalHistory.objects.get(id=pk)
    if request.POST:
        form = AddVaccineServiceForm(request.POST,initial={'medHistory': medHist,'dateofService':medHist.date})
        if form.is_valid():
            services = form.cleaned_data.get('service')
            vaccs = form.cleaned_data.get('vaccine')
            print(vaccs.id)
            if vaccineHistory.objects.filter(medHistory=medHist).filter(service=services).exists():
                messages.error(request,"Service is already added")
                return HttpResponseRedirect(reverse('add_medical_service', args=[str(pk)]))
            else:
                
                vaccine = Product.objects.get(id=vaccs.id)
                vaccine.quantity = vaccine.quantity - 1
                vaccine.save()
                displayproducts = ProductInfo.objects.filter(is_deleted = 0)
                for item in displayproducts:
                    prod = Product.objects.filter(product=item)
                    total=0
                    item.total_quantity = total
                    item.save()
                    for quantity in prod:
                        print(quantity)
                        value = quantity.quantity + total
                        total = value
                        item.total_quantity = total
                        item.save()
                x = form.save()
                codes= "VS" + "%x" % random.randint(0, 0xFFFFF)
                for med in all_vacc:
                    if med.code == codes:
                        codes= "VS" + "%x" % random.randint(0, 0xFFFFF)
                x.code=codes
                x.save()
                messages.success(request,'Successfully Added')
                return HttpResponseRedirect(reverse('add_medical_service', args=[str(pk)]))
        else:
            context['form'] = form

    else:
        form = AddVaccineServiceForm(initial ={"medHistory":medHist,'dateofService':medHist.date})
        context['form'] = form
        context['medHist'] = medHist
    return render(request,'secretary/create/vaccinationForm.html',context)

def edit_vaccination(request,pk,pk2):
    context = {'sideb':'edit_vaccination',}
    medHist = MedicalHistory.objects.get(id=pk)
    serve= vaccineHistory.objects.get(id=pk2)
    if request.POST:
        form = VaccineServiceForm(request.POST,instance=serve)
        if form.is_valid():
            services = form.cleaned_data.get('service')
            vaccs = form.cleaned_data.get('vaccine')
            if vaccineHistory.objects.filter(medHistory=medHist).exclude(id=pk2).filter(service=services).exists():
                messages.error(request,"Service is already added!")
                return HttpResponseRedirect(reverse('add_medical_service', args=[str(pk)]))
            else:
                x = form.save()
                messages.success(request,'Successfully Updated!')
                return HttpResponseRedirect(reverse('add_medical_service', args=[str(pk)]))
    else:
        form = VaccineServiceForm(initial ={'code':serve.code,"medHistory":serve.medHistory,'dateofService':serve.dateofService,'service':serve.service,'interpretation':serve.interpretation,'vet':serve.vet,'dateofReturn':serve.dateofReturn,'reason':serve.reason})
        context['form'] = form
        context['medHist'] = medHist
        context['serve'] = serve
    return render(request,'secretary/create/vaccinationForm.html',context)


def delete_availed_service(request,pk,pk2):
    medHist = MedicalHistory.objects.get(id=pk)
    med = serviceHistory.objects.get(id=pk2)
    if request.method == "POST":
        med.is_deleted = 1
        med.date_of_delete = datetime.today()
        med.save()
        return HttpResponseRedirect(reverse('add_medical_service', args=[str(pk)]))
    context ={'sideb':'delete_availed_service','med':med,'medHist':medHist}
    return render(request,'secretary/create/delete_availed_service.html',context)

def delete_availed_lab(request,pk,pk2):
    medHist = MedicalHistory.objects.get(id=pk)
    med = labHistory.objects.get(id=pk2)
    if request.method == "POST":
        med.is_deleted = 1
        med.date_of_delete = datetime.today()
        med.save()
        return HttpResponseRedirect(reverse('add_medical_service', args=[str(pk)]))
    context ={'sideb':'delete_availed_lab','med':med,'medHist':medHist}
    return render(request,'secretary/create/delete_availed_service.html',context)

def delete_availed_vaccine(request,pk,pk2):
    medHist = MedicalHistory.objects.get(id=pk)
    med = vaccineHistory.objects.get(id=pk2)
    if request.method == "POST":
        med.is_deleted = 1
        med.date_of_delete = datetime.today()
        med.save()
        return HttpResponseRedirect(reverse('add_medical_service', args=[str(pk)]))
    context ={'sideb':'delete_availed_vaccine','med':med,'medHist':medHist}
    return render(request,'secretary/create/delete_availed_service.html',context)





# PET OWNER

def petOwnerHome(request):
    user = request.user.id
    getProfile = Profile.objects.get(useracc=user)
    print(getProfile.firstName)
    context = {'getProfile':getProfile,'sideb':'petOwnerHome'}
    return render(request,'petowner/petOwnerHome.html',context)



def edit_owner_profile(request,pk):
   
    updprofile = Profile.objects.get(id=pk)
    profile_pic = request.FILES.get('image') #bago toh
    context = {'sideb' : 'petOwnerHome','profile_pic':profile_pic ,'updprofile':  updprofile}
    if request.POST:
        form = Edit_PetOwner_Profile(request.POST,instance=updprofile)
        if form.is_valid():
            if profile_pic:#bago toh
                updprofile.user_image = profile_pic #bago toh
            form.save()
            messages.success(request,'Successfully Updated')
            context['form'] = form
        
            return render(request,'petowner/edit_profile.html', context)
        else:
            messages.error(request,' ')
            context['form'] = form
            context['updprofile'] = updprofile
    else:
        form = Edit_PetOwner_Profile(initial ={"useracc":updprofile.useracc,"firstName":updprofile.firstName,"lastName":updprofile.lastName,"gender":updprofile.gender,"contactNum":updprofile.contactNum,"address":updprofile.address, "user_image":profile_pic})
        context['form'] = form
        context['updprofile'] = updprofile
    return render(request,'petowner/edit_profile.html',context)

def petOwnerDashBoard(request):
    user = request.user
    getProfile = Profile.objects.get(useracc=user)
    all_pets = pets.objects.filter(petOwner=getProfile.id)
    schedules = scheduling.objects.filter(pet__in=all_pets,status="Reserved")
    sched_count = scheduling.objects.filter(pet__in=all_pets,status="Reserved").count()
    charge_in = chargeSlip.objects.filter(is_deleted=False,petowner=getProfile).exclude(status="Fully Paid")
    charge_count = chargeSlip.objects.filter(is_deleted=False,petowner=getProfile).exclude(status="Fully Paid").count()
    petcount = all_pets.count()
    context = {'sched_count':sched_count,'charge_count':charge_count,'sideb':'petOwnerDashBoard','getProfile':getProfile,'all_pets':all_pets,'petcount':petcount,'schedules':schedules,'charge_in':charge_in}
    return render(request,'petowner/petownerDashboard.html',context)

def petOwnerDashBoard_one(request):
    user = request.user
    getProfile = Profile.objects.get(useracc=user)
    all_pets = pets.objects.filter(petOwner=getProfile.id)
    schedules = scheduling.objects.filter(pet__in=all_pets,status="Reserved")
    sched_count = scheduling.objects.filter(pet__in=all_pets,status="Reserved").count()
    charge_in = chargeSlip.objects.filter(is_deleted=False,petowner=getProfile).exclude(status="Fully Paid")
    charge_count = chargeSlip.objects.filter(is_deleted=False,petowner=getProfile).exclude(status="Fully Paid").count()
    petcount = all_pets.count()
    context = {'sched_count':sched_count,'charge_count':charge_count,'sideb':'petOwnerDashBoard','getProfile':getProfile,'all_pets':all_pets,'petcount':petcount,'schedules':schedules,'charge_in':charge_in}
    return render(request,'petowner/petownerDashboard_one.html',context)

def services_petOwner(request):
    return render(request,'petowner/services_petOwner.html', {'sideb' : 'services_petOwner'})
    
def view_pet_history(request,pk):
    param = pets.objects.get(id=pk)
    records = MedicalHistory.objects.filter(pet=param)
    context = {'sideb':'view_pet_history','records':records,'param':param}
    return render(request,'petowner/view_pet_history.html',context)


def edit_pet_pfp(request, pk): #bago toh pet 2
    context = {}
    param = pets.objects.get(id=pk)
    records = MedicalHistory.objects.filter(pet=param)
    if request.POST:
        pet_image = request.FILES.get('image')
        param.pet_image = pet_image #bago toh
        param.save()
        messages.success(request,'Successfully Updated')
        return HttpResponseRedirect(reverse('view_pet_history', args=[str(pk)]))
    else:
        context['param'] = param
    context = {'sideb':'edit_pet_pfp','param':param, 'records':records}
    return render(request,'petowner/edit_pet_pfp.html', context)


def owner_view_per_record(request,pk):
    medHist = MedicalHistory.objects.get(id=pk)
    vaccination =vaccineHistory.objects.filter(medHistory=medHist,is_deleted=False)
    labtest =labHistory.objects.filter(medHistory=medHist,is_deleted=False)
    availed = serviceHistory.objects.filter(medHistory=medHist,is_deleted=False)
    context={'sideb':'owner_view_per_record','vaccination':vaccination,'labtest':labtest,'availed':availed,'medHist':medHist}
    return render(request,'petowner/owner_view_per_record.html',context)



# HEAD VETERINARIAN
def headVetHome(request):
    user = request.user.id
    getProfile = StaffProfile.objects.get(useracc=user)
    context={'sideb':'headVetHome','getProfile':getProfile}
    return render(request,'headveterinarian/headVetHome.html',context)

def headvetDashboard(request):
    user = request.user.id
    today = date.today() 
    param = date.today() +  timedelta(14)
    getProfile = StaffProfile.objects.get(useracc=user)
    slot = schedule_slot.objects.filter(vet=getProfile)
    getSchedToday = scheduling.objects.filter(status="Reserved",date=today)
    getSchedToday_cancel = scheduling.objects.filter(slot__in=slot,date=today).exclude(status="Cancelled")
    getSched = scheduling.objects.filter(date=today).exclude(status="Reserved")
    getSchedarrive = scheduling.objects.filter(date=today,status="Arrived",slot__in=slot)
    getScheddone = scheduling.objects.filter(date=today,status="Done",slot__in=slot)
    schedCount = getSchedToday.count()
    arriveCount = getSchedarrive.count()
    doneCount = getScheddone.count()
    nostock = ProductInfo.objects.filter(status="No stock")
    lowstock = ProductInfo.objects.filter(status="Low in Stock")
    expire = Product.objects.filter(expireDate__lte=param)
    context = {'doneCount':doneCount,'arriveCount':arriveCount,'schedCount':schedCount,'getSchedToday_cancel':getSchedToday_cancel,'getProfile':getProfile, 'getSched':getSched, 'sideb':'headvetDashboard','getSchedToday':getSchedToday,'nostock':nostock,'lowstock':lowstock,'expire':expire,'getSchedarrive':getSchedarrive,'getScheddone':getScheddone}
    return render(request,'headveterinarian/vetDashboard.html', context) 


def headvetDashboard_one(request):
    user = request.user.id
    today = date.today() 
    param = date.today() +  timedelta(14)
    getProfile = StaffProfile.objects.get(useracc=user)
    slot = schedule_slot.objects.filter(vet=getProfile)
    getSchedToday = scheduling.objects.filter(status="Reserved",date=today)
    getSchedToday_cancel = scheduling.objects.filter(slot__in=slot,date=today).exclude(status="Cancelled")
    getSched = scheduling.objects.filter(date=today).exclude(status="Reserved")
    getSchedarrive = scheduling.objects.filter(date=today,status="Arrived",slot__in=slot)
    getScheddone = scheduling.objects.filter(date=today,status="Done",slot__in=slot)
    schedCount = getSchedToday.count()
    arriveCount = getSchedarrive.count()
    doneCount = getScheddone.count()
    nostock = ProductInfo.objects.filter(status="No stock")
    lowstock = ProductInfo.objects.filter(status="Low in Stock")
    expire = Product.objects.filter(expireDate__lte=param)
    context = {'doneCount':doneCount,'arriveCount':arriveCount,'schedCount':schedCount,'getSchedToday_cancel':getSchedToday_cancel,'getProfile':getProfile, 'getSched':getSched, 'sideb':'headvetDashboard','getSchedToday':getSchedToday,'nostock':nostock,'lowstock':lowstock,'expire':expire,'getSchedarrive':getSchedarrive,'getScheddone':getScheddone}
    return render(request,'headveterinarian/vetDashboard_one.html', context) 


def headdone_pet(request,pk):
    user = request.user.id
    getSched = scheduling.objects.get(id=pk)
    getSched.status = "Done"
    getSched.save()
    context = {'getSched':getSched}
    return HttpResponseRedirect(reverse('head_create_pet_record', args=[str(getSched.pet.id)]))

    

def edit_headvet_profile(request,pk):

    updprofile = StaffProfile.objects.get(id=pk)
    profile_pic = request.FILES.get('image') #bago toh
    context = {'sideb':'edit_headvet_profile','profile_pic':profile_pic ,'updprofile':  updprofile}
    if request.POST:
        form = Edit_Staff_Profile(request.POST,instance=updprofile)
        if form.is_valid():
            if profile_pic:#bago toh
                updprofile.user_image = profile_pic #bago toh
            form.save()
            messages.success(request,'Successfully Updated')
            context['form'] = form
        
            return render(request,'headveterinarian/edit_headvet_profile.html', context)
        else:
            messages.error(request,' ')
            context['form'] = form
            context['updprofile'] = updprofile
    else:
        form = Edit_Staff_Profile(initial ={"useracc":updprofile.useracc,"firstName":updprofile.firstName,"lastName":updprofile.lastName,"gender":updprofile.gender,"contactNum":updprofile.contactNum,"address":updprofile.address, "user_image":profile_pic})
        context['form'] = form
        context['updprofile'] = updprofile
    return render(request,'headveterinarian/edit_headvet_profile.html',context)

def head_patientsTab(request):
    allpets = pets.objects.filter(is_deleted=False)
    searchthis_query = request.GET.get('searchthis')
    if searchthis_query != " " and searchthis_query is not None:
        allpets = pets.objects.filter(Q(petOwner__firstName__icontains=searchthis_query) | Q(petOwner__lastName__icontains=searchthis_query)| Q(petName=searchthis_query)| Q(petOwner__useracc__email__icontains=searchthis_query)).distinct()
    context={'sideb':'head_patientsTab','allpets':allpets}
    return render(request,'headveterinarian/patients.html',context)

def head_vet_pet_create_view(request):
    
    form = AddPetForm()
    if request.method == 'POST':
        form = AddPetForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Pet has been successfully added!")
            return redirect('head_patientsTab')
    context={'sideb':'head_vet_add_pets', 'form': form}
    return render(request, 'headveterinarian/vet_pet_create.html', context)

def head_create_pet_record(request,pk):
    context={'sideb':'head_vet_add_pets'}
    id = request.user.id
    all_meds = MedicalHistory.objects.all()
    user = User.objects.get(pk=id)
    getuser = StaffProfile.objects.get(useracc=user.id)
    addtopet = pets.objects.get(id=pk)
    now = date.today()
    if request.POST:
        form = MedHistory(request.POST,initial={'pet': addtopet,'date':now,'vet':getuser})
        if form.is_valid():
            form.save()
            x = form.save()
            param = x.id
            codes= "PT" + "%x" % random.randint(0, 0xFFFFF)
            for med in all_meds:
                if med.code == codes:
                    codes= "PT" + "%x" % random.randint(0, 0xFFFFF)
            x.code=codes
            x.save()
            return HttpResponseRedirect(reverse('head_vet_add_medical_service', args=[str(param)]))
        else:
            context['form'] = form
    else:
        form = MedHistory(initial ={"pet":addtopet,'date':now,'vet':getuser})
        context['form'] = form
    return render(request,'headveterinarian/create_pet_record.html',context)

def head_view_record(request,pk):
    param = pets.objects.get(id=pk)
    records = MedicalHistory.objects.filter(pet=param)
    context = {'sideb':'head_view_record','records':records,'param':param}

    return render(request,'headveterinarian/view_record.html',context)

def head_view_per_record(request,pk):
    medHist = MedicalHistory.objects.get(id=pk)
    vaccination =vaccineHistory.objects.filter(medHistory=medHist,is_deleted=False)
    labtest =labHistory.objects.filter(medHistory=medHist,is_deleted=False)
    availed = serviceHistory.objects.filter(medHistory=medHist,is_deleted=False)
    context={'sideb':'head_view_per_record','vaccination':vaccination,'labtest':labtest,'availed':availed,'medHist':medHist}
    return render(request,'headveterinarian/view_per_record.html',context)

def head_vet_update_medical_history(request,pk):
    context={'sideb':'head_vet_update_medical_history'}
    medHist = MedicalHistory.objects.get(id=pk)
    if request.POST:
        form = MedHistory(request.POST,instance=medHist)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('head_view_per_record', args=[str(pk)]))
        else:
            context['form'] = form
    else:
        form = MedHistory(initial ={'code':medHist.code,'pet':medHist.pet,'date':medHist.date,'weight':medHist.weight,'symptoms':medHist.symptoms,'treatment':medHist.treatment,'prescription':medHist.prescription,'instruction':medHist.instruction,'dateofReturn':medHist.dateofReturn,'reason':medHist.reason,'vet':medHist.vet})
        context['form'] = form
   
    return render(request,'headveterinarian/create_pet_record.html',context)


def head_vet_add_medical_service(request,pk):
    user=request.user.id
    all_chargeslip=chargeSlip.objects.all()
    getuser = StaffProfile.objects.get(useracc=user)
    medHist = MedicalHistory.objects.get(id=pk)
    vaccination =vaccineHistory.objects.filter(medHistory=medHist)
    labtest =labHistory.objects.filter(medHistory=medHist)
    availed = serviceHistory.objects.filter(medHistory=medHist)
    all_service = serviceHistory.objects.filter(medHistory=pk)
    all_lab = labHistory.objects.filter(medHistory=pk)
    all_vaccine = vaccineHistory.objects.filter(medHistory=pk)
    if request.POST:
        add = chargeSlip(petowner=medHist.pet.petOwner,date=datetime.today(),staff=getuser)
        add.save()
        x = chargeSlip.objects.get(id=add.id)
        codes= "CS" + "%x" % random.randint(0, 0xFFFFF)
        for charge in all_chargeslip:
            if charge.code == codes:
                codes= "CS" + "%x" % random.randint(0, 0xFFFFF)
        x.code=codes
        x.save()
        for service in all_service:
            invoice = serviceInvoice(chargeslip=x,servicecode=service.code,service=service.service,total=service.service.price)
            invoice.save()   
        for service in all_lab:
            invoice = serviceInvoice(chargeslip=x,servicecode=service.code,service=service.service,total=service.service.price)
            invoice.save()   
        for service in all_vaccine:
            invoice = serviceInvoice(chargeslip=x,servicecode=service.code,service=service.service,total=service.service.price)
            invoice.save()   
        return HttpResponseRedirect(reverse('head_serviceInvoice', args=[str(x.id)]))
    context={'sideb':'head_vet_add_medical_service','vaccination':vaccination,'labtest':labtest,'availed':availed,'medHist':medHist}
    return render(request,'headveterinarian/vet_add_medical_service.html',context)

def head_vet_availed_service(request,pk):
    context = {'sideb':'head_vet_availed_service'}

    all_service = serviceHistory.objects.all()
    medHist = MedicalHistory.objects.get(id=pk)
    if request.POST:
        form = AvailedService(request.POST,initial={'medHistory': medHist,'dateofService':medHist.date,'vet':medHist.vet})
        if form.is_valid():
            services = form.cleaned_data.get('service')
            if serviceHistory.objects.filter(medHistory=medHist).filter(service=services).exists():
                messages.error(request,"Service is already added")
                return HttpResponseRedirect(reverse('head_vet_add_medical_service', args=[str(pk)]))
            else:
                x = form.save()
                codes= "GS" + "%x" % random.randint(0, 0xFFFFF)
                for med in all_service:
                    if med.code == codes:
                        codes= "GS" + "%x" % random.randint(0, 0xFFFFF)
                x.code=codes
                x.save()
                return HttpResponseRedirect(reverse('head_vet_add_medical_service', args=[str(pk)]))
        else:
            context['form'] = form
    else:
        form = AvailedService(initial ={"medHistory":medHist,'dateofService':medHist.date,'vet':medHist.vet})
        context['form'] = form
        context['medHist'] = medHist
    
    return render(request,'headveterinarian/vet_availed_service.html',context)

    
def head_vet_edit_availed_service(request,pk,pk2):
    context = {'sideb':'head_vet_edit_availed_service'}
    medHist = MedicalHistory.objects.get(id=pk)
    serve= serviceHistory.objects.get(id=pk2)
    if request.POST:
        form = AvailedService(request.POST,instance=serve)
        if form.is_valid():
            services = form.cleaned_data.get('service')
            if serviceHistory.objects.filter(medHistory=medHist).exclude(id=pk2).filter(service=services).exists():
                messages.error(request,"Service is already added")
                return HttpResponseRedirect(reverse('head_vet_add_medical_service', args=[str(pk)]))
            else:
                x = form.save()
                return HttpResponseRedirect(reverse('head_vet_add_medical_service', args=[str(pk)]))
        else:
            context['form'] = form
    else:
        form = AvailedService(initial ={'code':serve.code,"medHistory":serve.medHistory,'dateofService':serve.dateofService,'service':serve.service,'interpretation':serve.interpretation,'vet':serve.vet})
        context['form'] = form
        context['medHist'] = medHist
        context['serve'] = serve
    return render(request,'headveterinarian/vet_availed_service.html',context)

def head_vet_availed_labTest(request,pk):
    context = {'sideb':'head_vet_availed_labTest'}
    all_lab=labHistory.objects.all()
    medHist = MedicalHistory.objects.get(id=pk)
    if request.POST:
        form = LabTestForm(request.POST,initial={'medHistory': medHist,'dateofService':medHist.date,'vet':medHist.vet})
        if form.is_valid():
            services = form.cleaned_data.get('service')
            if labHistory.objects.filter(medHistory=medHist).filter(service=services).exists():
                messages.error(request,"Service is already added")
                return HttpResponseRedirect(reverse('head_vet_add_medical_service', args=[str(pk)]))
            else:
                x = form.save()
                codes= "LT" + "%x" % random.randint(0, 0xFFFFF)
                for charge in all_lab:
                    if charge.code == codes:
                        codes= "LT" + "%x" % random.randint(0, 0xFFFFF)
                x.code=codes
                x.save()
                return HttpResponseRedirect(reverse('head_vet_add_medical_service', args=[str(pk)]))
        else:
            context['form'] = form
    else:
        form = LabTestForm(initial ={"medHistory":medHist,'dateofService':medHist.date,'vet':medHist.vet})
        context['form'] = form
        context['medHist'] = medHist
    return render(request,'headveterinarian/vet_availed_labTest.html',context)

def head_vet_edit_lab_test(request,pk,pk2):
    context = {'sideb':'head_vet_edit_lab_test'}
    medHist = MedicalHistory.objects.get(id=pk)
    serve= labHistory.objects.get(id=pk2)
    if request.POST:
        form = LabTestForm(request.POST,instance=serve)
        if form.is_valid():
            services = form.cleaned_data.get('service')
            if labHistory.objects.filter(medHistory=medHist).exclude(id=pk2).filter(service=services).exists():
                messages.error(request,"Service is already added")
                return HttpResponseRedirect(reverse('head_vet_add_medical_service', args=[str(pk)]))
            else:
                x = form.save()
                return HttpResponseRedirect(reverse('head_vet_add_medical_service', args=[str(pk)]))
    else:
        form = LabTestForm(initial ={'code':serve.code,"medHistory":serve.medHistory,'dateofService':serve.dateofService,'service':serve.service,'interpretation':serve.interpretation,'vet':serve.vet,'dateofResult':serve.dateofResult})
        context['form'] = form
        context['medHist'] = medHist
        context['serve'] = serve
    return render(request,'headveterinarian/vet_availed_labTest.html',context)

def head_vet_availed_vaccination(request,pk):
    context = {'sideb':'head_vet_availed_vaccination'}
    all_vacc = vaccineHistory.objects.all()
    medHist = MedicalHistory.objects.get(id=pk)
    if request.POST:
        form = VaccineServiceForm(request.POST,initial={'medHistory': medHist,'dateofService':medHist.date,'vet':medHist.vet})
        if form.is_valid():
            services = form.cleaned_data.get('service')
            vaccs = form.cleaned_data.get('vaccine')
            print(vaccs.id)
            if vaccineHistory.objects.filter(medHistory=medHist).filter(service=services).exists():
                messages.error(request,"Service is already added")
                return HttpResponseRedirect(reverse('head_vet_add_medical_service', args=[str(pk)]))
            else:
                vaccine = Product.objects.get(id=vaccs.id)
                vaccine.quantity = vaccine.quantity - 1
                vaccine.save()
                displayproducts = ProductInfo.objects.filter(is_deleted = 0)
                for item in displayproducts:
                    prod = Product.objects.filter(product=item)
                    total=0
                    item.total_quantity = total
                    item.save()
                    for quantity in prod:
                        print(quantity)
                        value = quantity.quantity + total
                        total = value
                        item.total_quantity = total
                        item.save()
                x = form.save()
                codes= "VS" + "%x" % random.randint(0, 0xFFFFF)
                for charge in all_vacc:
                    if charge.code == codes:
                        codes= "VS" + "%x" % random.randint(0, 0xFFFFF)
                x.code=codes
                x.save()
                return HttpResponseRedirect(reverse('head_vet_add_medical_service', args=[str(pk)]))
        else:
            context['form'] = form
    else:
        form = VaccineServiceForm(initial ={"medHistory":medHist,'dateofService':medHist.date,'vet':medHist.vet})
        context['form'] = form
        context['medHist'] = medHist
    return render(request,'headveterinarian/vet_vaccinationForm.html',context)

def head_vet_edit_vaccination(request,pk,pk2):
    context = {'sideb':'head_vet_edit_vaccination'}
    medHist = MedicalHistory.objects.get(id=pk)
    serve= vaccineHistory.objects.get(id=pk2)
    x = Product.objects.get(id=serve.vaccine.id)
    if request.POST:
        form = VaccineServiceForm(request.POST,instance=serve)
        if form.is_valid():
            services = form.cleaned_data.get('service')
            if vaccineHistory.objects.filter(medHistory=medHist).exclude(id=pk2).filter(service=services).exists():
                messages.error(request,"Service is already added")
                return HttpResponseRedirect(reverse('head_vet_add_medical_service', args=[str(pk)]))
            else:
                x.quantity = x.quantity + 1
                x.save()
                form.save()
                vaccs = form.cleaned_data.get('vaccine')
                y = Product.objects.get(id=vaccs.id)
                print(y)
                y.quantity = y.quantity - 1
                print(y.quantity)
                y.save()
                return HttpResponseRedirect(reverse('head_vet_add_medical_service', args=[str(pk)]))
    else:
        form = VaccineServiceForm(initial ={'code':serve.code,"vaccine":serve.vaccine,"medHistory":serve.medHistory,'dateofService':serve.dateofService,'service':serve.service,'interpretation':serve.interpretation,'vet':serve.vet,'dateofReturn':serve.dateofReturn,'reason':serve.reason})
        context['form'] = form
        context['medHist'] = medHist
        context['serve'] = serve
    return render(request,'headveterinarian/vet_vaccinationForm.html',context)

def head_vet_delete_availed_service(request,pk,pk2):
    medHist = MedicalHistory.objects.get(id=pk)
    med = serviceHistory.objects.get(id=pk2)
    if request.method == "POST":
        med.is_deleted = 1
        med.date_of_delete = datetime.today()
        med.save()
        return HttpResponseRedirect(reverse('head_vet_add_medical_service', args=[str(pk)]))
    context ={'sideb':'head_vet_delete_availed_service','med':med,'medHist':medHist}
    return render(request,'headveterinarian/delete_availed_service.html',context)

def head_vet_delete_availed_lab(request,pk,pk2):
    medHist = MedicalHistory.objects.get(id=pk)
    med = labHistory.objects.get(id=pk2)
    if request.method == "POST":
        med.is_deleted = 1
        med.date_of_delete = datetime.today()
        med.save()
        return HttpResponseRedirect(reverse('head_vet_add_medical_service', args=[str(pk)]))
    context ={'sideb':'head_vet_delete_availed_lab','med':med,'medHist':medHist}
    return render(request,'headveterinarian/delete_availed_service.html',context)

def head_vet_delete_availed_vaccine(request,pk,pk2):
    medHist = MedicalHistory.objects.get(id=pk)
    med = vaccineHistory.objects.get(id=pk2)
    if request.method == "POST":
        med.is_deleted = 1
        med.date_of_delete = datetime.today()
        med.save()
        return HttpResponseRedirect(reverse('head_vet_add_medical_service', args=[str(pk)]))
    context ={'sideb':'head_vet_delete_availed_vaccine','med':med,'medHist':medHist}
    return render(request,'headveterinarian/delete_availed_service.html',context)

def headvet_generateServiceInvoice(request,pk2):
    id = request.user.id
    user = User.objects.get(pk=id)
    charge_in = chargeSlip.objects.get(id=pk2)
    servicequery = serviceInvoice.objects.filter(chargeslip=charge_in)
    productquery = productInvoice.objects.filter(chargeslip=charge_in)
    form=ProductInvoice()
    if request.POST:
        form = ProductInvoice(request.POST,initial={'chargeslip':charge_in})
        if form.is_valid():
            prod_in = form.cleaned_data.get('product')
            quantity_in = form.cleaned_data.get('quantity')
            get_prod_in = Product.objects.get(id=prod_in.id)
            if productInvoice.objects.filter(chargeslip=charge_in).filter(product=get_prod_in).exists():
                messages.error(request, "Product is already added!")
                return HttpResponseRedirect(reverse('serviceInvoice', args=[str(pk2)]))
            if quantity_in > get_prod_in.quantity or quantity_in <= 0:
                messages.error(request, "Insufficient amount of quantity!")
                return HttpResponseRedirect(reverse('head_serviceInvoice', args=[str(pk2)]))
            else:
                a = form.save()
                total_in = quantity_in * get_prod_in.product.price
                remaining_prod_in = get_prod_in.quantity - quantity_in
                get_prod_in.quantity = remaining_prod_in
                get_prod_in.save()
                a.total = total_in
                a.save()
            messages.success(request, "Successfully Added!")
            return HttpResponseRedirect(reverse('head_serviceInvoice', args=[str(pk2)]))
        else:
            messages.error(request, "There is an error upon adding!")
    else:
        form = ProductInvoice(initial={'chargeslip':charge_in })
    all_service_total = 0 
    for services in servicequery:
        vars = services.total + all_service_total
        all_service_total = vars
    all_prod_total = 0
    for prods in productquery:
        var = prods.total + all_prod_total
        all_prod_total = var
    charge_in.totalAmount = all_service_total + all_prod_total
    if charge_in.status == "Unpaid":
        charge_in.balance = charge_in.totalAmount 
        charge_in.save()
    context = {'sideb':'head_serviceInvoice','chargeslip':charge_in ,'form': form,'productquery':productquery,'servicequery':servicequery}
    return render(request,'headveterinarian/chargeSlip.html',context) 


def headvet_modify_quantity(request,pk,pk2):
    context={}
    id = request.user.id
    user = User.objects.get(pk=id)
    charge_in = chargeSlip.objects.get(id=pk)
    get_invoice = productInvoice.objects.get(id=pk2)
    sample = get_invoice.quantity
    sample_id = get_invoice.product.id
    x = Product.objects.get(id=sample_id)
    servicequery = serviceInvoice.objects.filter(chargeslip=charge_in)
    productquery = productInvoice.objects.filter(chargeslip=charge_in)
    y = x.quantity + sample
    if request.POST:
        form = ProductInvoice(request.POST,instance=get_invoice)
        if form.is_valid():
            prod_in = form.cleaned_data.get('product')
            quantity_in = form.cleaned_data.get('quantity')
            if productInvoice.objects.filter(chargeslip=charge_in).exclude(id=pk2).filter(product=prod_in).exists():
                messages.error(request, "Product is already added!")
                return HttpResponseRedirect(reverse('head_serviceInvoice', args=[str(pk)]))
            if quantity_in > y or quantity_in <= 0:
                messages.error(request, "Invalid quantity!")
                return HttpResponseRedirect(reverse('head_serviceInvoice', args=[str(pk)]))
            else:
                quanti = x.quantity + sample
                x.quantity = quanti
                x.save()
                a = form.save()
                get_prod_in = Product.objects.get(id=prod_in.id)
                total_in = quantity_in * prod_in.product.price
                remaining_prod_in = get_prod_in.quantity - quantity_in
                get_prod_in.quantity = remaining_prod_in
                get_prod_in.save()
                a.total = total_in
                a.save()
                messages.success(request, "Quantity has been changed!")
                return HttpResponseRedirect(reverse('head_serviceInvoice', args=[str(pk)]))
    else:
        form = ProductInvoice(initial ={"chargeslip":get_invoice.chargeslip,"product":get_invoice.product,'quantity':get_invoice.quantity})
        context['form'] = form
        context['get_invoice'] = get_invoice
        context['productquery'] = productquery
        context['servicequery'] = servicequery
        context['chargeslip'] = charge_in
    return render(request,'headveterinarian/chargeSlip.html',context) 

def head_vet_remove_product(request,pk,pk2):
    product_invoice = productInvoice.objects.get(id=pk2)
    query = product_invoice.product.id
    get_product = Product.objects.get(id=query)
    quantity = product_invoice.quantity + get_product.quantity
    get_product.quantity = quantity
    get_product.save()
    product_invoice.delete()
    messages.success(request, "Removed Successfully!")
    return HttpResponseRedirect(reverse('head_serviceInvoice', args=[str(pk)]))


def vet_remove_product(request,pk,pk2):
    product_invoice = productInvoice.objects.get(id=pk2)
    query = product_invoice.product.id
    get_product = Product.objects.get(id=query)
    quantity = product_invoice.quantity + get_product.quantity
    get_product.quantity = quantity
    get_product.save()
    product_invoice.delete()
    messages.success(request, "Removed Successfully!")
    return HttpResponseRedirect(reverse('serviceInvoice', args=[str(pk)]))


# VETERINARIAN
def veterinarianHome(request):
    user = request.user.id
    getProfile = StaffProfile.objects.get(useracc=user)
    context={'getProfile':getProfile,'sideb' : 'veterinarianHome'}
    return render(request,'veterinarian/veterinarianHome.html', context)

def vetDashboard(request):
    user = request.user.id
    today = date.today() 
    param = date.today() +  timedelta(14)
    getProfile = StaffProfile.objects.get(useracc=user)
    slot = schedule_slot.objects.filter(vet=getProfile)
    getSchedToday = scheduling.objects.filter(status="Reserved",date=today)
    getSchedToday_cancel = scheduling.objects.filter(slot__in=slot,date=today).exclude(status="Cancelled")
    getSched = scheduling.objects.filter(date=today).exclude(status="Reserved")
    getSchedarrive = scheduling.objects.filter(date=today,status="Arrived",slot__in=slot)
    getScheddone = scheduling.objects.filter(date=today,status="Done",slot__in=slot)
    schedCount = getSchedToday.count()
    arriveCount = getSchedarrive.count()
    doneCount = getScheddone.count()
    nostock = ProductInfo.objects.filter(status="No stock")
    lowstock = ProductInfo.objects.filter(status="Low in Stock")
    expire = Product.objects.filter(expireDate__lte=param)
    context = {'doneCount':doneCount,'arriveCount':arriveCount,'schedCount':schedCount,'getSchedToday_cancel':getSchedToday_cancel, 'getProfile':getProfile,'getSched':getSched, 'sideb':'vetDashboard','getSchedToday':getSchedToday,'nostock':nostock,'lowstock':lowstock,'expire':expire,'getSchedarrive':getSchedarrive,'getScheddone':getScheddone}
    return render(request,'veterinarian/vetDashboard.html', context) 

def vetDashboard_one(request):
    user = request.user.id
    today = date.today() 
    param = date.today() +  timedelta(14)
    getProfile = StaffProfile.objects.get(useracc=user)
    slot = schedule_slot.objects.filter(vet=getProfile)
    getSchedToday = scheduling.objects.filter(status="Reserved",date=today)
    getSchedToday_cancel = scheduling.objects.filter(slot__in=slot,date=today).exclude(status="Cancelled")
    getSched = scheduling.objects.filter(date=today).exclude(status="Reserved")
    getSchedarrive = scheduling.objects.filter(date=today,status="Arrived",slot__in=slot)
    getScheddone = scheduling.objects.filter(date=today,status="Done",slot__in=slot)
    schedCount = getSchedToday.count()
    arriveCount = getSchedarrive.count()
    doneCount = getScheddone.count()
    nostock = ProductInfo.objects.filter(status="No stock")
    lowstock = ProductInfo.objects.filter(status="Low in Stock")
    expire = Product.objects.filter(expireDate__lte=param)
    context = {'doneCount':doneCount,'arriveCount':arriveCount,'schedCount':schedCount,'getSchedToday_cancel':getSchedToday_cancel, 'getProfile':getProfile,'getSched':getSched, 'sideb':'vetDashboard_one','getSchedToday':getSchedToday,'nostock':nostock,'lowstock':lowstock,'expire':expire,'getSchedarrive':getSchedarrive,'getScheddone':getScheddone}
    return render(request,'veterinarian/vetDashboard_one.html', context)  


def done_pet(request,pk):
    user = request.user.id
    getSched = scheduling.objects.get(id=pk)
    getSched.status = "Done"
    getSched.save()
    context = {'getSched':getSched}
    return HttpResponseRedirect(reverse('create_pet_record', args=[str(getSched.pet.id)]))

def edit_vet_profile(request,pk):
   
    updprofile = StaffProfile.objects.get(id=pk)
    profile_pic = request.FILES.get('image') #bago toh
    context = {'sideb':'edit_vet_profile','profile_pic':profile_pic ,'updprofile':  updprofile}
    if request.POST:
        form = Edit_Staff_Profile(request.POST,instance=updprofile)
        if form.is_valid():
            if profile_pic:#bago toh
                updprofile.user_image = profile_pic #bago toh
            form.save()
            messages.success(request,'Successfully Updated')
            context['form'] = form
        
            return render(request,'veterinarian/edit_vet_profile.html', context)
        else:
            messages.error(request,' ')
            context['form'] = form
            context['updprofile'] = updprofile
    else:
        form = Edit_Staff_Profile(initial ={"useracc":updprofile.useracc,"firstName":updprofile.firstName,"lastName":updprofile.lastName,"gender":updprofile.gender,"contactNum":updprofile.contactNum,"address":updprofile.address,"user_image":profile_pic})
        context['form'] = form
        context['updprofile'] = updprofile
    return render(request,'veterinarian/edit_vet_profile.html',context)

def services_veterinarian(request):
    allpets = pets.objects.filter(is_deleted=False)
    searchthis_query = request.GET.get('searchthis')
    if searchthis_query != " " and searchthis_query is not None:
        allpets = pets.objects.filter(Q(petOwner__firstName__icontains=searchthis_query) | Q(petOwner__lastName__icontains=searchthis_query)| Q(petName=searchthis_query)| Q(petOwner__useracc__email__icontains=searchthis_query)).distinct()
    context={'allpets':allpets, 'sideb' : 'services_veterinarian'}
    return render(request,'veterinarian/services_veterinarian.html', context)

def vet_pet_create_view(request):
    form = AddPetForm()
    if request.method == 'POST':
        form = AddPetForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Pet has been successfully added!")
            return redirect('services_veterinarian')
    context={'sideb':'vet_add_pets','form': form}
    return render(request, 'veterinarian/vet_pet_create.html', context)

def create_pet_record(request,pk):
    context = { 'sideb':'vet_add_medical_service'}
    id = request.user.id
    all_meds = MedicalHistory.objects.all()
    user = User.objects.get(pk=id)
    getuser = StaffProfile.objects.get(useracc=user.id)
    addtopet = pets.objects.get(id=pk)
    now = date.today()
    if request.POST:
        form = MedHistory(request.POST,initial={'pet': addtopet,'date':now,'vet':getuser})
        if form.is_valid():
            form.save()
            x = form.save()
            param = x.id
            codes= "PT" + "%x" % random.randint(0, 0xFFFFF)
            for med in all_meds:
                if med.code == codes:
                    codes= "PT" + "%x" % random.randint(0, 0xFFFFF)
            x.code=codes
            x.save()
            return HttpResponseRedirect(reverse('vet_add_medical_service', args=[str(param)]))
        else:
            context['form'] = form
    else:
        form = MedHistory(initial ={"pet":addtopet,'date':now,'vet':getuser})
        context['form'] = form
    return render(request,'veterinarian/create_pet_record.html',context)

def view_record(request,pk):
    param = pets.objects.get(id=pk)
    records = MedicalHistory.objects.filter(pet=param)
    context = {'sideb':'view_record','records':records,'param':param}
    return render(request,'veterinarian/view_record.html',context)

def view_per_record(request,pk):
    medHist = MedicalHistory.objects.get(id=pk)
    vaccination =vaccineHistory.objects.filter(medHistory=medHist,is_deleted=False)
    labtest =labHistory.objects.filter(medHistory=medHist,is_deleted=False)
    availed = serviceHistory.objects.filter(medHistory=medHist,is_deleted=False)
    context={'sideb':'view_per_record','vaccination':vaccination,'labtest':labtest,'availed':availed,'medHist':medHist}
    return render(request,'veterinarian/view_per_record.html',context)

def vet_update_medical_history(request,pk):
    context = {'sideb':'vet_update_medical_history'}
    medHist = MedicalHistory.objects.get(id=pk)
    if request.POST:
        form = MedHistory(request.POST,instance=medHist)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('view_per_record', args=[str(pk)]))
        else:
            context['form'] = form
    else:
        form = MedHistory(initial ={'code':medHist.code,'pet':medHist.pet,'date':medHist.date,'weight':medHist.weight,'symptoms':medHist.symptoms,'treatment':medHist.treatment,'prescription':medHist.prescription,'instruction':medHist.instruction,'dateofReturn':medHist.dateofReturn,'reason':medHist.reason,'vet':medHist.vet})
        context['form'] = form
    return render(request,'veterinarian/create_pet_record.html',context)


def vet_add_medical_service(request,pk):
    user=request.user.id
    all_chargeslip=chargeSlip.objects.all()
    getuser = StaffProfile.objects.get(useracc=user)
    medHist = MedicalHistory.objects.get(id=pk)
    vaccination =vaccineHistory.objects.filter(medHistory=medHist,is_deleted=False)
    labtest =labHistory.objects.filter(medHistory=medHist,is_deleted=False)
    availed = serviceHistory.objects.filter(medHistory=medHist,is_deleted=False)
    all_service = serviceHistory.objects.filter(medHistory=pk)
    all_lab = labHistory.objects.filter(medHistory=pk)
    all_vaccine = vaccineHistory.objects.filter(medHistory=pk)
    if request.POST:
        add = chargeSlip(petowner=medHist.pet.petOwner,date=datetime.today(),staff=getuser)
        add.save()
        x = chargeSlip.objects.get(id=add.id)
        codes= "CS" + "%x" % random.randint(0, 0xFFFFF)
        for charge in all_chargeslip:
            if charge.code == codes:
                codes= "CS" + "%x" % random.randint(0, 0xFFFFF)
        x.code=codes
        x.save()
        for service in all_service:
            invoice = serviceInvoice(chargeslip=x,servicecode=service.code,service=service.service,total=service.service.price)
            invoice.save()   
        for service in all_lab:
            invoice = serviceInvoice(chargeslip=x,servicecode=service.code,service=service.service,total=service.service.price)
            invoice.save()   
        for service in all_vaccine:
            invoice = serviceInvoice(chargeslip=x,servicecode=service.code,service=service.service,total=service.service.price)
            invoice.save()   
        return HttpResponseRedirect(reverse('serviceInvoice', args=[str(x.id)]))
    context={'sideb':'vet_add_medical_service','vaccination':vaccination,'labtest':labtest,'availed':availed,'medHist':medHist}
    return render(request,'veterinarian/vet_add_medical_service.html',context)

def vet_availed_service(request,pk):
    context = {'sideb':'vet_availed_service'}
    all_service = serviceHistory.objects.all()
    medHist = MedicalHistory.objects.get(id=pk)
    if request.POST:
        form = AvailedService(request.POST,initial={'medHistory': medHist,'dateofService':medHist.date,'vet':medHist.vet})
        if form.is_valid():
            services = form.cleaned_data.get('service')
            if serviceHistory.objects.filter(medHistory=medHist).filter(service=services).exists():
                messages.error(request,"Service is already added")
                return HttpResponseRedirect(reverse('vet_add_medical_service', args=[str(pk)]))
            else:
                x = form.save()
                codes= "GS" + "%x" % random.randint(0, 0xFFFFF)
                for med in all_service:
                    if med.code == codes:
                        codes= "GS" + "%x" % random.randint(0, 0xFFFFF)
                x.code=codes
                x.save()
                return HttpResponseRedirect(reverse('vet_add_medical_service', args=[str(pk)]))
        else:
            context['form'] = form
    else:
        form = AvailedService(initial ={"medHistory":medHist,'dateofService':medHist.date,'vet':medHist.vet})
        context['form'] = form
        context['medHist'] = medHist
    return render(request,'veterinarian/vet_availed_service.html',context)

    
def vet_edit_availed_service(request,pk,pk2):
    context = {'sideb':'vet_edit_availed_service'}
    medHist = MedicalHistory.objects.get(id=pk)
    serve= serviceHistory.objects.get(id=pk2)
    if request.POST:
        form = AvailedService(request.POST,instance=serve)
        if form.is_valid():
            services = form.cleaned_data.get('service')
            if serviceHistory.objects.filter(medHistory=medHist).exclude(id=pk2).filter(service=services).exists():
                messages.error(request,"Service is already added")
                return HttpResponseRedirect(reverse('vet_add_medical_service', args=[str(pk)]))
            else:
                x = form.save()
                return HttpResponseRedirect(reverse('vet_add_medical_service', args=[str(pk)]))
        else:
            context['form'] = form
    else:
        form = AvailedService(initial ={'code':serve.code,"medHistory":serve.medHistory,'dateofService':serve.dateofService,'service':serve.service,'interpretation':serve.interpretation,'vet':serve.vet})
        context['form'] = form
        context['medHist'] = medHist
        context['serve'] = serve
    return render(request,'veterinarian/vet_availed_service.html',context)

def vet_availed_labTest(request,pk):
    context = {'sideb':'vet_availed_labTest'}
    all_lab=labHistory.objects.all()
    medHist = MedicalHistory.objects.get(id=pk)
    if request.POST:
        form = LabTestForm(request.POST,initial={'medHistory': medHist,'dateofService':medHist.date,'vet':medHist.vet})
        if form.is_valid():
            services = form.cleaned_data.get('service')
            if labHistory.objects.filter(medHistory=medHist).filter(service=services).exists():
                messages.error(request,"Service is already added")
                return HttpResponseRedirect(reverse('vet_add_medical_service', args=[str(pk)]))
            else:
                x = form.save()
                codes= "LT" + "%x" % random.randint(0, 0xFFFFF)
                for charge in all_lab:
                    if charge.code == codes:
                        codes= "LT" + "%x" % random.randint(0, 0xFFFFF)
                x.code=codes
                x.save()
                return HttpResponseRedirect(reverse('vet_add_medical_service', args=[str(pk)]))
        else:
            context['form'] = form
    else:
        form = LabTestForm(initial ={"medHistory":medHist,'dateofService':medHist.date,'vet':medHist.vet})
        context['form'] = form
        context['medHist'] = medHist
    return render(request,'veterinarian/vet_availed_labTest.html',context)

def vet_edit_lab_test(request,pk,pk2):
    context = {'sideb':'vet_edit_lab_test'}
    medHist = MedicalHistory.objects.get(id=pk)
    serve= labHistory.objects.get(id=pk2)
    if request.POST:
        form = LabTestForm(request.POST,instance=serve)
        if form.is_valid():
            services = form.cleaned_data.get('service')
            if labHistory.objects.filter(medHistory=medHist).exclude(id=pk2).filter(service=services).exists():
                messages.error(request,"Service is already added")
                return HttpResponseRedirect(reverse('vet_add_medical_service', args=[str(pk)]))
            else:
                x = form.save()
                return HttpResponseRedirect(reverse('vet_add_medical_service', args=[str(pk)]))
    else:
        form = LabTestForm(initial ={'code':serve.code,"medHistory":serve.medHistory,'dateofService':serve.dateofService,'service':serve.service,'interpretation':serve.interpretation,'vet':serve.vet,'dateofResult':serve.dateofResult})
        context['form'] = form
        context['medHist'] = medHist
        context['serve'] = serve
    return render(request,'veterinarian/vet_availed_labTest.html',context)

def vet_availed_vaccination(request,pk):
    context = {'sideb':'vet_availed_vaccination'}
    all_vacc = vaccineHistory.objects.all()
    medHist = MedicalHistory.objects.get(id=pk)
    if request.POST:
        form = VaccineServiceForm(request.POST,initial={'medHistory': medHist,'dateofService':medHist.date,'vet':medHist.vet})
        if form.is_valid():
            services = form.cleaned_data.get('service')
            vaccs = form.cleaned_data.get('vaccine')
            print(vaccs.id)
            if vaccineHistory.objects.filter(medHistory=medHist).filter(service=services).exists():
                messages.error(request,"Service is already added")
                return HttpResponseRedirect(reverse('vet_add_medical_service', args=[str(pk)]))
            else:
                vaccine = Product.objects.get(id=vaccs.id)
                vaccine.quantity = vaccine.quantity - 1
                vaccine.save()
                displayproducts = ProductInfo.objects.filter(is_deleted = 0)
                for item in displayproducts:
                    prod = Product.objects.filter(product=item)
                    total=0
                    item.total_quantity = total
                    item.save()
                    for quantity in prod:
                        print(quantity)
                        value = quantity.quantity + total
                        total = value
                        item.total_quantity = total
                        item.save()
                x = form.save()
                codes= "VS" + "%x" % random.randint(0, 0xFFFFF)
                for charge in all_vacc:
                    if charge.code == codes:
                        codes= "VS" + "%x" % random.randint(0, 0xFFFFF)
                x.code=codes
                x.save()
                return HttpResponseRedirect(reverse('vet_add_medical_service', args=[str(pk)]))
        else:
            context['form'] = form
    else:
        form = VaccineServiceForm(initial ={"medHistory":medHist,'dateofService':medHist.date,'vet':medHist.vet})
        context['form'] = form
        context['medHist'] = medHist
    return render(request,'veterinarian/vet_vaccinationForm.html',context)

def vet_edit_vaccination(request,pk,pk2):
    context = {'sideb':'vet_edit_vaccination'}
    medHist = MedicalHistory.objects.get(id=pk)
    serve= vaccineHistory.objects.get(id=pk2)
    x = Product.objects.get(id=serve.vaccine.id)
    if request.POST:
        form = VaccineServiceForm(request.POST,instance=serve)
        if form.is_valid():
            services = form.cleaned_data.get('service')
            if vaccineHistory.objects.filter(medHistory=medHist).exclude(id=pk2).filter(service=services).exists():
                messages.error(request,"Service is already added")
                return HttpResponseRedirect(reverse('vet_add_medical_service', args=[str(pk)]))
            else:
                x.quantity = x.quantity + 1
                x.save()
                form.save()
                vaccs = form.cleaned_data.get('vaccine')
                y = Product.objects.get(id=vaccs.id)
                print(y)
                y.quantity = y.quantity - 1
                print(y.quantity)
                y.save()
                return HttpResponseRedirect(reverse('vet_add_medical_service', args=[str(pk)]))
    else:
        form = VaccineServiceForm(initial ={'code':serve.code,"vaccine":serve.vaccine,"medHistory":serve.medHistory,'dateofService':serve.dateofService,'service':serve.service,'interpretation':serve.interpretation,'vet':serve.vet,'dateofReturn':serve.dateofReturn,'reason':serve.reason})
        context['form'] = form
        context['medHist'] = medHist
        context['serve'] = serve
    return render(request,'veterinarian/vet_vaccinationForm.html',context)

def vet_delete_availed_service(request,pk,pk2):
    medHist = MedicalHistory.objects.get(id=pk)
    med = serviceHistory.objects.get(id=pk2)
    if request.method == "POST":
        med.is_deleted = 1
        med.date_of_delete = datetime.today()
        med.save()
        return HttpResponseRedirect(reverse('vet_add_medical_service', args=[str(pk)]))
    context ={'sideb':'vet_delete_availed_service','med':med,'medHist':medHist}
    return render(request,'veterinarian/delete_availed_service.html',context)

def vet_delete_availed_lab(request,pk,pk2):
    medHist = MedicalHistory.objects.get(id=pk)
    med = labHistory.objects.get(id=pk2)
    if request.method == "POST":
        med.is_deleted = 1
        med.date_of_delete = datetime.today()
        med.save()
        return HttpResponseRedirect(reverse('vet_add_medical_service', args=[str(pk)]))
    context ={'sideb':'vet_delete_availed_lab','med':med,'medHist':medHist}
    return render(request,'veterinarian/delete_availed_service.html',context)

def vet_delete_availed_vaccine(request,pk,pk2):
    medHist = MedicalHistory.objects.get(id=pk)
    med = vaccineHistory.objects.get(id=pk2)
    if request.method == "POST":
        med.is_deleted = 1
        med.date_of_delete = datetime.today()
        med.save()
        return HttpResponseRedirect(reverse('vet_add_medical_service', args=[str(pk)]))
    context ={'sideb':'vet_delete_availed_vaccine','med':med,'medHist':medHist}
    return render(request,'veterinarian/delete_availed_service.html',context)


def add_species(request):
    context = {}
    if request.POST:
        form = AddSpecies(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Successfully Added!")
            context['form'] = form
            return render(request,'secretary/add_species.html', context)
        else:
            messages.error(request, "-") #hindi ko gets san galing yung text na dinidisplay T_T
            context['form'] = form
            return render(request,'secretary/add_species.html', context)
    else:
        form = AddSpecies()
        context['form'] = form
    return render(request,'secretary/add_species.html', context)

def update_species(request,pk):
    context = {}
    updspecies = petspecies.objects.get(id=pk)
    if request.POST:
        form = AddSpecies(request.POST,instance=updspecies)
        if form.is_valid():
            form.save()
            return redirect('add_dropdown_details')
        else:
            context['form'] = form
    else:
        form = AddSpecies(initial ={"species":updspecies.species})
        context['form'] = form
    return render(request,'secretary/add_species.html', context)

def delete_species(request,pk):
    species = petspecies.objects.get(id=pk)
    if request.method == "POST":
        species.is_deleted = 1
        species.date_of_delete = datetime.today()
        species.save()
        messages.success(request, "Successfully Deleted!")
        return redirect('add_dropdown_details')
    context ={'species':species}
    return render(request,'secretary/delete_species.html',context)

def add_vaccineType(request):
    context = {}
    if request.POST:
        form = AddVaccineTypeForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Successfully Added!")
            context['form'] = form
            return render(request,'secretary/add_vaxtype.html', context)
            return redirect('add_dropdown_details')
        else:
            messages.error(request, "-") #hindi ko gets san galing yung text na dinidisplay T_T
            context['form'] = form
            return render(request,'secretary/add_vaxtype.html', context)
            
    else:
        form = AddVaccineTypeForm()
        context['form'] = form
    return render(request,'secretary/add_vaxtype.html', context)

def update_vaccineType(request,pk):
    context = {}
    updvaxtype = vaxType.objects.get(id=pk)
    if request.POST:
        form = AddVaccineTypeForm(request.POST,instance=updvaxtype)
        if form.is_valid():
            form.save()
            return redirect('add_dropdown_details')
        else:
            context['form'] = form
    else:
        form = AddVaccineTypeForm(initial ={"vaccineType":updvaxtype.vaccineType})
        context['form'] = form
    return render(request,'secretary/add_vaxType.html', context)

def delete_vaccineType(request,pk):
    vaccineType = vaxType.objects.get(id=pk)
    if request.method == "POST":
        vaccineType.is_deleted = 1
        vaccineType.date_of_delete = datetime.today()
        vaccineType.save()
        messages.success(request, "Successfully Deleted!")
        return redirect('add_dropdown_details')
    context ={'vaccineType':vaccineType}
    return render(request,'secretary/delete_vaxType.html',context)

def add_service(request):
    context = {}
    if request.POST:
        form = Add_ServiceForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Successfully Added!")
            context['form'] = form
            return render(request,'secretary/add_services.html', context)
        else:
            messages.error(request, "-") #??
            context['form'] = form
            return render(request,'secretary/add_services.html', context)
    else:
        form = Add_ServiceForm()
        context['form'] = form
    return render(request,'secretary/add_services.html', context)

def update_service(request,pk):
    context = {}
    updservice = services.objects.get(id=pk)
    if request.POST:
        form = Add_ServiceForm(request.POST,instance=updservice)
        if form.is_valid():
            form.save()
            return redirect('add_dropdown_details')
        else:
            context['form'] = form
    else:
        form = Add_ServiceForm(initial ={'serviceName':updservice.serviceName,'description':updservice.description,'price':updservice.price,'is_labTest':updservice.is_labTest})
        context['form'] = form
    return render(request,'secretary/add_services.html', context)

def delete_service(request,pk):
    service = services.objects.get(id=pk)
    if request.method == "POST":
        service.is_deleted = 1
        service.date_of_delete = datetime.today()
        service.save()
        messages.success(request, "Successfully Deleted!")
        return redirect('add_dropdown_details')
    context ={'service':service}
    return render(request,'secretary/delete_services.html',context)

def add_prodType(request):
    petowners = User.objects.filter(is_petowner=True,is_active=True)
    context = {'petowners':petowners}
    if request.POST:
        form = AddProductTypeForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Successfully Added!')
            context['form'] = form
            return render(request,'secretary/add_prodType.html', context)
        else:
            messages.error(request, '-')#?
            context['form'] = form
    else:
        form = AddProductTypeForm()
        context['form'] = form
    return render(request,'secretary/add_prodType.html', context)

def update_prodType(request,pk):
    context = {}
    updprodTpye = ProductType.objects.get(id=pk)
    if request.POST:
        form = AddProductTypeForm(request.POST,instance=updprodTpye)
        if form.is_valid():
            form.save()
            return redirect('add_dropdown_details')
        else:
            context['form'] = form
    else:
        form = AddProductTypeForm(initial ={"prodType":updprodTpye.prodType})
        context['form'] = form
    return render(request,'secretary/add_prodType.html', context)

def delete_prodType(request,pk):
    prodType = ProductType.objects.get(id=pk)
    if request.method == "POST":
        prodType.is_deleted = 1
        prodType.date_of_delete = datetime.today()
        prodType.save()
        messages.success(request, "Successfully Deleted!")
        return redirect('add_dropdown_details')
    context ={'prodType':prodType}
    return render(request,'secretary/delete_prodType.html',context)

def addProduct(request):
    form = AddProductForm()
    if request.method == 'POST':
        form = AddProductForm(request.POST)
        if form.is_valid():
            medium = form.cleaned_data.get('medium_margin')
            low = form.cleaned_data.get('low_margin')
            price = form.cleaned_data.get('price')
            if price < 0:
                messages.error (request,'Invalid Price.')
                return redirect('add_product')
            if low <= 0:
                messages.error (request,'Invalid Threshold margin')
                return redirect('add_product')
            if medium <= 0:
                messages.error (request,'Invalid Threshold margin')
                return redirect('add_product')
            if low >= medium:
                messages.error (request,'Invalid Threshold margin.')
                return redirect('add_product')
            else:
                form.save()
                messages.success(request, "Successfully Added!")
                return redirect('products')
    context = {'sideb':'add_product','form': form}
    return render(request, 'secretary/products/add_product.html', context)

def updateProduct(request, pk):
    update = ProductInfo.objects.get(id=pk)
    form = AddProductForm(instance=update)
    if request.method == 'POST':
        form = AddProductForm(request.POST, instance=update)
        if form.is_valid():
            form.save()
            messages.success(request, "Successfully Updated!")
            return redirect('products')
    context = {'form': form}
    return render(request, 'secretary/products/add_product.html', context)

def deleteProduct(request, pk):
    update = ProductInfo.objects.get(id=pk)
    if request.method == "POST":
        update.is_deleted = 1
        update.date_of_delete = datetime.today()
        update.save()
        messages.success(request, "Successfully Deleted!")
        return redirect('products')
    context = {'item': update}
    return render(request, 'secretary/products/delete_product.html', context)

    #products = Product.objects.all()
    #myFilter = stocksStatusFilter(request.GET, queryset=products)
    #products = myFilter.qs
 
def products(request):
    displayproducts = ProductInfo.objects.filter(is_deleted = False)
    for item in displayproducts:
        prod = Product.objects.filter(product=item)
        total=0
        item.total_quantity = total
        item.save()
        for quantity in prod:
            print(quantity)
            value = quantity.quantity + total
            total = value
            item.total_quantity = total
            item.save()
        if item.total_quantity == 0:
            item.status = "No Stock"
            item.save()
        elif item.total_quantity > item.medium_margin:
            item.status = "High in Stock"
            item.save()
        elif item.total_quantity > item.low_margin and item.total_quantity <= item.medium_margin:
            item.status = "Medium in Stock"
            item.save()
        else:
            item.status = "Low in Stock"
            item.save()
    searchthis_query = request.GET.get('searchthis')
    if searchthis_query != " " and searchthis_query is not None:
         displayproducts = ProductInfo.objects.filter(Q(product_name__icontains=searchthis_query) | Q(product_type__prodType__icontains=searchthis_query) | Q(description__icontains=searchthis_query)).distinct()
    context={'sideb': 'products', 'displayproducts':displayproducts}
    return render(request, 'secretary/products/products.html', context)


def productsInventory(request, pk):
    prod = ProductInfo.objects.get(id=pk)
    products= Product.objects.filter(product=pk,is_deleted=False)
    all_products = Product.objects.filter(product=prod,is_deleted=False)
    total = 0
    for quantity in all_products:
        value = quantity.quantity + total
        total = value
        prod.total_quantity = total
        prod.save()
    if prod.total_quantity == 0:
        prod.status = "No stock"
        prod.save()
    elif prod.total_quantity > prod.medium_margin:
        prod.status = "High in Stock"
        prod.save()
    elif prod.total_quantity > prod.low_margin and prod.total_quantity <= prod.medium_margin:
        prod.status = "Medium in Stock"
        prod.save()
    else:
        prod.status = "Low in Stock"
        prod.save()
    context = {'sideb':'available_products','products':products,'prod':prod}
    return render(request, 'secretary/products/available_products.html', context)

def addproductsInventory(request, pk):
    prod = ProductInfo.objects.get(id=pk)
    form = AddProductInventoryForm(initial={'product': prod})
    today = date.today()
    print(today)
    if request.method == 'POST':
        form = AddProductInventoryForm(request.POST, initial={'product': prod})
        if form.is_valid():
            manuDate = form.cleaned_data.get('manuDate')
            expireDate = form.cleaned_data.get('expireDate')
            if manuDate > today:
                messages.error(request, "Invalid Date!")
                return HttpResponseRedirect(reverse('add_available_products', args=[str(pk)]))
            elif expireDate <= today:
                messages.error(request, "Invalid Date!")
                return HttpResponseRedirect(reverse('add_available_products', args=[str(pk)]))
            elif expireDate <= manuDate:
                messages.error(request, "Invalid Date!")
                return HttpResponseRedirect(reverse('add_available_products', args=[str(pk)]))
            else:
                form.save()
                messages.success(request, "Successfully Added!")
        all_products = Product.objects.filter(product=prod,is_deleted=False)
        total = 0
        for quantity in all_products:
            value = quantity.quantity + total
            total = value
            prod.total_quantity = total
            prod.save()
        if prod.total_quantity == 0:
            prod.status = "No stock"
            prod.save()
        elif prod.total_quantity > prod.medium_margin:
            prod.status = "High in Stock"
            prod.save()
        elif prod.total_quantity > prod.low_margin and prod.total_quantity <= prod.medium_margin:
            prod.status = "Medium in Stock"
            prod.save()
        else:
            prod.status = "Low in Stock"
            prod.save()
        return HttpResponseRedirect(reverse('available_products', args=[str(pk)]))
    context = {'sideb':'add_available_products','form': form}
    return render(request, 'secretary/products/add_available_products.html', context)

def updateproductsInventory(request,pk,pk2):
    context = {'sideb':'update_product'}
    today = date.today()
    prod = ProductInfo.objects.get(id=pk2)
    prod1 = Product.objects.get(id=pk)
    if request.POST:
        form = AddProductInventoryForm(request.POST,instance=prod1)
        if form.is_valid():
            manuDate = form.cleaned_data.get('manuDate')
            expireDate = form.cleaned_data.get('expireDate')
            if manuDate > today:
                messages.error(request, "Invalid Date!")
                return HttpResponseRedirect(reverse('update_available_products', args=[str(pk)]))
            elif expireDate <= today:
                messages.error(request, "Invalid Date!")
                return HttpResponseRedirect(reverse('update_available_products', args=[str(pk)]))
            elif expireDate <= manuDate:
                messages.error(request, "Invalid Date!")
                return HttpResponseRedirect(reverse('update_available_products', args=[str(pk)]))
            else:
                form.save()
                messages.success(request, "Successfully Added!")
            all_products = Product.objects.filter(product=prod,is_deleted=False)
            total = 0
            for quantity in all_products:
                value = quantity.quantity + total
                total = value
                prod.total_quantity = total
                prod.save()
            if prod.total_quantity == 0:
                prod.status = "No stock"
                prod.save()
            elif prod.total_quantity > prod.medium_margin:
                prod.status = "High in Stock"
                prod.save()
            elif prod.total_quantity > prod.low_margin and prod.total_quantity <= prod.medium_margin:
                prod.status = "Medium in Stock"
                prod.save()
            else:
                prod.status = "Low in Stock"
                prod.save()
            return HttpResponseRedirect(reverse('available_products', args=[str(pk2)]))
        else:
            context['form'] = form
    else:
        form = AddProductInventoryForm(initial ={'product':prod1.product,'manuDate':prod1.manuDate,'expireDate':prod1.expireDate,'quantity':prod1.quantity})
        context['form'] = form

    
    return render(request,'secretary/products/add_available_products.html', context)

def deleteproductsInventory(request,pk,pk2):
    update = Product.objects.get(id=pk)
    
    if request.method == "POST":
        update.is_deleted = 1
        update.date_of_delete = datetime.today()
        update.save()
        messages.success(request, "Successfully Deleted")
        return HttpResponseRedirect(reverse('available_products', args=[str(pk2)]))
    context = {'item': update,}
    return render(request, 'secretary/products/delete_available_products.html', context)

def add_gender(request):
    context = {}
    if request.POST:
        form = GenderForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Successfully Added!")
            context['form'] = form
            return render(request,'secretary/add_gender.html', context)
        else:
            messages.error(request, "-")#??
            context['form'] = form
    else:
        form = GenderForm()
        context['form'] = form
    return render(request,'secretary/add_gender.html', context)

def update_gender(request,pk):
    context = {}
    updgender = Gender.objects.get(id=pk)
    if request.POST:
        form = GenderForm(request.POST,instance=updgender)
        if form.is_valid():
            form.save()
            return redirect('add_dropdown_details')
        else:
            context['form'] = form
    else:
        form = GenderForm(initial ={"gender":updgender.gender})
        context['form'] = form
    return render(request,'secretary/add_gender.html', context)

def delete_gender(request,pk):
    gend = Gender.objects.get(id=pk)
    if request.method == "POST":
        gend.is_deleted = 1
        gend.save()
        messages.success(request, "Successfully Deleted!")
        return redirect('add_dropdown_details')
    context ={'gend':gend}
    return render(request,'secretary/delete_vaxType.html',context)

def pet_create_view(request):
    form = AddPetForm()
    if request.method == 'POST':
        form = AddPetForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Pet has been successfully added!")
            return redirect('pet_record')
    return render(request, 'secretary/pet_create.html', {'form': form})

def pet_update_view(request, pk):
    person = get_object_or_404(pets, pk=pk)
    form = AddPetForm(instance=person)
    pet = pets.objects.get(id=pk) #bago toh pet
    pet_img = request.FILES.get('image') #bago toh pet
    if request.method == 'POST':
        form = AddPetForm(request.POST, instance=person)  
        if form.is_valid():
            if pet_img:#bago toh pet
                pet.pet_image = pet_img #bago toh pet
            form.save()
            messages.success(request, "Pet information has been successfully updated!")
            return redirect('pet_record')
    return render(request, 'secretary/pet_create.html', {'form': form, "pet_image":pet_img}) #bago toh pet

def pet_create_view_per_owner(request, pk):
    person = Profile.objects.get(id=pk)
    form = AddPetForm(initial={'petOwner': person})
    pet = pets.objects.get(id=pk) #bago toh pet
    pet_img = request.FILES.get('image') #bago toh pet
    if request.method == 'POST':
        form = AddPetForm(request.POST, initial={'petOwner': person})  
        if form.is_valid():
            if pet_img:#bago toh pet
                pet.pet_image = pet_img #bago toh pet
            form.save()
            return redirect('user_profile')
    return render(request, 'secretary/pet_create.html', {'form': form, "pet_image":pet_img}) #bago toh pet

def delete_pets(request,pk):
    pet = pets.objects.get(id=pk)
    if request.method == "POST":
        pet.is_deleted = 1
        pet.date_of_delete = datetime.today()
        pet.save()
        messages.success(request, "Pet has been successfully deleted!")
        return redirect('pet_record')
    context ={'pet':pet}
    return render(request,'secretary/delete_pet.html',context)

def load_breed(request):
    species_id = request.GET.get('kind')
    breeds = breed.objects.filter(kind=species_id,is_deleted=False)
    #print(list(breeds.values('id', 'breed')))
    return render(request, 'secretary/pet_dropdown_list.html', {'breeds': breeds})
    #return JsonResponse(list(breeds.values('id', 'breed')), safe=False)
def add_breeds(request):
    context = {}
    if request.POST:
        form = BreedForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Successfully added!.")
            context['form'] = form
            return render(request,'secretary/add_breed.html', context)
        else:
            messages.error(request, "-")
            context['form'] = form
            return render(request,'secretary/add_breed.html', context)
    else:
        form = BreedForm()
        context['form'] = form
    return render(request,'secretary/add_breed.html', context)

def update_breeds(request,pk):
    context = {}
    updbreed = breed.objects.get(id=pk)
    if request.POST:
        form = BreedForm(request.POST,instance=updbreed)
        if form.is_valid():
            form.save()
            return redirect('add_dropdown_details')
        else:
            context['form'] = form
    else:
        form = BreedForm(initial ={"kind":updbreed.kind,"breed":updbreed.breed})
        context['form'] = form
    return render(request,'secretary/add_breed.html', context)

def delete_breeds(request,pk):
    breeds = breed.objects.get(id=pk)
    if request.method == "POST":
        breeds.is_deleted = 1
        breeds.date_of_delete = datetime.today()
        breeds.save()
        messages.success(request, "Successfully Deleted!")
        return redirect('add_dropdown_details')
    context ={'breeds':breeds}
    return render(request,'secretary/delete_breed.html',context)


def recover(request):
    petowners = User.objects.filter(is_petowner=True,is_active=False)
    veterinarian = User.objects.filter(is_veterinarian=True,is_active=False)
    headvet = User.objects.filter(is_headveterinarian=True,is_active=False)
    secretary = User.objects.filter(is_secretary=True,is_active=False)  
    deletedpets= pets.objects.filter(is_deleted=True)
    history = MedicalHistory.objects.filter(is_deleted=True)
    context ={'petowners':petowners,'veterinarian':veterinarian,'headvet':headvet,'secretary':secretary,'deletedpets':deletedpets,'history':history}
    return render(request,'secretary/recovery.html',context)

def archive_accounts(request):
    petowners = User.objects.filter(is_petowner=True,is_active=False)
    veterinarian = User.objects.filter(is_veterinarian=True,is_active=False)
    headvet = User.objects.filter(is_headveterinarian=True,is_active=False)
    secretary = User.objects.filter(is_secretary=True,is_active=False)  
    deletedpets= pets.objects.filter(is_deleted=True)
    history = MedicalHistory.objects.filter(is_deleted=True)
    context ={'sideb' : 'archive_accounts','petowners':petowners,'veterinarian':veterinarian,'headvet':headvet,'secretary':secretary,'deletedpets':deletedpets,'history':history}
    return render(request, 'secretary/archive/archive_accounts.html',context)

def archive_pets(request):
    petowners = User.objects.filter(is_petowner=True,is_active=False)
    deletedpets= pets.objects.filter(is_deleted=True)
    context ={'sideb' : 'archive_pets','petowners':petowners,'deletedpets':deletedpets}
    return render(request, 'secretary/archive/archive_pets.html',context)


def archive_medHistory(request):
    petowners = User.objects.filter(is_petowner=True,is_active=False)
    veterinarian = User.objects.filter(is_veterinarian=True,is_active=False)
    headvet = User.objects.filter(is_headveterinarian=True,is_active=False)
    secretary = User.objects.filter(is_secretary=True,is_active=False)  
    deletedpets= pets.objects.filter(is_deleted=True)
    history = MedicalHistory.objects.filter(is_deleted=True)
    context ={'sideb' : 'archive_medHistory','petowners':petowners,'veterinarian':veterinarian,'headvet':headvet,'secretary':secretary,'deletedpets':deletedpets,'history':history}
    return render(request,'secretary/archive/archive_medHistory.html',context)


def recover_user(request,pk):
    user = User.objects.get(id=pk)
    if request.method == "POST":
        user.is_active = 1
        user.save()
        messages.success(request, "User has been Successfully Activated!")
        return redirect('archive_accounts')

    context ={'user':user}
    return render(request,'secretary/archive/user_activate.html', context)

def recover_pet(request,pk):
    pet = pets.objects.get(id=pk)
    if request.method == "POST":
        pet.is_deleted = 0
        pet.save()
        messages.success(request, "Pet has been Successfully Activated!")
        return redirect('archive_pets')
    context ={'pet':pet}
    return render(request,'secretary/archive/recover_pet.html', context)


def recover_history(request,pk):
    history = MedicalHistory.objects.get(id=pk)
    if request.method == "POST":
        history.is_deleted = 0
        history.save()
        messages.success(request, "Medical History has been Successfully Restored!")
        return redirect('archive_medHistory')
    context ={'history':history}
    return render(request,'secretary/archive/recover_history.html', context)


def generateServiceInvoice(request,pk2):
    id = request.user.id
    user = User.objects.get(pk=id)
    charge_in = chargeSlip.objects.get(id=pk2)
    servicequery = serviceInvoice.objects.filter(chargeslip=charge_in)
    productquery = productInvoice.objects.filter(chargeslip=charge_in)
    form=ProductInvoice()
    if request.POST:
        form = ProductInvoice(request.POST,initial={'chargeslip':charge_in})
        if form.is_valid():
            prod_in = form.cleaned_data.get('product')
            quantity_in = form.cleaned_data.get('quantity')
            get_prod_in = Product.objects.get(id=prod_in.id)
            if productInvoice.objects.filter(chargeslip=charge_in).filter(product=get_prod_in).exists():
                messages.error(request, "Product is already added!")
                return HttpResponseRedirect(reverse('serviceInvoice', args=[str(pk2)]))
            if quantity_in > get_prod_in.quantity or quantity_in <= 0:
                messages.error(request, "Insufficient amount of quantity!")
                return HttpResponseRedirect(reverse('serviceInvoice', args=[str(pk2)]))
            else:
                a = form.save()
                total_in = quantity_in * get_prod_in.product.price
                remaining_prod_in = get_prod_in.quantity - quantity_in
                get_prod_in.quantity = remaining_prod_in
                get_prod_in.save()
                a.total = total_in
                a.save()
            messages.success(request, "Successfully Added!")
            return HttpResponseRedirect(reverse('serviceInvoice', args=[str(pk2)]))
        else:
            messages.error(request, "There is an error upon adding!")
    else:
        form = ProductInvoice(initial={'chargeslip':charge_in })
    all_service_total = 0 
    for services in servicequery:
        vars = services.total + all_service_total
        all_service_total = vars
    all_prod_total = 0
    for prods in productquery:
        var = prods.total + all_prod_total
        all_prod_total = var
    charge_in.totalAmount = all_service_total + all_prod_total
    if charge_in.status == "Unpaid":
        charge_in.balance = charge_in.totalAmount 
        charge_in.save()
    context = {'sideb':'generateServiceInvoice', 'chargeslip':charge_in ,'form': form,'productquery':productquery,'servicequery':servicequery}
    return render(request,'veterinarian/chargeSlip.html',context) 


def modify_quantity(request,pk,pk2):
    context={}
    id = request.user.id
    user = User.objects.get(pk=id)
    charge_in = chargeSlip.objects.get(id=pk)
    get_invoice = productInvoice.objects.get(id=pk2)
    sample = get_invoice.quantity
    sample_id = get_invoice.product.id
    x = Product.objects.get(id=sample_id)
    servicequery = serviceInvoice.objects.filter(chargeslip=charge_in)
    productquery = productInvoice.objects.filter(chargeslip=charge_in)
    y = x.quantity + sample
    if request.POST:
        form = ProductInvoice(request.POST,instance=get_invoice)
        if form.is_valid():
            prod_in = form.cleaned_data.get('product')
            quantity_in = form.cleaned_data.get('quantity')
            if productInvoice.objects.filter(chargeslip=charge_in).exclude(id=pk2).filter(product=prod_in).exists():
                messages.error(request, "Product is already added!")
                return HttpResponseRedirect(reverse('serviceInvoice', args=[str(pk)]))
            if quantity_in > y or quantity_in <= 0:
                messages.error(request, "Invalid quantity!")
                return HttpResponseRedirect(reverse('serviceInvoice', args=[str(pk)]))
            else:
                quanti = x.quantity + sample
                x.quantity = quanti
                x.save()
                a = form.save()
                get_prod_in = Product.objects.get(id=prod_in.id)
                total_in = quantity_in * prod_in.product.price
                remaining_prod_in = get_prod_in.quantity - quantity_in
                get_prod_in.quantity = remaining_prod_in
                get_prod_in.save()
                a.total = total_in
                a.save()
                messages.success(request, "Quantity has been changed!")
                return HttpResponseRedirect(reverse('serviceInvoice', args=[str(pk)]))
    else:
        form = ProductInvoice(initial ={"chargeslip":get_invoice.chargeslip,"product":get_invoice.product,'quantity':get_invoice.quantity})
        context['form'] = form
        context['get_invoice'] = get_invoice
        context['productquery'] = productquery
        context['servicequery'] = servicequery
        context['chargeslip'] = charge_in
    return render(request,'veterinarian/chargeSlip.html',context) 

def vet_remove_product(request,pk,pk2):
    product_invoice = productInvoice.objects.get(id=pk2)
    query = product_invoice.product.id
    get_product = Product.objects.get(id=query)
    quantity = product_invoice.quantity + get_product.quantity
    get_product.quantity = quantity
    get_product.save()
    product_invoice.delete()
    messages.success(request, "Removed Successfully!")
    return HttpResponseRedirect(reverse('serviceInvoice', args=[str(pk)]))


def sec_chargeslip(request):
    all_chargeslip = chargeSlip.objects.filter(is_deleted=False)
    flag = 0
    context={'all_chargeslip':all_chargeslip, 'sideb' : 'sec_chargeSlip','flag':flag}
    return render(request,'secretary/transaction/sec_chargeslip.html',context) 

def sec_chargeslip_fully(request):
    all_chargeslip = chargeSlip.objects.filter(is_deleted=False,status="Fully Paid")
    flag = 1
    context={'all_chargeslip':all_chargeslip, 'sideb' : 'sec_chargeSlip','flag':flag}
    return render(request,'secretary/transaction/sec_chargeslip.html',context) 

def sec_chargeslip_partial(request):
    all_chargeslip = chargeSlip.objects.filter(is_deleted=False,status="Partially Paid")
    flag = 2
    context={'all_chargeslip':all_chargeslip, 'sideb' : 'sec_chargeSlip','flag':flag}
    return render(request,'secretary/transaction/sec_chargeslip.html',context) 

def sec_chargeslip_unpaid(request):
    all_chargeslip = chargeSlip.objects.filter(is_deleted=False,status="Unpaid")
    flag = 3
    context={'all_chargeslip':all_chargeslip, 'sideb' : 'sec_chargeSlip','flag':flag}
    return render(request,'secretary/transaction/sec_chargeslip.html',context) 

def sec_transaction(request):
    all_chargeslip = transaction.objects.filter(is_deleted=False)
    context={'sideb':'sec_transaction','all_chargeslip':all_chargeslip}
    return render(request,'secretary/transaction/sec_transaction.html',context) 


def petowner_transaction_history(request):
    user = request.user.id
    owner = Profile.objects.get(useracc=user)
    all_chargeslip = chargeSlip.objects.filter(petowner=owner)
    print(all_chargeslip)
    context={'sideb':'petowner_transaction_history','all_chargeslip':all_chargeslip}
    return render(request,'petowner/view_transaction_history.html',context) 


def owner_view_transaction(request,pk):
    context={}
    user = request.user.id
    charge_in = chargeSlip.objects.get(id=pk)
    servicequery = serviceInvoice.objects.filter(chargeslip=charge_in)
    productquery = productInvoice.objects.filter(chargeslip=charge_in)
    transact = transaction.objects.filter(chargeslip=charge_in).order_by('id')
    all_service_total = 0 
    for services in servicequery:
        vars = services.total + all_service_total
        all_service_total = vars
    all_prod_total = 0
    for prods in productquery:
        var = prods.total + all_prod_total
        all_prod_total = var
    if request.method == 'POST':
        context['productquery'] = productquery
        context['servicequery'] = servicequery
        context['chargeslip'] = charge_in
        context['transact'] = transact
        context['all_prod_total'] = all_prod_total
        context['all_service_total'] = all_service_total
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] =  'filename="Service_Invoice_Report.pdf"'
        # find the template and render it.
        template = get_template('for_render_pdf/individual_chargeslip.html')
        html = template.render(context)
        # create a pdf
        pisa_status = pisa.CreatePDF(
        html, dest=response)
        # if error then show some funny view
        if pisa_status.err:
            return HttpResponse('We had some errors <pre>' + html + '</pre>')
        return response
    context={'sideb':'view_transaction','chargeslip':charge_in,'servicequery':servicequery,'productquery':productquery,'all_service_total':all_service_total,'all_prod_total':all_prod_total,'transact':transact}
    return render(request,'petowner/view_transaction.html',context) 


def transaction_view(request,pk):
    user = request.user.id
    trans = transaction.objects.get(id=pk)
    context={'sideb' : 'transaction_view','trans':trans}
    return render(request,'secretary/transaction/view_per_transaction.html',context) 


def chargeSlip_edit(request,pk):
    charge_in = chargeSlip.objects.get(id=pk)
    servicequery = serviceInvoice.objects.filter(chargeslip=charge_in)
    productquery = productInvoice.objects.filter(chargeslip=charge_in)
    form=ProductInvoice()
    if request.POST:
        form = ProductInvoice(request.POST,initial={'chargeslip':charge_in})
        if form.is_valid():
            prod_in = form.cleaned_data.get('product')
            quantity_in = form.cleaned_data.get('quantity')
            get_prod_in = Product.objects.get(id=prod_in.id)
            if productInvoice.objects.filter(chargeslip=charge_in).filter(product=get_prod_in).exists():
                messages.error(request, "Product is already added!")
                return HttpResponseRedirect(reverse('chargeslip_edit', args=[str(pk)]))
            if quantity_in > get_prod_in.quantity or quantity_in <= 0:
                messages.error(request, "Insufficient amount of quantity!")
                return HttpResponseRedirect(reverse('chargeslip_edit', args=[str(pk)]))
            else:
                a = form.save()
                total_in = quantity_in * get_prod_in.product.price
                remaining_prod_in = get_prod_in.quantity - quantity_in
                get_prod_in.quantity = remaining_prod_in
                get_prod_in.save()
                a.total = total_in
                a.save()
            messages.success(request, "Successfully Added!")
            return HttpResponseRedirect(reverse('chargeslip_edit', args=[str(pk)]))
        else:
            messages.error(request, "There is an error upon adding!")
    else:
        form = ProductInvoice(initial={'chargeslip':charge_in })
    all_service_total = 0 
    for services in servicequery:
        vars = services.total + all_service_total
        all_service_total = vars
    all_prod_total = 0
    for prods in productquery:
        var = prods.total + all_prod_total
        all_prod_total = var
    charge_in.totalAmount = all_service_total + all_prod_total
    if charge_in.status == "Unpaid":
        charge_in.balance = charge_in.totalAmount 
        charge_in.save()
    context={'sideb':'chargeslipEdit','form':form,'chargeslip':charge_in,'servicequery':servicequery,'productquery':productquery,'all_service_total':all_service_total,'all_prod_total':all_prod_total}
    return render(request,'secretary/transaction/chargeslipEdit.html',context) 

def sec_modify_quantity(request,pk,pk2):
    context={}
    id = request.user.id
    user = User.objects.get(pk=id)
    charge_in = chargeSlip.objects.get(id=pk)
    get_invoice = productInvoice.objects.get(id=pk2)
    sample = get_invoice.quantity
    sample_id = get_invoice.product.id
    x = Product.objects.get(id=sample_id)
    servicequery = serviceInvoice.objects.filter(chargeslip=charge_in)
    productquery = productInvoice.objects.filter(chargeslip=charge_in)
    y = x.quantity + sample
    if request.POST:
        form = ProductInvoice(request.POST,instance=get_invoice)
        if form.is_valid():
            prod_in = form.cleaned_data.get('product')
            quantity_in = form.cleaned_data.get('quantity')
            if productInvoice.objects.filter(chargeslip=charge_in).exclude(id=pk2).filter(product=prod_in).exists():
                messages.error(request, "Product is already added!")
                return HttpResponseRedirect(reverse('chargeslip_edit', args=[str(pk)]))
            if quantity_in > y or quantity_in <= 0:
                messages.error(request, "Invalid quantity!")
                return HttpResponseRedirect(reverse('chargeslip_edit', args=[str(pk)]))
            else:
                quanti = x.quantity + sample
                x.quantity = quanti
                x.save()
                a = form.save()
                get_prod_in = Product.objects.get(id=prod_in.id)
                total_in = quantity_in * prod_in.product.price
                remaining_prod_in = get_prod_in.quantity - quantity_in
                get_prod_in.quantity = remaining_prod_in
                get_prod_in.save()
                a.total = total_in
                a.save()
                messages.success(request, "Quantity has been changed!")
                return HttpResponseRedirect(reverse('chargeslip_edit', args=[str(pk)]))
    else:
        form = ProductInvoice(initial ={"chargeslip":get_invoice.chargeslip,"product":get_invoice.product,'quantity':get_invoice.quantity})
        context['form'] = form
        context['get_invoice'] = get_invoice
        context['productquery'] = productquery
        context['servicequery'] = servicequery
        context['chargeslip'] = charge_in
    return render(request,'secretary/transaction/chargeslipEdit.html',context) 

def sec_remove_product(request,pk,pk2):
    product_invoice = productInvoice.objects.get(id=pk2)
    query = product_invoice.product.id
    get_product = Product.objects.get(id=query)
    quantity = product_invoice.quantity + get_product.quantity
    get_product.quantity = quantity
    get_product.save()
    product_invoice.delete()
    messages.success(request, "Removed Successfully!")
    return HttpResponseRedirect(reverse('chargeslip_edit', args=[str(pk)]))


def chargeslipView(request,pk):
    context={}
    id = request.user.id
    user = User.objects.get(pk=id)
    charge_in = chargeSlip.objects.get(id=pk)
    servicequery = serviceInvoice.objects.filter(chargeslip=charge_in)
    productquery = productInvoice.objects.filter(chargeslip=charge_in)
    transact = transaction.objects.filter(chargeslip=charge_in).order_by('id')
    all_service_total = 0 
    for services in servicequery:
        vars = services.total + all_service_total
        all_service_total = vars
    all_prod_total = 0
    for prods in productquery:
        var = prods.total + all_prod_total
        all_prod_total = var
    #all_chargeslip = chargeSlip.objects.filter(is_deleted=False)
    all_chargeslip = chargeSlip.objects.get(id=pk)
    all_service_total = 0 
    for services in servicequery:
        vars = services.total + all_service_total
        all_service_total = vars
    all_prod_total = 0
    for prods in productquery:
        var = prods.total + all_prod_total
        all_prod_total = var
    charge_in.totalAmount = all_service_total + all_prod_total
    charge_in.save()
    if charge_in.status == "Unpaid":
        charge_in.balance = charge_in.totalAmount 
        charge_in.save()
    if request.method == 'POST':
        context['productquery'] = productquery
        context['servicequery'] = servicequery
        context['chargeslip'] = charge_in
        context['transact'] = transact
        context['all_chargeslip'] = all_chargeslip
        context['all_prod_total'] = all_prod_total
        context['all_service_total'] = all_service_total
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] =  'filename="Service_Invoice_Report.pdf"'
        # find the template and render it.
        template = get_template('for_render_pdf/individual_chargeslip.html')
        html = template.render(context)
        # create a pdf
        pisa_status = pisa.CreatePDF(
        html, dest=response)
        # if error then show some funny view
        if pisa_status.err:
            return HttpResponse('We had some errors <pre>' + html + '</pre>')
        return response
    context={'sideb' : 'chargeslip_view','all_chargeslip':all_chargeslip,'chargeslip':charge_in,'servicequery':servicequery,'productquery':productquery,'all_service_total':all_service_total,'all_prod_total':all_prod_total,'transact': transact}
    return render(request,'secretary/transaction/chargeSlipView.html',context) 

def transact_payment(request,pk):
    id = request.user.id
    user = User.objects.get(pk=id)
    today = date.today()
    more = date.today() + timedelta(7)
    staffs = StaffProfile.objects.get(useracc=user)
    all_trans = transaction.objects.all()
    charge_in = chargeSlip.objects.get(id=pk)
    if request.method == 'POST':
        grandTotal = request.POST.get('grandTotal')
        tenderedAmount = request.POST.get('tenderedAmount')
        changeAmount = request.POST.get('change')
        balance = request.POST.get('balance')
        trans = transaction(chargeslip=charge_in,grandTotal=charge_in.balance,tenderedAmount=tenderedAmount,changeAmount=changeAmount,staff=staffs)
        trans.save()
        codes= "TH" + "%x" % random.randint(0, 0xFFFFF)
        for i in all_trans:
            if i.code == codes:
                codes= "TH" + "%x" % random.randint(0, 0xFFFFF)
        trans.code=codes
        trans.save()
        param = trans.id
        charge_in.balance = balance
        print(charge_in.balance)
        if charge_in.balance == '0':
            print('no')
            charge_in.status = "Fully Paid"
            charge_in.save()
            if charge_in.petowner is not None:
                subject = 'Dagupan Animal Clinic Payment'
                message = 'You have successfully paid the amount of'+ charge_in.balance + ' php! Thank you for availing our services'
                recipient = charge_in.petowner.useracc.email
                send_mail(subject, message, settings.EMAIL_HOST_USER, [recipient], fail_silently=False)
            else:
                pass
        else:
            print('yes')
            charge_in.status  = "Partially Paid"
            charge_in.save()
            if charge_in.petowner is not None:
                subject = 'Dagupan Animal Clinic Payment'
                message = 'You have successfully paid the amount of'+ tenderedAmount + ' php but you still have a remaining balance amounting of'+ charge_in.balance + ' php. Please settle it with the clinic immediately, thank you!'
                recipient = charge_in.petowner.useracc.email
                send_mail(subject, message, settings.EMAIL_HOST_USER, [recipient], fail_silently=False)
            else:
                pass
        return redirect('billing')
    context={'sideb' : 'transact_payment','chargeslip':charge_in}
    return render(request,'secretary/transaction/transact_payment.html',context) 


def outside_buyer(request):
    all_charge = chargeSlip.objects.all()
    
    context = {'sideb' : 'product_chargeslip_raw'}
    if request.POST:
        form = Sec_ProductInvoice(request.POST)
        if form.is_valid():
            x = form.save()
            prod_in = form.cleaned_data.get('product')
            quantity_in = form.cleaned_data.get('quantity')
            get_prod_in = Product.objects.get(id=prod_in.id)
            total_in = quantity_in * get_prod_in.product.price
            remaining_prod_in = get_prod_in.quantity - quantity_in
            get_prod_in.quantity = remaining_prod_in
            get_prod_in.save()
            x.total = total_in
            charge_in = chargeSlip()
            charge_in.save()
            codes= "CS" + "%x" % random.randint(0, 0xFFFFF)
            for i in all_charge:
                if i.code == codes:
                    codes= "CS" + "%x" % random.randint(0, 0xFFFFF)
            b = charge_in.id
            charge = chargeSlip.objects.get(id=b)
            charge.code = codes
            charge.save()
            x.chargeslip = charge
            x.save()
            messages.success(request, "Successfully Added!")
            context['form'] = form
            return HttpResponseRedirect(reverse('outside_buyer_edit', args=[str(charge.id)]))
        else:
            messages.error(request, "-") #hindi ko gets san galing yung text na dinidisplay T_T
            context['form'] = form
            return render(request,'secretary/transaction/product_chargeslip.html', context)
    else:
        form = Sec_ProductInvoice()
        context['form'] = form
    return render(request,'secretary/transaction/product_chargeslip_raw.html', context)


def outside_buyer_created(request,pk):
    charge_in = chargeSlip.objects.get(id=pk)
    productquery = productInvoice.objects.filter(chargeslip=charge_in)
    form=ProductInvoice()
    if request.POST:
        form = ProductInvoice(request.POST,initial={'chargeslip':charge_in})
        if form.is_valid():
            prod_in = form.cleaned_data.get('product')
            quantity_in = form.cleaned_data.get('quantity')
            get_prod_in = Product.objects.get(id=prod_in.id)
            if productInvoice.objects.filter(chargeslip=charge_in).filter(product=get_prod_in).exists():
                messages.error(request, "Product is already added!")
                return HttpResponseRedirect(reverse('outside_buyer_edit', args=[str(pk)]))
            if quantity_in > get_prod_in.quantity or quantity_in <= 0:
                messages.error(request, "Insufficient amount of quantity!")
                return HttpResponseRedirect(reverse('outside_buyer_edit', args=[str(pk)]))
            else:
                a = form.save()
                total_in = quantity_in * get_prod_in.product.price
                remaining_prod_in = get_prod_in.quantity - quantity_in
                get_prod_in.quantity = remaining_prod_in
                get_prod_in.save()
                a.total = total_in
                a.save()
            messages.success(request, "Successfully Added!")
            return HttpResponseRedirect(reverse('outside_buyer_edit', args=[str(pk)]))
        else:
            messages.error(request, "There is an error upon adding!")
    else:
        form = ProductInvoice(initial={'chargeslip':charge_in })
    all_prod_total = 0
    for prods in productquery:
        var = prods.total + all_prod_total
        all_prod_total = var
    charge_in.totalAmount =  all_prod_total
    if charge_in.status == "Unpaid":
        charge_in.balance = charge_in.totalAmount 
        charge_in.save()
    
    context={'sideb' : 'product_chargeslip','form':form,'chargeslip':charge_in,'productquery':productquery,'all_prod_total':all_prod_total}
    return render(request,'secretary/transaction/product_chargeslip.html',context) 


def sec_remove_outside(request,pk,pk2):
    product_invoice = productInvoice.objects.get(id=pk2)
    query = product_invoice.product.id
    get_product = Product.objects.get(id=query)
    quantity = product_invoice.quantity + get_product.quantity
    get_product.quantity = quantity
    get_product.save()
    product_invoice.delete()
    messages.success(request, "Removed Successfully!")
    return HttpResponseRedirect(reverse('outside_buyer_edit', args=[str(pk)]))


def sec_modify_outside(request,pk,pk2):
    context={}
    id = request.user.id
    user = User.objects.get(pk=id)
    charge_in = chargeSlip.objects.get(id=pk)
    get_invoice = productInvoice.objects.get(id=pk2)
    sample = get_invoice.quantity
    sample_id = get_invoice.product.id
    x = Product.objects.get(id=sample_id)
    productquery = productInvoice.objects.filter(chargeslip=charge_in)
    y = x.quantity + sample
    if request.POST:
        form = Sec_ProductInvoice(request.POST,instance=get_invoice)
        if form.is_valid():
            prod_in = form.cleaned_data.get('product')
            quantity_in = form.cleaned_data.get('quantity')
            if productInvoice.objects.filter(chargeslip=charge_in).exclude(id=pk2).filter(product=prod_in).exists():
                messages.error(request, "Product is already added!")
                return HttpResponseRedirect(reverse('outside_buyer_edit', args=[str(pk)]))
            if quantity_in > y or quantity_in <= 0:
                messages.error(request, "Invalid quantity!")
                return HttpResponseRedirect(reverse('outside_buyer_edit', args=[str(pk)]))
            else:
                quanti = x.quantity + sample
                x.quantity = quanti
                x.save()
                a = form.save()
                get_prod_in = Product.objects.get(id=prod_in.id)
                total_in = quantity_in * prod_in.product.price
                remaining_prod_in = get_prod_in.quantity - quantity_in
                get_prod_in.quantity = remaining_prod_in
                get_prod_in.save()
                a.total = total_in
                a.save()
                messages.success(request, "Quantity has been changed!")
                return HttpResponseRedirect(reverse('outside_buyer_edit', args=[str(pk)]))
    else:
        form = Sec_ProductInvoice(initial ={"chargeslip":get_invoice.chargeslip,"product":get_invoice.product,'quantity':get_invoice.quantity})
        context['form'] = form
        context['get_invoice'] = get_invoice
        context['productquery'] = productquery
        context['chargeslip'] = charge_in
        return render(request,'secretary/transaction/product_chargeslip.html',context) 

def set_appointment_slot(request):
    context = {'sideb': 'scheduling_slot'}
    
    all_sched = schedule_slot.objects.all()
    all_sched_del = schedule_slot.objects.filter(is_deleted=False)
    today = date.today()
    form = Schedule_Slot(request.POST)
    if request.method == "POST":
        form = Schedule_Slot(request.POST)
        if form.is_valid():
            dates = form.cleaned_data.get('date')
            formatdate = dates.strftime("%A")
            timeIn = form.cleaned_data.get('timeIn')
            timeOut = form.cleaned_data.get('timeOut')
            inputIn = str(timeIn).split(':')
            inputOut = str(timeOut).split(':')
            vet = form.cleaned_data.get('vet')
            limit = float(inputIn[0])*60 + float(inputIn[1]) + 30
            print(limit)
            limits = float(inputOut[0])*60 + float(inputOut[1])
            print(limits)
            if timeIn >= timeOut:
                messages.error(request,'Time Start should not be later than Time End')  
                print()     
                return redirect('scheduling_slot')
            elif float(inputIn[0]) < 8 or float(inputOut[0]) < 8:
                messages.error(request,'Time should not be earlier that Opening Hour')         
                return redirect('scheduling_slot')       
            elif (float(inputIn[0])*60 + float(inputIn[1]) > 1050) or  (float(inputOut[0])*60 + float(inputOut[1]) > 1050):
                messages.error(request,'Time should not be later than Closing Hours')         
                return redirect('scheduling_slot')  
            elif dates < today:
                messages.error(request,'Invalid Date of Schedule')         
                return redirect('scheduling_slot')      
            elif limit != limits:
                messages.error(request,"Time must only be 30 minutes")         
                return redirect('scheduling_slot')    
            else:
                if formatdate == "Sunday" and float(inputIn[0]) < 9:
                    messages.error(request,'Time should not be earlier that Opening Hour')
                    return redirect('scheduling_slot')
                elif formatdate == "Sunday" and float(inputIn[0]) > 12:
                    messages.error(request,'Time should not be later than Closing Hours')
                    return redirect('scheduling_slot') 
                else:
                    if schedule_slot.objects.filter(date=dates,timeIn = timeIn, vet=vet).exists():
                        messages.error(request,'Schedule is already added')         
                        return redirect('scheduling_slot')
                    else: 
                        print('hi')
                        x = form.save()
                        codes= "CS" + "%x" % random.randint(0, 0xFFFFF)
                        for i in all_sched:
                            if i.code == codes:
                                codes= "CS" + "%x" % random.randint(0, 0xFFFFF)
                        x.code = codes
                        x.save()
                        context['form'] = form
                        messages.success(request,'Slot has been successfully created!')         
                        return redirect('scheduling_slot') 
        else:
            print('hi')
            context['form'] = form
    else:
        form = Schedule_Slot()
        context['form'] = form
        context['all_sched'] = all_sched
        context['all_sched_del'] = all_sched_del
    return render(request,'secretary/schedule/schedule_slot.html',context) 


def edit_set_appointment_slot(request,pk):
    context = {}
    today = date.today()
    all_sched_del = schedule_slot.objects.filter(is_deleted=False)
    sched = schedule_slot.objects.get(id=pk)
    all_sched = schedule_slot.objects.all()
    form = Schedule_Slot(request.POST,instance=sched)
    if request.method == "POST":
        form = Schedule_Slot(request.POST,instance=sched)
        if form.is_valid():
            dates = form.cleaned_data.get('date')
            formatdate = dates.strftime("%A")
            timeIn = form.cleaned_data.get('timeIn')
            timeOut = form.cleaned_data.get('timeOut')
            inputIn = str(timeIn).split(':')
            inputOut = str(timeOut).split(':')
            vet = form.cleaned_data.get('vet')
            limit = float(inputIn[0])*60 + float(inputIn[1]) + 30
            print(limit)
            limits = float(inputOut[0])*60 + float(inputOut[1])
            print(limits)
            if timeIn >= timeOut:
                messages.error(request,'Time Start should not be later than Time End')  
                print()     
                return redirect('scheduling_slot')
            elif float(inputIn[0]) < 8 or float(inputOut[0]) < 8:
                messages.error(request,'Time should not be earlier that Opening Hour')         
                return redirect('scheduling_slot')       
            elif (float(inputIn[0])*60 + float(inputIn[1]) > 1050) or  (float(inputOut[0])*60 + float(inputOut[1]) > 1050):
                messages.error(request,'Time should not be later than Closing Hours')         
                return redirect('scheduling_slot')   
            elif dates < today:
                messages.error(request,'Invalid Date of Schedule')         
                return redirect('scheduling_slot')      
            elif limit != limits:
                messages.error(request,'Time must only be 30 minutes')         
                return redirect('scheduling_slot')
            elif schedule_slot.objects.filter(date=dates,timeIn = timeIn,vet=vet).exclude(id=pk).exists():
                messages.error(request,'Schedule is already plotted')         
                return redirect('scheduling_slot')
            else:
                if formatdate == "Sunday" and float(inputIn[0]) < 9:
                    messages.error(request,'Time should not be earlier that Opening Hour')
                    return redirect('scheduling_slot')
                elif formatdate == "Sunday" and float(inputIn[0]) > 12:
                    messages.error(request,'Time should not be earlier that Closing Hour')
                    return redirect('scheduling_slot') 
                else:
                    if schedule_slot.objects.filter(date=dates,timeIn = timeIn,vet=vet).exclude(id=pk).exists():
                        messages.error(request,'Schedule is already added')         
                        return redirect('scheduling_slot')
                    else: 
                        print('hi')
                        x = form.save()
                        codes= "CS" + "%x" % random.randint(0, 0xFFFFF)
                        for i in all_sched:
                            if i.code == codes:
                                codes= "CS" + "%x" % random.randint(0, 0xFFFFF)
                        x.code = codes
                        x.save()
                        context['form'] = form
                        messages.success(request,'Slot has been successfully updated!')         
                        return redirect('scheduling_slot') 
        else:
            context['form'] = form
    else:
        form = Schedule_Slot(instance=sched)
        context['form'] = form
        context['all_sched'] = all_sched
        context['all_sched_del'] = all_sched_del
    return render(request,'secretary/schedule/schedule_slot.html',context) 

def delete_scheduling_slot(request,pk):
    sched = schedule_slot.objects.get(id=pk)
    if request.method == "POST":
        sched.is_deleted = 1
        sched.date_of_delete = datetime.today()
        sched.save()
        messages.success(request, "Successfully Deleted!")
        return redirect('scheduling_slot')
    context ={'sched':sched}
    return render(request,'secretary/schedule/delete_schedule.html',context)


def choose_pet(request):
   
    user = request.user.id
    getProf = Profile.objects.get(useracc=user)
    all_pets = pets.objects.filter(petOwner=getProf)
    try:
        flagstatus = flagsystem.objects.get(petOwner=getProf.id)
        if flagstatus.is_restricted == 1:
            flag = 1
        else:
            flag = 0
        context = {'flagstatus':flagstatus}
    except flagsystem.DoesNotExist:
        flag = 0
    context = {'sideb':'choose_pet','all_pets':all_pets}
    context['flag'] = flag
    return render(request,'petowner/choose_pet.html',context)


def schedulings(request,pk):
    user = request.user
    pet = pets.objects.get(id=pk)
    today = date.today()
    form = SchedulingForm(initial={'pet': pet})
    if request.method == 'POST':
        form = SchedulingForm(request.POST,initial={'pet': pet})
        if form.is_valid():
            get_pet = form.cleaned_data.get('pet')
            print(get_pet)
            dates = form.cleaned_data.get('date')
            print(date)
            slot = form.cleaned_data.get('slot')
            print(slot)
            if dates < today:
                messages.error(request,"Schedule Date is invalid, date must not be earlier than today!")
                return redirect('choose_pet')
            else:
                form.save()
                reserve = schedule_slot.objects.get(id=slot.id)
                reserve.is_reserved = 1
                reserve.save()
                subject = 'Dagupan Animal Clinic Appointment'
                formatDate = dates.strftime("%d-%b-%y")
                message = 'You have successfully reserved an appointment on' +  formatDate + '-' + str(reserve.timeIn) + '-' + str(reserve.timeOut) + ".Please come on time." 
                recipient = user
                send_mail(subject, message, settings.EMAIL_HOST_USER, [recipient], fail_silently=False)
                messages.success(request,"Appointment is successfully reserved")
                return redirect('choose_pet')
        else:
            form = SchedulingForm(request.POST,initial={'pet': pet})
            print('heloo')
    context ={'sideb':'scheduling','form':form,'pet':pet}
    return render(request,'petowner/scheduling.html',context)

def scheduling_terms_condition(request):

    return render(request,'petowner/scheduling_terms_condition.html')




def load_slot(request):
    dateId = request.GET.get('date_Id')
    slots = schedule_slot.objects.filter(date=dateId,is_deleted=False,is_reserved=False).all()
    return render(request, 'petowner/slot_dropdown_option.html', {'slots': slots})


def upcomming_app(request):
    user = request.user.id
    getProf = Profile.objects.get(useracc=user)
    pet = pets.objects.filter(petOwner=getProf)
    getSched = scheduling.objects.filter(pet__petOwner=getProf,status="Reserved")
    cancelledSched = scheduling.objects.filter(pet__petOwner=getProf,status="Cancelled")
    context = {'sideb':'upcomming_app','getSched':getSched,'cancelledSched':cancelledSched}
    return render(request, 'petowner/upcoming_app.html', context)

def cancelled_appointments(request):
    user = request.user.id
    getProf = Profile.objects.get(useracc=user)
    pet = pets.objects.filter(petOwner=getProf)
    getSched = scheduling.objects.filter(pet__petOwner=getProf,status="Reserved")
    cancelledSched = scheduling.objects.filter(pet__petOwner=getProf,status="Cancelled")
    context = {'sideb':'cancelled_appointments','getSched':getSched,'cancelledSched':cancelledSched}
    return render(request, 'petowner/cancelled_appointments.html', context)

def cancelled_app(request,pk):
    user = request.user.id
    today = date.today()
    getProf = Profile.objects.get(useracc=user)
    pet = pets.objects.filter(petOwner=getProf)
    getSched = scheduling.objects.get(id=pk)
    getSlot = schedule_slot.objects.get(id=getSched.slot.id)
    delta = getSched.date -  today  
    print(delta)
    if request.method == "POST":
        if delta.days < 1:
            messages.error(request,'You are not eligible to cancel your appointment')
            return redirect('upcomming_app')
        else:
            getSched.status = "Cancelled"
            getSched.date_of_cancelled = datetime.today()
            getSched.save()
            getSlot.is_reserved = 0
            getSlot.save()
            messages.success(request,"Appointment has been successfully cancelled!")
            return redirect('upcomming_app')
    context = {'sideb':'cancelled_app', 'getSched':getSched}
    return render(request, 'petowner/cancelled_app.html', context)


def sec_set_of_appointments(request):
    user = request.user.id
    today = date.today()
    print(today)
    getSched = scheduling.objects.filter(status="Reserved",date=today)
    upcomingSched = scheduling.objects.filter(status="Reserved")
    cancelledSched = scheduling.objects.filter(status="Cancelled")
    arrived = scheduling.objects.filter(status="Arrived",)
    didnotarrived = scheduling.objects.filter(status="Did Not Arrive")
    context = {'sideb':'sec_upcoming_app','upcomingSched':upcomingSched,'getSched':getSched,'cancelledSched':cancelledSched,'arrived':arrived,'didnotarrived':didnotarrived}
    return render(request, 'secretary/schedule/sec_set_of_appointments.html', context)


def arrived_pet(request,pk):
    user = request.user.id
    getSched = scheduling.objects.get(id=pk)
    getSched.status = "Arrived"
    getSched.save()
    context = {'getSched':getSched}
    return redirect('secDashBoard')

def didnotarrived(request,pk):
    user = request.user.id
    getSched = scheduling.objects.get(id=pk)
    petss = pets.objects.get(id=getSched.pet.id)
    print(petss)
    getProf = Profile.objects.get(id = petss.petOwner.id)
    print(getProf)
    getSched.status = "Did Not Arrive"
    getSched.save()
    flag = flagsystem()
    if flagsystem.objects.filter(petOwner=getProf.id).exists():
        a = flagsystem.objects.get(petOwner=getProf.id)
        a.flagpoints = a.flagpoints + 1
        a.save()
        if a.flagpoints >= 3:
            a.is_restricted = True
            a.save()
            subject = 'Dagupan Animal Clinic Restriction'
            message = "You can no longer set an appointment for the mean time. Please contact the clinic for further information. Res Tel. Nos: 703-7067 / 255-5953 / 703-5519, Clinic Nos. 0927-113-9135 or 0933-823-9772" 
            recipient = getProf.useracc.email
            send_mail(subject, message, settings.EMAIL_HOST_USER, [recipient], fail_silently=False)
        else:
            a.save()
    else:
        flag = flagsystem(petOwner=getProf,flagpoints = 1) 
        flag.save()
        
    context = {'getSched':getSched}
    return redirect('sec_upcoming_app')

def setarrived_pet(request,pk):
    user = request.user.id
    getSched = scheduling.objects.get(id=pk)
    getSched.status = "Arrived"
    getSched.save()
    context = {'getSched':getSched}
    return redirect('sec_upcoming_app')

def setdidnotarrived(request,pk):
    user = request.user.id
    getSched = scheduling.objects.get(id=pk)
    petss = pets.objects.get(id=getSched.pet.id)
    print(petss)
    getProf = Profile.objects.get(id = petss.petOwner.id)
    print(getProf)
    getSched.status = "Did Not Arrive"
    getSched.save()
    flag = flagsystem()
    if flagsystem.objects.filter(petOwner=getProf.id).exists():
        a = flagsystem.objects.get(petOwner=getProf.id)
        a.flagpoints = a.flagpoints + 1
        a.save()
        if a.flagpoints >= 3:
            a.is_restricted = True
            a.save()
            subject = 'Dagupan Animal Clinic Restriction'
            message = "You can no longer set an appointment for the mean time. Please contact the clinic for further information"
            recipient = getProf.useracc.email
            send_mail(subject, message, settings.EMAIL_HOST_USER, [recipient], fail_silently=False)
        else:
            a.save()
    else:
        flag = flagsystem(petOwner=getProf,flagpoints = 1) 
        flag.save()
    context = {'getSched':getSched}
    return redirect('secDashBoard')

def restricted(request):
    user = request.user.id
    getProf = flagsystem.objects.all()
    context = {'sideb':'restricted','getProf':getProf}
    return render(request,'secretary/schedule/restrict.html',context)


def unsrestrict(request,pk):
    user = request.user.id
    getProf = flagsystem.objects.get(id=pk)
    if request.method == "POST":
        getProf.is_restricted = 0
        getProf.flagpoints = 0
        getProf.save()
        subject = 'Dagupan Animal Clinic Unrestriction'
        message = "Your restrictions have been lifted, you can now set an appointment again."
        recipient = getProf.petOwner.useracc
        send_mail(subject, message, settings.EMAIL_HOST_USER, [recipient], fail_silently=False)
        return redirect('restricted')
    context = {'sideb':'unrestrict','getProf':getProf}
    return render(request, 'secretary/schedule/unrestrict.html', context)



def vet_upcoming_app(request):
    user = request.user.id
    today = date.today()
    getProf = StaffProfile.objects.get(useracc=user)
    getSched = scheduling.objects.filter(slot__vet=getProf,status="Arrived")
    getScheddone = scheduling.objects.filter(slot__vet=getProf,status="Done")
    cancelledSched = scheduling.objects.filter(slot__vet=getProf,status="Cancelled")
    didnotarrived = scheduling.objects.filter(slot__vet=getProf,status="Did Not Arrive")
    reserved = scheduling.objects.filter(slot__vet=getProf,status="Reserved")
    context = {'sideb':'vet_upcoming_app','getSched':getSched,'cancelledSched':cancelledSched,'didnotarrived':didnotarrived,'getScheddone':getScheddone,'reserved':reserved}
    return render(request, 'veterinarian/schedule/vet_upcoming_app.html', context)


def headvet_upcoming_app(request):
    user = request.user.id
    today = date.today()
    getProf = StaffProfile.objects.get(useracc=user)
    getSched = scheduling.objects.filter(slot__vet=getProf,status="Arrived")
    getScheddone = scheduling.objects.filter(slot__vet=getProf,status="Done")
    cancelledSched = scheduling.objects.filter(slot__vet=getProf,status="Cancelled")
    didnotarrived = scheduling.objects.filter(slot__vet=getProf,status="Did Not Arrive")
    reserved = scheduling.objects.filter(slot__vet=getProf,status="Reserved")
    context = {'sideb':'headvet_upcoming_app','getSched':getSched,'cancelledSched':cancelledSched,'didnotarrived':didnotarrived,'getScheddone':getScheddone,'reserved':reserved}
    return render(request, 'headveterinarian/vet_upcoming_app.html', context)






#transactions report

def transaction_reports(request):
    context={}
    use = request.user.id
    user = StaffProfile.objects.get(useracc=use)
    today = date.today()
    all_chargeslip = transaction.objects.filter(is_deleted=False)
    if request.method == 'POST':
        if request.POST['filter'] == "Range":
            a = request.POST.get('a')
            b = request.POST.get('b')
            services = transaction.objects.filter(is_deleted=False,date__gte=a,date__lte=b)
            total = 0
            tender = 0
            change = 0
            for serve in services:
                vars = serve.grandTotal + total
                vars2 = serve.tenderedAmount + tender
                var3 = serve.changeAmount + change
                tender = vars2
                total = vars
                change=var3
            context['services'] = services
            context['total'] = total
            context['tender'] = tender
            context['change'] = change
            context['user'] = user
            context['today'] = today
            response = HttpResponse(content_type='application/pdf')
            response['Content-Disposition'] =  'filename="Service_Invoice_Report.pdf"'
            # find the template and render it.
            template = get_template('for_render_pdf/transaction_reports.html')
            html = template.render(context)
            # create a pdf
            pisa_status = pisa.CreatePDF(
            html, dest=response)
            # if error then show some funny view
            if pisa_status.err:
                return HttpResponse('We had some errors <pre>' + html + '</pre>')
            return response

    context={'sideb':'transaction_reports','all_chargeslip':all_chargeslip,'use':use}
    return render(request,'secretary/reports/transaction_reports.html',context) 

def transaction_reports_select(request,pk):
    user = request.user.id
    trans = transaction.objects.get(id=pk)
    context={'sideb' : 'transaction_reports_select','trans':trans,'user':user}
    return render(request,'secretary/reports/transaction_reports_select.html',context)   

#service invoice report

def service_reports(request):
    context={'sideb':'service_reports'}
    #lte,lt,gte,gt
    use = request.user.id
    user = StaffProfile.objects.get(useracc=use)
    today = date.today()
    services = serviceInvoice.objects.all()
    if request.method == 'POST':
        if request.POST['filter'] == "Range":
            a = request.POST.get('a')
            b = request.POST.get('b')
            services = serviceInvoice.objects.filter(is_deleted=False,date__gte=a,date__lte=b)
            total = 0
            for serve in services:
                vars = serve.total + total
                total = vars
            context['services'] = services
            context['total'] = total
            context['today'] = today
            context['user'] = user
            response = HttpResponse(content_type='application/pdf')
            response['Content-Disposition'] =  'filename="Service_Invoice_Report.pdf"'
            # find the template and render it.
            template = get_template('for_render_pdf/try.html')
            html = template.render(context)
            # create a pdf
            pisa_status = pisa.CreatePDF(
            html, dest=response)
            # if error then show some funny view
            if pisa_status.err:
                return HttpResponse('We had some errors <pre>' + html + '</pre>')
            return response
        if request.POST['filter'] == "Report":
            total = 0
            for serve in services:
                vars = serve.total + total
                total = vars
            context['services'] = services
            context['total'] = total
            context['user'] = user
            context['today'] = today
            response = HttpResponse(content_type='application/pdf')
            response['Content-Disposition'] =  'filename="Service_Invoice_Report.pdf"'
            # find the template and render it.
            template = get_template('for_render_pdf/try.html')
            html = template.render(context)
            # create a pdf
            pisa_status = pisa.CreatePDF(
            html, dest=response)
            # if error then show some funny view
            if pisa_status.err:
                return HttpResponse('We had some errors <pre>' + html + '</pre>')
            return response
    context['services'] = services
    context['use'] = use
    return render(request, 'secretary/reports/service_reports.html', context)

def today_service_reports(request):
    context={}
    #lte,lt,gte,gt
    use = request.user.id
    user = StaffProfile.objects.get(useracc=use)
    today = date.today()
    services = serviceInvoice.objects.filter(date=today)
    if request.method == 'POST':
        if request.POST['filter'] == "Range":
            a = request.POST.get('a')
            b = request.POST.get('b')
            services = serviceInvoice.objects.filter(is_deleted=False,date__gte=a,date__lte=b)
            total = 0
            for serve in services:
                vars = serve.total + total
                total = vars
            context['services'] = services
            context['total'] = total
            context['today'] = today
            context['user'] = user
            response = HttpResponse(content_type='application/pdf')
            response['Content-Disposition'] =  'filename="Service_Invoice_Report.pdf"'
            # find the template and render it.
            template = get_template('for_render_pdf/try.html')
            html = template.render(context)
            # create a pdf
            pisa_status = pisa.CreatePDF(
            html, dest=response)
            # if error then show some funny view
            if pisa_status.err:
                return HttpResponse('We had some errors <pre>' + html + '</pre>')
            return response
        if request.POST['filter'] == "Report":
            total = 0
            for serve in services:
                vars = serve.total + total
                total = vars
            context['services'] = services
            context['total'] = total
            context['user'] = user
            context['today'] = today
            response = HttpResponse(content_type='application/pdf')
            response['Content-Disposition'] =  'filename="Service_Invoice_Report.pdf"'
            # find the template and render it.
            template = get_template('for_render_pdf/try.html')
            html = template.render(context)
            # create a pdf
            pisa_status = pisa.CreatePDF(
            html, dest=response)
            # if error then show some funny view
            if pisa_status.err:
                return HttpResponse('We had some errors <pre>' + html + '</pre>')
            return response
    context['services'] = services
    context['use'] = use
    return render(request, 'secretary/reports/service_reports.html', context)

def seven_service_reports(request):
    context={}
    #lte,lt,gte,gt
    use = request.user.id
    user = StaffProfile.objects.get(useracc=use)
    today = date.today()
    last_seven = date.today() - timedelta(7)
    services = serviceInvoice.objects.filter(date__gte=last_seven)
    if request.method == 'POST':
        if request.POST['filter'] == "Range":
            a = request.POST.get('a')
            b = request.POST.get('b')
            services = serviceInvoice.objects.filter(is_deleted=False,date__gte=a,date__lte=b)
            total = 0
            for serve in services:
                vars = serve.total + total
                total = vars
            context['services'] = services
            context['total'] = total
            context['today'] = today
            context['user'] = user
            response = HttpResponse(content_type='application/pdf')
            response['Content-Disposition'] =  'filename="Service_Invoice_Report.pdf"'
            # find the template and render it.
            template = get_template('for_render_pdf/try.html')
            html = template.render(context)
            # create a pdf
            pisa_status = pisa.CreatePDF(
            html, dest=response)
            # if error then show some funny view
            if pisa_status.err:
                return HttpResponse('We had some errors <pre>' + html + '</pre>')
            return response
        if request.POST['filter'] == "Report":
            total = 0
            for serve in services:
                vars = serve.total + total
                total = vars
            context['services'] = services
            context['total'] = total
            context['user'] = user
            context['today'] = today
            response = HttpResponse(content_type='application/pdf')
            response['Content-Disposition'] =  'filename="Service_Invoice_Report.pdf"'
            # find the template and render it.
            template = get_template('for_render_pdf/try.html')
            html = template.render(context)
            # create a pdf
            pisa_status = pisa.CreatePDF(
            html, dest=response)
            # if error then show some funny view
            if pisa_status.err:
                return HttpResponse('We had some errors <pre>' + html + '</pre>')
            return response
    context['services'] = services
    context['use'] = use
    return render(request, 'secretary/reports/service_reports.html', context)

def last_thirty_service_reports(request):
    context={}
    #lte,lt,gte,gt
    use = request.user.id
    user = StaffProfile.objects.get(useracc=use)
    today = date.today()
    last_thirty = date.today() - timedelta(30)
    services = serviceInvoice.objects.filter(date__gte=last_thirty)
    if request.method == 'POST':
        if request.POST['filter'] == "Range":
            a = request.POST.get('a')
            b = request.POST.get('b')
            services = serviceInvoice.objects.filter(is_deleted=False,date__gte=a,date__lte=b)
            total = 0
            for serve in services:
                vars = serve.total + total
                total = vars
            context['services'] = services
            context['total'] = total
            context['today'] = today
            context['user'] = user
            response = HttpResponse(content_type='application/pdf')
            response['Content-Disposition'] =  'filename="Service_Invoice_Report.pdf"'
            # find the template and render it.
            template = get_template('for_render_pdf/try.html')
            html = template.render(context)
            # create a pdf
            pisa_status = pisa.CreatePDF(
            html, dest=response)
            # if error then show some funny view
            if pisa_status.err:
                return HttpResponse('We had some errors <pre>' + html + '</pre>')
            return response
        if request.POST['filter'] == "Report":
            total = 0
            for serve in services:
                vars = serve.total + total
                total = vars
            context['services'] = services
            context['total'] = total
            context['user'] = user
            context['today'] = today
            response = HttpResponse(content_type='application/pdf')
            response['Content-Disposition'] =  'filename="Service_Invoice_Report.pdf"'
            # find the template and render it.
            template = get_template('for_render_pdf/try.html')
            html = template.render(context)
            # create a pdf
            pisa_status = pisa.CreatePDF(
            html, dest=response)
            # if error then show some funny view
            if pisa_status.err:
                return HttpResponse('We had some errors <pre>' + html + '</pre>')
            return response
    context['services'] = services
    context['use'] = use
    return render(request, 'secretary/reports/service_reports.html', context)

def a_year_ago_service_reports(request):
    context={}
    #lte,lt,gte,gt
    use = request.user.id
    user = StaffProfile.objects.get(useracc=use)
    today = date.today()
    a_year_ago = date.today() - timedelta(365)
    services = serviceInvoice.objects.filter(date__gte=a_year_ago)
    if request.method == 'POST':
        if request.POST['filter'] == "Range":
            a = request.POST.get('a')
            b = request.POST.get('b')
            services = serviceInvoice.objects.filter(is_deleted=False,date__gte=a,date__lte=b)
            total = 0
            for serve in services:
                vars = serve.total + total
                total = vars
            context['services'] = services
            context['total'] = total
            context['today'] = today
            context['user'] = user
            response = HttpResponse(content_type='application/pdf')
            response['Content-Disposition'] =  'filename="Service_Invoice_Report.pdf"'
            # find the template and render it.
            template = get_template('for_render_pdf/try.html')
            html = template.render(context)
            # create a pdf
            pisa_status = pisa.CreatePDF(
            html, dest=response)
            # if error then show some funny view
            if pisa_status.err:
                return HttpResponse('We had some errors <pre>' + html + '</pre>')
            return response
        if request.POST['filter'] == "Report":
            total = 0
            for serve in services:
                vars = serve.total + total
                total = vars
            context['services'] = services
            context['total'] = total
            context['user'] = user
            context['today'] = today
            response = HttpResponse(content_type='application/pdf')
            response['Content-Disposition'] =  'filename="Service_Invoice_Report.pdf"'
            # find the template and render it.
            template = get_template('for_render_pdf/try.html')
            html = template.render(context)
            # create a pdf
            pisa_status = pisa.CreatePDF(
            html, dest=response)
            # if error then show some funny view
            if pisa_status.err:
                return HttpResponse('We had some errors <pre>' + html + '</pre>')
            return response
    context['services'] = services
    context['use'] = use
    return render(request, 'secretary/reports/service_reports.html', context)

def more_service_reports(request):
    context={}
    #lte,lt,gte,gt
    use = request.user.id
    user = StaffProfile.objects.get(useracc=use)
    today = date.today()
    more = date.today() - timedelta(365)
    services = serviceInvoice.objects.filter(date__lte=more)
    if request.method == 'POST':
        if request.POST['filter'] == "Range":
            a = request.POST.get('a')
            b = request.POST.get('b')
            services = serviceInvoice.objects.filter(is_deleted=False,date__gte=a,date__lte=b)
            total = 0
            for serve in services:
                vars = serve.total + total
                total = vars
            context['services'] = services
            context['total'] = total
            context['today'] = today
            context['user'] = user
            response = HttpResponse(content_type='application/pdf')
            response['Content-Disposition'] =  'filename="Service_Invoice_Report.pdf"'
            # find the template and render it.
            template = get_template('for_render_pdf/try.html')
            html = template.render(context)
            # create a pdf
            pisa_status = pisa.CreatePDF(
            html, dest=response)
            # if error then show some funny view
            if pisa_status.err:
                return HttpResponse('We had some errors <pre>' + html + '</pre>')
            return response
        if request.POST['filter'] == "Report":
            total = 0
            for serve in services:
                vars = serve.total + total
                total = vars
            context['services'] = services
            context['total'] = total
            context['user'] = user
            context['today'] = today
            response = HttpResponse(content_type='application/pdf')
            response['Content-Disposition'] =  'filename="Service_Invoice_Report.pdf"'
            # find the template and render it.
            template = get_template('for_render_pdf/try.html')
            html = template.render(context)
            # create a pdf
            pisa_status = pisa.CreatePDF(
            html, dest=response)
            # if error then show some funny view
            if pisa_status.err:
                return HttpResponse('We had some errors <pre>' + html + '</pre>')
            return response
    context['services'] = services
    context['use'] = use
    return render(request, 'secretary/reports/service_reports.html', context)

#product Invoice report
def product_reports(request):
    context={'sideb':'product_reports'}
    #lte,lt,gte,gt
    use = request.user.id
    user = StaffProfile.objects.get(useracc=use)
    today = date.today()
    services = productInvoice.objects.all()
    if request.method == 'POST':
        if request.POST['filter'] == "Range":
            a = request.POST.get('a')
            b = request.POST.get('b')
            services = productInvoice.objects.filter(is_deleted=False,date__gte=a,date__lte=b)
            total = 0
            for serve in services:
                vars = serve.total + total
                total = vars
            context['services'] = services
            context['total'] = total
            context['today'] = today
            context['user'] = user
            response = HttpResponse(content_type='application/pdf')
            response['Content-Disposition'] =  'filename="Service_Invoice_Report.pdf"'
            # find the template and render it.
            template = get_template('for_render_pdf/productsInvoiceTemplate.html')
            html = template.render(context)
            # create a pdf
            pisa_status = pisa.CreatePDF(
            html, dest=response)
            # if error then show some funny view
            if pisa_status.err:
                return HttpResponse('We had some errors <pre>' + html + '</pre>')
            return response
        if request.POST['filter'] == "Report":
            total = 0
            for serve in services:
                vars = serve.total + total
                total = vars
            context['services'] = services
            context['total'] = total
            context['user'] = user
            context['today'] = today
            response = HttpResponse(content_type='application/pdf')
            response['Content-Disposition'] =  'filename="Service_Invoice_Report.pdf"'
            # find the template and render it.
            template = get_template('for_render_pdf/try.html')
            html = template.render(context)
            # create a pdf
            pisa_status = pisa.CreatePDF(
            html, dest=response)
            # if error then show some funny view
            if pisa_status.err:
                return HttpResponse('We had some errors <pre>' + html + '</pre>')
            return response
    context['services'] = services
    context['use'] = use
    return render(request, 'secretary/reports/product_reports.html', context)

def today_product_reports(request):
    context={}
    #lte,lt,gte,gt
    use = request.user.id
    user = StaffProfile.objects.get(useracc=use)
    today = date.today()
    services = productInvoice.objects.filter(date=today)
    if request.method == 'POST':
        if request.POST['filter'] == "Range":
            a = request.POST.get('a')
            b = request.POST.get('b')
            services = productInvoice.objects.filter(is_deleted=False,date__gte=a,date__lte=b)
            total = 0
            for serve in services:
                vars = serve.total + total
                total = vars
            context['services'] = services
            context['total'] = total
            context['today'] = today
            context['user'] = user
            response = HttpResponse(content_type='application/pdf')
            response['Content-Disposition'] =  'filename="Service_Invoice_Report.pdf"'
            # find the template and render it.
            template = get_template('for_render_pdf/productsInvoiceTemplate.html')
            html = template.render(context)
            # create a pdf
            pisa_status = pisa.CreatePDF(
            html, dest=response)
            # if error then show some funny view
            if pisa_status.err:
                return HttpResponse('We had some errors <pre>' + html + '</pre>')
            return response
        if request.POST['filter'] == "Report":
            total = 0
            for serve in services:
                vars = serve.total + total
                total = vars
            context['services'] = services
            context['total'] = total
            context['user'] = user
            context['today'] = today
            response = HttpResponse(content_type='application/pdf')
            response['Content-Disposition'] =  'filename="Service_Invoice_Report.pdf"'
            # find the template and render it.
            template = get_template('for_render_pdf/try.html')
            html = template.render(context)
            # create a pdf
            pisa_status = pisa.CreatePDF(
            html, dest=response)
            # if error then show some funny view
            if pisa_status.err:
                return HttpResponse('We had some errors <pre>' + html + '</pre>')
            return response
    context['services'] = services
    context['use'] = use
    return render(request, 'secretary/reports/product_reports.html', context)

def seven_product_reports(request):
    context={}
    #lte,lt,gte,gt
    use = request.user.id
    user = StaffProfile.objects.get(useracc=use)
    today = date.today()
    last_seven = date.today() - timedelta(7)
    services = productInvoice.objects.filter(date__gte=last_seven)
    if request.method == 'POST':
        if request.POST['filter'] == "Range":
            a = request.POST.get('a')
            b = request.POST.get('b')
            services = productInvoice.objects.filter(is_deleted=False,date__gte=a,date__lte=b)
            total = 0
            for serve in services:
                vars = serve.total + total
                total = vars
            context['services'] = services
            context['total'] = total
            context['today'] = today
            context['user'] = user
            response = HttpResponse(content_type='application/pdf')
            response['Content-Disposition'] =  'filename="Service_Invoice_Report.pdf"'
            # find the template and render it.
            template = get_template('for_render_pdf/productsInvoiceTemplate.html')
            html = template.render(context)
            # create a pdf
            pisa_status = pisa.CreatePDF(
            html, dest=response)
            # if error then show some funny view
            if pisa_status.err:
                return HttpResponse('We had some errors <pre>' + html + '</pre>')
            return response
        if request.POST['filter'] == "Report":
            total = 0
            for serve in services:
                vars = serve.total + total
                total = vars
            context['services'] = services
            context['total'] = total
            context['user'] = user
            context['today'] = today
            response = HttpResponse(content_type='application/pdf')
            response['Content-Disposition'] =  'filename="Service_Invoice_Report.pdf"'
            # find the template and render it.
            template = get_template('for_render_pdf/try.html')
            html = template.render(context)
            # create a pdf
            pisa_status = pisa.CreatePDF(
            html, dest=response)
            # if error then show some funny view
            if pisa_status.err:
                return HttpResponse('We had some errors <pre>' + html + '</pre>')
            return response
    context['services'] = services
    context['use'] = use
    return render(request, 'secretary/reports/product_reports.html', context)

def last_thirty_product_reports(request):
    context={}
    #lte,lt,gte,gt
    use = request.user.id
    user = StaffProfile.objects.get(useracc=use)
    today = date.today()
    last_thirty = date.today() - timedelta(30)
    services = productInvoice.objects.filter(date__gte=last_thirty)
    if request.method == 'POST':
        if request.POST['filter'] == "Range":
            a = request.POST.get('a')
            b = request.POST.get('b')
            services = productInvoice.objects.filter(is_deleted=False,date__gte=a,date__lte=b)
            total = 0
            for serve in services:
                vars = serve.total + total
                total = vars
            context['services'] = services
            context['total'] = total
            context['today'] = today
            context['user'] = user
            response = HttpResponse(content_type='application/pdf')
            response['Content-Disposition'] =  'filename="Service_Invoice_Report.pdf"'
            # find the template and render it.
            template = get_template('for_render_pdf/productsInvoiceTemplate.html')
            html = template.render(context)
            # create a pdf
            pisa_status = pisa.CreatePDF(
            html, dest=response)
            # if error then show some funny view
            if pisa_status.err:
                return HttpResponse('We had some errors <pre>' + html + '</pre>')
            return response
        if request.POST['filter'] == "Report":
            total = 0
            for serve in services:
                vars = serve.total + total
                total = vars
            context['services'] = services
            context['total'] = total
            context['user'] = user
            context['today'] = today
            response = HttpResponse(content_type='application/pdf')
            response['Content-Disposition'] =  'filename="Service_Invoice_Report.pdf"'
            # find the template and render it.
            template = get_template('for_render_pdf/try.html')
            html = template.render(context)
            # create a pdf
            pisa_status = pisa.CreatePDF(
            html, dest=response)
            # if error then show some funny view
            if pisa_status.err:
                return HttpResponse('We had some errors <pre>' + html + '</pre>')
            return response
    context['services'] = services
    context['use'] = use
    return render(request, 'secretary/reports/product_reports.html', context)

def a_year_ago_product_reports(request):
    context={}
    #lte,lt,gte,gt
    use = request.user.id
    user = StaffProfile.objects.get(useracc=use)
    today = date.today()
    a_year_ago = date.today() - timedelta(365)
    services = productInvoice.objects.filter(date__gte=a_year_ago)
    if request.method == 'POST':
        if request.POST['filter'] == "Range":
            a = request.POST.get('a')
            b = request.POST.get('b')
            services = productInvoice.objects.filter(is_deleted=False,date__gte=a,date__lte=b)
            total = 0
            for serve in services:
                vars = serve.total + total
                total = vars
            context['services'] = services
            context['total'] = total
            context['today'] = today
            context['user'] = user
            response = HttpResponse(content_type='application/pdf')
            response['Content-Disposition'] =  'filename="Service_Invoice_Report.pdf"'
            # find the template and render it.
            template = get_template('for_render_pdf/productsInvoiceTemplate.html')
            html = template.render(context)
            # create a pdf
            pisa_status = pisa.CreatePDF(
            html, dest=response)
            # if error then show some funny view
            if pisa_status.err:
                return HttpResponse('We had some errors <pre>' + html + '</pre>')
            return response
        if request.POST['filter'] == "Report":
            total = 0
            for serve in services:
                vars = serve.total + total
                total = vars
            context['services'] = services
            context['total'] = total
            context['user'] = user
            context['today'] = today
            response = HttpResponse(content_type='application/pdf')
            response['Content-Disposition'] =  'filename="Service_Invoice_Report.pdf"'
            # find the template and render it.
            template = get_template('for_render_pdf/try.html')
            html = template.render(context)
            # create a pdf
            pisa_status = pisa.CreatePDF(
            html, dest=response)
            # if error then show some funny view
            if pisa_status.err:
                return HttpResponse('We had some errors <pre>' + html + '</pre>')
            return response
    context['services'] = services
    context['use'] = use
    return render(request, 'secretary/reports/product_reports.html', context)

def more_product_reports(request):
    context={}
    #lte,lt,gte,gt
    use = request.user.id
    user = StaffProfile.objects.get(useracc=use)
    today = date.today()
    a_year_ago = date.today() - timedelta(365)
    services = productInvoice.objects.filter(date__lte=a_year_ago)
    if request.method == 'POST':
        if request.POST['filter'] == "Range":
            a = request.POST.get('a')
            b = request.POST.get('b')
            services = productInvoice.objects.filter(is_deleted=False,date__gte=a,date__lte=b)
            total = 0
            for serve in services:
                vars = serve.total + total
                total = vars
            context['services'] = services
            context['total'] = total
            context['today'] = today
            context['user'] = user
            response = HttpResponse(content_type='application/pdf')
            response['Content-Disposition'] =  'filename="Service_Invoice_Report.pdf"'
            # find the template and render it.
            template = get_template('for_render_pdf/productsInvoiceTemplate.html')
            html = template.render(context)
            # create a pdf
            pisa_status = pisa.CreatePDF(
            html, dest=response)
            # if error then show some funny view
            if pisa_status.err:
                return HttpResponse('We had some errors <pre>' + html + '</pre>')
            return response
        if request.POST['filter'] == "Report":
            total = 0
            for serve in services:
                vars = serve.total + total
                total = vars
            context['services'] = services
            context['total'] = total
            context['today'] = today
            context['user'] = user
            response = HttpResponse(content_type='application/pdf')
            response['Content-Disposition'] =  'filename="Service_Invoice_Report.pdf"'
            # find the template and render it.
            template = get_template('for_render_pdf/try.html')
            html = template.render(context)
            # create a pdf
            pisa_status = pisa.CreatePDF(
            html, dest=response)
            # if error then show some funny view
            if pisa_status.err:
                return HttpResponse('We had some errors <pre>' + html + '</pre>')
            return response
    context['services'] = services
    context['use'] = use
    return render(request, 'secretary/reports/product_reports.html', context)

#chargeslip
def chargeSlip_reports(request):
    context={}
    #lte,lt,gte,gt
    use = request.user.id
    user = StaffProfile.objects.get(useracc=use)
    today = date.today()
    services = chargeSlip.objects.all().order_by('status')
    total = 0
    balance = 0
    for serve in services:
        vars = serve.totalAmount + total
        vars2 = serve.balance + balance
        balance = vars2
        total = vars
    context['services'] = services
    context['total'] = total
    context['balance'] = balance
    context['user'] = user
    context['today'] = today
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] =  'filename="ChargeSlip_Report.pdf"'
    # find the template and render it.
    template = get_template('for_render_pdf/chargeSlip_pdf.html')
    html = template.render(context)
    # create a pdf
    pisa_status = pisa.CreatePDF(
    html, dest=response)
    # if error then show some funny view
    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response

def today_chargeSlip_reports(request):
    context={}
    #lte,lt,gte,gt
    use = request.user.id
    user = StaffProfile.objects.get(useracc=use)
    today = date.today()
    services = chargeSlip.objects.filter(date=today).order_by('status')
    total = 0
    balance = 0
    for serve in services:
        vars = serve.totalAmount + total
        vars2 = serve.balance + balance
        balance = vars2
        total = vars
    context['services'] = services
    context['total'] = total
    context['balance'] = balance
    context['user'] = user
    context['today'] = today
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] =  'filename="ChargeSlip_Report.pdf"'
    # find the template and render it.
    template = get_template('for_render_pdf/chargeSlip_pdf.html')
    html = template.render(context)
    # create a pdf
    pisa_status = pisa.CreatePDF(
    html, dest=response)
    # if error then show some funny view
    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response

def seven_chargeSlip_reports(request):
    context={}
    #lte,lt,gte,gt
    use = request.user.id
    user = StaffProfile.objects.get(useracc=use)
    today = date.today()
    last_seven = date.today() - timedelta(7)
    services = chargeSlip.objects.filter(date__gte=last_seven).order_by('status')
    total = 0
    balance = 0
    for serve in services:
        vars = serve.totalAmount + total
        vars2 = serve.balance + balance
        balance = vars2
        total = vars
    context['services'] = services
    context['total'] = total
    context['balance'] = balance
    context['user'] = user
    context['today'] = today
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] =  'filename="ChargeSlip_Report.pdf"'
    # find the template and render it.
    template = get_template('for_render_pdf/chargeSlip_pdf.html')
    html = template.render(context)
    # create a pdf
    pisa_status = pisa.CreatePDF(
    html, dest=response)
    # if error then show some funny view
    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response

def last_thirty_chargeSlip_reports(request):
    context={}
    #lte,lt,gte,gt
    use = request.user.id
    user = StaffProfile.objects.get(useracc=use)
    today = date.today()
    last_thirty = date.today() - timedelta(30)
    services = chargeSlip.objects.filter(date__gte=last_thirty).order_by('status')
    total = 0
    balance = 0
    for serve in services:
        vars = serve.totalAmount + total
        vars2 = serve.balance + balance
        balance = vars2
        total = vars
    context['services'] = services
    context['total'] = total
    context['balance'] = balance
    context['user'] = user
    context['today'] = today
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] =  'filename="ChargeSlip_Report.pdf"'
    # find the template and render it.
    template = get_template('for_render_pdf/chargeSlip_pdf.html')
    html = template.render(context)
    # create a pdf
    pisa_status = pisa.CreatePDF(
    html, dest=response)
    # if error then show some funny view
    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response

def a_year_ago_chargeSlip_reports(request):
    context={}
    #lte,lt,gte,gt
    use = request.user.id
    user = StaffProfile.objects.get(useracc=use)
    today = date.today()
    a_year_ago = date.today() - timedelta(365)
    services = chargeSlip.objects.filter(date__gte=a_year_ago).order_by('status')
    total = 0
    balance = 0
    for serve in services:
        vars = serve.totalAmount + total
        vars2 = serve.balance + balance
        balance = vars2
        total = vars
    context['services'] = services
    context['total'] = total
    context['balance'] = balance
    context['user'] = user
    context['today'] = today
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] =  'filename="ChargeSlip_Report.pdf"'
    # find the template and render it.
    template = get_template('for_render_pdf/chargeSlip_pdf.html')
    html = template.render(context)
    # create a pdf
    pisa_status = pisa.CreatePDF(
    html, dest=response)
    # if error then show some funny view
    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response

def more_chargeSlip_reports(request):
    context={}
    #lte,lt,gte,gt
    use = request.user.id
    user = StaffProfile.objects.get(useracc=use)
    today = date.today()
    a_year_ago = date.today() - timedelta(365)
    services = chargeSlip.objects.filter(date__lte=a_year_ago).order_by('status')
    total = 0
    balance = 0
    for serve in services:
        vars = serve.totalAmount + total
        vars2 = serve.balance + balance
        balance = vars2
        total = vars
    context['services'] = services
    context['total'] = total
    context['balance'] = balance
    context['user'] = user
    context['today'] = today
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] =  'filename="ChargeSlip_Report.pdf"'
    # find the template and render it.
    template = get_template('for_render_pdf/chargeSlip_pdf.html')
    html = template.render(context)
    # create a pdf
    pisa_status = pisa.CreatePDF(
    html, dest=response)
    # if error then show some funny view
    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response

#fully paid
def fully_chargeSlip_reports(request):
    context={}
    #lte,lt,gte,gt
    use = request.user.id
    user = StaffProfile.objects.get(useracc=use)
    today = date.today()
    services = chargeSlip.objects.filter(is_deleted=False,status="Fully Paid")
    total = 0
    balance = 0
    for serve in services:
        vars = serve.totalAmount + total
        vars2 = serve.balance + balance
        balance = vars2
        total = vars
    context['services'] = services
    context['total'] = total
    context['balance'] = balance
    context['user'] = user
    context['today'] = today
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] =  'filename="ChargeSlip_Report.pdf"'
    # find the template and render it.
    template = get_template('for_render_pdf/chargeSlip_pdf.html')
    html = template.render(context)
    # create a pdf
    pisa_status = pisa.CreatePDF(
    html, dest=response)
    # if error then show some funny view
    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response

def fully_today_chargeSlip_reports(request):
    context={}
    #lte,lt,gte,gt
    use = request.user.id
    user = StaffProfile.objects.get(useracc=use)
    today = date.today()
    services = chargeSlip.objects.filter(is_deleted=False,status="Fully Paid",date=today)
    total = 0
    balance = 0
    for serve in services:
        vars = serve.totalAmount + total
        vars2 = serve.balance + balance
        balance = vars2
        total = vars
    context['services'] = services
    context['total'] = total
    context['balance'] = balance
    context['user'] = user
    context['today'] = today
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] =  'filename="ChargeSlip_Report.pdf"'
    # find the template and render it.
    template = get_template('for_render_pdf/chargeSlip_pdf.html')
    html = template.render(context)
    # create a pdf
    pisa_status = pisa.CreatePDF(
    html, dest=response)
    # if error then show some funny view
    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response

def fully_seven_chargeSlip_reports(request):
    context={}
    #lte,lt,gte,gt
    use = request.user.id
    user = StaffProfile.objects.get(useracc=use)
    today = date.today()
    last_seven = date.today() - timedelta(7)
    services = chargeSlip.objects.filter(is_deleted=False,status="Fully Paid",date__gte=last_seven)
    total = 0
    balance = 0
    for serve in services:
        vars = serve.totalAmount + total
        vars2 = serve.balance + balance
        balance = vars2
        total = vars
    context['services'] = services
    context['total'] = total
    context['balance'] = balance
    context['user'] = user
    context['today'] = today
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] =  'filename="ChargeSlip_Report.pdf"'
    # find the template and render it.
    template = get_template('for_render_pdf/chargeSlip_pdf.html')
    html = template.render(context)
    # create a pdf
    pisa_status = pisa.CreatePDF(
    html, dest=response)
    # if error then show some funny view
    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response

def fully_last_thirty_chargeSlip_reports(request):
    context={}
    #lte,lt,gte,gt
    use = request.user.id
    user = StaffProfile.objects.get(useracc=use)
    today = date.today()
    last_thirty = date.today() - timedelta(30)
    services = chargeSlip.objects.filter(is_deleted=False,status="Fully Paid",date__gte=last_thirty)
    total = 0
    balance = 0
    for serve in services:
        vars = serve.totalAmount + total
        vars2 = serve.balance + balance
        balance = vars2
        total = vars
    context['services'] = services
    context['total'] = total
    context['balance'] = balance
    context['user'] = user
    context['today'] = today
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] =  'filename="ChargeSlip_Report.pdf"'
    # find the template and render it.
    template = get_template('for_render_pdf/chargeSlip_pdf.html')
    html = template.render(context)
    # create a pdf
    pisa_status = pisa.CreatePDF(
    html, dest=response)
    # if error then show some funny view
    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response

def fully_a_year_ago_chargeSlip_reports(request):
    context={}
    #lte,lt,gte,gt
    use = request.user.id
    user = StaffProfile.objects.get(useracc=use)
    today = date.today()
    a_year_ago = date.today() - timedelta(365)
    services = chargeSlip.objects.filter(is_deleted=False,status="Fully Paid",date__gte=a_year_ago)
    total = 0
    balance = 0
    for serve in services:
        vars = serve.totalAmount + total
        vars2 = serve.balance + balance
        balance = vars2
        total = vars
    context['services'] = services
    context['total'] = total
    context['balance'] = balance
    context['user'] = user
    context['today'] = today
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] =  'filename="ChargeSlip_Report.pdf"'
    # find the template and render it.
    template = get_template('for_render_pdf/chargeSlip_pdf.html')
    html = template.render(context)
    # create a pdf
    pisa_status = pisa.CreatePDF(
    html, dest=response)
    # if error then show some funny view
    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response

def fully_more_chargeSlip_reports(request):
    context={}
    #lte,lt,gte,gt
    use = request.user.id
    user = StaffProfile.objects.get(useracc=use)
    today = date.today()
    a_year_ago = date.today() - timedelta(365)
    services = chargeSlip.objects.filter(is_deleted=False,status="Fully Paid",date__lte=a_year_ago)
    total = 0
    balance = 0
    for serve in services:
        vars = serve.totalAmount + total
        vars2 = serve.balance + balance
        balance = vars2
        total = vars
    context['services'] = services
    context['total'] = total
    context['balance'] = balance
    context['user'] = user
    context['today'] = today
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] =  'filename="ChargeSlip_Report.pdf"'
    # find the template and render it.
    template = get_template('for_render_pdf/chargeSlip_pdf.html')
    html = template.render(context)
    # create a pdf
    pisa_status = pisa.CreatePDF(
    html, dest=response)
    # if error then show some funny view
    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response

#Unpaid paid
def Unpaid_chargeSlip_reports(request):
    context={}
    #lte,lt,gte,gt
    use = request.user.id
    user = StaffProfile.objects.get(useracc=use)
    today = date.today()
    services = chargeSlip.objects.filter(is_deleted=False,status="Unpaid")
    total = 0
    balance = 0
    for serve in services:
        vars = serve.totalAmount + total
        vars2 = serve.balance + balance
        balance = vars2
        total = vars
    context['services'] = services
    context['total'] = total
    context['balance'] = balance
    context['user'] = user
    context['today'] = today
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] =  'filename="ChargeSlip_Report.pdf"'
    # find the template and render it.
    template = get_template('for_render_pdf/chargeSlip_pdf.html')
    html = template.render(context)
    # create a pdf
    pisa_status = pisa.CreatePDF(
    html, dest=response)
    # if error then show some funny view
    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response

def Unpaid_today_chargeSlip_reports(request):
    context={}
    #lte,lt,gte,gt
    use = request.user.id
    user = StaffProfile.objects.get(useracc=use)
    today = date.today()
    services = chargeSlip.objects.filter(is_deleted=False,status="Unpaid",date=today)
    total = 0
    balance = 0
    for serve in services:
        vars = serve.totalAmount + total
        vars2 = serve.balance + balance
        balance = vars2
        total = vars
    context['services'] = services
    context['total'] = total
    context['balance'] = balance
    context['user'] = user
    context['today'] = today
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] =  'filename="ChargeSlip_Report.pdf"'
    # find the template and render it.
    template = get_template('for_render_pdf/chargeSlip_pdf.html')
    html = template.render(context)
    # create a pdf
    pisa_status = pisa.CreatePDF(
    html, dest=response)
    # if error then show some funny view
    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response

def Unpaid_seven_chargeSlip_reports(request):
    context={}
    #lte,lt,gte,gt
    use = request.user.id
    user = StaffProfile.objects.get(useracc=use)
    today = date.today()
    last_seven = date.today() - timedelta(7)
    services = chargeSlip.objects.filter(is_deleted=False,status="Unpaid",date__gte=last_seven)
    total = 0
    balance = 0
    for serve in services:
        vars = serve.totalAmount + total
        vars2 = serve.balance + balance
        balance = vars2
        total = vars
    context['services'] = services
    context['total'] = total
    context['balance'] = balance
    context['user'] = user
    context['today'] = today
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] =  'filename="ChargeSlip_Report.pdf"'
    # find the template and render it.
    template = get_template('for_render_pdf/chargeSlip_pdf.html')
    html = template.render(context)
    # create a pdf
    pisa_status = pisa.CreatePDF(
    html, dest=response)
    # if error then show some funny view
    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response

def Unpaid_last_thirty_chargeSlip_reports(request):
    context={}
    #lte,lt,gte,gt
    use = request.user.id
    user = StaffProfile.objects.get(useracc=use)
    today = date.today()
    last_thirty = date.today() - timedelta(30)
    services = chargeSlip.objects.filter(is_deleted=False,status="Unpaid",date__gte=last_thirty)
    total = 0
    balance = 0
    for serve in services:
        vars = serve.totalAmount + total
        vars2 = serve.balance + balance
        balance = vars2
        total = vars
    context['services'] = services
    context['total'] = total
    context['balance'] = balance
    context['user'] = user
    context['today'] = today
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] =  'filename="ChargeSlip_Report.pdf"'
    # find the template and render it.
    template = get_template('for_render_pdf/chargeSlip_pdf.html')
    html = template.render(context)
    # create a pdf
    pisa_status = pisa.CreatePDF(
    html, dest=response)
    # if error then show some funny view
    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response

def Unpaid_a_year_ago_chargeSlip_reports(request):
    context={}
    #lte,lt,gte,gt
    use = request.user.id
    user = StaffProfile.objects.get(useracc=use)
    today = date.today()
    a_year_ago = date.today() - timedelta(365)
    services = chargeSlip.objects.filter(is_deleted=False,status="Unpaid",date__gte=a_year_ago)
    total = 0
    balance = 0
    for serve in services:
        vars = serve.totalAmount + total
        vars2 = serve.balance + balance
        balance = vars2
        total = vars
    context['services'] = services
    context['total'] = total
    context['balance'] = balance
    context['user'] = user
    context['today'] = today
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] =  'filename="ChargeSlip_Report.pdf"'
    # find the template and render it.
    template = get_template('for_render_pdf/chargeSlip_pdf.html')
    html = template.render(context)
    # create a pdf
    pisa_status = pisa.CreatePDF(
    html, dest=response)
    # if error then show some funny view
    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response

def Unpaid_more_chargeSlip_reports(request):
    context={}
    #lte,lt,gte,gt
    use = request.user.id
    user = StaffProfile.objects.get(useracc=use)
    today = date.today()
    a_year_ago = date.today() - timedelta(365)
    services = chargeSlip.objects.filter(is_deleted=False,status="Unpaid",date__lte=a_year_ago)
    total = 0
    balance = 0
    for serve in services:
        vars = serve.totalAmount + total
        vars2 = serve.balance + balance
        balance = vars2
        total = vars
    context['services'] = services
    context['total'] = total
    context['balance'] = balance
    context['user'] = user
    context['today'] = today
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] =  'filename="ChargeSlip_Report.pdf"'
    # find the template and render it.
    template = get_template('for_render_pdf/chargeSlip_pdf.html')
    html = template.render(context)
    # create a pdf
    pisa_status = pisa.CreatePDF(
    html, dest=response)
    # if error then show some funny view
    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response

#partial paid
def partial_chargeSlip_reports(request):
    context={}
    #lte,lt,gte,gt
    use = request.user.id
    user = StaffProfile.objects.get(useracc=use)
    today = date.today()
    services = chargeSlip.objects.filter(is_deleted=False,status="Partially Paid")
    total = 0
    balance = 0
    for serve in services:
        vars = serve.totalAmount + total
        vars2 = serve.balance + balance
        balance = vars2
        total = vars
    context['services'] = services
    context['total'] = total
    context['balance'] = balance
    context['user'] = user
    context['today'] = today
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] =  'filename="ChargeSlip_Report.pdf"'
    # find the template and render it.
    template = get_template('for_render_pdf/chargeSlip_pdf.html')
    html = template.render(context)
    # create a pdf
    pisa_status = pisa.CreatePDF(
    html, dest=response)
    # if error then show some funny view
    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response

def partial_today_chargeSlip_reports(request):
    context={}
    #lte,lt,gte,gt
    user = request.user.id
    today = date.today()
    services = chargeSlip.objects.filter(is_deleted=False,status="Partially Paid",date=today)
    total = 0
    balance = 0
    for serve in services:
        vars = serve.totalAmount + total
        vars2 = serve.balance + balance
        balance = vars2
        total = vars
    context['services'] = services
    context['total'] = total
    context['balance'] = balance
    context['user'] = user
    context['today'] = today
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] =  'filename="ChargeSlip_Report.pdf"'
    # find the template and render it.
    template = get_template('for_render_pdf/chargeSlip_pdf.html')
    html = template.render(context)
    # create a pdf
    pisa_status = pisa.CreatePDF(
    html, dest=response)
    # if error then show some funny view
    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response

def partial_seven_chargeSlip_reports(request):
    context={}
    #lte,lt,gte,gt
    use = request.user.id
    user = StaffProfile.objects.get(useracc=use)
    today = date.today()
    last_seven = date.today() - timedelta(7)
    services = chargeSlip.objects.filter(is_deleted=False,status="Partially Paid",date__gte=last_seven)
    total = 0
    balance = 0
    for serve in services:
        vars = serve.totalAmount + total
        vars2 = serve.balance + balance
        balance = vars2
        total = vars
    context['services'] = services
    context['total'] = total
    context['balance'] = balance
    context['user'] = user
    context['today'] = today
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] =  'filename="ChargeSlip_Report.pdf"'
    # find the template and render it.
    template = get_template('for_render_pdf/chargeSlip_pdf.html')
    html = template.render(context)
    # create a pdf
    pisa_status = pisa.CreatePDF(
    html, dest=response)
    # if error then show some funny view
    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response

def partial_last_thirty_chargeSlip_reports(request):
    context={}
    #lte,lt,gte,gt
    use = request.user.id
    user = StaffProfile.objects.get(useracc=use)
    today = date.today()
    last_thirty = date.today() - timedelta(30)
    services = chargeSlip.objects.filter(is_deleted=False,status="Partially Paid",date__gte=last_thirty)
    total = 0
    balance = 0
    for serve in services:
        vars = serve.totalAmount + total
        vars2 = serve.balance + balance
        balance = vars2
        total = vars
    context['services'] = services
    context['total'] = total
    context['balance'] = balance
    context['user'] = user
    context['today'] = today
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] =  'filename="ChargeSlip_Report.pdf"'
    # find the template and render it.
    template = get_template('for_render_pdf/chargeSlip_pdf.html')
    html = template.render(context)
    # create a pdf
    pisa_status = pisa.CreatePDF(
    html, dest=response)
    # if error then show some funny view
    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response

def partial_a_year_ago_chargeSlip_reports(request):
    context={}
    #lte,lt,gte,gt
    use = request.user.id
    user = StaffProfile.objects.get(useracc=use)
    today = date.today()
    a_year_ago = date.today() - timedelta(365)
    services = chargeSlip.objects.filter(is_deleted=False,status="Partially Paid",date__gte=a_year_ago)
    total = 0
    balance = 0
    for serve in services:
        vars = serve.totalAmount + total
        vars2 = serve.balance + balance
        balance = vars2
        total = vars
    context['services'] = services
    context['total'] = total
    context['balance'] = balance
    context['user'] = user
    context['today'] = today
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] =  'filename="ChargeSlip_Report.pdf"'
    # find the template and render it.
    template = get_template('for_render_pdf/chargeSlip_pdf.html')
    html = template.render(context)
    # create a pdf
    pisa_status = pisa.CreatePDF(
    html, dest=response)
    # if error then show some funny view
    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response

def partial_more_chargeSlip_reports(request):
    context={}
    #lte,lt,gte,gt
    use = request.user.id
    user = StaffProfile.objects.get(useracc=use)
    today = date.today()
    a_year_ago = date.today() - timedelta(365)
    services = chargeSlip.objects.filter(is_deleted=False,status="Partially Paid",date__lte=a_year_ago)
    total = 0
    balance = 0
    for serve in services:
        vars = serve.totalAmount + total
        vars2 = serve.balance + balance
        balance = vars2
        total = vars
    context['services'] = services
    context['total'] = total
    context['balance'] = balance
    context['user'] = user
    context['today'] = today
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] =  'filename="ChargeSlip_Report.pdf"'
    # find the template and render it.
    template = get_template('for_render_pdf/chargeSlip_pdf.html')
    html = template.render(context)
    # create a pdf
    pisa_status = pisa.CreatePDF(
    html, dest=response)
    # if error then show some funny view
    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response


def inventory_summary(request):
    context={}
    #lte,lt,gte,gt
    use = request.user.id
    user = StaffProfile.objects.get(useracc=use)
    today = date.today()
    services = ProductInfo.objects.filter(is_deleted=False)
    context = {"services":services}
    context['user'] = user
    context['today'] = today
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] =  'filename="Product_Invoice_Report.pdf"'
    # find the template and render it.
    template = get_template('for_render_pdf/inventory_summary.html')
    html = template.render(context)
    # create a pdf
    pisa_status = pisa.CreatePDF(
    html, dest=response)
    # if error then show some funny view
    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response

def all_products_reports(request):
    context={}
    #lte,lt,gte,gt
    use = request.user.id
    user = StaffProfile.objects.get(useracc=use)
    today = date.today()
    services = Product.objects.filter(is_deleted=False)
    context = {"services":services}
    context['user'] = user
    context['today'] = today
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] =  'filename="Product_Invoice_Report.pdf"'
    # find the template and render it.
    template = get_template('for_render_pdf/all_products.html')
    html = template.render(context)
    # create a pdf
    pisa_status = pisa.CreatePDF(
    html, dest=response)
    # if error then show some funny view
    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response

def single_product_reports(request,pk):
    context={}
    #lte,lt,gte,gt
    use = request.user.id
    user = StaffProfile.objects.get(useracc=use)
    today = date.today()
    prod = ProductInfo.objects.filter(id=pk)
    services = Product.objects.filter(product__in=prod)
    context = {"services":services}
    context['user'] = user
    context['today'] = today
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] =  'filename="Product_Invoice_Report.pdf"'
    # find the template and render it.
    template = get_template('for_render_pdf/all_products.html')
    html = template.render(context)
    # create a pdf
    pisa_status = pisa.CreatePDF(
    html, dest=response)
    # if error then show some funny view
    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response

def transaction_report(request):
    context={}
    #lte,lt,gte,gt
    use = request.user.id
    user = StaffProfile.objects.get(useracc=use)
    today = date.today()
    services = transaction.objects.filter(is_deleted=False)
    total = 0
    tender = 0
    change = 0
    for serve in services:
        vars = serve.grandTotal + total
        vars2 = serve.tenderedAmount + tender
        var3 = serve.changeAmount + change
        tender = vars2
        total = vars
        change=var3
    context['services'] = services
    context['total'] = total
    context['tender'] = tender
    context['change'] = change
    context['user'] = user
    context['today'] = today
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] =  'filename="Transaction_Report.pdf"'
    # find the template and render it.
    template = get_template('for_render_pdf/transaction_reports.html')
    html = template.render(context)
    # create a pdf
    pisa_status = pisa.CreatePDF(
    html, dest=response)
    # if error then show some funny view
    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response

def today_transaction_reports(request):
    context={}
    #lte,lt,gte,gt
    use = request.user.id
    user = StaffProfile.objects.get(useracc=use)
    today = date.today()
    services = transaction.objects.filter(date=today)
    total = 0
    tender = 0
    change = 0
    for serve in services:
        vars = serve.grandTotal + total
        vars2 = serve.tenderedAmount + tender
        var3 = serve.changeAmount + change
        tender = vars2
        total = vars
        change=var3
    context['services'] = services
    context['total'] = total
    context['tender'] = tender
    context['change'] = change
    context['user'] = user
    context['today'] = today
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] =  'filename="Transaction_Report.pdf"'
    # find the template and render it.
    template = get_template('for_render_pdf/transaction_reports.html')
    html = template.render(context)
    # create a pdf
    pisa_status = pisa.CreatePDF(
    html, dest=response)
    # if error then show some funny view
    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response

def seven_transaction_reports(request):
    context={}
    #lte,lt,gte,gt
    use = request.user.id
    user = StaffProfile.objects.get(useracc=use)
    today = date.today()
    last_seven = date.today() - timedelta(7)
    services = transaction.objects.filter(date__gte=last_seven)
    total = 0
    tender = 0
    change = 0
    for serve in services:
        vars = serve.grandTotal + total
        vars2 = serve.tenderedAmount + tender
        var3 = serve.changeAmount + change
        tender = vars2
        total = vars
        change=var3
    context['services'] = services
    context['total'] = total
    context['tender'] = tender
    context['change'] = change
    context['user'] = user
    context['today'] = today
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] =  'filename="Transaction_Report.pdf"'
    # find the template and render it.
    template = get_template('for_render_pdf/transaction_reports.html')
    html = template.render(context)
    # create a pdf
    pisa_status = pisa.CreatePDF(
    html, dest=response)
    # if error then show some funny view
    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response

def last_thirty_transaction_reports(request):
    context={}
    #lte,lt,gte,gt
    use = request.user.id
    user = StaffProfile.objects.get(useracc=use)
    today = date.today()
    last_thirty = date.today() - timedelta(30)
    services = transaction.objects.filter(date__gte=last_thirty)
    total = 0
    tender = 0
    change = 0
    for serve in services:
        vars = serve.grandTotal + total
        vars2 = serve.tenderedAmount + tender
        var3 = serve.changeAmount + change
        tender = vars2
        total = vars
        change=var3
    context['services'] = services
    context['total'] = total
    context['tender'] = tender
    context['change'] = change
    context['user'] = user
    context['today'] = today
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] =  'filename="Transaction_Report.pdf"'
    # find the template and render it.
    template = get_template('for_render_pdf/transaction_reports.html')
    html = template.render(context)
    # create a pdf
    pisa_status = pisa.CreatePDF(
    html, dest=response)
    # if error then show some funny view
    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response

def a_year_ago_transaction_reports(request):
    context={}
    #lte,lt,gte,gt
    use = request.user.id
    user = StaffProfile.objects.get(useracc=use)
    today = date.today()
    a_year_ago = date.today() - timedelta(365)
    services = chargeSlip.objects.filter(date__gte=a_year_ago)
    total = 0
    tender = 0
    change = 0
    for serve in services:
        vars = serve.grandTotal + total
        vars2 = serve.tenderedAmount + tender
        var3 = serve.changeAmount + change
        tender = vars2
        total = vars
        change=var3
    context['services'] = services
    context['total'] = total
    context['tender'] = tender
    context['change'] = change
    context['user'] = user
    context['today'] = today
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] =  'filename="Transaction_Report.pdf"'
    # find the template and render it.
    template = get_template('for_render_pdf/transaction_reports.html')
    html = template.render(context)
    # create a pdf
    pisa_status = pisa.CreatePDF(
    html, dest=response)
    # if error then show some funny view
    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response

def more_transaction_reports(request):
    context={}
    #lte,lt,gte,gt
    use = request.user.id
    user = StaffProfile.objects.get(useracc=use)
    today = date.today()
    a_year_ago = date.today() - timedelta(365)
    services = transaction.objects.filter(date__lte=a_year_ago)
    total = 0
    tender = 0
    change = 0
    for serve in services:
        vars = serve.grandTotal + total
        vars2 = serve.tenderedAmount + tender
        var3 = serve.changeAmount + change
        tender = vars2
        total = vars
        change=var3
    context['services'] = services
    context['total'] = total
    context['tender'] = tender
    context['change'] = change
    context['user'] = user
    context['today'] = today
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] =  'filename="Transaction_Report.pdf"'
    # find the template and render it.
    template = get_template('for_render_pdf/transaction_reports.html')
    html = template.render(context)
    # create a pdf
    pisa_status = pisa.CreatePDF(
    html, dest=response)
    # if error then show some funny view
    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response



#headvet

def head_transaction_reports(request):
    context={}
    use = request.user.id
    user = StaffProfile.objects.get(useracc=use)
    today = date.today()
    all_chargeslip = transaction.objects.filter(is_deleted=False)
    if request.method == 'POST':
        if request.POST['filter'] == "Range":
            a = request.POST.get('a')
            b = request.POST.get('b')
            services = transaction.objects.filter(is_deleted=False,date__gte=a,date__lte=b)
            total = 0
            tender = 0
            change = 0
            for serve in services:
                vars = serve.grandTotal + total
                vars2 = serve.tenderedAmount + tender
                var3 = serve.changeAmount + change
                tender = vars2
                total = vars
                change=var3
            context['services'] = services
            context['total'] = total
            context['tender'] = tender
            context['change'] = change
            context['user'] = user
            context['today'] = today
            response = HttpResponse(content_type='application/pdf')
            response['Content-Disposition'] =  'filename="Service_Invoice_Report.pdf"'
            # find the template and render it.
            template = get_template('for_render_pdf/transaction_reports.html')
            html = template.render(context)
            # create a pdf
            pisa_status = pisa.CreatePDF(
            html, dest=response)
            # if error then show some funny view
            if pisa_status.err:
                return HttpResponse('We had some errors <pre>' + html + '</pre>')
            return response

    context={'sideb':'transaction_reports','all_chargeslip':all_chargeslip,'use':use}
    return render(request,'headveterinarian/reports/transaction_reports.html',context) 

def head_transaction_reports_select(request,pk):
    user = request.user.id
    trans = transaction.objects.get(id=pk)
    context={'sideb' : 'transaction_reports_select','trans':trans,'user':user}
    return render(request,'headveterinarian/reports/transaction_reports_select.html',context)   

#service invoice report

def head_service_reports(request):
    context={'sideb':'service_reports'}
    #lte,lt,gte,gt
    use = request.user.id
    user = StaffProfile.objects.get(useracc=use)
    today = date.today()
    services = serviceInvoice.objects.all()
    if request.method == 'POST':
        if request.POST['filter'] == "Range":
            a = request.POST.get('a')
            b = request.POST.get('b')
            services = serviceInvoice.objects.filter(is_deleted=False,date__gte=a,date__lte=b)
            total = 0
            for serve in services:
                vars = serve.total + total
                total = vars
            context['services'] = services
            context['total'] = total
            context['today'] = today
            context['user'] = user
            response = HttpResponse(content_type='application/pdf')
            response['Content-Disposition'] =  'filename="Service_Invoice_Report.pdf"'
            # find the template and render it.
            template = get_template('for_render_pdf/try.html')
            html = template.render(context)
            # create a pdf
            pisa_status = pisa.CreatePDF(
            html, dest=response)
            # if error then show some funny view
            if pisa_status.err:
                return HttpResponse('We had some errors <pre>' + html + '</pre>')
            return response
        if request.POST['filter'] == "Report":
            total = 0
            for serve in services:
                vars = serve.total + total
                total = vars
            context['services'] = services
            context['total'] = total
            context['user'] = user
            context['today'] = today
            response = HttpResponse(content_type='application/pdf')
            response['Content-Disposition'] =  'filename="Service_Invoice_Report.pdf"'
            # find the template and render it.
            template = get_template('for_render_pdf/try.html')
            html = template.render(context)
            # create a pdf
            pisa_status = pisa.CreatePDF(
            html, dest=response)
            # if error then show some funny view
            if pisa_status.err:
                return HttpResponse('We had some errors <pre>' + html + '</pre>')
            return response
    context['services'] = services
    context['use'] = use
    return render(request, 'headveterinarian/reports/service_reports.html', context)

def head_today_service_reports(request):
    context={}
    #lte,lt,gte,gt
    use = request.user.id
    user = StaffProfile.objects.get(useracc=use)
    today = date.today()
    services = serviceInvoice.objects.filter(date=today)
    if request.method == 'POST':
        if request.POST['filter'] == "Range":
            a = request.POST.get('a')
            b = request.POST.get('b')
            services = serviceInvoice.objects.filter(is_deleted=False,date__gte=a,date__lte=b)
            total = 0
            for serve in services:
                vars = serve.total + total
                total = vars
            context['services'] = services
            context['total'] = total
            context['today'] = today
            context['user'] = user
            response = HttpResponse(content_type='application/pdf')
            response['Content-Disposition'] =  'filename="Service_Invoice_Report.pdf"'
            # find the template and render it.
            template = get_template('for_render_pdf/try.html')
            html = template.render(context)
            # create a pdf
            pisa_status = pisa.CreatePDF(
            html, dest=response)
            # if error then show some funny view
            if pisa_status.err:
                return HttpResponse('We had some errors <pre>' + html + '</pre>')
            return response
        if request.POST['filter'] == "Report":
            total = 0
            for serve in services:
                vars = serve.total + total
                total = vars
            context['services'] = services
            context['total'] = total
            context['user'] = user
            context['today'] = today
            response = HttpResponse(content_type='application/pdf')
            response['Content-Disposition'] =  'filename="Service_Invoice_Report.pdf"'
            # find the template and render it.
            template = get_template('for_render_pdf/try.html')
            html = template.render(context)
            # create a pdf
            pisa_status = pisa.CreatePDF(
            html, dest=response)
            # if error then show some funny view
            if pisa_status.err:
                return HttpResponse('We had some errors <pre>' + html + '</pre>')
            return response
    context['services'] = services
    context['use'] = use
    return render(request, 'headveterinarian/reports/service_reports.html', context)

def head_seven_service_reports(request):
    context={}
    #lte,lt,gte,gt
    use = request.user.id
    user = StaffProfile.objects.get(useracc=use)
    today = date.today()
    last_seven = date.today() - timedelta(7)
    services = serviceInvoice.objects.filter(date__gte=last_seven)
    if request.method == 'POST':
        if request.POST['filter'] == "Range":
            a = request.POST.get('a')
            b = request.POST.get('b')
            services = serviceInvoice.objects.filter(is_deleted=False,date__gte=a,date__lte=b)
            total = 0
            for serve in services:
                vars = serve.total + total
                total = vars
            context['services'] = services
            context['total'] = total
            context['today'] = today
            context['user'] = user
            response = HttpResponse(content_type='application/pdf')
            response['Content-Disposition'] =  'filename="Service_Invoice_Report.pdf"'
            # find the template and render it.
            template = get_template('for_render_pdf/try.html')
            html = template.render(context)
            # create a pdf
            pisa_status = pisa.CreatePDF(
            html, dest=response)
            # if error then show some funny view
            if pisa_status.err:
                return HttpResponse('We had some errors <pre>' + html + '</pre>')
            return response
        if request.POST['filter'] == "Report":
            total = 0
            for serve in services:
                vars = serve.total + total
                total = vars
            context['services'] = services
            context['total'] = total
            context['user'] = user
            context['today'] = today
            response = HttpResponse(content_type='application/pdf')
            response['Content-Disposition'] =  'filename="Service_Invoice_Report.pdf"'
            # find the template and render it.
            template = get_template('for_render_pdf/try.html')
            html = template.render(context)
            # create a pdf
            pisa_status = pisa.CreatePDF(
            html, dest=response)
            # if error then show some funny view
            if pisa_status.err:
                return HttpResponse('We had some errors <pre>' + html + '</pre>')
            return response
    context['services'] = services
    context['use'] = use
    return render(request, 'headveterinarian/reports/service_reports.html', context)

def head_last_thirty_service_reports(request):
    context={}
    #lte,lt,gte,gt
    use = request.user.id
    user = StaffProfile.objects.get(useracc=use)
    today = date.today()
    last_thirty = date.today() - timedelta(30)
    services = serviceInvoice.objects.filter(date__gte=last_thirty)
    if request.method == 'POST':
        if request.POST['filter'] == "Range":
            a = request.POST.get('a')
            b = request.POST.get('b')
            services = serviceInvoice.objects.filter(is_deleted=False,date__gte=a,date__lte=b)
            total = 0
            for serve in services:
                vars = serve.total + total
                total = vars
            context['services'] = services
            context['total'] = total
            context['today'] = today
            context['user'] = user
            response = HttpResponse(content_type='application/pdf')
            response['Content-Disposition'] =  'filename="Service_Invoice_Report.pdf"'
            # find the template and render it.
            template = get_template('for_render_pdf/try.html')
            html = template.render(context)
            # create a pdf
            pisa_status = pisa.CreatePDF(
            html, dest=response)
            # if error then show some funny view
            if pisa_status.err:
                return HttpResponse('We had some errors <pre>' + html + '</pre>')
            return response
        if request.POST['filter'] == "Report":
            total = 0
            for serve in services:
                vars = serve.total + total
                total = vars
            context['services'] = services
            context['total'] = total
            context['user'] = user
            context['today'] = today
            response = HttpResponse(content_type='application/pdf')
            response['Content-Disposition'] =  'filename="Service_Invoice_Report.pdf"'
            # find the template and render it.
            template = get_template('for_render_pdf/try.html')
            html = template.render(context)
            # create a pdf
            pisa_status = pisa.CreatePDF(
            html, dest=response)
            # if error then show some funny view
            if pisa_status.err:
                return HttpResponse('We had some errors <pre>' + html + '</pre>')
            return response
    context['services'] = services
    context['use'] = use
    return render(request, 'headveterinarian/reports/service_reports.html', context)

def head_a_year_ago_service_reports(request):
    context={}
    #lte,lt,gte,gt
    use = request.user.id
    user = StaffProfile.objects.get(useracc=use)
    today = date.today()
    a_year_ago = date.today() - timedelta(365)
    services = serviceInvoice.objects.filter(date__gte=a_year_ago)
    if request.method == 'POST':
        if request.POST['filter'] == "Range":
            a = request.POST.get('a')
            b = request.POST.get('b')
            services = serviceInvoice.objects.filter(is_deleted=False,date__gte=a,date__lte=b)
            total = 0
            for serve in services:
                vars = serve.total + total
                total = vars
            context['services'] = services
            context['total'] = total
            context['today'] = today
            context['user'] = user
            response = HttpResponse(content_type='application/pdf')
            response['Content-Disposition'] =  'filename="Service_Invoice_Report.pdf"'
            # find the template and render it.
            template = get_template('for_render_pdf/try.html')
            html = template.render(context)
            # create a pdf
            pisa_status = pisa.CreatePDF(
            html, dest=response)
            # if error then show some funny view
            if pisa_status.err:
                return HttpResponse('We had some errors <pre>' + html + '</pre>')
            return response
        if request.POST['filter'] == "Report":
            total = 0
            for serve in services:
                vars = serve.total + total
                total = vars
            context['services'] = services
            context['total'] = total
            context['user'] = user
            context['today'] = today
            response = HttpResponse(content_type='application/pdf')
            response['Content-Disposition'] =  'filename="Service_Invoice_Report.pdf"'
            # find the template and render it.
            template = get_template('for_render_pdf/try.html')
            html = template.render(context)
            # create a pdf
            pisa_status = pisa.CreatePDF(
            html, dest=response)
            # if error then show some funny view
            if pisa_status.err:
                return HttpResponse('We had some errors <pre>' + html + '</pre>')
            return response
    context['services'] = services
    context['use'] = use
    return render(request, 'headveterinarian/reports/service_reports.html', context)

def head_more_service_reports(request):
    context={}
    #lte,lt,gte,gt
    use = request.user.id
    user = StaffProfile.objects.get(useracc=use)
    today = date.today()
    more = date.today() - timedelta(365)
    services = serviceInvoice.objects.filter(date__lte=more)
    if request.method == 'POST':
        if request.POST['filter'] == "Range":
            a = request.POST.get('a')
            b = request.POST.get('b')
            services = serviceInvoice.objects.filter(is_deleted=False,date__gte=a,date__lte=b)
            total = 0
            for serve in services:
                vars = serve.total + total
                total = vars
            context['services'] = services
            context['total'] = total
            context['today'] = today
            context['user'] = user
            response = HttpResponse(content_type='application/pdf')
            response['Content-Disposition'] =  'filename="Service_Invoice_Report.pdf"'
            # find the template and render it.
            template = get_template('for_render_pdf/try.html')
            html = template.render(context)
            # create a pdf
            pisa_status = pisa.CreatePDF(
            html, dest=response)
            # if error then show some funny view
            if pisa_status.err:
                return HttpResponse('We had some errors <pre>' + html + '</pre>')
            return response
        if request.POST['filter'] == "Report":
            total = 0
            for serve in services:
                vars = serve.total + total
                total = vars
            context['services'] = services
            context['total'] = total
            context['user'] = user
            context['today'] = today
            response = HttpResponse(content_type='application/pdf')
            response['Content-Disposition'] =  'filename="Service_Invoice_Report.pdf"'
            # find the template and render it.
            template = get_template('for_render_pdf/try.html')
            html = template.render(context)
            # create a pdf
            pisa_status = pisa.CreatePDF(
            html, dest=response)
            # if error then show some funny view
            if pisa_status.err:
                return HttpResponse('We had some errors <pre>' + html + '</pre>')
            return response
    context['services'] = services
    context['use'] = use
    return render(request, 'headveterinarian/reports/service_reports.html', context)

#product Invoice report
def head_product_reports(request):
    context={'sideb':'product_reports'}
    #lte,lt,gte,gt
    use = request.user.id
    user = StaffProfile.objects.get(useracc=use)
    today = date.today()
    services = productInvoice.objects.all()
    if request.method == 'POST':
        if request.POST['filter'] == "Range":
            a = request.POST.get('a')
            b = request.POST.get('b')
            services = productInvoice.objects.filter(is_deleted=False,date__gte=a,date__lte=b)
            total = 0
            for serve in services:
                vars = serve.total + total
                total = vars
            context['services'] = services
            context['total'] = total
            context['today'] = today
            context['user'] = user
            response = HttpResponse(content_type='application/pdf')
            response['Content-Disposition'] =  'filename="Service_Invoice_Report.pdf"'
            # find the template and render it.
            template = get_template('for_render_pdf/productsInvoiceTemplate.html')
            html = template.render(context)
            # create a pdf
            pisa_status = pisa.CreatePDF(
            html, dest=response)
            # if error then show some funny view
            if pisa_status.err:
                return HttpResponse('We had some errors <pre>' + html + '</pre>')
            return response
        if request.POST['filter'] == "Report":
            total = 0
            for serve in services:
                vars = serve.total + total
                total = vars
            context['services'] = services
            context['total'] = total
            context['user'] = user
            context['today'] = today
            response = HttpResponse(content_type='application/pdf')
            response['Content-Disposition'] =  'filename="Service_Invoice_Report.pdf"'
            # find the template and render it.
            template = get_template('for_render_pdf/try.html')
            html = template.render(context)
            # create a pdf
            pisa_status = pisa.CreatePDF(
            html, dest=response)
            # if error then show some funny view
            if pisa_status.err:
                return HttpResponse('We had some errors <pre>' + html + '</pre>')
            return response
    context['services'] = services
    context['use'] = use
    return render(request, 'headveterinarian/reports/product_reports.html', context)

def head_today_product_reports(request):
    context={}
    #lte,lt,gte,gt
    use = request.user.id
    user = StaffProfile.objects.get(useracc=use)
    today = date.today()
    services = productInvoice.objects.filter(date=today)
    if request.method == 'POST':
        if request.POST['filter'] == "Range":
            a = request.POST.get('a')
            b = request.POST.get('b')
            services = productInvoice.objects.filter(is_deleted=False,date__gte=a,date__lte=b)
            total = 0
            for serve in services:
                vars = serve.total + total
                total = vars
            context['services'] = services
            context['total'] = total
            context['today'] = today
            context['user'] = user
            response = HttpResponse(content_type='application/pdf')
            response['Content-Disposition'] =  'filename="Service_Invoice_Report.pdf"'
            # find the template and render it.
            template = get_template('for_render_pdf/productsInvoiceTemplate.html')
            html = template.render(context)
            # create a pdf
            pisa_status = pisa.CreatePDF(
            html, dest=response)
            # if error then show some funny view
            if pisa_status.err:
                return HttpResponse('We had some errors <pre>' + html + '</pre>')
            return response
        if request.POST['filter'] == "Report":
            total = 0
            for serve in services:
                vars = serve.total + total
                total = vars
            context['services'] = services
            context['total'] = total
            context['user'] = user
            context['today'] = today
            response = HttpResponse(content_type='application/pdf')
            response['Content-Disposition'] =  'filename="Service_Invoice_Report.pdf"'
            # find the template and render it.
            template = get_template('for_render_pdf/try.html')
            html = template.render(context)
            # create a pdf
            pisa_status = pisa.CreatePDF(
            html, dest=response)
            # if error then show some funny view
            if pisa_status.err:
                return HttpResponse('We had some errors <pre>' + html + '</pre>')
            return response
    context['services'] = services
    context['use'] = use
    return render(request, 'headveterinarian/reports/product_reports.html', context)

def head_seven_product_reports(request):
    context={}
    #lte,lt,gte,gt
    use = request.user.id
    user = StaffProfile.objects.get(useracc=use)
    today = date.today()
    last_seven = date.today() - timedelta(7)
    services = productInvoice.objects.filter(date__gte=last_seven)
    if request.method == 'POST':
        if request.POST['filter'] == "Range":
            a = request.POST.get('a')
            b = request.POST.get('b')
            services = productInvoice.objects.filter(is_deleted=False,date__gte=a,date__lte=b)
            total = 0
            for serve in services:
                vars = serve.total + total
                total = vars
            context['services'] = services
            context['total'] = total
            context['today'] = today
            context['user'] = user
            response = HttpResponse(content_type='application/pdf')
            response['Content-Disposition'] =  'filename="Service_Invoice_Report.pdf"'
            # find the template and render it.
            template = get_template('for_render_pdf/productsInvoiceTemplate.html')
            html = template.render(context)
            # create a pdf
            pisa_status = pisa.CreatePDF(
            html, dest=response)
            # if error then show some funny view
            if pisa_status.err:
                return HttpResponse('We had some errors <pre>' + html + '</pre>')
            return response
        if request.POST['filter'] == "Report":
            total = 0
            for serve in services:
                vars = serve.total + total
                total = vars
            context['services'] = services
            context['total'] = total
            context['user'] = user
            context['today'] = today
            response = HttpResponse(content_type='application/pdf')
            response['Content-Disposition'] =  'filename="Service_Invoice_Report.pdf"'
            # find the template and render it.
            template = get_template('for_render_pdf/try.html')
            html = template.render(context)
            # create a pdf
            pisa_status = pisa.CreatePDF(
            html, dest=response)
            # if error then show some funny view
            if pisa_status.err:
                return HttpResponse('We had some errors <pre>' + html + '</pre>')
            return response
    context['services'] = services
    context['use'] = use
    return render(request, 'headveterinarian/reports/product_reports.html', context)

def head_last_thirty_product_reports(request):
    context={}
    #lte,lt,gte,gt
    use = request.user.id
    user = StaffProfile.objects.get(useracc=use)
    today = date.today()
    last_thirty = date.today() - timedelta(30)
    services = productInvoice.objects.filter(date__gte=last_thirty)
    if request.method == 'POST':
        if request.POST['filter'] == "Range":
            a = request.POST.get('a')
            b = request.POST.get('b')
            services = productInvoice.objects.filter(is_deleted=False,date__gte=a,date__lte=b)
            total = 0
            for serve in services:
                vars = serve.total + total
                total = vars
            context['services'] = services
            context['total'] = total
            context['today'] = today
            context['user'] = user
            response = HttpResponse(content_type='application/pdf')
            response['Content-Disposition'] =  'filename="Service_Invoice_Report.pdf"'
            # find the template and render it.
            template = get_template('for_render_pdf/productsInvoiceTemplate.html')
            html = template.render(context)
            # create a pdf
            pisa_status = pisa.CreatePDF(
            html, dest=response)
            # if error then show some funny view
            if pisa_status.err:
                return HttpResponse('We had some errors <pre>' + html + '</pre>')
            return response
        if request.POST['filter'] == "Report":
            total = 0
            for serve in services:
                vars = serve.total + total
                total = vars
            context['services'] = services
            context['total'] = total
            context['user'] = user
            context['today'] = today
            response = HttpResponse(content_type='application/pdf')
            response['Content-Disposition'] =  'filename="Service_Invoice_Report.pdf"'
            # find the template and render it.
            template = get_template('for_render_pdf/try.html')
            html = template.render(context)
            # create a pdf
            pisa_status = pisa.CreatePDF(
            html, dest=response)
            # if error then show some funny view
            if pisa_status.err:
                return HttpResponse('We had some errors <pre>' + html + '</pre>')
            return response
    context['services'] = services
    context['use'] = use
    return render(request, 'headveterinarian/reports/product_reports.html', context)

def head_a_year_ago_product_reports(request):
    context={}
    #lte,lt,gte,gt
    use = request.user.id
    user = StaffProfile.objects.get(useracc=use)
    today = date.today()
    a_year_ago = date.today() - timedelta(365)
    services = productInvoice.objects.filter(date__gte=a_year_ago)
    if request.method == 'POST':
        if request.POST['filter'] == "Range":
            a = request.POST.get('a')
            b = request.POST.get('b')
            services = productInvoice.objects.filter(is_deleted=False,date__gte=a,date__lte=b)
            total = 0
            for serve in services:
                vars = serve.total + total
                total = vars
            context['services'] = services
            context['total'] = total
            context['today'] = today
            context['user'] = user
            response = HttpResponse(content_type='application/pdf')
            response['Content-Disposition'] =  'filename="Service_Invoice_Report.pdf"'
            # find the template and render it.
            template = get_template('for_render_pdf/productsInvoiceTemplate.html')
            html = template.render(context)
            # create a pdf
            pisa_status = pisa.CreatePDF(
            html, dest=response)
            # if error then show some funny view
            if pisa_status.err:
                return HttpResponse('We had some errors <pre>' + html + '</pre>')
            return response
        if request.POST['filter'] == "Report":
            total = 0
            for serve in services:
                vars = serve.total + total
                total = vars
            context['services'] = services
            context['total'] = total
            context['user'] = user
            context['today'] = today
            response = HttpResponse(content_type='application/pdf')
            response['Content-Disposition'] =  'filename="Service_Invoice_Report.pdf"'
            # find the template and render it.
            template = get_template('for_render_pdf/try.html')
            html = template.render(context)
            # create a pdf
            pisa_status = pisa.CreatePDF(
            html, dest=response)
            # if error then show some funny view
            if pisa_status.err:
                return HttpResponse('We had some errors <pre>' + html + '</pre>')
            return response
    context['services'] = services
    context['use'] = use
    return render(request, 'headveterinarian/reports/product_reports.html', context)

def head_more_product_reports(request):
    context={}
    #lte,lt,gte,gt
    use = request.user.id
    user = StaffProfile.objects.get(useracc=use)
    today = date.today()
    a_year_ago = date.today() - timedelta(365)
    services = productInvoice.objects.filter(date__lte=a_year_ago)
    if request.method == 'POST':
        if request.POST['filter'] == "Range":
            a = request.POST.get('a')
            b = request.POST.get('b')
            services = productInvoice.objects.filter(is_deleted=False,date__gte=a,date__lte=b)
            total = 0
            for serve in services:
                vars = serve.total + total
                total = vars
            context['services'] = services
            context['total'] = total
            context['today'] = today
            context['user'] = user
            response = HttpResponse(content_type='application/pdf')
            response['Content-Disposition'] =  'filename="Service_Invoice_Report.pdf"'
            # find the template and render it.
            template = get_template('for_render_pdf/productsInvoiceTemplate.html')
            html = template.render(context)
            # create a pdf
            pisa_status = pisa.CreatePDF(
            html, dest=response)
            # if error then show some funny view
            if pisa_status.err:
                return HttpResponse('We had some errors <pre>' + html + '</pre>')
            return response
        if request.POST['filter'] == "Report":
            total = 0
            for serve in services:
                vars = serve.total + total
                total = vars
            context['services'] = services
            context['total'] = total
            context['today'] = today
            context['user'] = user
            response = HttpResponse(content_type='application/pdf')
            response['Content-Disposition'] =  'filename="Service_Invoice_Report.pdf"'
            # find the template and render it.
            template = get_template('for_render_pdf/try.html')
            html = template.render(context)
            # create a pdf
            pisa_status = pisa.CreatePDF(
            html, dest=response)
            # if error then show some funny view
            if pisa_status.err:
                return HttpResponse('We had some errors <pre>' + html + '</pre>')
            return response
    context['services'] = services
    context['use'] = use
    return render(request, 'headveterinarian/reports/product_reports.html', context)


def client_reports(request):
    context={}
    use = request.user.id
    user = StaffProfile.objects.get(useracc=use)
    today = date.today()
    all_chargeslip = MedicalHistory.objects.filter(is_deleted=False)
    if request.method == 'POST':
        if request.POST['filter'] == "Range":
            a = request.POST.get('a')
            b = request.POST.get('b')
            services = MedicalHistory.objects.filter(is_deleted=False,date__gte=a,date__lte=b)
            context['services'] = services
            context['user'] = user
            context['today'] = today
            response = HttpResponse(content_type='application/pdf')
            response['Content-Disposition'] =  'filename="Client_Report.pdf"'
            # find the template and render it.
            template = get_template('for_render_pdf/client.html')
            html = template.render(context)
            # create a pdf
            pisa_status = pisa.CreatePDF(
            html, dest=response)
            # if error then show some funny view
            if pisa_status.err:
                return HttpResponse('We had some errors <pre>' + html + '</pre>')
            return response

    context={'sideb':'client_reports','all_chargeslip':all_chargeslip,'use':use}
    return render(request,'secretary/reports/client_reports.html',context) 
 

def client_report(request):
    context={}
    #lte,lt,gte,gt
    use = request.user.id
    user = StaffProfile.objects.get(useracc=use)
    today = date.today()
    services = MedicalHistory.objects.filter(is_deleted=False)
    context['services'] = services
    context['user'] = user
    context['today'] = today
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] =  'filename="Client_Report.pdf"'
    # find the template and render it.
    template = get_template('for_render_pdf/client.html')
    html = template.render(context)
    # create a pdf
    pisa_status = pisa.CreatePDF(
    html, dest=response)
    # if error then show some funny view
    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response

def today_client_reports(request):
    context={}
    #lte,lt,gte,gt
    use = request.user.id
    user = StaffProfile.objects.get(useracc=use)
    today = date.today()
    services = MedicalHistory.objects.filter(date=today)
    total = 0
    tender = 0
    change = 0
    for serve in services:
        vars = serve.grandTotal + total
        vars2 = serve.tenderedAmount + tender
        var3 = serve.changeAmount + change
        tender = vars2
        total = vars
        change=var3
    context['services'] = services
    context['user'] = user
    context['today'] = today
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] =  'filename="Client_Report.pdf"'
    # find the template and render it.
    template = get_template('for_render_pdf/client.html')
    html = template.render(context)
    # create a pdf
    pisa_status = pisa.CreatePDF(
    html, dest=response)
    # if error then show some funny view
    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response

def seven_client_reports(request):
    context={}
    #lte,lt,gte,gt
    use = request.user.id
    user = StaffProfile.objects.get(useracc=use)
    today = date.today()
    last_seven = date.today() - timedelta(7)
    services = MedicalHistory.objects.filter(date__gte=last_seven)
    context['services'] = services
    context['user'] = user
    context['today'] = today
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] =  'filename="Client_Report.pdf"'
    # find the template and render it.
    template = get_template('for_render_pdf/client.html')
    html = template.render(context)
    # create a pdf
    pisa_status = pisa.CreatePDF(
    html, dest=response)
    # if error then show some funny view
    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response

def last_thirty_client_reports(request):
    context={}
    #lte,lt,gte,gt
    use = request.user.id
    user = StaffProfile.objects.get(useracc=use)
    today = date.today()
    last_thirty = date.today() - timedelta(30)
    services = MedicalHistory.objects.filter(date__gte=last_thirty)
    context['services'] = services
    context['user'] = user
    context['today'] = today
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] =  'filename="Client_Report.pdf"'
    # find the template and render it.
    template = get_template('for_render_pdf/client.html')
    html = template.render(context)
    # create a pdf
    pisa_status = pisa.CreatePDF(
    html, dest=response)
    # if error then show some funny view
    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response

def a_year_ago_client_reports(request):
    context={}
    #lte,lt,gte,gt
    use = request.user.id
    user = StaffProfile.objects.get(useracc=use)
    today = date.today()
    a_year_ago = date.today() - timedelta(365)
    services = MedicalHistory.objects.filter(date__gte=a_year_ago)
    context['services'] = services
    context['user'] = user
    context['today'] = today
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] =  'filename="Client_Report.pdf"'
    # find the template and render it.
    template = get_template('for_render_pdf/client.html')
    html = template.render(context)
    # create a pdf
    pisa_status = pisa.CreatePDF(
    html, dest=response)
    # if error then show some funny view
    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response

def more_client_reports(request):
    context={}
    #lte,lt,gte,gt
    use = request.user.id
    user = StaffProfile.objects.get(useracc=use)
    today = date.today()
    a_year_ago = date.today() - timedelta(365)
    services = MedicalHistory.objects.filter(date__lte=a_year_ago)
    context['services'] = services
    context['user'] = user
    context['today'] = today
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] =  'filename="Client_Report.pdf"'
    # find the template and render it.
    template = get_template('for_render_pdf/client.html')
    html = template.render(context)
    # create a pdf
    pisa_status = pisa.CreatePDF(
    html, dest=response)
    # if error then show some funny view
    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response
