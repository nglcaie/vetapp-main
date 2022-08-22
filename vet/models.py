from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.core.validators import RegexValidator
from django.db.models.deletion import CASCADE, DO_NOTHING
from datetime import datetime
from django.utils import timezone
import os, random
from django.utils.html import mark_safe #para madisplay ng tama 'yung pic sa admin panel

# Create your models here.

class UserManager(BaseUserManager):
    def create_user(self,email, password=None):
        if not email:
            raise ValueError("Users must have an email address")

        user = self.model(
            email=self.normalize_email(email),
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self,email,password):
        """
        Creates and saves a superuser with the giv email, name and password.
        """
        user = self.create_user(
            email=self.normalize_email(email),
            password=password,
        )
        user.is_active = True
        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    email = models.EmailField(verbose_name="Email",max_length=60,unique=True)
    date_joined = models.DateTimeField(verbose_name='Date Joined',auto_now_add=True)
    last_login = models.DateTimeField(verbose_name="Last Login",null=True,blank=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_of_inactive = models.DateTimeField(verbose_name="Date of Inacitve",null=True,blank=True)
    is_used = models.BooleanField(default=False)
    is_secretary = models.BooleanField(default=False, verbose_name='Secretary')
    is_headveterinarian = models.BooleanField(default=False, verbose_name='Head Veterinarian')
    is_veterinarian = models.BooleanField(default=False, verbose_name='Veterinarian')
    is_petowner = models.BooleanField(default=False, verbose_name='Pet Owner')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return f"{self.email}"

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        """Does the user have permissions to view the app `app_label`?"""
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        """Is the user a member of staff?"""
        # Simplest possible answer: All admins are staff
        return self.is_admin

class Gender(models.Model):
    gender = models.CharField(max_length=50, verbose_name="Gender",unique=True,null=True, blank = True)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.gender}"


def image_path(instance, filename):
    basefilename, file_extension = os.path.splitext(filename)
    chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890'
    randomstr = ''.join((random.choice(chars)) for x in range(10))
    _now = datetime.now()

    return 'profile_pic/{year}-{month}-{image_id}-{basename}-{randomstring}-{ext}'.format(image_id = instance, 
    basename=basefilename, randomstring=randomstr, ext=file_extension, year=_now.strftime('%Y'), month=_now.strftime('%M'), day=_now.strftime('%d'))


class Profile(models.Model):
    # Contact Number format code
    phone_error_message = 'Contact number must be entered in format: 09XXXXXXXXX'
    phone_regex = RegexValidator(
        regex=r'^09\d{9}$',
        message=phone_error_message
    )
    useracc = models.ForeignKey(User, verbose_name='User Account',null=True, blank=True,on_delete=models.CASCADE,default=None)
    firstName = models.CharField(max_length=50,verbose_name="First Name")
    lastName = models.CharField(max_length=50,verbose_name="Last Name")
    gender = models.ForeignKey(Gender, verbose_name='Gender',null=True,blank=True,on_delete=models.CASCADE)
    contactNum = models.CharField(validators=[phone_regex], max_length=50,null=True, blank=True,verbose_name='Contact Number',default="")
    address = models.CharField(max_length=100, verbose_name='Address',null=True,blank=True,default="")
    is_deleted = models.BooleanField(default=False)
    date_of_delete = models.DateTimeField(verbose_name="Date of Delete",null=True,blank=True)

    user_image = models.ImageField(upload_to=image_path, default='profile_pic/image.jpg')

    def image_tag(self):
        return mark_safe('<img src="/media/%s" width="50" height="50" />'%(self.user_image))


    class Meta:
        verbose_name_plural = "Pet Owner Profile"

    def __str__(self):
        return f"{self.firstName} {self.lastName}"

