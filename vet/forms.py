from dataclasses import field
from faulthandler import disable
from tkinter import Widget
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm
from django.forms.fields import DateField
from django.contrib.admin.widgets import AdminDateWidget
from .models import *



class DateInput(forms.DateInput):
    input_type = 'date'

#USER ACCOUNTS
class HeadVetUserForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["email"].widget.attrs.update(
            {'required': True, 'name': 'email', 'id': 'email', 'type': 'text', 'class': 'form-control', 'placeholder': 'Email'})
        self.fields["password1"].widget.attrs.update(
            {'required': True, 'name': 'password1', 'id': 'password1', 'type': 'password', 'class': 'form-control', 'placeholder': 'Password'})
        self.fields["password2"].widget.attrs.update(
            {'required': True, 'name': 'password2', 'id': 'password2', 'type': 'password', 'class': 'form-control', 'placeholder': 'Confirm Password'})

    class Meta:
        model = User
        fields = ('email','password1','password2','is_headveterinarian')
        widgets = {
        'is_headveterinarian': forms.HiddenInput(),
     }

class SecretaryUserForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["email"].widget.attrs.update(
            {'required': True, 'name': 'email', 'id': 'email', 'type': 'text', 'class': 'form-control', 'placeholder': 'Email'})
        self.fields["password1"].widget.attrs.update(
            {'required': True, 'name': 'password1', 'id': 'password1', 'type': 'password', 'class': 'form-control', 'placeholder': 'Password'})
        self.fields["password2"].widget.attrs.update(
            {'required': True, 'name': 'password2', 'id': 'password2', 'type': 'password', 'class': 'form-control', 'placeholder': 'Confirm Password'})

    class Meta:
        model = User
        fields = ('email','password1','password2','is_secretary')
        widgets = {
        'is_secretary': forms.HiddenInput(),
     }

class VeterinarianUserForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["email"].widget.attrs.update(
            {'required': True, 'name': 'email', 'id': 'email', 'type': 'text', 'class': 'form-control', 'placeholder': 'Email'})
        self.fields["password1"].widget.attrs.update(
            {'required': True, 'name': 'password1', 'id': 'password1', 'type': 'password', 'class': 'form-control', 'placeholder': 'Password'})
        self.fields["password2"].widget.attrs.update(
            {'required': True, 'name': 'password2', 'id': 'password2', 'type': 'password', 'class': 'form-control', 'placeholder': 'Confirm Password'})

    class Meta:
        model = User
        fields = ('email','password1','password2','is_veterinarian')
        widgets = {
        'is_veterinarian': forms.HiddenInput(),
     }

class CreateUserForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["email"].widget.attrs.update(
            {'required': True, 'name': 'email', 'id': 'email', 'type': 'text', 'class': 'form-control', 'placeholder': 'Email'})
        self.fields["password1"].widget.attrs.update(
            {'required': True, 'name': 'password1', 'id': 'password1', 'type': 'password', 'class': 'form-control', 'placeholder': 'Password'})
        self.fields["password2"].widget.attrs.update(
            {'required': True, 'name': 'password2', 'id': 'password2', 'type': 'password', 'class': 'form-control', 'placeholder': 'Confirm Password'})

    class Meta:
        model = User
        fields = ('email','password1','password2','is_petowner')
        widgets = {
        'is_petowner': forms.HiddenInput(),
     }


class UpdateUserForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["email"].widget.attrs.update(
            {'required': True, 'name': 'email', 'id': 'email', 'type': 'text', 'class': 'form-control', 'placeholder': 'Email'})

    class Meta:
        model = User
        fields = ('email',)



#END USER ACCOUNTS

#USER PROFILE
class UpdateProfileForm(forms.ModelForm):
    useracc= forms.ModelChoiceField(queryset=User.objects.filter(is_petowner=True, is_active=True,is_used=False),required=False)
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["useracc"].widget.attrs.update(
            { 'name': 'useracc', 'id': 'useracc', 'type': 'text', 'class': 'form-control', 'placeholder': 'User Account'})
        self.fields["firstName"].widget.attrs.update(
            {'required': True, 'name': 'firstname', 'id': 'firstName', 'type': 'text', 'class': 'form-control', 'placeholder': 'First Name'})
        self.fields["lastName"].widget.attrs.update(
            {'required': True, 'name': 'lastname', 'id': 'lastName', 'type': 'text', 'class': 'form-control', 'placeholder': 'Last Name'})
        self.fields["gender"].widget.attrs.update(
            {'name': 'gender', 'id': 'gender', 'type': 'text', 'class': 'form-control', 'placeholder': 'Gender'})
        self.fields["contactNum"].widget.attrs.update(
            { 'name': 'contactNum', 'id': 'contactNum', 'type': 'text', 'class': 'form-control', 'placeholder': 'Contact Number'})
        self.fields["address"].widget.attrs.update(
            {'name': 'address', 'id': 'address', 'type': 'text', 'class': 'form-control', 'placeholder': 'Address'})

    class Meta:
        model = Profile
        fields = ('useracc','firstName', 'lastName', 'gender', 'contactNum', 'address')

class UpdatePetOwnerProfileForm(forms.ModelForm):
    useracc= forms.ModelChoiceField(queryset=User.objects.filter(is_petowner=True, is_active=True),required=False)
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["useracc"].widget.attrs.update(
            { 'name': 'useracc', 'id': 'useracc', 'type': 'text', 'class': 'form-control', 'placeholder': 'User Account'})
        self.fields["firstName"].widget.attrs.update(
            {'required': True, 'name': 'firstname', 'id': 'firstName', 'type': 'text', 'class': 'form-control', 'placeholder': 'First Name'})
        self.fields["lastName"].widget.attrs.update(
            {'required': True, 'name': 'lastname', 'id': 'lastName', 'type': 'text', 'class': 'form-control', 'placeholder': 'Last Name'})
        self.fields["gender"].widget.attrs.update(
            {'name': 'gender', 'id': 'gender', 'type': 'text', 'class': 'form-control', 'placeholder': 'Gender'})
        self.fields["contactNum"].widget.attrs.update(
            { 'name': 'contactNum', 'id': 'contactNum', 'type': 'text', 'class': 'form-control', 'placeholder': 'Contact Number'})
        self.fields["address"].widget.attrs.update(
            {'name': 'address', 'id': 'address', 'type': 'text', 'class': 'form-control', 'placeholder': 'Address'})

    class Meta:
        model = Profile
        fields = ('useracc','firstName', 'lastName', 'gender', 'contactNum', 'address')

