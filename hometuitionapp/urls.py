from django.urls import path
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls import url
from .views import *
from . import views
from .tokens import user_tokenizer

app_name = 'hometuitionapp'
urlpatterns = [
    # client side
    path('', HomeView.as_view(), name="home"),
    path("aboutus/", AboutusView.as_view(), name="aboutus"),
    path("contactus/", ContactusView.as_view(), name="contactus"),
    path('login/', LoginView.as_view(), name="login"),
    path('student/login/', StudentLoginView.as_view(), name="studentlogin"),
    path('student/register/', StudentRegisterView.as_view(), name="studentregister"),
    path('teacher/login/', TeacherLoginView.as_view(), name="teacherlogin"),
    path('teacher/register/',TeacherRegisterView.as_view(),
         name="teacherregister"),
    path('confirm-email/<str:user_id>/<str:token>/',
         views.ConfirmRegistrationView.as_view(), name='confirm_email'),
    path('confirm-email1/<str:user_id>/<str:token>/',
         views.ConfirmRegistration1View.as_view(), name='confirm_email1'),
    path('teacher/home/', TeacherHomeView.as_view(), name="teacherhome"),
    path('student/home/', StudentHomeView.as_view(), name="studenthome"),
    path('password_reset',views.password_reset_request, name="password_reset"),
    path('password_resett',views.password_reset_requestt, name="password_resett"),
    path('teacher/<int:pk>/profile/',
         TeacherProfileView.as_view(), name="teacherprofile"),
    path('teacher/<int:pk>/detail/',
         TeacherDetailView.as_view(), name="teacherdetail"),
    path('teacher/<int:pk>/update/',
         TeacherUpdateView.as_view(), name="teacherupdate"),
    path('teacher/<int:pk>/delete/',
         TeacherDeleteView.as_view(), name="teacherdelete"),
    path('student/<int:pk>/detail/',
         StudentDetailView.as_view(), name="studentdetail"),
    path('student/<int:pk>/update/',
         StudentUpdateView.as_view(), name="studentupdate"),
    path('student/<int:pk>/delete/',
         StudentDeleteView.as_view(), name="studentdelete"),
    path('logout/', LogoutView.as_view(), name="logout"),
    path('teacher/notification/create/', TeacherNotificationCreateView.as_view(), name="teachernotificationcreate"),
    path('teacher/hire/', AjaxTeacherHireView.as_view(), name="ajaxhireteacher"),
    # path('student/accept/', AjaxStudentAcceptView.as_view(), name="ajaxstudentaccept"),
    path('student/<int:pk>notification/update/', StudentNotificationUpdateView.as_view(), name="studentnotificationupdate"),
    path('teacher/notification/list/', TeacherNotificationListView.as_view(), name="teachernotificationlist"),
    path('student/notification/list/', StudentNotificationListView.as_view(), name="studentnotificationlist"),
    path('teacher/notification/<int:pk>/detail/',
         TeacherNotificationDetailView.as_view(), name="teachernotificationdetail"),
    path("ajax/hiring/accept/request/", AjaxHiringAcceptRequestView.as_view(), name="ajaxacceptrequest"),
    path("ajax/hiring/reject/request", AjaxHiringRejectRequestView.as_view(), name="ajaxrejectrequest"),
    path('payment/status/', PaymentStatusView.as_view(), name="paymentstatus"),


    # admin side
    path('system_admin/', AdminHomeView.as_view(), name="adminhome"),
    path('adminlogin/', AdminLoginView.as_view(), name="adminlogin"),
    path('system_admin/hometuitionsystem/<int:pk>/detail/',
         AdminHomeTuitionSystemDetailView.as_view(), name="adminsystemdetail"),
    path('system_admin/hometuitionsystem/<int:pk>/update/',
         AdminHomeTuitionSystemUpdateView.as_view(), name="adminsystemupdate"),
    path('system_admin/course/list/',
         AdminCourseListView.as_view(), name="admincourselist"),
    path('system_admin/course/create/',
         AdminCourseCreateView.as_view(), name="admincoursecreate"),
    path('system_admin/course/<int:pk>/update/',
         AdminCourseUpdateView.as_view(), name="admincourseupdate"),
    path('system_admin/course/<int:pk>/delete/',
         AdminCourseDeleteView.as_view(), name="admincoursedelete"),
    path('system_admin/subject/list/',
         AdminSubjectListView.as_view(), name="adminsubjectlist"),
    path('system_admin/hire/list/',
         AdminHireListView.as_view(), name="adminhirelist"),
    path('system_admin/subject/create/',
         AdminSubjectCreateView.as_view(), name="adminsubjectcreate"),
    path('system_admin/subject/<int:pk>/update/',
         AdminSubjectUpdateView.as_view(), name="adminsubjectupdate"),
    path('system_admin/subject/<int:pk>/delete/',
         AdminSubjectDeleteView.as_view(), name="adminsubjectdelete"),
    path('system_admin/student/list/',
         AdminStudentListView.as_view(), name="adminstudentlist"),

    path('system_admin/student/<int:pk>/detail/',
         AdminStudentDetailView.as_view(), name="adminstudentdetail"),

    path('system_admin/student/<int:pk>/update/',
         AdminStudentUpdateView.as_view(), name="adminstudentupdate"),
    path('system_admin/student/<int:pk>/delete/',
         AdminStudentDeleteView.as_view(), name="adminstudentdelete"),
    path('system_admin/teacher/list/',
         AdminTeacherListView.as_view(), name="adminteacherlist"),

    path('system_admin/teacher/<int:pk>/detail/',
         AdminTeacherDetailView.as_view(), name="adminteacherdetail"),

    path('system_admin/teacher/<int:pk>/update',
         AdminTeacherUpdateView.as_view(), name="adminteacherupdate"),
    path('system_admin/teacher/<int:pk>delete',
         AdminTeacherDeleteView.as_view(), name="adminteacherdelete"),

     path('system_admin/ajax/search/', 
     AdminAjaxTeacherSearchView.as_view(), name='adminajaxteachersearch'),
    path('adminlogout/', AdminLogoutView.as_view(), name="adminlogout"),

]
