from django.views.generic import *
from django.views import generic
from .models import *
from django.db.models import Q
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, reverse
from django.template.loader import get_template
from django.conf import settings
from django.urls import reverse
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.forms import AuthenticationForm
from django.core.mail import EmailMessage
from django.core.mail import send_mail, BadHeaderError
from django.core.paginator import Paginator
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_text
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from .forms import *
from django.views import View
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site
from django.http import HttpResponseRedirect

from django.http import JsonResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .tokens import user_tokenizer


class TeacherRequiredMixin(object):
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user.groups.filter(name="teacher").exists():
            pass
        else:
            return redirect('/login/')
        return super().dispatch(request, *args, **kwargs)

class StudentRequiredMixin(object):
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user.groups.filter(name="student").exists():
            pass
        else:
            return redirect("/login/")
        return super().dispatch(request, *args, **kwargs)


class HomeView(TemplateView):
    template_name = "clienttemplates/home.html"


class AboutusView(TemplateView):
    template_name = "clienttemplates/aboutus.html"


class ContactusView(TemplateView):
    template_name = "clienttemplates/contactus.html"


class LoginView(TemplateView):
    template_name = "clienttemplates/login.html"


class StudentLoginView(FormView):
    template_name = "clienttemplates/studentlogin.html"
    form_class = StudentLoginForm
    success_url = reverse_lazy("hometuitionapp:studenthome")

    # validating username and password by form_valid method using cleaned_data
    def form_valid(self, form):
        uname = form.cleaned_data["username"]
        pword = form.cleaned_data["password"]
        user = authenticate(username=uname, password=pword)
        print(user)
        if user is not None:
            login(self.request, user)
        else:
            return render(self.request, 'clienttemplates/studentlogin.html',
                          {
                              "error": "Invalid username or password", "form": form
                          })
        return super().form_valid(form)

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user.groups.filter(name="student").exists():
            return redirect('/student/home/')
        else:
            pass
        return super().dispatch(request, *args, **kwargs)


class StudentRegisterView(SuccessMessageMixin, CreateView):
    template_name = "clienttemplates/studentregister.html"
    form_class = StudentRegisterForm
    success_url = reverse_lazy("hometuitionapp:studentlogin")
    success_message ="A confirmation email has been sent to %(email)s. Please confirm to finish registering."  

    def form_valid(self, form):
        uname = form.cleaned_data['username']
        password = form.cleaned_data['password']
        email = form.cleaned_data['email']
        user1 = User.objects.create_user(username=uname,email=email,password=password,is_active=False)
        user = form.save(commit=False)
        form.instance.user = user1

        user.is_active = False
        user.save()
        # test_data = User.objects.get(id=user1.id).id
        # print("sjdbfisdjfsdkjfk",test_data)
        token = user_tokenizer.make_token(user1)
        print(user1.id)
        print("+++++++++++++++++++++",user)
        user_id = urlsafe_base64_encode(force_bytes(user1.id))
        url = 'http://localhost:8000' + reverse('hometuitionapp:confirm_email1', kwargs={'user_id': user_id, 'token': token})
        message = get_template('clienttemplates/register_email.html').render({
            'confirm_url': url
        })
        mail = EmailMessage('Email Confirmation', message, to=[user.email], from_email=settings.EMAIL_HOST_USER)
        mail.content_subtype = 'html'
        mail.send()
        return super().form_valid(form)
        

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user.groups.filter(name="student").exists():
            return redirect('/student/home/')
        else:
            pass
        return super().dispatch(request, *args, **kwargs)

class ConfirmRegistration1View(View):
    def get(self, request, user_id, token):
        user_id = force_text(urlsafe_base64_decode(user_id))
        print(user_id)
        user = User.objects.get(pk=user_id)
        print(user)

        if user is not None and user_tokenizer.check_token(user, token):
            user.is_active = True
            user.save()
            messages.success(request,('Your account have been confirmed.'))
            return redirect('hometuitionapp:studentlogin')
        else:
            messages.warning(request, ('The confirmation link was invalid, possibly because it has already been used.'))
            return redirect('hometuitionapp:studentlogin')

