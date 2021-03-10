from django import forms
from django.contrib.auth.forms import AuthenticationForm,UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from django.forms.models import inlineformset_factory
from django.utils.encoding import force_text
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Fieldset, Div, HTML, ButtonHolder, Submit, Row, Column
from app.models import  District, Facility, Region, ExpensesCategory, ExpensesType, CustomUser, EntityDetails, Expenditure, \
    AuditorDetails, ManagementDetails, AuditScope, Observation



ENTITY_TYPE = (
    ('','Choose from drop down'),
    ('District Hospital', 'District Hospital'),
    ('Regional Hospital', 'Regional Hospital'),
    ('Health Center', 'Health Center'),
    ('Regional Medical Stores','Regional Medical Stores'),
    ('Regional Health Directorate','Regional Health Directorate'),
    ('CHPS Compound','CHPS Compound'),
)
MEMBER_POSITION = (
    ('','Choose from drop down'),
    ('medical superintendent','Medical Superintendent'),
    ('administrator','Administrator'),
    ('internal auditor','Internal Auditor'),
    ('nurse manager','Nurse Manager'),
    ('pharmacist','Pharmacist'),
    ('accountant','Accountant'),
    ('clinical doctor','Clinical Doctor'),
    ('supply officer','Supply Oficer'),
    ('physician assistant','Physician Assistant'),
)
AUDITOR_ROLE = (
    ('','Choose from drop down'),
    ('audit_supervisor','Audit Supervisor'),
    ('lead_auditor','Lead Auditor'),
    ('audit_team_member','Audit Team Member'),
)
OPTIONS = (
    ('','Choose from drop down'),
    ('yes','Yes'),
    ('no','No'),
)

REMARKS = (
    ("Non Payment of SSF Contribution For Casual/Temporary Staff","Non Payment of SSF Contribution For Casual/Temporary Staff"),
    ("Payment Vouchers without Requisite Supporting Documents","Payment Vouchers without Requisite Supporting Documents"),
    ("Payments not Accounted for","Payments not Accounted for"),
    ("Payment Vouchers not signed by recipient","Payment Vouchers not signed by recipient"),
    ("Cash payments to Suppliers","Cash payments to Suppliers"),
    ("Payment Vouchers not Pre Audited","Payment Vouchers not Pre Audited"),
    ("No evidence of receipt by beneficiaries","No evidence of receipt by beneficiaries"),
    ("Unapproved Payment Vouchers","Unapproved Payment Vouchers"),
    ("Payments without memo","Payments without memo"),
    ("Failure to obtain fuel receipts","Failure to obtain fuel receipts"),
    ("Unjustified payments","Unjustified payments"),
    ("Failure to deduct withholding tax","Failure to deduct withholding tax"),
    ("Double Payment","Double Payment"),

)



class LoginForm(AuthenticationForm):
    """Authentication form which uses boostrap CSS."""
    username = forms.CharField(max_length=254, widget=forms.TextInput({'class': 'form-control form-control-sm','placeholder': 'Enter username here'}))
    password = forms.CharField(label=_("Password"), widget=forms.PasswordInput({'class': 'form-control form-control-sm','placeholder':'Enter your password here'}))


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('username','email','user_region','user_district','user_facility',)

    def __init__(self,*args,**kwargs):
        super(CustomUserCreationForm,self).__init__(*args,**kwargs)
        self.fields['username'].widget.attrs['autofocus'] = False

        for name in self.fields.keys():
            self.fields[name].widget.attrs.update({'class': 'form-control-sm'})
            self.fields[name].widget.attrs['required'] = True
        self.fields['user_district'].queryset = District.objects.none()
        self.fields['user_facility'].queryset = Facility.objects.none()
        if 'user_region' in self.data:
            try:
                region = int(self.data.get('user_region'))
                self.fields['user_district'].queryset = District.objects.filter(region = region).order_by('district_name')
            except (ValueError,TypeError):
                pass
        elif self.instance.pk:
            self.fields['user_district'].queryset = self.instance.user_region.district_set.order_by('district_name')
        
        if 'user_district' in self.data:
            try:
                district = int(self.data.get('user_district'))
                self.fields['user_facility'].queryset = Facility.objects.filter(district = district).order_by('facility_name')
            except(ValueError,TypeError):
                pass
        elif self.instance.pk:
            self.fields['user_facility'].queryset = self.instance.district_name.facility_set.order_by('facility_name')

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ('username','email','user_region','user_district','user_facility',)

    def __init__(self,*args,**kwargs):
        super(CustomUserChangeForm,self).__init__(*args,**kwargs)
        for name in self.fields.keys():
            self.fields[name].widget.attrs.update({'class': 'form-control-sm'})