class StaffProfile(models.Model):
    # Contact Number format code
    phone_error_message = 'Contact number must be entered in format: 09XXXXXXXXX'
    phone_regex = RegexValidator(
        regex=r'^09\d{9}$',
        message=phone_error_message
    )
    useracc = models.ForeignKey(User, verbose_name='User Account',null=True,blank=True,on_delete=models.CASCADE,default=None)
    firstName = models.CharField(max_length=50,verbose_name="First Name")
    lastName = models.CharField(max_length=50,verbose_name="Last Name")
    gender = models.ForeignKey(Gender, verbose_name='Gender',null=True,blank=True,on_delete=models.CASCADE)
    contactNum = models.CharField(validators=[phone_regex], max_length=50,null=True, blank=True,verbose_name='Contact Number',default="")
    address = models.CharField(max_length=100, verbose_name='Address',null=True,blank=True,default="")
    is_deleted = models.BooleanField(default=False)
    date_of_delete = models.DateTimeField(verbose_name="Date of Delete",null=True,blank=True)

    user_image = models.ImageField(upload_to=image_path, default='profile_pic/image.jpg')

    def image_tag(self):
        return mark_safe('<img src="/media/%s" width="50" height="50" />'%(self.user_image))


    class Meta:
        verbose_name_plural = "Staff Profile"

    def __str__(self):
        return f"{self.firstName} {self.lastName}"


class petspecies(models.Model):
    species = models.CharField(max_length=50, verbose_name="Species",unique=True,null=True, blank = False)
    is_deleted = models.BooleanField(default=False)
    date_of_delete = models.DateTimeField(verbose_name="Date of Delete",null=True,blank=True)

    class Meta:
        verbose_name_plural = "Pet Species"

    def __str__(self):
        return self.species
    

class breed(models.Model):
    kind = models.ForeignKey(petspecies, verbose_name='Species',null=True, blank = True,on_delete=models.CASCADE)
    breed = models.CharField(max_length=50, verbose_name="Species",unique=True,null=True, blank = False)
    is_deleted = models.BooleanField(default=False)
    date_of_delete = models.DateTimeField(verbose_name="Date of Delete",null=True,blank=True)

    class Meta:
        verbose_name_plural = "Breed"

    def __str__(self):
        return self.breed

def pet_image_path(instance, filename): #bago toh pet
    basefilename, file_extension = os.path.splitext(filename)
    chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890'
    randomstr = ''.join((random.choice(chars)) for x in range(10))
    _now = datetime.now()

    return 'pet_img/{year}-{month}-{image_id}-{basename}-{randomstring}-{ext}'.format(image_id = instance, 
    basename=basefilename, randomstring=randomstr, ext=file_extension, year=_now.strftime('%Y'), month=_now.strftime('%M'), day=_now.strftime('%d'))

class pets(models.Model):
    Gender_CHOICES = (
        ('Male', 'Male'),
        ('Female', 'Female'),
    )
    petOwner = models.ForeignKey(Profile, verbose_name='Pet Owner',null=True, blank = True,on_delete=models.CASCADE)
    petName = models.CharField(max_length=50, verbose_name="Pet Name",null=True, blank = True)
    dob = models.DateField(verbose_name="Date of Birth")
    sex = models.CharField(max_length=50, choices=Gender_CHOICES, verbose_name='Gender', null=True,blank=True)
    species = models.ForeignKey(petspecies, verbose_name='Species',null=True, blank = True,on_delete=models.CASCADE)
    description = models.ForeignKey(breed, verbose_name='Breed',null=True, blank = True,on_delete=models.CASCADE)
    colorMarking = models.CharField(max_length=50, verbose_name="Color Marking",null=True, blank = True)
    is_deleted = models.BooleanField(default=False)
    date_of_delete = models.DateTimeField(verbose_name="Date of Delete",null=True,blank=True)

    pet_image = models.ImageField(upload_to=pet_image_path, default='pet_img/pet_img.png') #bago toh pet

    def image_tag(self):
        return mark_safe('<img src="/media/%s" width="50" height="50" />'%(self.pet_image)) #bago toh pet


    class Meta:
        verbose_name_plural = "Pets"


    def __str__(self):
        return f"{self.petName} - {self.petOwner}"
    
class vaxType(models.Model):
    vaccineType = models.CharField(max_length=50, verbose_name="Vaccine Type",unique=True,null=True, blank = True)
    is_deleted = models.BooleanField(default=False)
    date_of_delete = models.DateTimeField(verbose_name="Date of Delete",null=True,blank=True)

    class Meta:
        verbose_name_plural = "Vaccine Type"

    def __str__(self):
        return self.vaccineType

class services(models.Model):
    serviceName = models.CharField(max_length=50, verbose_name="Service",unique=True,null=True, blank = True)
    description = models.CharField(max_length=50, verbose_name="Description",null=True, blank = True)
    is_labTest = models.BooleanField(default=False,verbose_name="Laboratory Test")
    is_vaccination = models.BooleanField(default=False,verbose_name="Vaccination")
    price = models.DecimalField(decimal_places=2,max_digits=20,default=0.00, verbose_name="Price")
    is_deleted = models.BooleanField(default=False)
    date_of_delete = models.DateTimeField(verbose_name="Date of Delete",null=True,blank=True)

    class Meta:
        verbose_name_plural = "Services"

    def __str__(self):
        return self.serviceName