class AddVetProfileForm(forms.ModelForm):
    useracc= forms.ModelChoiceField(queryset=User.objects.filter(is_veterinarian=True, is_active=True,is_used=False))
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["useracc"].widget.attrs.update(
            { 'name': 'useracc', 'id': 'useracc', 'type': 'text', 'class': 'form-control', 'placeholder': 'User Account'})
        self.fields["firstName"].widget.attrs.update(
            {'required': True, 'name': 'firstname', 'id': 'firstName', 'type': 'text', 'class': 'form-control', 'placeholder': 'First Name'})
        self.fields["lastName"].widget.attrs.update(
            {'required': True, 'name': 'lastname', 'id': 'lastName', 'type': 'text', 'class': 'form-control', 'placeholder': 'Last Name'})
        self.fields["gender"].widget.attrs.update(
            {'name': 'gender', 'id': 'gender', 'type': 'text', 'class': 'form-control', 'placeholder': 'Gender'})
        self.fields["contactNum"].widget.attrs.update(
            { 'name': 'contactNum', 'id': 'contactNum', 'type': 'text', 'class': 'form-control', 'placeholder': 'Contact Number'})
        self.fields["address"].widget.attrs.update(
            {'name': 'address', 'id': 'address', 'type': 'text', 'class': 'form-control', 'placeholder': 'Address'})

    class Meta:
        model = StaffProfile
        fields = ('useracc','firstName', 'lastName', 'gender', 'contactNum', 'address')

class UpdateVetProfileForm(forms.ModelForm):
    useracc= forms.ModelChoiceField(queryset=User.objects.filter(is_veterinarian=True, is_active=True))
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["useracc"].widget.attrs.update(
            { 'name': 'useracc', 'id': 'useracc', 'type': 'text', 'class': 'form-control', 'placeholder': 'User Account'})
        self.fields["firstName"].widget.attrs.update(
            {'required': True, 'name': 'firstname', 'id': 'firstName', 'type': 'text', 'class': 'form-control', 'placeholder': 'First Name'})
        self.fields["lastName"].widget.attrs.update(
            {'required': True, 'name': 'lastname', 'id': 'lastName', 'type': 'text', 'class': 'form-control', 'placeholder': 'Last Name'})
        self.fields["gender"].widget.attrs.update(
            {'name': 'gender', 'id': 'gender', 'type': 'text', 'class': 'form-control', 'placeholder': 'Gender'})
        self.fields["contactNum"].widget.attrs.update(
            { 'name': 'contactNum', 'id': 'contactNum', 'type': 'text', 'class': 'form-control', 'placeholder': 'Contact Number'})
        self.fields["address"].widget.attrs.update(
            {'name': 'address', 'id': 'address', 'type': 'text', 'class': 'form-control', 'placeholder': 'Address'})

    class Meta:
        model = StaffProfile
        fields = ('useracc','firstName', 'lastName', 'gender', 'contactNum', 'address')

class AddHeadVetProfileForm(forms.ModelForm):
    useracc= forms.ModelChoiceField(queryset=User.objects.filter(is_headveterinarian=True, is_active=True,is_used=False))
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["useracc"].widget.attrs.update(
            { 'name': 'useracc', 'id': 'useracc', 'type': 'text', 'class': 'form-control', 'placeholder': 'User Account'})
        self.fields["firstName"].widget.attrs.update(
            {'required': True, 'name': 'firstname', 'id': 'firstName', 'type': 'text', 'class': 'form-control', 'placeholder': 'First Name'})
        self.fields["lastName"].widget.attrs.update(
            {'required': True, 'name': 'lastname', 'id': 'lastName', 'type': 'text', 'class': 'form-control', 'placeholder': 'Last Name'})
        self.fields["gender"].widget.attrs.update(
            {'name': 'gender', 'id': 'gender', 'type': 'text', 'class': 'form-control', 'placeholder': 'Gender'})
        self.fields["contactNum"].widget.attrs.update(
            { 'name': 'contactNum', 'id': 'contactNum', 'type': 'text', 'class': 'form-control', 'placeholder': 'Contact Number'})
        self.fields["address"].widget.attrs.update(
            {'name': 'address', 'id': 'address', 'type': 'text', 'class': 'form-control', 'placeholder': 'Address'})

    class Meta:
        model = StaffProfile
        fields = ('useracc','firstName', 'lastName', 'gender', 'contactNum', 'address')

class UpdateHeadVetProfileForm(forms.ModelForm):
    useracc= forms.ModelChoiceField(blank=True,queryset=User.objects.filter(is_headveterinarian=True, is_active=True))
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["useracc"].widget.attrs.update(
            { 'name': 'useracc', 'id': 'useracc', 'type': 'text', 'class': 'form-control', 'placeholder': 'User Account'})
        self.fields["firstName"].widget.attrs.update(
            {'required': True, 'name': 'firstname', 'id': 'firstName', 'type': 'text', 'class': 'form-control', 'placeholder': 'First Name'})
        self.fields["lastName"].widget.attrs.update(
            {'required': True, 'name': 'lastname', 'id': 'lastName', 'type': 'text', 'class': 'form-control', 'placeholder': 'Last Name'})
        self.fields["gender"].widget.attrs.update(
            {'name': 'gender', 'id': 'gender', 'type': 'text', 'class': 'form-control', 'placeholder': 'Gender'})
        self.fields["contactNum"].widget.attrs.update(
            { 'name': 'contactNum', 'id': 'contactNum', 'type': 'text', 'class': 'form-control', 'placeholder': 'Contact Number'})
        self.fields["address"].widget.attrs.update(
            {'name': 'address', 'id': 'address', 'type': 'text', 'class': 'form-control', 'placeholder': 'Address'})

    class Meta:
        model = StaffProfile
        fields = ('useracc','firstName', 'lastName', 'gender', 'contactNum', 'address')

