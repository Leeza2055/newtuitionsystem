from django import forms
from django.contrib.auth.models import User
from .models import *


class StudentLoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={
         "class": "form-control",

    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        "class": "form-control",

    }))


class StudentRegisterForm(forms.ModelForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        "class": "form-control",

    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        "class": "form-control",

    }))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={
        "class": "form-control",

    }))
    email = forms.CharField(widget=forms.TextInput(attrs={
        "class": "form-control",

    }))
    name = forms.CharField(widget=forms.TextInput(attrs={
        "class": "form-control",

    }))
    phone_no = forms.CharField(widget=forms.TextInput(attrs={
        "class": "form-control",

    }))
    address = forms.CharField(widget=forms.TextInput(attrs={
        "class": "form-control",

    }))

    class Meta:
        model = Student
        fields = ['username', 'email', 'password', 'confirm_password', 'name',
                  'phone_no', 'address', 'report_card', 'course', 'subject']

    def clean_username(self):
        uname = self.cleaned_data["username"]
        if User.objects.filter(username=uname).exists():
            raise forms.ValidationError(
                "User with this user name already exists")
        return uname

    def clean_confirm_password(self):
        password = self.cleaned_data["password"]
        c_pword = self.cleaned_data["confirm_password"]
        if password != c_pword:
            raise forms.ValidationError("Password did not match")
        return c_pword

    def clean_email(self):
        email = self.cleaned_data["email"]
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError(
                "Email with this email address already exists"
            )
        return email


class TeacherLoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={
        "class": "form-control",

    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        "class": "form-control",

    }))


class TeacherRegisterForm(forms.ModelForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        "class": "form-control",

    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        
        "class": "form-control",
    }))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={
        "class": "form-control",

    }))
    email = forms.CharField(widget=forms.TextInput(attrs={
        "class": "form-control",

    }))
    name = forms.CharField(widget=forms.TextInput(attrs={
        "class": "form-control",

    }))
    address = forms.CharField(widget=forms.TextInput(attrs={
        "class": "form-control",

    }))
    phone_no = forms.CharField(widget=forms.TextInput(attrs={
        "class": "form-control",

    }))
    education = forms.CharField(widget=forms.TextInput(attrs={
        "class": "form-control",

    }))
    can_teach_location = forms.CharField(widget=forms.Textarea(attrs={
        "class": "form-control",

    }))

    teaching_experience = forms.CharField(widget=forms.Textarea(attrs={
        'class': 'form-control',
    }))

    monthly_fee = forms.CharField(widget=forms.NumberInput(attrs={
        "class": "form-control",

    }))

    availabilty = forms.CharField(widget=forms.Textarea(attrs={
        "class": "form-control",

    }))


    class Meta:
        model = Teacher
        fields = ['username', 'email', 'password', 'confirm_password', 'name', 'gender', 'photo',
                  'phone_no', 'address', 'education', 'cv', 'citizenship', 'course', 'subject',
                  'can_teach_location','teaching_experience','monthly_fee',
                  'training_license','availabilty','reference_person','reference_person_contact_no',]

    def clean_username(self):
        uname = self.cleaned_data["username"]
        if User.objects.filter(username=uname).exists():
            raise forms.ValidationError(
                "User with this user name already exists")
        return uname

    def clean_confirm_password(self):
        password = self.cleaned_data["password"]
        c_pword = self.cleaned_data["confirm_password"]
        if password != c_pword:
            raise forms.ValidationError("Password did not match")
        return c_pword
    
    def clean_email(self):
        email = self.cleaned_data["email"]
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError(
                "Email with this email address already exists"
            )
        return email


class TeacherUpdateForm(forms.ModelForm):
    email = forms.CharField(widget=forms.TextInput(attrs={
        "class": "form-control",

    }))
    name = forms.CharField(widget=forms.TextInput(attrs={
        "class": "form-control",

    }))
    address = forms.CharField(widget=forms.TextInput(attrs={
        "class": "form-control",

    }))
    phone_no = forms.CharField(widget=forms.TextInput(attrs={
        "class": "form-control",

    }))
    education = forms.CharField(widget=forms.TextInput(attrs={
        "class": "form-control",

    }))
   

    class Meta:
        model = Teacher
        fields = ['email','name', 'gender', 'photo',
                  'phone_no', 'address', 'education', 'cv', 'citizenship', 'course', 'subject']

class StudentUpdateForm(forms.ModelForm):
    email = forms.CharField(widget=forms.TextInput(attrs={
        "class": "form-control",

    }))
    name = forms.CharField(widget=forms.TextInput(attrs={
        "class": "form-control",

    }))
    phone_no = forms.CharField(widget=forms.TextInput(attrs={
        "class": "form-control",

    }))
    address = forms.CharField(widget=forms.TextInput(attrs={
        "class": "form-control",

    }))

    class Meta:
        model = Student
        fields = ['email', 'name','phone_no', 'address', 'report_card', 'course', 'subject']

class RatingForm(forms.ModelForm):
    class Meta:
        model = Rating
        fields = ['rate']


class HomeTuitionSystemForm(forms.ModelForm):
    class Meta:
        model = HomeTuitionSystem
        fields = "__all__"


class AdminLoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={
        "placeholder": "Enter your username...",
        "class": "form-control"

    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        "placeholder": "Enter password...",
        "class": "form-control",

    }))


class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = "__all__"


class SubjectForm(forms.ModelForm):
    class Meta:
        model = Subject
        fields = "__all__"


class TeacherNotification(forms.ModelForm):
    class Meta:
        model = Hiring
        fields = ['teacher','student','accept']

# class PaymentForm(forms.ModelForm):
#     class Meta:
#         model = Payment
#         fields = "__all__"
    


        