class ProductType(models.Model):
    prodType = models.CharField(max_length=50, verbose_name="Vaccine Type",unique=True,null=True, blank = True)
    is_deleted = models.BooleanField(default=False)
    date_of_delete = models.DateTimeField(verbose_name="Date of Delete",null=True,blank=True)

    class Meta:
        verbose_name_plural = "Product Type"

    def __str__(self):
        return self.prodType


class ProductInfo(models.Model):
    product_name = models.CharField(max_length=200, verbose_name='Product Name')
    product_type = models.ForeignKey(ProductType, on_delete=models.CASCADE, related_name='products')
    description = models.CharField(max_length=200, verbose_name='Description')
    price = models.DecimalField(decimal_places=2,max_digits=20,default=0.00, verbose_name="Price")
    status = models.CharField(max_length=200, null=True,default="No stock")
    total_quantity = models.IntegerField(default='0', blank=False, null=True, verbose_name='Total Quantity')
    medium_margin = models.IntegerField(default='0', blank=False, null=True)
    low_margin = models.IntegerField(default='0', blank=False, null=True)
    is_deleted = models.BooleanField(default=False)
    date_of_delete = models.DateTimeField(verbose_name="Date of Delete",null=True,blank=True)

    
    def __str__(self):
        return self.product_name

class Product(models.Model):
    product = models.ForeignKey(ProductInfo, on_delete=models.CASCADE, related_name='products')
    manuDate = models.DateField(verbose_name='Manufacturing Date',null=True, blank = True)
    expireDate = models.DateField(verbose_name='Expiration Date',null=True, blank = True)
    quantity = models.IntegerField(default='0', blank=False, null=True)
    is_deleted = models.BooleanField(default=False)
    date_of_delete = models.DateTimeField(verbose_name="Date of Delete",null=True,blank=True)
    
    def __str__(self):
        return f"{self.product} - {self.quantity}"

class MedicalHistory(models.Model):
    code = models.CharField(max_length=200, null=True,blank=True, unique=True)
    pet = models.ForeignKey(pets, on_delete=models.CASCADE, related_name='pet')
    date = models.DateField(verbose_name='Medical Examination Date')
    weight = models.CharField(max_length=100, verbose_name="Weight",null=True, blank = True)
    symptoms = models.CharField(max_length=1000, verbose_name="Symptoms",null=True, blank = True)
    treatment = models.CharField(max_length=1000, verbose_name="Treatment",null=True, blank = True)
    prescription = models.CharField(max_length=1000, verbose_name="Prescription",null=True, blank = True)
    instruction = models.CharField(max_length=1000, verbose_name="Instruction",null=True, blank = True)
    dateofReturn = models.DateField(verbose_name='Date of return',null=True, blank = True)
    reason = models.CharField(max_length=1000, verbose_name="Reason for Return",null=True, blank = True)
    vet = models.ForeignKey(StaffProfile, on_delete=models.CASCADE, verbose_name="Veterinarian",null=True, blank = True)
    is_deleted = models.BooleanField(default=False)
    date_of_delete = models.DateTimeField(verbose_name="Date of Delete",null=True,blank=True)
    last_modified = models.DateTimeField(verbose_name="Last Modified",null=True,auto_now=True)
    
    class Meta:
        verbose_name_plural = "Medical History"

    def __str__(self):
        return f"{self.pet} - {self.date}"

class serviceHistory(models.Model):
    code = models.CharField(max_length=200, null=True,blank=True, unique=True)
    medHistory = models.ForeignKey(MedicalHistory, on_delete=models.CASCADE, verbose_name='Medical History')
    dateofService = models.DateField(verbose_name='Date of Service')
    service = models.ForeignKey(services, on_delete=models.CASCADE, related_name='Service')
    interpretation = models.CharField(max_length=1000, verbose_name="Remarks",null=True, blank = True)
    vet = models.ForeignKey(StaffProfile, on_delete=models.CASCADE, verbose_name="Veterinarian",null=True, blank = True)
    is_deleted = models.BooleanField(default=False)
    date_of_delete = models.DateTimeField(verbose_name="Date of Delete",null=True,blank=True)
    last_modified = models.DateTimeField(verbose_name="Last Modified",null=True,auto_now=True)

    class Meta:
        verbose_name_plural = "General Service"

    def __str__(self):
        return f"{self.medHistory.pet.petName} - {self.service}"