class AddSecProfileForm(forms.ModelForm):
    useracc= forms.ModelChoiceField(queryset=User.objects.filter(is_secretary=True, is_active=True,is_used=False))
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["useracc"].widget.attrs.update(
            { 'name': 'useracc', 'id': 'useracc', 'type': 'text', 'class': 'form-control', 'placeholder': 'User Account'})
        self.fields["firstName"].widget.attrs.update(
            {'required': True, 'name': 'firstname', 'id': 'firstName', 'type': 'text', 'class': 'form-control', 'placeholder': 'First Name'})
        self.fields["lastName"].widget.attrs.update(
            {'required': True, 'name': 'lastname', 'id': 'lastName', 'type': 'text', 'class': 'form-control', 'placeholder': 'Last Name'})
        self.fields["gender"].widget.attrs.update(
            {'name': 'gender', 'id': 'gender', 'type': 'text', 'class': 'form-control', 'placeholder': 'Gender'})
        self.fields["contactNum"].widget.attrs.update(
            { 'name': 'contactNum', 'id': 'contactNum', 'type': 'text', 'class': 'form-control', 'placeholder': 'Contact Number'})
        self.fields["address"].widget.attrs.update(
            {'name': 'address', 'id': 'address', 'type': 'text', 'class': 'form-control', 'placeholder': 'Address'})

    class Meta:
        model = StaffProfile
        fields = ('useracc','firstName', 'lastName', 'gender', 'contactNum', 'address')

class UpdateSecProfileForm(forms.ModelForm):
    useracc= forms.ModelChoiceField(blank=True,queryset=User.objects.filter(is_secretary=True, is_active=True))
    gender = forms.RadioSelect()
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["useracc"].widget.attrs.update(
            { 'name': 'useracc', 'id': 'useracc', 'type': 'text', 'class': 'form-control', 'placeholder': 'User Account'})
        self.fields["firstName"].widget.attrs.update(
            {'required': True, 'name': 'firstname', 'id': 'firstName', 'type': 'text', 'class': 'form-control', 'placeholder': 'First Name'})
        self.fields["lastName"].widget.attrs.update(
            {'required': True, 'name': 'lastname', 'id': 'lastName', 'type': 'text', 'class': 'form-control', 'placeholder': 'Last Name'})
        self.fields["gender"].widget.attrs.update(
            {'name': 'gender', 'id': 'gender', 'type': 'text', 'class': 'form-control', 'placeholder': 'Gender'})
        self.fields["contactNum"].widget.attrs.update(
            { 'name': 'contactNum', 'id': 'contactNum', 'type': 'text', 'class': 'form-control', 'placeholder': 'Contact Number'})
        self.fields["address"].widget.attrs.update(
            {'name': 'address', 'id': 'address', 'type': 'text', 'class': 'form-control', 'placeholder': 'Address'})

    class Meta:
        model = StaffProfile
        fields = ('useracc','firstName', 'lastName', 'gender', 'contactNum', 'address')
#END USER PROFILE

#ADD MEDICAL HISTORY
class SecMedHistory(forms.ModelForm):
    pet= forms.ModelChoiceField(queryset=pets.objects.filter(is_deleted=False))
    date= forms.DateField(widget=DateInput)
    symptoms = forms.CharField(widget=forms.Textarea,required=False)
    treatment = forms.CharField(widget=forms.Textarea,required=False)
    prescription = forms.CharField(widget=forms.Textarea,required=False)
    instruction = forms.CharField(widget=forms.Textarea,required=False)
    dateofReturn = forms.DateField(widget=DateInput,required=False)
    reason = forms.CharField(widget=forms.Textarea,required=False)
    sec = queryset=User.objects.exclude(is_secretary=True)
    vet = forms.ModelChoiceField(queryset=StaffProfile.objects.filter(is_deleted=False,useracc__in=sec),required=False)
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["pet"].widget.attrs.update(
            { 'name': 'pet', 'id': 'pet', 'type': 'text', 'class': 'form-control', 'placeholder': 'Pet Name'})
        self.fields["date"].widget.attrs.update(
            { 'name': 'date', 'id': 'pet', 'type': 'date', 'class': 'form-control', 'placeholder': 'date'})
        self.fields["vet"].widget.attrs.update(
            { 'name': 'vet', 'id': 'vet', 'type': 'text', 'class': 'form-control', 'placeholder': 'Veterinarian'})
        self.fields["weight"].widget.attrs.update(
            { 'name': 'weight', 'id': 'weight', 'type': 'text', 'class': 'form-control', 'placeholder': 'Weight'})
        self.fields["symptoms"].widget.attrs.update(
            { 'name': 'symptoms', 'id': 'symptoms', 'type': 'text', 'class': 'form-control', 'placeholder': 'Symptoms'})
        self.fields["treatment"].widget.attrs.update(
            { 'name': 'treatment', 'id': 'treatment', 'type': 'text', 'class': 'form-control', 'placeholder': 'Treatment'})
        self.fields["prescription"].widget.attrs.update(
            { 'name': 'prescription', 'id': 'prescription', 'type': 'text', 'class': 'form-control', 'placeholder': 'Prescription'})
        self.fields["instruction"].widget.attrs.update(
            { 'name': 'instruction', 'id': 'instruction', 'type': 'text', 'class': 'form-control', 'placeholder': 'Instruction'})
        self.fields["dateofReturn"].widget.attrs.update(
            { 'name': 'dateofReturn', 'id': 'dateofReturn', 'type': 'date', 'class': 'form-control',})
        self.fields["reason"].widget.attrs.update(
            { 'name': 'reason', 'id': 'reason', 'type': 'text', 'class': 'form-control', 'placeholder': 'Reason'})
        

    class Meta:
        model = MedicalHistory
        fields = ('pet','date','weight','symptoms','treatment','prescription','instruction','dateofReturn','reason','vet')

