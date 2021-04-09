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
    phone_no = forms.IntegerField(widget=forms.NumberInput(attrs={
        "class": "form-control",

    }))
    address = forms.CharField(widget=forms.TextInput(attrs={
        "class": "form-control",

    }))
    salary = forms.IntegerField(widget=forms.NumberInput(attrs={
        "class": "form-control",
        "placeholder": "In Rs. Per Month(Price Range e.g Rs.2000-Rs.3000)"
    }))
    time = forms.CharField(widget=forms.Textarea(attrs={
        'class': 'form-control',
        "placeholder": "Eg. 5pm-7pm"
    }))
    


    class Meta:
        model = Student
        fields = ['username', 'email', 'password', 'confirm_password', 'name',
                  'phone_no', 'address', 'report_card', "tuition_type", "salary", "time"]

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
    phone_no = forms.IntegerField(widget=forms.NumberInput(attrs={
        "class": "form-control",

    }))
    can_teach_location = forms.CharField(widget=forms.Textarea(attrs={
        "class": "form-control",
        "placeholder": "Eg: Baneshwor, Gwarko"

    }))

    teaching_experience = forms.CharField(widget=forms.Textarea(attrs={
        'class': 'form-control',
        "placeholder": "Experience in years and other details..."

    }))
    availabilty = forms.CharField(widget=forms.Textarea(attrs={
        "class": "form-control",
        "placeholder": "Eg: 5pm-7pm"

    }))
    reference_person = forms.CharField(widget=forms.TextInput(attrs={
        "class": "form-control",
    }))
    reference_person_contact_no = forms.CharField(widget=forms.NumberInput(attrs={
        'class': "form-control",
    }))


    class Meta:
        model = Teacher
        fields = ['username', 'email', 'password', 'confirm_password', 'name', 'gender', 'photo',
                  'phone_no', 'address', 'education', 'cv', 'citizenship',
                  'can_teach_location','teaching_experience',
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
    phone_no = forms.IntegerField(widget=forms.NumberInput(attrs={
        "class": "form-control",

    }))
    
    can_teach_location = forms.CharField(widget=forms.Textarea(attrs={
        "class": "form-control",

    }))

    teaching_experience = forms.CharField(widget=forms.Textarea(attrs={
        'class': 'form-control',
    }))
    
    availabilty = forms.CharField(widget=forms.Textarea(attrs={
        "class": "form-control",

    }))
    reference_person = forms.CharField(widget=forms.TextInput(attrs={
        "class": "form-control",
    }))
    reference_person_contact_no = forms.CharField(widget=forms.NumberInput(attrs={
        'class': "form-control",
    }))


    class Meta:
        model = Teacher
        fields = ['name', 'photo','email','phone_no', 'address', 'education', 'cv', 'citizenship',
                  'can_teach_location','teaching_experience',
                  'training_license','availabilty','reference_person','reference_person_contact_no',]
   

    
class StudentUpdateForm(forms.ModelForm):
    email = forms.CharField(widget=forms.TextInput(attrs={
        "class": "form-control",

    }))
    name = forms.CharField(widget=forms.TextInput(attrs={
        "class": "form-control",

    }))
    phone_no = forms.IntegerField(widget=forms.NumberInput(attrs={
        "class": "form-control",

    }))
    address = forms.CharField(widget=forms.TextInput(attrs={
        "class": "form-control",

    }))
    tuition_type = forms.ChoiceField(choices=Tuition_type, widget=forms.Select(attrs={
        "class": "form-control",
    }))
    salary = forms.IntegerField(widget=forms.NumberInput(attrs={
        "class": "form-control",
    }))
    report_card = forms.FileField(widget=forms.FileInput(attrs={
        'class': 'form-control',
       
    }))
    time = forms.CharField(widget=forms.Textarea(attrs={
        'class': 'form-control',
    }))
    


    class Meta:
        model = Student
        fields = ['email','name',
                  'phone_no', 'address', 'report_card', "tuition_type", "salary", "time"]

class RatingForm(forms.ModelForm):
    class Meta:
        model = Rating
        fields = ['rate', 'comment']


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
    
class TeacherSubjectFee(forms.ModelForm):
    class Meta:
        model = SubjectFee
        fields = "__all__"


class SliderForm(forms.ModelForm):
    class Meta:
        model = Slider
        fields = ['title', 'content', 'image','status']


class TicketRaiseForm(forms.ModelForm):
    class Meta:
        model = TicketRaise
        fields = [ 'issue_type', 'issue']
        widgets = {
       
        'issue_type': forms.Select(attrs={
            'class': 'form-control', 
            'placeholder': 'Issue Type',
            }),
        'issue': forms.Textarea(attrs={
            'class': 'form-control', 
            'placeholder': 'Describe Your Issue',
            })
        }

class TicketRaiseRemarkForm(forms.ModelForm):
    class Meta:
        model = TicketRaiseRemark
        fields = ['issue_remark']
        widgets = {
        'issue_remark': forms.Textarea(attrs={
            'class': 'input-msg-send form-control',
            'placeholder': 'Enter Message',
            'rows': 3,
            }),
        }