def password_reset_requestt(request):
    if request.method == "POST":
        password_reset_form = PasswordResetForm(request.POST)
        if password_reset_form.is_valid():
            data = password_reset_form.cleaned_data['email']
            associated_users = User.objects.filter(Q(email=data))
            if associated_users.exists():
                for user in associated_users:
                    subject = "Password Reset Requested"
                    email_template_name = "clienttemplates/password_reset_email.html"
                    c = {
                    "email":user.email,
                    'domain':'127.0.0.1:8000',
                    'site_name': 'Website',
                    "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                    "user": user,
                    'token': default_token_generator.make_token(user),
                    'protocol': 'http',
                    }
                    email = render_to_string(email_template_name, c)
                    try:
                        send_mail(subject, email, 'tuitionsystem07@gmail.com' , [user.email], fail_silently=False)
                    except BadHeaderError:
                        return HttpResponse('Invalid header found.')
                    messages.success(request, 'A message with reset password instructions has been sent to your inbox.')
                    return redirect ("hometuitionapp:studentlogin")
            messages.error(request, 'An invalid email has been entered.')
    password_reset_form = PasswordResetForm()
    return render(request=request, template_name="clienttemplates/password_reset.html", context={"password_reset_form":password_reset_form})
    


class TeacherLoginView(FormView):
    template_name = "clienttemplates/teacherlogin.html"
    form_class = TeacherLoginForm
    success_url = reverse_lazy("hometuitionapp:teacherhome")

    # validating username and password by form_valid method using cleaned_data

    def form_valid(self, form):
        uname = form.cleaned_data["username"]
        pword = form.cleaned_data["password"]
        user = authenticate(username=uname, password=pword)
        if user is not None:
            login(self.request, user)

        else:
            return render(self.request, 'clienttemplates/teacherlogin.html',
                        {
                            "error": "Invalid username or password", "form": form
                        })
        return super().form_valid(form)

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user.groups.filter(name="teacher").exists():
            return redirect('/teacher/home/')
        else:
            pass
        return super().dispatch(request, *args, **kwargs)

    


class TeacherRegisterView(SuccessMessageMixin, CreateView):
    template_name = "clienttemplates/teacherregister.html"
    form_class = TeacherRegisterForm
    success_url = reverse_lazy("hometuitionapp:teacherlogin")
    success_message =  "A confirmation email has been sent to %(email)s. Please confirm to finish registering." 

    def form_valid(self, form):
        uname = form.cleaned_data['username']
        password = form.cleaned_data['password']
        email = form.cleaned_data['email']
        user1 = User.objects.create_user(username=uname,email=email,password=password,is_active=False)
        user = form.save(commit=False)
        form.instance.user = user1

        user.is_active = False
        user.save()
        # test_data = User.objects.get(id=user1.id).id
        # print("sjdbfisdjfsdkjfk",test_data)
        token = user_tokenizer.make_token(user1)
        print(user1.id)
        print("+++++++++++++++++++++",user)
        user_id = urlsafe_base64_encode(force_bytes(user1.id))
        url = 'http://localhost:8000' + reverse('hometuitionapp:confirm_email', kwargs={'user_id': user_id, 'token': token})
        message = get_template('clienttemplates/register_email.html').render({
            'confirm_url': url
        })
        mail = EmailMessage('Email Confirmation', message, to=[user.email], from_email=settings.EMAIL_HOST_USER)
        mail.content_subtype = 'html'
        mail.send()
        return super().form_valid(form)

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user.groups.filter(name="teacher").exists():
            return redirect('/teacher/home/')
        else:
            pass
        return super().dispatch(request, *args, **kwargs)
        

class ConfirmRegistrationView(View):
    def get(self, request, user_id, token):
        user_id = force_text(urlsafe_base64_decode(user_id))
        print(user_id)
        user = User.objects.get(pk=user_id)
        print(user)
        if user is not None and user_tokenizer.check_token(user, token):
            user.is_active = True
            user.save()
            messages.success(request,('Your account have been confirmed.'))
            return redirect('hometuitionapp:teacherlogin')
        else:
            messages.warning(request, ('The confirmation link was invalid, possibly because it has already been used.'))
            return redirect('hometuitionapp:teacherlogin')
          

