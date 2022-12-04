from django.urls import path

from .views import *

urlpatterns = [
    path("",index,name='index'),
    path("departments/<int:id>",dept_detail,name='detail'),
    path("departments/inverst/<int:id>",inverst,name='inverst'),

    path("pay/<int:id>",pay_inverst,name='pay'),

    path("departments/dashboard/",dashboard,name='dash'),
    path("bond/<int:id>",gen_bond,name='bond'),

    path("accounts/login/",login_user,name='login'),
    path("accounts/register/",register_profile,name='register'),
    path("accounts/logout/",logout_inverst,name='logout'),

    

]