class labHistory(models.Model):
    code = models.CharField(max_length=200, null=True,blank=True, unique=True)
    medHistory = models.ForeignKey(MedicalHistory, on_delete=models.CASCADE, verbose_name='Medical History')
    dateofService = models.DateField(verbose_name='Date of Service')
    service = models.ForeignKey(services, on_delete=models.CASCADE, verbose_name='Service')
    dateofResult = models.DateField(verbose_name='Date of Result',null=True, blank = True)
    interpretation = models.CharField(max_length=1000, verbose_name="Remarks",null=True, blank = True)
    vet = models.ForeignKey(StaffProfile, on_delete=models.CASCADE, verbose_name="Veterinarian",null=True, blank = True)
    is_deleted = models.BooleanField(default=False)
    date_of_delete = models.DateTimeField(verbose_name="Date of Delete",null=True,blank=True)
    last_modified = models.DateTimeField(verbose_name="Last Modified",null=True,auto_now=True)

    class Meta:
        verbose_name_plural = "Laboratory History"

    def __str__(self):
        return f"{self.medHistory.pet.petName} - {self.service}"

class vaccineHistory(models.Model):
    code = models.CharField(max_length=200, null=True,blank=True, unique=True)
    medHistory = models.ForeignKey(MedicalHistory, on_delete=models.CASCADE, verbose_name='Medical History')
    dateofService = models.DateField(verbose_name='Date of Service')
    service = models.ForeignKey(services, on_delete=models.CASCADE, verbose_name='Service')
    vaccine = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Vaccine')
    interpretation = models.CharField(max_length=1000, verbose_name="Remarks",null=True, blank = True)
    dateofReturn = models.DateField(verbose_name='Date of Result',null=True, blank = True)
    reason = models.CharField(max_length=1000, verbose_name="Remarks",null=True, blank = True)
    vet = models.ForeignKey(StaffProfile, on_delete=models.CASCADE, verbose_name="Veterinarian",null=True, blank = True)
    is_deleted = models.BooleanField(default=False)
    date_of_delete = models.DateTimeField(verbose_name="Date of Delete",null=True,blank=True)
    last_modified = models.DateTimeField(verbose_name="Last Modified",null=True,auto_now=True)

    class Meta:
        verbose_name_plural = "Vaccination History"

    def __str__(self):
        return f"{self.medHistory.pet.petName} - {self.service}"

class chargeSlip(models.Model):
    code = models.CharField(max_length=200, null=True,blank=True, unique=True)
    petowner = models.ForeignKey(Profile, on_delete=models.CASCADE, verbose_name='Pet Owner',blank=True, null=True)
    date = models.DateField(verbose_name='Date Created',null=True,auto_now_add=True)
    totalAmount = models.DecimalField(decimal_places=2,max_digits=20,default=0.00, verbose_name="Total Amount")
    balance = models.DecimalField(decimal_places=2,max_digits=20,default=0.00, verbose_name="Balance")
    status = models.CharField(max_length=200, null=True,default="Unpaid")
    staff = models.ForeignKey(StaffProfile, on_delete=models.CASCADE, verbose_name='Staff',blank=True, null=True)
    is_deleted = models.BooleanField(default=False)
    date_of_delete = models.DateTimeField(verbose_name="Date of Delete",null=True,blank=True)
    last_modified = models.DateTimeField(verbose_name="Last Modified",null=True,auto_now=True)

    class Meta:
        verbose_name_plural = "Charge Slip Invoice"

    def __str__(self):
        return f"{self.petowner}-{self.id}"