def password_reset_request(request):
    if request.method == "POST":
        password_reset_form = PasswordResetForm(request.POST)
        if password_reset_form.is_valid():
            data = password_reset_form.cleaned_data['email']
            associated_users = User.objects.filter(Q(email=data))
            if associated_users.exists():
                for user in associated_users:
                    subject = "Password Reset Requested"
                    email_template_name = "clienttemplates/password_reset_email.html"
                    c = {
                    "email":user.email,
                    'domain':'127.0.0.1:8000',
                    'site_name': 'Website',
                    "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                    "user": user,
                    'token': default_token_generator.make_token(user),
                    'protocol': 'http',
                    }
                    email = render_to_string(email_template_name, c)
                    try:
                        send_mail(subject, email, 'tuitionsystem07@gmail.com' , [user.email], fail_silently=False)
                    except BadHeaderError:
                        return HttpResponse('Invalid header found.')
                    messages.success(request, 'A message with reset password instructions has been sent to your inbox.')
                    return redirect ("hometuitionapp:teacherlogin")
            messages.error(request, 'An invalid email has been entered.')
    password_reset_form = PasswordResetForm()
    return render(request=request, template_name="clienttemplates/password_reset.html", context={"password_reset_form":password_reset_form})



class StudentHomeView(StudentRequiredMixin, ListView):
    template_name = "clienttemplates/studenthome.html"

    def get(self, request):
        qs = Teacher.objects.all()
        subject_query = request.GET.get('subject')
        location_query = request.GET.get('location')
        
        # if (subject_query != '' and location_query != '') and (subject_query is not None and location_query is not None):
        #     qset = qs.filter(Q(subject__name__icontains=subject_query), Q(address__icontains=location_query)).distinct()
        #     print(qset)
        #     if not qset:
        #         queryset = qs.order_by("-id")
        #         messages.error(request, "No results found.")          
        #         return render(request, "clienttemplates/studenthome.html", {
        #             'teacher_list' : queryset
        #         })  
        #     else:
        #         return render(request, "clienttemplates/studenthome.html", {
        #             'teacher_list' : qset
        #         })

        # elif subject_query != '' and subject_query is not None:
        #     qset = qs.filter(subject__name__icontains=subject_query) 
        #     if not qset:
        #         queryset = qs.order_by("-id")  
        #         messages.error(request, "No results found.")        
        #         return render(request, "clienttemplates/studenthome.html", {
        #             'teacher_list' : queryset
        #         })
        #     else:
        #         return render(request, "clienttemplates/studenthome.html", {
        #             'teacher_list' : qset
        #         })

        # elif location_query != '' and location_query is not None:
        #     qset = qs.filter(address__icontains=location_query)
        #     if not qset:
        #         queryset = qs.order_by("-id")
        #         messages.error(request, "No results found.")          
        #         return render(request, "clienttemplates/studenthome.html", {
        #             'teacher_list' : queryset
        #         })  
        #     else:
        #         return render(request, "clienttemplates/studenthome.html", {
        #             'teacher_list' : qset
        #         })

        # else:
        qset = qs.order_by("-id")
        paginator = Paginator(qset, 2)
        page_number = request.GET.get('page', 1)
        page = paginator.get_page(page_number)

        if page.has_next():
            next_url = f'?page={page.next_page_number()}'
        else:
            next_url = ''
        if page.has_previous():
            prev_url = f'?page={page.previous_page_number()}'
        else:
            prev_url = ''

        return render(request, "clienttemplates/studenthome.html", { 'teacher_list' : page, 'next_page_url' : next_url, 'prev_page_url' : prev_url
        })
      
class TeacherProfileView(StudentRequiredMixin,DetailView):
    template_name = "clienttemplates/teacherprofile.html"
    model = Teacher
    form_class = RatingForm
    context_object_name = "profile"
    
    def post(self, request, **kwargs):
        url = request.META.get('HTTP_REFERER') #GET last url
        form = self.form_class(request.POST)
        if form.is_valid():
            user_rate = form.cleaned_data['rate']
            teacher_id = self.kwargs["pk"]
            rated_teacher = Teacher.objects.get(id=teacher_id)
            current_user = request.user
            student_user = User.objects.get(id=current_user.id)

            obj, created = Rating.objects.update_or_create(
                teacher= rated_teacher.id, user =  current_user.id,
                defaults = { 'rate': user_rate,
                'teacher' : rated_teacher,
                'user' : student_user,
                },
            )
            print(obj)
            if(created):
                messages.success(request,"Your review has been sent")
            else:
                messages.success(request,"Your review has been updated")
            return HttpResponseRedirect(url)
        else:
            return render(self.request, url)

    
            