class MedHistory(forms.ModelForm):
    sec = queryset=User.objects.exclude(is_secretary=True)
   
    date= forms.DateField(widget=DateInput)
    symptoms = forms.CharField(widget=forms.Textarea,required=False)
    treatment = forms.CharField(widget=forms.Textarea,required=False)
    prescription = forms.CharField(widget=forms.Textarea,required=False)
    instruction = forms.CharField(widget=forms.Textarea,required=False)
    dateofReturn = forms.DateField(widget=DateInput,required=False)
    reason = forms.CharField(widget=forms.Textarea,required=False)
    vet = forms.ModelChoiceField(queryset=StaffProfile.objects.filter(is_deleted=False,useracc__in=sec))
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["pet"].widget.attrs.update(
            { 'name': 'pet', 'id': 'pet', 'type': 'text', 'class': 'form-control', 'placeholder': 'Pet Name'})
        self.fields["date"].widget.attrs.update(
            { 'name': 'date', 'id': 'pet', 'type': 'date', 'class': 'form-control', 'placeholder': 'date'})
        self.fields["vet"].widget.attrs.update(
            { 'name': 'vet', 'id': 'vet', 'type': 'text', 'class': 'form-control', 'placeholder': 'Veterinarian'})
        self.fields["weight"].widget.attrs.update(
            { 'name': 'weight', 'id': 'weight', 'type': 'text', 'class': 'form-control', 'placeholder': 'Weight'})
        self.fields["symptoms"].widget.attrs.update(
            { 'name': 'symptoms', 'id': 'symptoms', 'type': 'text', 'class': 'form-control', 'placeholder': 'Symptoms'})
        self.fields["treatment"].widget.attrs.update(
            { 'name': 'treatment', 'id': 'treatment', 'type': 'text', 'class': 'form-control', 'placeholder': 'Treatment'})
        self.fields["prescription"].widget.attrs.update(
            { 'name': 'prescription', 'id': 'prescription', 'type': 'text', 'class': 'form-control', 'placeholder': 'Prescription'})
        self.fields["instruction"].widget.attrs.update(
            { 'name': 'instruction', 'id': 'instruction', 'type': 'text', 'class': 'form-control', 'placeholder': 'Instruction'})
        self.fields["dateofReturn"].widget.attrs.update(
            { 'name': 'dateofReturn', 'id': 'dateofReturn', 'type': 'date', 'class': 'form-control',})
        self.fields["reason"].widget.attrs.update(
            { 'name': 'reason', 'id': 'reason', 'type': 'text', 'class': 'form-control', 'placeholder': 'Reason'})

    class Meta:
        model = MedicalHistory
        fields = ('pet','date','weight','symptoms','treatment','prescription','instruction','dateofReturn','reason','vet')
        widgets = {
        'pet': forms.HiddenInput()

     }

#END MEDICAL HISTORY

#ADD AVAILED SERVICE
class AddAvailedService(forms.ModelForm):
    sec = queryset=User.objects.exclude(is_secretary=True)
    dateofService = forms.DateField(widget=DateInput)
    service = forms.ModelChoiceField(queryset=services.objects.filter(is_labTest=False,is_vaccination=False))
    interpretation = forms.CharField(widget=forms.Textarea,required=False)
    vet = forms.ModelChoiceField(queryset=StaffProfile.objects.filter(is_deleted=False,useracc__in=sec),required= False)
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["medHistory"].widget.attrs.update(
                {'required': True, 'name': 'medHistory', 'id': 'medHistory', 'type': '', 
                'class': 'form-control', 'placeholder': ''})
        self.fields["dateofService"].widget.attrs.update(
                {'required': True, 'name': 'dateofService', 'id': 'dateofService', 'type': 'date', 
                'class': 'form-control', 'placeholder': ''})
        self.fields["service"].widget.attrs.update(
                {'required': True, 'name': 'service', 'id': 'service', 'type': 'text', 
                'class': 'form-control', 'placeholder': 'service'})
        self.fields["interpretation"].widget.attrs.update(
                {'required': False, 'name': 'service', 'id': 'service', 'type': 'text', 
                'class': 'form-control', 'placeholder': 'Remarks'})
        self.fields["vet"].widget.attrs.update(
                {'required': False, 'name': 'service', 'id': 'service', 'type': 'text', 
                'class': 'form-control', 'placeholder': ''})

    class Meta:
        model = serviceHistory
        fields = ('medHistory','dateofService','service','interpretation','vet')

class AvailedService(forms.ModelForm):
    sec = queryset=User.objects.exclude(is_secretary=True)
    dateofService = forms.DateField(widget=DateInput)
    service = forms.ModelChoiceField(queryset=services.objects.filter(is_labTest=False,is_vaccination=False))
    interpretation = forms.CharField(widget=forms.Textarea,required=False)
    vet = forms.ModelChoiceField(queryset=StaffProfile.objects.filter(is_deleted=False,useracc__in=sec),required= False)
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["medHistory"].widget.attrs.update(
                {'required': True, 'name': 'medHistory', 'id': 'medHistory', 'type': '', 
                'class': 'form-control', 'placeholder': ''})
        self.fields["dateofService"].widget.attrs.update(
                {'required': True, 'name': 'dateofService', 'id': 'dateofService', 'type': 'date', 
                'class': 'form-control', 'placeholder': ''})
        self.fields["service"].widget.attrs.update(
                {'required': True, 'name': 'service', 'id': 'service', 'type': 'text', 
                'class': 'form-control', 'placeholder': 'service'})
        self.fields["interpretation"].widget.attrs.update(
                {'required': False, 'name': 'service', 'id': 'service', 'type': 'text', 
                'class': 'form-control', 'placeholder': 'Remarks'})
        self.fields["vet"].widget.attrs.update(
                {'required': False, 'name': 'service', 'id': 'service', 'type': 'text', 
                'class': 'form-control', 'placeholder': ''})

    class Meta:
        model = serviceHistory
        fields = ('medHistory','dateofService','service','interpretation','vet')
        widgets = {
        'medHistory': forms.HiddenInput()
     }


