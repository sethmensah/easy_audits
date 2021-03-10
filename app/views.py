"""
Definition of views.
"""

from datetime import datetime
from django.conf import settings
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.shortcuts import render,redirect,reverse, HttpResponse, get_object_or_404
from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text
from django.template.loader import render_to_string
from django.http import HttpRequest, HttpResponseRedirect, JsonResponse
from django.views.generic.edit import CreateView, View, UpdateView, FormView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.urls import reverse_lazy
from django.core.mail import EmailMessage, send_mail
from django.db import transaction
from django.forms.models import construct_instance
from app.models import  District, Facility, Region, ExpensesCategory, ExpensesType, CustomUser, EntityDetails, Expenditure, \
    AuditorDetails, ManagementDetails, AuditScope
from app.forms import  CustomUserCreationForm, EntityDetailsForm, ExpensesForm, ExpensesFormSet, LoginForm, AuditorDetailsFormSet, \
    ManagementDetailsFormSet, AuditScopeForm
from formtools.wizard.views import SessionWizardView
from django.contrib.auth.decorators import login_required
from django.db.models import Sum

from app.helpers import  observations, recommend



def home(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/cover.html',
        {
            'title':'Cover Page',
            'year':datetime.now().year,
        }
    )


class MainPageView(ListView,FormView):
    """Renders the dashboard page."""
    template_name = 'app/dashboard.html'
    model = EntityDetails
    form_class = AuditScopeForm

    def get_context_data(self, **kwargs):
        context = super(MainPageView,self).get_context_data(**kwargs)
        context['entity'] = EntityDetails.objects.filter(created_by = self.request.user)
        context['scope'] = AuditScope.objects.order_by('review_date')
        #context['scope'] = AuditScope.objects.select_related('auditee_name').order_by('review_date')
        context["form"] = self.form_class
        return context
  

class RegisterView(CreateView):

    def get(self,request):
        return render(request,'app/register.html',{'year':datetime.now().year,'title':'User Registration','form':CustomUserCreationForm()})

    def post(self,request):
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('login'))
        return render(request,'app/register.html',
                      {'form':form,
                       'title':'User Registration',
                        'year':datetime.now().year,
                       })

class CreateEntityDetails(CreateView):
    model = EntityDetails
    #login_url = '/login/'
    template_name = 'app/create_entity.html'
    form_class = EntityDetailsForm
    success_url = reverse_lazy('dashboard')

    def get_success_url(self):
        return super().get_success_url()

    def get(self,request,*args,**kwargs):
        self.object = None
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        management = ManagementDetailsFormSet()
        auditor = AuditorDetailsFormSet()
        return self.render_to_response(
            self.get_context_data(form=form,
                                  management=management,
                                  auditor=auditor,
                                  ))
    def post(self,request,*args,**kwargs):
        self.object = None
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        management = ManagementDetailsFormSet(self.request.POST)
        auditor = AuditorDetailsFormSet(self.request.POST)
        if (form.is_valid() and management.is_valid() and auditor.is_valid()):
            return self.form_valid(form, management, auditor,)
        else:
            return self.form_invalid(form, management, auditor,)

    def form_invalid(self, form, management, auditor):
        return self.render_to_response(
            self.get_context_data(form=form,
                                  management=management,
                                  auditor=auditor,
                                  ))

    def form_valid(self, form, management, auditor):
        form.instance.created_by = self.request.user
        self.object = form.save()
        management.instance = self.object
        management.save()
        auditor.instance = self.object
        auditor.save()
        return HttpResponseRedirect(self.get_success_url())


    