class TeacherHomeView(TeacherRequiredMixin,TemplateView):
    template_name = "clienttemplates/teacherhome.html"

    

class TeacherDetailView(TeacherRequiredMixin,DetailView):
    template_name = "clienttemplates/teacherdetail.html"
    model = Teacher
    form_class = RatingForm
    # context_object_name = "profile"
    context_object_name = "teacherdetail"

class TeacherDeleteView(TeacherRequiredMixin,DeleteView):
    template_name = "clienttemplates/teacherdelete.html"
    success_url = reverse_lazy("hometuitionapp:teacherregister")
    model = Teacher
    context_object_name = "teacherdetail"

class TeacherUpdateView(TeacherRequiredMixin,UpdateView):
    template_name = "clienttemplates/teacherupdate.html"
    form_class = TeacherUpdateForm
    success_url = reverse_lazy("hometuitionapp:teacherhome")
    model = Teacher

class StudentDetailView(StudentRequiredMixin,DetailView):
    template_name = "clienttemplates/studentdetail.html"
    model = Student
    context_object_name = "studentdetail"

class StudentDeleteView(StudentRequiredMixin,DeleteView):
    template_name = "clienttemplates/studentdelete.html"
    success_url = reverse_lazy("hometuitionapp:studentregister")
    model = Student
    context_object_name = "studentdetail"

class StudentUpdateView(StudentRequiredMixin, UpdateView):
    template_name = "clienttemplates/studentupdate.html"
    form_class = StudentUpdateForm
    success_url = reverse_lazy("hometuitionapp:studenthome")
    model = Student


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect("/login")


class TeacherNotificationCreateView(SuccessMessageMixin,StudentRequiredMixin, CreateView):
    template_name = "clienttemplates/teachernotificationcreate.html"
    form_class = TeacherNotification
    success_url = reverse_lazy("hometuitionapp:studenthome")
    # success_message = "You have sent a request to %(teacher)s"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        hires = Hiring.objects.all()
        return context

    def form_valid(self, form):
        teacher = form.cleaned_data['teacher']
        
        print(teacher,'\n 000000000000000000000000')
        return super().form_valid(form)

    # def post(self, request, **kwargs):
    #     url = request.META.get('HTTP_REFERER')
    #     form = self.form_class(request.POST)
    #     if form.is_valid:
    #         current_user = request.user
    #         # teacher_id = request.POST.get("teacher")

    #         student_user = Student.objects.get(user_id=current_user.id)

    #         obj, created = Hiring.objects.update_or_create(
    #             student = current_user.id,
    #             defaults = {
    #             'student': student_user

    #             },
    #         )
    #         print(obj)
    #         if(created):
    #             messages.success(request,"You have sent a request to %(teacher)s")
    #         else:
    #             messages.success(request,"Your request to %(teacher)s has been updated")
    #         return HttpResponseRedirect(url)
    #     else:
    #         return render(self.request, url)

    def post(self, request, *args, **kwargs):
        # teacher_id = request.POST.get("teacher_id")
        # print(teacher_id)
        print("asdfasdfasdfsadf")

        return JsonResponse({"message":"success"})


class AjaxTeacherHireView(View):
    def post(self, request, *args, **kwargs):
        teacher_id = request.POST.get("teacher_id")
        teacher = Teacher.objects.get(id=teacher_id)
        student = request.user.student
        if Hiring.objects.filter(teacher=teacher, student=request.user.student).exists():
            return JsonResponse({"message":"already"})
        else:
            Hiring.objects.create(teacher=teacher, student=request.user.student)
            return JsonResponse({"message":"success"})

# class AjaxStudentAcceptView(View):
#     def post(self, request, *args, **kwargs):

# class PaymentStatusView(CreateView):
#     template_name = "clienttemplates/payment.html"
#     form_class = PaymentForm
#     success_url = reverse_lazy("hometuitionapp:studenthome")

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         pay = Payment.objects.all()
#         return context


class PaymentStatusView(TemplateView):
    template_name = "clienttemplates/payment.html"

class StudentNotificationUpdateView(SuccessMessageMixin,TeacherRequiredMixin, UpdateView):
    template_name = "clienttemplates/studentnotificationcreate.html"
    form_class = TeacherNotification
    success_url = reverse_lazy("hometuitionapp:teacherhome")
    success_message = "You accepted the request of %(student)s"
    model = Hiring