class EntityDetailsForm(forms.ModelForm):
    
    class Meta:
        model = EntityDetails
        exclude = ['created_by',]
        widgets = {
            'entity_type': forms.Select(choices = ENTITY_TYPE),
        }

    def __init__(self, *args, **kwargs):
        super(EntityDetailsForm,self).__init__(*args, **kwargs)
        self.fields['district_name'].queryset = District.objects.none()
        self.fields['facility_name'].queryset = Facility.objects.none()
        if 'region_name' in self.data:
            try:
                region = int(self.data.get('region_name'))
                self.fields['district_name'].queryset = District.objects.filter(region = region).order_by('district_name')
            except (ValueError,TypeError):
                pass
        elif self.instance.pk:
            self.fields['district_name'].queryset = self.instance.region_name.districts_set.order_by('district_name')

            #district dropdown

        if 'district_name' in self.data:
            try:
                district = int(self.data.get('district_name'))
                self.fields['facility_name'].queryset = Facility.objects.filter(district = district).order_by('facility_name')
            except(ValueError,TypeError):
                pass
        elif self.instance.pk:
            self.fields['facility_name'].queryset = self.instance.district_name.facility_set.order_by('facility_name')

        for name in self.fields.keys():
            self.fields[name].widget.attrs.update({'class': 'form-control-sm'})
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Row(
                Column('region_name', css_class='form-group col-md-3 mb-0'),
                Column('district_name', css_class='form-group col-md-4 mb-0'),
                Column('facility_name', css_class='form-group col-md-5 mb-0'),
                css_class='form-row'
            ),
             Row(
                Column('entity_type', css_class='form-group col-md-6 mb-0'),
                Column('entity_address', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
                ),
              Row(
                Column('locality', css_class='form-group col-md-6 mb-0'),
                Column('employee_no', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
                ),
            )

class AuditorDetailsForm(forms.ModelForm):
    
    class Meta:
        model = AuditorDetails
        exclude = ()
        widgets = {
            'auditor_role': forms.Select(choices = AUDITOR_ROLE),
            
             }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name in self.fields.keys():
            self.fields[name].widget.attrs.update({'class': 'form-control-sm'})
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
             Row(
                Column('auditor_name', css_class='form-group col-md-6 mb-0'),
                Column('auditor_role', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
        )

class ManagementDetailsForm(forms.ModelForm):
    
    class Meta:
        model = ManagementDetails
        exclude = ()
        widgets = {
            'member_position': forms.Select(choices = MEMBER_POSITION),
            
             }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name in self.fields.keys():
            self.fields[name].widget.attrs.update({'class': 'form-control-sm'})
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
             Row(
                Column('member_name', css_class='form-group col-md-6 mb-0'),
                Column('member_position', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
        )


class ExpensesForm(forms.ModelForm):
    remarks = forms.ModelMultipleChoiceField(queryset = Observation.objects.all(),widget = forms.CheckboxSelectMultiple,required = False)
    
    class Meta:
        model = Expenditure
        exclude = ['entity_name','scope_covered','type_audit','remarks',]

    def __init__(self, *args, **kwargs):
        super(ExpensesForm,self).__init__(*args, **kwargs)
        self.fields['expense_type'].queryset = ExpensesType.objects.none() 
        if 'category' in self.data:
            try:
                cate = int(self.data.get('category'))
                self.fields['expense_type'].queryset = ExpensesType.objects.filter(category_id = cate)
            except (ValueError,TypeError):
                pass
        elif self.instance.pk:
            self.fields['expense_type'].queryset = self.instance.category.expenses_set.all()

        for name in self.fields.keys():
            self.fields[name].widget.attrs.update({'class': 'form-control-sm'})
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Row(
                Column('expense_date', css_class='form-group col-md-4 mb-0'),
                Column('payment_voucher', css_class='form-group col-md-4 mb-0'),
                Column('cheque_number', css_class='form-group col-md-4 mb-0'),
                css_class='form-row'
            ),
             Row(
                  Column('description', css_class='form-group col-md-12 mb-0'),
                css_class='form-row'
            ),

            Row(
                Column('payee', css_class='form-group col-md-6 mb-0'),
                Column('category', css_class='form-group col-md-3 mb-0'),
                Column('expense_type', css_class='form-group col-md-3 mb-0'),
                css_class='form-row'
            ),
           Row(
                Column('amount', css_class='form-group col-md-3 mb-0'),
                Column('tax_withheld', css_class='form-group col-md-3 mb-0'),
                Column('remarks', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
        )
    def clean(self):
        cleaned_data = super().clean()
        remarks = cleaned_data.get('remarks')

class AuditScopeForm(forms.ModelForm):
    
    class Meta:
        model = AuditScope
        exclude = ['auditee_name','audit_objective']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name in self.fields.keys():
            self.fields[name].widget.attrs.update({'class': 'form-control-sm'})
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
             Row(
                Column('review_date', css_class='form-group col-md-6 mb-0'),
                Column('period_covered', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
        )

ExpensesFormSet = inlineformset_factory(
                            AuditScope,
                            Expenditure,
                            form = ExpensesForm,
                            fields = ['expense_date','payment_voucher','cheque_number','payee','description','category','expense_type','amount','tax_withheld','remarks',],
                            extra=1,can_delete=True)
AuditorDetailsFormSet = inlineformset_factory(
                            EntityDetails,
                            AuditorDetails,
                            form = AuditorDetailsForm,
                            fields = ['auditor_name','auditor_role',],
                            extra=1,can_delete=True)

ManagementDetailsFormSet = inlineformset_factory(
                            EntityDetails,
                            ManagementDetails,
                            form = ManagementDetailsForm,
                            fields = ['member_name','member_position',],
                            extra=1,can_delete=True)