class ExpenditureView(CreateView):
    model = Expenditure
    form_class = ExpensesForm
    template_name = "app/expenses.html"

    def get(self,request,id):
        key = self.kwargs['id']
        data = AuditScope.objects.get(id = key)
        form = super(ExpenditureView,self).get_form()
        return render(request,self.template_name,
                      {'year':datetime.now().year,
                       'title':'Expenditure Audit',
                       'form':form,
                       'data':data,
                       })

    def post(self,request,id):
        data = AuditScope.objects.get(id = self.kwargs['id'])
        form = ExpensesForm(request.POST)
        if form.is_valid():
            f = form.save(commit = False)
            f.scope_covered = data
            f.save()
            f.remarks.set(form.cleaned_data.get('remarks'))
            form.save_m2m()
            return redirect("/create-expense/{}/".format(id))
        self.object = None
        return self.form_invalid(form)



class ModalView(FormView):
    def get(self,request,id):
        data = EntityDetails.objects.get(id = id)
        #dt = AuditScope.objects.get(auditee_name = data.id)
        return render(request,'app/audit_scope.html',{'title':'Adudit Scope','form':AuditScopeForm(),'data':data,})

    def post(self,request,id):
        #key = self.kwargs['id']
        data = EntityDetails.objects.get(id = id)
        form = AuditScopeForm(request.POST)
        if form.is_valid():
            form = form.save(commit = False)
            form.auditee_name = data
            form.save()
            return redirect("/expenses/{}/".format(id))
        return render(request,'app/audit_scope.html',
                      {'title':'Adudit Scope','form':form,'data':data})
   

#arr = set([datetime.strftime(d.expense_date,'%Y') for d in Expenditure.objects.all()]) 
#data = Expenditure.objects.all().values('category').annotate(Sum('amount'))
def category_chart(request):
    try:
        labels = []
        data = []
        exp_data = []
        exp_labels = []

        queryset = Expenditure.objects.values('category__category_name').annotate(total = Sum('amount')).order_by('category__category_name')
        query = Expenditure.objects.values('expense_type__type_name').annotate(total_exp = Sum('amount')).order_by('expense_type__type_name')
        for ent in queryset:
            labels.append(ent['category__category_name'])
            data.append(float(ent['total']))
        for item in query:
            exp_labels.append(item['expense_type__type_name'])
            exp_data.append(float(item['total_exp']))
        return render(request,'app/reports.html',{
                    'title':'User Registration',
                    'year':datetime.now().year,
                    'data':data,
                    'labels':labels,
                    'exp_data':exp_data,
                    'exp_labels':exp_labels,
                    })
    except Exception as err:
        print(err)

def view_report(request,id):
    data = EntityDetails.objects.get(pk =id)
    entry = data.managementdetails.all()
    expense = Expenditure.objects.all()
    info = observations(Expenditure)
    name = str(data.facility_name).title()
    scope = Expenditure.get_scope
    context = {
        'data':data,
        'entry':entry,
        'title':'Report',
        'expense': expense,
        'info':info,
        'recommendation': recommend(name),
        'scope':scope,
        }
    return render(request,'app/reports/report.html',context)




def load_types(request):
    type_id = int(request.GET.get('category'))
    ty = ExpensesType.objects.filter(category_id = type_id)
    return render(request,'app/expenses_dropdown.html',{'ty':ty})

def load_districts(request):
    reg_id = request.GET.get('region')
    districts = District.objects.filter(region_id = reg_id).order_by('district_name')
    return render(request,'app/districts_dropdown.html',{'districts':districts})

def load_facilities(request):
    dist_id = request.GET.get('district')
    facilities = Facility.objects.filter(district_id = dist_id).order_by('facility_name')
    return render(request,'app/facility_dropdown.html',{'facilities':facilities})

def load_user_district(request):
    reg_id = request.GET.get('region')
    districts = District.objects.filter(region_id = reg_id).order_by('district_name')
    return render(request,'app/districts_dropdown.html',{'districts':districts})

def load_user_facility(request):
    dist_id = request.GET.get('district')
    facilities = Facility.objects.filter(district_id = dist_id).order_by('facility_name')
    return render(request,'app/facility_dropdown.html',{'facilities':facilities})