#ADD LAB TEST SERVICE
class AddLabTestForm(forms.ModelForm):
    sec = queryset=User.objects.exclude(is_secretary=True)
    dateofService = forms.DateField(widget=DateInput)
    service = forms.ModelChoiceField(queryset=services.objects.filter(is_labTest=True))
    dateofResult = forms.DateField(widget=DateInput,required=False)
    interpretation = forms.CharField(widget=forms.Textarea,required=False)
    vet = forms.ModelChoiceField(queryset=StaffProfile.objects.filter(is_deleted=False,useracc__in=sec),required= False)
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["medHistory"].widget.attrs.update(
                {'required': True, 'name': 'medHistory', 'id': 'medHistory', 'type': '', 
                'class': 'form-control', 'placeholder': ''})
        self.fields["dateofService"].widget.attrs.update(
                {'required': True, 'name': 'dateofService', 'id': 'dateofService', 'type': 'date', 
                'class': 'form-control', 'placeholder': ''})
        self.fields["service"].widget.attrs.update(
                {'required': True, 'name': 'service', 'id': 'service', 'type': 'text', 
                'class': 'form-control', 'placeholder': ''})
        self.fields["dateofResult"].widget.attrs.update(
                {'required': False, 'name': 'dateofResult', 'id': 'dateofService', 'type': 'date', 
                'class': 'form-control', 'placeholder': ''})
        self.fields["interpretation"].widget.attrs.update(
                {'required': False, 'name': 'service', 'id': 'service', 'type': 'text', 
                'class': 'form-control', 'placeholder': 'Remarks'})
        self.fields["vet"].widget.attrs.update(
                {'required': False, 'name': 'service', 'id': 'service', 'type': 'text', 
                'class': 'form-control', 'placeholder': ''})

    class Meta:
        model = labHistory
        fields = ('medHistory','dateofService','service','dateofResult','interpretation','vet')

class LabTestForm(forms.ModelForm):
    sec = queryset=User.objects.exclude(is_secretary=True)
    dateofService = forms.DateField(widget=DateInput)
    service = forms.ModelChoiceField(queryset=services.objects.filter(is_labTest=True))
    dateofResult = forms.DateField(widget=DateInput,required=False)
    interpretation = forms.CharField(widget=forms.Textarea,required=False)
    vet = forms.ModelChoiceField(queryset=StaffProfile.objects.filter(is_deleted=False,useracc__in=sec),required= False)
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["medHistory"].widget.attrs.update(
                {'required': True, 'name': 'medHistory', 'id': 'medHistory', 'type': '', 
                'class': 'form-control', 'placeholder': ''})
        self.fields["dateofService"].widget.attrs.update(
                {'required': True, 'name': 'dateofService', 'id': 'dateofService', 'type': 'date', 
                'class': 'form-control', 'placeholder': ''})
        self.fields["service"].widget.attrs.update(
                {'required': True, 'name': 'service', 'id': 'service', 'type': 'text', 
                'class': 'form-control', 'placeholder': ''})
        self.fields["dateofResult"].widget.attrs.update(
                {'required': False, 'name': 'dateofResult', 'id': 'dateofService', 'type': 'date', 
                'class': 'form-control', 'placeholder': ''})
        self.fields["interpretation"].widget.attrs.update(
                {'required': False, 'name': 'service', 'id': 'service', 'type': 'text', 
                'class': 'form-control', 'placeholder': 'Remarks'})
        self.fields["vet"].widget.attrs.update(
                {'required': False, 'name': 'service', 'id': 'service', 'type': 'text', 
                'class': 'form-control', 'placeholder': ''})

    class Meta:
        model = labHistory
        fields = ('medHistory','dateofService','service','dateofResult','interpretation','vet')
        widgets = {
        'medHistory': forms.HiddenInput()
     }

#ADD VACCINE SERVICE
class AddVaccineServiceForm(forms.ModelForm):
    sec = User.objects.exclude(is_secretary=True)
    dateofService = forms.DateField(widget=DateInput)
    service = forms.ModelChoiceField(queryset=services.objects.filter(is_vaccination=True))
    interpretation = forms.CharField(widget=forms.Textarea)
    dateofReturn = forms.DateField(widget=DateInput,required=False)
    reason = forms.CharField(widget=forms.Textarea,required=False)
    vet = forms.ModelChoiceField(queryset=StaffProfile.objects.filter(is_deleted=False,useracc__in=sec),required= False)
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["medHistory"].widget.attrs.update(
                {'required': True, 'name': 'medHistory', 'id': 'medHistory', 'type': '', 
                'class': 'form-control', 'placeholder': ''})
        self.fields["dateofService"].widget.attrs.update(
                {'required': True, 'name': 'dateofService', 'id': 'dateofService', 'type': 'date', 
                'class': 'form-control', 'placeholder': ''})
        self.fields["service"].widget.attrs.update(
                {'required': True, 'name': 'service', 'id': 'service', 'type': 'text', 
                'class': 'form-control', 'placeholder': ''})
        self.fields["vaccine"].widget.attrs.update(
                {'required': False, 'type': 'text', 
                'class': 'form-control', 'placeholder': ''})
        self.fields["interpretation"].widget.attrs.update(
                {'required': False, 'name': 'service', 'id': 'service', 'type': 'text', 
                'class': 'form-control', 'placeholder': 'Remarks'})
        self.fields["dateofReturn"].widget.attrs.update(
                {'required': False, 'name': 'dateofReturn', 'id': 'dateofService', 'type': 'date', 
                'class': 'form-control', 'placeholder': ''})
        self.fields["reason"].widget.attrs.update(
                {'required': False, 'name': 'service', 'id': 'service', 'type': 'text', 
                'class': 'form-control', 'placeholder': 'Reason'})
        self.fields["vet"].widget.attrs.update(
                {'required': False, 'name': 'service', 'id': 'service', 'type': 'text', 
                'class': 'form-control', 'placeholder': ''})
                
    class Meta:
        model = vaccineHistory
        fields = ('medHistory','dateofService','service','vaccine','interpretation','dateofReturn','reason','vet')