class TeacherNotificationListView(TeacherRequiredMixin, ListView):
    template_name = "clienttemplates/teachernotificationlist.html"
    queryset = Hiring.objects.all()
    context_object_name = "teachernotificationlist"

class StudentNotificationListView(StudentRequiredMixin, ListView):
    template_name = "clienttemplates/studentnotificationlist.html"
    queryset = Hiring.objects.all()
    context_object_name = "studentnotificationlist"

class TeacherNotificationDetailView(TeacherRequiredMixin, DetailView):
    template_name = "clienttemplates/teachernotificationdetail.html"
    model = Hiring
    context_object_name = "teachernotificationdetail"


class AjaxHiringAcceptRequestView(View):
    def get(self, request, *args, **kwargs):
        obj = Hiring.objects.get(id=request.GET.get("hiring_id"))
        obj.accept = True
        obj.save()

        return JsonResponse({"message":"success"})

class AjaxHiringRejectRequestView(View):
    def get(self, request, *args, **kwargs):
        obj = Hiring.objects.get(id=request.GET.get("hiring_id"))
        obj.accept = False
        obj.save()

        return JsonResponse({"message":"success"})



class AdminRequiredMixin(object):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            return redirect("/adminlogin/")
        return super().dispatch(request, *args, **kwargs)


class AdminHomeView(AdminRequiredMixin, TemplateView):
    template_name = "admintemplates/adminhome.html"

    #to send multiple context in single view
    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['teacher_list'] = Teacher.objects.count()
        data['student_list'] = Student.objects.count()
        data['course_list'] = Course.objects.count()
        return data


class AdminLoginView(FormView):
    template_name = "admintemplates/adminlogin.html"
    form_class = AdminLoginForm
    success_url = reverse_lazy("hometuitionapp:adminhome")

    def form_valid(self, form):
        uname = form.cleaned_data["username"]
        pword = form.cleaned_data["password"]
        user = authenticate(username=uname, password=pword)
        if user is not None:
            login(self.request, user)
        else:
            return render(self.request, "admintemplates/adminlogin.html",
                          {
                              "error": "Invalid username or password", "form": form
                          })
        return super().form_valid(form)


class AdminHomeTuitionSystemDetailView(AdminRequiredMixin, DetailView):
    template_name = "admintemplates/adminsystemdetail.html"
    model = HomeTuitionSystem
    # this context_object_name is used to display data for eg{{systemdetail.name}} will display name of the system
    context_object_name = "systemdetail"


class AdminHomeTuitionSystemUpdateView(AdminRequiredMixin, UpdateView):
    template_name = "admintemplates/adminsystemupdate.html"
    form_class = HomeTuitionSystemForm
    success_url = reverse_lazy("hometuitionapp:adminhome")
    model = HomeTuitionSystem


class AdminCourseListView(AdminRequiredMixin, ListView):
    template_name = "admintemplates/admincourselist.html"
    queryset = Course.objects.all().order_by("-id")
    context_object_name = "courselist"

class AdminHireListView(AdminRequiredMixin, ListView):
    template_name = "admintemplates/adminhirelist.html"
    queryset = Hiring.objects.all().order_by("-id")
    context_object_name = "hirelist"


class AdminCourseCreateView(AdminRequiredMixin, CreateView):
    template_name = "admintemplates/admincoursecreate.html"
    form_class = CourseForm
    success_url = reverse_lazy("hometuitionapp:admincourselist")


class AdminCourseUpdateView(AdminRequiredMixin, UpdateView):
    template_name = "admintemplates/admincourseupdate.html"
    form_class = CourseForm
    success_url = reverse_lazy("hometuitionapp:admincourselist")
    model = Course


class AdminCourseDeleteView(AdminRequiredMixin, DeleteView):
    template_name = "admintemplates/admincoursedelete.html"
    success_url = reverse_lazy("hometuitionapp:admincourselist")
    model = Course


class AdminSubjectListView(AdminRequiredMixin, ListView):
    template_name = "admintemplates/adminsubjectlist.html"
    queryset = Subject.objects.all().order_by("-id")
    context_object_name = "subjectlist"


class AdminSubjectCreateView(AdminRequiredMixin, CreateView):
    template_name = "admintemplates/adminsubjectcreate.html"
    form_class = SubjectForm
    success_url = reverse_lazy("hometuitionapp:adminsubjectlist")