class productInvoice(models.Model):
    chargeslip = models.ForeignKey(chargeSlip, on_delete=models.CASCADE, verbose_name='Charge Slip',blank=False, null=True)
    date = models.DateField(verbose_name='Date Created',null=True,auto_now_add=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Product')
    quantity = models.IntegerField(default='1', blank=False, null=True)
    total = models.DecimalField(decimal_places=2,max_digits=20,default=0.00, verbose_name="Amount")
    is_deleted = models.BooleanField(default=False)
    date_of_delete = models.DateTimeField(verbose_name="Date of Delete",null=True,blank=True)
    last_modified = models.DateTimeField(verbose_name="Last Modified",null=True,auto_now=True)

    class Meta:
        verbose_name_plural = "Product Invoice"

    def __str__(self):
        return f"{self.chargeslip} - {self.product}"

class serviceInvoice(models.Model):
    chargeslip = models.ForeignKey(chargeSlip, on_delete=models.CASCADE, verbose_name='Charge Slip')
    date = models.DateField(verbose_name='Date Created',null=True,auto_now_add=True)
    servicecode = models.CharField(max_length=200, null=True,blank=True)
    service = models.ForeignKey(services, on_delete=models.CASCADE, verbose_name='Service')
    total = models.DecimalField(decimal_places=2,max_digits=20,default=0.00, verbose_name="Amount")
    is_deleted = models.BooleanField(default=False)
    date_of_delete = models.DateTimeField(verbose_name="Date of Delete",null=True,blank=True)
    last_modified = models.DateTimeField(verbose_name="Last Modified",null=True,auto_now=True)

    class Meta:
        verbose_name_plural = "Service Invoice"

    def __str__(self):
        return f"{self.chargeslip} - {self.service}"

class transaction(models.Model):
    code = models.CharField(max_length=200, null=True,blank=True, unique=True)
    chargeslip = models.ForeignKey(chargeSlip, on_delete=models.CASCADE, verbose_name='Charge Slip')
    date = models.DateField(verbose_name='Date of Transaction',null=True,auto_now_add=True)
    grandTotal = models.DecimalField(decimal_places=2,max_digits=20,default=0.00, verbose_name="Total Amount")
    tenderedAmount = models.DecimalField(decimal_places=2,max_digits=20,default=0.00, verbose_name="Amount")
    changeAmount = models.DecimalField(decimal_places=2,max_digits=20,default=0.00, verbose_name="Change")
    staff = models.ForeignKey(StaffProfile, on_delete=models.CASCADE, verbose_name='Staff')
    is_deleted = models.BooleanField(default=False)
    date_of_delete = models.DateTimeField(verbose_name="Date of Delete",null=True,blank=True)
    last_modified = models.DateTimeField(verbose_name="Last Modified",null=True,auto_now=True)

    class Meta:
        verbose_name_plural = "Transaction"

    def __str__(self):
        return f"{self.chargeslip} - {self.date}"

    
class schedule_slot(models.Model):
    code = models.CharField(max_length=200, null=True,blank=True, unique=True)
    date = models.DateField(verbose_name='Date',blank=True,null=True)
    timeIn = models.TimeField(verbose_name='Start Time',blank=True,null=True)
    timeOut = models.TimeField(verbose_name='End Time',blank=True,null=True)
    vet = models.ForeignKey(StaffProfile, on_delete=models.CASCADE, verbose_name='Veterinarian',blank=True,null=True)
    is_reserved =  models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)
    date_of_delete = models.DateTimeField(verbose_name="Date of Delete",null=True,blank=True)

    class Meta:
        verbose_name_plural = "Schedule Slot"

    def __str__(self):
        return f" Dr. {self.vet} : {self.timeIn.strftime('%I:%M %p')} - {self.timeOut.strftime('%I:%M %p')}"

    
class scheduling(models.Model):
    code = models.CharField(max_length=200, null=True,blank=True, unique=True)
    date = models.DateField(verbose_name='Date',blank=True,null=True)
    pet = models.ForeignKey(pets, on_delete=models.CASCADE, verbose_name='Pet')
    slot = models.ForeignKey(schedule_slot, on_delete=models.CASCADE, verbose_name="Schedule")
    reason = models.CharField(max_length=200, null=True,blank=True)
    date_of_cancelled  = models.DateTimeField(verbose_name="Date of Delete",null=True,blank=True)
    status = models.CharField(max_length=200, null=True,blank=True,default="Reserved")
    is_deleted = models.BooleanField(default=False)
    date_of_delete = models.DateTimeField(verbose_name="Date of Delete",null=True,blank=True)
    class Meta:
        verbose_name_plural = "Scheduling"

    def __str__(self):
        return f"{self.slot}"


class flagsystem(models.Model):
    petOwner=models.ForeignKey(Profile, on_delete=models.CASCADE, verbose_name='Pet Owner')
    flagpoints = models.IntegerField(default='0', blank=False, null=True)
    is_restricted = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = "Restriction for Scheduling"

    def __str__(self):
        return f"{self.petOwner}"