class VaccineServiceForm(forms.ModelForm):
    sec = User.objects.exclude(is_secretary=True)
    dateofService = forms.DateField(widget=DateInput)
    service = forms.ModelChoiceField(queryset=services.objects.filter(is_vaccination=True))
    interpretation = forms.CharField(widget=forms.Textarea)
    dateofReturn = forms.DateField(widget=DateInput,required=False)
    reason = forms.CharField(widget=forms.Textarea,required=False)
    vet = forms.ModelChoiceField(queryset=StaffProfile.objects.filter(is_deleted=False,useracc__in=sec),required= False)
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["medHistory"].widget.attrs.update(
                {'required': True, 'name': 'medHistory', 'id': 'medHistory', 'type': '', 
                'class': 'form-control', 'placeholder': ''})
        self.fields["dateofService"].widget.attrs.update(
                {'required': True, 'name': 'dateofService', 'id': 'dateofService', 'type': 'date', 
                'class': 'form-control', 'placeholder': ''})
        self.fields["service"].widget.attrs.update(
                {'required': True, 'name': 'service', 'id': 'service', 'type': 'text', 
                'class': 'form-control', 'placeholder': ''})
        self.fields["vaccine"].widget.attrs.update(
                {'required': False,'type': 'text', 
                'class': 'form-control', 'placeholder': ''})
        self.fields["interpretation"].widget.attrs.update(
                {'required': False, 'name': 'service', 'id': 'service', 'type': 'text', 
                'class': 'form-control', 'placeholder': 'Remarks'})
        self.fields["dateofReturn"].widget.attrs.update(
                {'required': False, 'name': 'dateofReturn', 'id': 'dateofService', 'type': 'date', 
                'class': 'form-control', 'placeholder': ''})
        self.fields["reason"].widget.attrs.update(
                {'required': False, 'name': 'service', 'id': 'service', 'type': 'text', 
                'class': 'form-control', 'placeholder': 'Reason'})
        self.fields["vet"].widget.attrs.update(
                {'required': False, 'name': 'service', 'id': 'service', 'type': 'text', 
                'class': 'form-control', 'placeholder': ''})
                
    class Meta:
        model = vaccineHistory
        fields = ('medHistory','dateofService','service','vaccine','interpretation','dateofReturn','reason','vet')
        widgets = {
        'medHistory': forms.HiddenInput()
     }