class AdminSubjectUpdateView(AdminRequiredMixin, UpdateView):
    template_name = "admintemplates/adminsubjectupdate.html"
    form_class = SubjectForm
    success_url = reverse_lazy("hometuitionapp:adminsubjectlist")
    model = Subject


class AdminSubjectDeleteView(AdminRequiredMixin, DeleteView):
    template_name = "admintemplates/adminsubjectdelete.html"
    success_url = reverse_lazy("hometuitionapp:adminsubjectlist")
    model = Subject


class AdminStudentListView(AdminRequiredMixin, ListView):
    template_name = "admintemplates/adminstudentlist.html"
    queryset = Student.objects.all().order_by("-id")
    context_object_name = "studentlist"


class AdminStudentDetailView(AdminRequiredMixin, DetailView):
    template_name = "admintemplates/adminstudentdetail.html"
    model = Student
    context_object_name = "studentdetail"


class AdminStudentUpdateView(AdminRequiredMixin, UpdateView):
    template_name = "admintemplates/adminstudentupdate.html"
    form_class = StudentRegisterForm
    success_url = reverse_lazy("hometuitionapp:adminstudentlist")
    model = Student


class AdminStudentDeleteView(AdminRequiredMixin, DeleteView):
    template_name = "admintemplates/adminstudentdelete.html"
    success_url = reverse_lazy("hometuitionapp:adminstudentlist")
    model = Student


class AdminTeacherListView(AdminRequiredMixin, ListView):
    template_name = "admintemplates/adminteacherlist.html"
    queryset = Teacher.objects.all().order_by("-id")
    context_object_name = "teacherlist"


class AdminTeacherUpdateView(AdminRequiredMixin, UpdateView):
    template_name = "admintemplates/adminteacherupdate.html"
    form_class = TeacherRegisterForm
    success_url = reverse_lazy("hometuitionapp:adminteacherlist")
    model = Teacher


class AdminTeacherDeleteView(DeleteView):
    template_name = "admintemplates/adminteacherdelete.html"
    success_url = reverse_lazy("hometuitionapp:adminteacherlist")
    model = Teacher

class AdminTeacherDetailView(AdminRequiredMixin, DetailView):
    template_name = "admintemplates/adminteacherdetail.html"
    model = Teacher
    context_object_name = "teacherdetail"

class AdminAjaxTeacherSearchView(View):
    def get(self, request, *args, **kwargs):
        subject = self.request.GET.get("subject")
        location = self.request.GET.get("location")
        print(subject, location, '\n +++++++++++++++++++++++')
        if subject != "" and location != "":
            # teacherlist = Teacher.objects.all()
            # listobj = teacherlist.filter(subject__a=subject)
            teacherlist = Teacher.objects.filter(Q(subject__name__icontains=subject) |
            Q(address__icontains=location)
            )
            # teacher = Teacher.objects.filter(subject=subject)
            print("sdafdsf")
            print(teacherlist)

        elif subject != "" and location == "":
            teacherlist = Teacher.objects.filter(Q(subject__name__icontains=subject))
            print(subject)
            print(teacherlist)
        
        elif location != "" and subject == "" :
            teacherlist = Teacher.objects.filter(Q(address__icontains=location))
            print(location)
            print(teacherlist)
        else:
            teacherlist = Teacher.objects.all()
            # print("Else +++++++++++++++++")
            # teacherlist = []


        page = self.request.GET.get("page", 1)
        paginator = Paginator(teacherlist, 1)
        try:
            results = paginator.page(page)
        except PageNotAnInteger:
            results = paginator.page(1)
        except EmptyPage:
            results = paginator.page(paginator.num_pages)
        print(results, "\n page ++++++++++++++++++++++++++")



        # page = self.request.GET.get('page', 1)
        # paginator = Paginator(teacherlist, 1)

        # results = paginator.get_page(1)


        # try:
        #     results = paginator.page(page)
        # except PageNotAnInteger:
        #     results = paginator.page(1)
        # except EmptyPage:
        #     results = paginator.page(paginator.num_pages)

        return render(self.request, 'clienttemplates/ajaxteachersearch.html', {
            'teacherlist': results, 'subject': subject, 'location': location
        })

        # return JsonResponse({"message": "success"})
        
class AdminLogoutView(View):
    def get(self, request):
        logout(request)
        return redirect("/adminlogin/")
    
