"""
Definition of urls for audit_app.
"""

from datetime import datetime
from django.urls import path
from django.contrib import admin
from django.contrib.auth.views import LogoutView, LoginView
from app import forms, views


urlpatterns = [
    path('', views.home, name='home'),
    path('dashboard/',views.MainPageView.as_view(extra_context={'title':'Facility Information','year':datetime.now().year}),name = 'dashboard'),
    path('register/',views.RegisterView.as_view(),name = 'register'),
    path('entity/',views.CreateEntityDetails.as_view(extra_context={'title':'Add Entity Information','year':datetime.now().year}),name = 'entity'),
    path('scope/<int:id>/',views.ModalView.as_view(extra_context={'title':'Adudit Scope','year':datetime.now().year}), name = 'modal_view'),
    path('create-expense/<int:id>/',views.ExpenditureView.as_view(extra_context={'title':'Add Details','year':datetime.now().year}),name = 'create_expense'),
    path('expenses/<int:id>/',views.ExpenditureView.as_view(extra_context={'title':'Add Details','year':datetime.now().year}),name = 'expenses'),
    path('reports/<int:id>/',views.view_report,name = 'report'),
    path('login/',
         LoginView.as_view
         (
             template_name='app/login.html',
             authentication_form=forms.LoginForm,
             extra_context=
             {
                 'title': 'Log in',
                 'year' : datetime.now().year,
             }
         ),
         name='login'),
    path('load-districts/', views.load_districts, name='ajax_load_districts'),
    path('load-facilities/', views.load_facilities, name='ajax_load_facilities'),
    path('load-user_district/', views.load_user_district, name='ajax_user_district'),
    path('load-user_facility/', views.load_user_facility, name='ajax_user_facility'),
    path('load-expense-type/', views.load_types, name='ajax_expense_type'),
    path('logout/', LogoutView.as_view(next_page='/'), name='logout'),
    path('admin/', admin.site.urls),
]