class AddSpecies(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["species"].widget.attrs.update(
            {'required': True, 'name': 'species', 'id': 'species', 'type': 'text', 'class': 'form-control', 'placeholder': 'Species'})

    class Meta:
        model = petspecies
        fields = ('species',)

class AddVaccineTypeForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["vaccineType"].widget.attrs.update(
            {'required': True, 'name': 'vaccineType', 'id': 'vaccineType', 'type': 'text', 'class': 'form-control', 'placeholder': 'Vaccine'})

    class Meta:
        model = vaxType
        fields = ('vaccineType',)

class Add_PetForm(forms.ModelForm):
    petOwner = forms.ModelChoiceField(
        queryset=Profile.objects.filter(useracc=User.objects.filter(is_petowner=True,is_active=True)))
    species = forms.ModelChoiceField(
        queryset=petspecies.objects.filter(is_deleted=False))
    dob = forms.DateField(widget=DateInput)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["petOwner"].widget.attrs.update(
            {'required': True, 'name': 'petOwner', 'id': 'petOwner', 'type': 'text', 'class': 'form-control', 'placeholder': 'Pet Owner'})
        self.fields["petName"].widget.attrs.update(
            {'required': True, 'name': 'petName', 'id': 'petName', 'type': 'text', 'class': 'form-control', 'placeholder': 'Pet Name'})
        self.fields["dob"].widget.attrs.update(
            {'required': True, 'name': 'dob', 'id': 'dob', 'type': 'date', 'class': 'form-control', 'placeholder': 'Date of Birth'})
        self.fields["sex"].widget.attrs.update(
            {'required': True, 'name': 'sex', 'id': 'sex', 'type': 'text', 'class': 'form-control', 'placeholder': 'Gender'})
        self.fields["species"].widget.attrs.update(
            {'required': True, 'name': 'species', 'id': 'species', 'type': 'text', 'class': 'form-control', 'placeholder': 'Species'})
        self.fields["description"].widget.attrs.update(
            {'required': True, 'name': 'description', 'id': 'description', 'type': 'text', 'class': 'form-control', 'placeholder': 'Breed'})
        self.fields["colorMarking"].widget.attrs.update(
            {'required': True, 'name': 'colorMarking', 'id': 'colorMarking', 'type': 'text', 'class': 'form-control', 'placeholder': 'Color Marking'})

    class Meta:
        model = pets
        fields = ('petOwner', 'petName', 'dob', 'sex',
                  'species', 'description', 'colorMarking', 'pet_image') #bago toh pet

class Add_ServiceForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["serviceName"].widget.attrs.update(
            {'required': True, 'name': 'serviceName', 'id': 'serviceName', 'type': 'text', 'class': 'form-control', 'placeholder': 'Service'})
        self.fields["description"].widget.attrs.update(
            {'required': True, 'name': 'description', 'id': 'description', 'type': 'text', 'class': 'form-control', 'placeholder': 'Description'})
        self.fields["price"].widget.attrs.update(
            {'required': True, 'name': 'price', 'id': 'price', 'type': 'number', 'class': 'form-control', 'placeholder': 'Price'})

    class Meta:
        model = services
        fields = ('serviceName', 'description', 'price', 'is_labTest','is_vaccination')

class AddProductTypeForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["prodType"].widget.attrs.update(
            {'required': True, 'name': 'prodType', 'id': 'prodType', 'type': 'text', 'class': 'form-control', 'placeholder': 'Product Type'})

    class Meta:
        model = ProductType
        fields = ('prodType',)

class AddProductForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["product_name"].widget.attrs.update({'class': 'form-control'})
        self.fields["product_type"].widget.attrs.update({'class': 'form-control'})
        self.fields["description"].widget.attrs.update({'class': 'form-control'})
        self.fields["price"].widget.attrs.update({'class': 'form-control'})
        self.fields["medium_margin"].widget.attrs.update({'class': 'form-control','type':'number'})
        self.fields["low_margin"].widget.attrs.update({'class': 'form-control','type':'number'})

    class Meta:
        model = ProductInfo
        fields = ('product_name', 'description', 'product_type', 'price','medium_margin','low_margin')

class AddProductInventoryForm(forms.ModelForm):
    manuDate = forms.DateField(widget=DateInput)
    expireDate = forms.DateField(widget=DateInput)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["product"].widget.attrs.update({'class': 'form-control'})
        self.fields["manuDate"].widget.attrs.update({'class': 'form-control'})
        self.fields["expireDate"].widget.attrs.update(
            {'class': 'form-control'})
        self.fields["quantity"].widget.attrs.update({'class': 'form-control'})

    class Meta:
        model = Product
        fields = ('product', 'manuDate', 'expireDate', 'quantity')

class GenderForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["gender"].widget.attrs.update(
            {'required': True, 'name': 'gender', 'id': 'gender', 'type': 'text', 'class': 'form-control', 'placeholder': 'Gender'})

    class Meta:
        model = Gender
        fields = ('gender',)

class AddPetForm(forms.ModelForm):
    class Meta:
        model = pets
        fields = ('petOwner', 'petName', 'dob', 'sex',
                  'species', 'description', 'colorMarking', 'pet_image') #bago toh pet
    petOwner = forms.ModelChoiceField(
        queryset=Profile.objects.filter(is_deleted=0))
    species = forms.ModelChoiceField(
        queryset=petspecies.objects.filter(is_deleted=False))
    dob = forms.DateField(widget=DateInput)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['description'].queryset = breed.objects.none()
        self.fields['petName'].widget.attrs.update(
            {'required': True, 'name': 'gender', 'id': 'id_petName', 'type': 'text', 'class': 'form-controll', 'placeholder': 'Pet Name'})
        self.fields['petOwner'].widget.attrs.update(
            {'required': True, 'name': 'petOwner', 'id': 'id_petOwner', 'type': 'text', 'class': 'form-controll', 'placeholder': 'Gender'})
        self.fields['sex'].widget.attrs.update(
            {'required': True, 'name': 'sex', 'id': 'gender', 'type': 'text', 'class': 'form-controll', 'placeholder': 'Gender'})
        self.fields['dob'].widget.attrs.update(
            {'required': True, 'name': 'dob', 'id': 'id_dob', 'type': 'text', 'class': 'form-controll', 'placeholder': 'Date of Birth'})
        self.fields['species'].widget.attrs.update(
            {'required': True, 'name': 'species', 'id': 'id_species', 'type': 'text', 'class': 'form-controll', 'placeholder': 'Species'})
        self.fields['description'].widget.attrs.update(
            {'required': True, 'name': 'description', 'id': 'id_description', 'type': 'text', 'class': 'form-controll', 'placeholder': 'Breeed'})
        self.fields['colorMarking'].widget.attrs.update(
            {'required': True, 'name': 'colorMarking', 'id': 'id_colorMarking', 'type': 'text', 'class': 'form-controll', 'placeholder': 'Color Marking'})
        if 'species' in self.data:
            try:
                species_id = int(self.data.get('species'))
                self.fields['description'].queryset = breed.objects.filter(
                    kind=species_id, is_deleted=False).order_by('breed')
            except (ValueError, TypeError):
                pass
        elif self.instance.pk:
            self.fields['description'].queryset = self.instance.species.breed_set.order_by(
                'breed')

class BreedForm(forms.ModelForm):
    kind = forms.ModelChoiceField(
        queryset=petspecies.objects.filter(is_deleted=False))
    widgets = {

        'kind': forms.Select(attrs={'class': 'form-control'}),

    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["kind"].widget.attrs.update(
            {'required': True, 'name': 'kind', 'id': 'kind', 'class': 'form-control', 'placeholder': 'Kind'})
        self.fields["breed"].widget.attrs.update(
            {'required': True, 'name': 'kind', 'id': 'id_breed', 'class': 'form-control', 'placeholder': 'Breed'})

    class Meta:
        model = breed
        fields = ('kind', 'breed')


class ProductInvoice(forms.ModelForm):
    product = forms.ModelChoiceField(queryset=Product.objects.filter(is_deleted=False))
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["product"].widget.attrs.update(
            {'required': True, 'class': 'form-control', 'placeholder': 'Product'})
        self.fields["quantity"].widget.attrs.update(
            {'required': True, 'class': 'form-control', 'placeholder': 'quantity','type':'number'})
            
    class Meta:
        model=productInvoice
        fields = ('chargeslip','product','quantity')
        widgets = {
        'chargeslip': forms.HiddenInput(),
     }


class Sec_ProductInvoice(forms.ModelForm):
    product = forms.ModelChoiceField(queryset=Product.objects.filter(is_deleted=False))
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["product"].widget.attrs.update(
            {'required': True, 'class': 'form-control', 'placeholder': 'Product'})
        self.fields["quantity"].widget.attrs.update(
            {'required': True, 'class': 'form-control', 'placeholder': 'quantity','type':'number'})
            
    class Meta:
        model=productInvoice
        fields = ('product','quantity')


class Edit_PetOwner_Profile(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["gender"].widget.attrs.update(
            {'name': 'gender', 'id': 'gender', 'type': 'text', 'class': 'form-control', 'placeholder': 'Gender'})
        self.fields["contactNum"].widget.attrs.update(
            { 'name': 'contactNum', 'id': 'contactNum', 'type': 'text', 'class': 'form-control', 'placeholder': 'Contact Number'})
        self.fields["address"].widget.attrs.update(
            {'name': 'address', 'id': 'address', 'type': 'text', 'class': 'form-control', 'placeholder': 'Address'})

    class Meta:
        model = Profile
        fields = ('gender', 'contactNum', 'address', 'user_image') #bago toh

class Edit_Staff_Profile(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["gender"].widget.attrs.update(
            {'name': 'gender', 'id': 'gender', 'type': 'text', 'class': 'form-control', 'placeholder': 'Gender'})
        self.fields["contactNum"].widget.attrs.update(
            { 'name': 'contactNum', 'id': 'contactNum', 'type': 'text', 'class': 'form-control', 'placeholder': 'Contact Number'})
        self.fields["address"].widget.attrs.update(
            {'name': 'address', 'id': 'address', 'type': 'text', 'class': 'form-control', 'placeholder': 'Address'})

    class Meta:
        model = StaffProfile
        fields = ('gender', 'contactNum', 'address', 'user_image') #bago toh


class Schedule_Slot(forms.ModelForm):
    date = forms.DateField(widget=DateInput)
    sec = queryset=User.objects.exclude(is_secretary=True)
    timeIn = forms.TimeInput()
    timeOut = forms.TimeInput()
    vet = forms.ModelChoiceField(queryset=StaffProfile.objects.filter(is_deleted=False,useracc__in=sec),required=False)
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["date"].widget.attrs.update(
            { 'name': 'date', 'id': 'date', 'type': 'date', 'class': 'form-control', 'placeholder': 'hh:mm'})
        self.fields["timeIn"].widget.attrs.update(
            { 'type': 'text', 'class': 'form-control', 'placeholder': 'hh:mm'})
        self.fields["timeOut"].widget.attrs.update(
            { 'type': 'text', 'class': 'form-control', 'placeholder': 'hh:mm'})
        self.fields["vet"].widget.attrs.update(
            {'name': 'vet', 'id': 'vet', 'type': 'text', 'class': 'form-control'})

    class Meta:
        model = schedule_slot
        fields = ('date','timeIn','timeOut','vet') 
        TIME_CHOICES = (('08:30:00', '8:30 AM'),
                        ('09:00:00', '9:00 AM'),
                        ('09:30:00', '9:30 AM'),
                        ('10:00:00', '10:00 AM'),
                        ('10:30:00', '10:30 AM'),
                        ('11:00:00', '11:00 AM'),
                        ('11:30:00', '11:30 AM'),
                        ('12:00:00', '12:00 PM'),
                        ('12:30:00', '12:30 PM'),
                        ('13:00:00', '1:00 PM'),
                        ('13:30:00', '1:30 PM'),
                        ('14:00:00', '2:00 PM'),
                        ('14:30:00', '2:30 PM'),
                        ('15:00:00', '3:00 PM'),
                        ('15:30:00', '3:30 PM'),
                        ('16:00:00', '4:00 PM'),
                        ('16:30:00', '4:30 PM'),
                        ('17:00:00', '5:00 PM'),
                        ('17:30:00', '5:30 PM'), )
        widgets = {
        'timeIn':  forms.Select(choices=TIME_CHOICES),
        'timeOut': forms.Select(choices=TIME_CHOICES),

     }

class SchedulingForm(forms.ModelForm):

    class Meta:
        model = scheduling
        fields = ('pet', 'date', 'slot', 'reason')
        widgets = {
        'pet': forms.HiddenInput(),

     }
    date = forms.DateField(widget=DateInput)
    slot = forms.ModelChoiceField(queryset=schedule_slot.objects.filter(is_deleted=False,is_reserved=False))


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

       
        if 'date' in self.data:
            try:
                date_id = int(self.data.get('date'))
                self.fields['slot'].queryset = schedule_slot.objects.filter(date=date_id,is_deleted=False,is_reserved=False).order_by('date')
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty City queryset
        elif self.instance.pk:
            self.fields['slot'].queryset = self.instance.date.slot_set.order_by('date')
        
        self.fields["date"].widget.attrs.update(
            { 'class': 'form-control'})
        self.fields["slot"].widget.attrs.update(
            {  'class': 'form-control'})
        self.fields["reason"].widget.attrs.update(
            { 'class': 'form-control'})


class FilterForm(forms.Form):
    from_date = forms.DateField(widget=DateInput)
    to_date = forms.DateField(widget=DateInput)



class ExtraForm(forms.ModelForm):
    class Meta:
        widgets = {
            'product_name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.TextInput(attrs={'class': 'form-control'}),
            'product_type': forms.TextInput(attrs={'class': 'form-control'}),
            'price': forms.TextInput(attrs={'class': 'form-control'}),

        }

    def clean_email(self):
        if self.is_valid():
            email = self.cleaned_data['email']
            try:
                updateuser = User.objects.exclude(
                    pk=self.instance.pk).get(email=email)
            except User.DoesNotExist:
                return email
            raise forms.ValidationError(
                'Email "%s" is already in use.' % updateuser.username)

    def clean_username(self):
        if self.is_valid():
            username = self.cleaned_data['username']
            try:
                updateuser = User.objects.exclude(
                    pk=self.instance.pk).get(username=username)
            except User.DoesNotExist:
                return username
            raise forms.ValidationError(
                'Username "%s" is already in use.' % updateuser.email)

                
