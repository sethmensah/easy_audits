"""
Definition of models.
"""

from django.db import models
from datetime import date
from django.contrib.auth.models import User,AbstractUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.forms.models import model_to_dict
from django.utils import timezone

# Create your models here.



class Region(models.Model):
    region_name = models.CharField(verbose_name='Region Name',max_length=100,blank=False,null = False)

    def __str__(self):
        return self.region_name
    

class District(models.Model):
    district_name = models.CharField(verbose_name='District Name',max_length=100,blank=False,null = False)
    region = models.ForeignKey(Region, on_delete=models.CASCADE,blank = True, null = True)

    def __str__(self):
        return self.district_name

class Facility(models.Model):
    region = models.ForeignKey(Region, on_delete=models.CASCADE,blank = True, null = True)
    district = models.ForeignKey(District, on_delete=models.CASCADE,blank = True, null = True)
    facility_name = models.CharField(verbose_name='Facility Name',max_length=100,blank=False,null = False)

    def __str__(self):
        return self.facility_name


class CustomUser(AbstractUser):
    email = models.EmailField(verbose_name='Email',max_length=100, unique= True)
    user_region = models.ForeignKey(Region, on_delete=models.CASCADE,blank = True, null = True)
    user_district = models.ForeignKey(District, on_delete=models.CASCADE,blank = True, null = True)
    user_facility = models.ForeignKey(Facility, on_delete=models.CASCADE,blank = True, null = True)

    def __str__(self):
        return self.email


class UserTrail(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)
    action = models.CharField(max_length=100, null=True, blank=True)
    now = models.DateTimeField(default=timezone.now)
    date = models.DateField(default=date.today)
    crud = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return [self.name,self.action]

#session_id = request.session.session_key

class EntityDetails(models.Model):
    facility_name = models.ForeignKey(Facility, verbose_name='Facility Name',on_delete=models.SET_NULL, blank = False, null=True)
    entity_type = models.CharField(verbose_name='Entity Type',max_length=300,blank=False,null = False)
    district_name = models.ForeignKey(District, on_delete=models.SET_NULL, blank = False, null=True)
    region_name = models.ForeignKey(Region, on_delete=models.SET_NULL,blank = False, null=True)
    entity_address = models.CharField(verbose_name='Entity Address',max_length=300,blank=False,null = False)
    employee_no = models.CharField(verbose_name='Total Employee',max_length=300,blank= True,null = True)
    locality = models.CharField(verbose_name='Locality',max_length=300,blank= True,null = True)
    created_by = models.ForeignKey(CustomUser,on_delete = models.SET_NULL,blank = True, null = True)

    def __str__(self):
        return self.facility_name

class AuditorDetails(models.Model):
    entity_details = models.ForeignKey(EntityDetails,related_name ='auditordetails',on_delete =models.CASCADE)
    auditor_name = models.CharField(verbose_name='Auditor Name',max_length=300,blank=True,null = True)
    auditor_role = models.CharField(verbose_name='Auditor Role',max_length=300,blank=True,null = True)

    def __str__(self):
        return self.auditor_name

class ManagementDetails(models.Model):
    entity_details = models.ForeignKey(EntityDetails,related_name ='managementdetails',on_delete =models.CASCADE)
    member_name = models.CharField(verbose_name='Member Name',max_length=300,blank=True,null = True)
    member_position = models.CharField(verbose_name='Member Position',max_length=300,blank=True,null = True)

    def __str__(self):
        return self.member_name

class FundsReceived(models.Model):
    entity_details = models.ForeignKey(EntityDetails,related_name ='fundsreceived',on_delete =models.CASCADE)
    receipt_date = models.DateField(verbose_name='Receipt Date',blank=True, null=True)
    opening_balance = models.DecimalField(verbose_name='Opening Balance',max_digits=8, decimal_places=2,blank=True,null = True)
    gcr_number = models.CharField(verbose_name='GCR Number',max_length=300,blank=True,null = True)
    cheque_details = models.CharField(verbose_name='Cheque Details',max_length=300,blank=True,null = True)
    amount_received =  models.DecimalField(verbose_name='Amount Received',max_digits=8, decimal_places=2,blank=True,null = True)
    fund_received_type = models.CharField(verbose_name='Fund Received Type',max_length=300,blank=True,null = True)
    purpose_of_receipt = models.CharField(verbose_name='Purpose of Receipt',max_length=300,blank=True,null = True)

    def __str__(self):
        return self.id

class CommodityReceived(models.Model):
    entity_details = models.ForeignKey(EntityDetails,related_name ='commodityreceived',on_delete =models.CASCADE)
    commodity_receipt_date = models.DateField(verbose_name='Commodity Receipt Date',blank=True, null=True)
    commodity_type_received= models.CharField(verbose_name='Commodity Type Received',max_length=300,blank=True,null = True)
    quantity_received = models.CharField(verbose_name='Quantity Received',max_length=300,blank=True,null = True)
    SRA_number = models.CharField(verbose_name='SRA Number',max_length=300,blank=True,null = True)
    remarks_on_commodity_received = models.CharField(verbose_name='Remarks on Commodity Received',max_length=300,blank=True,null = True)

    def __str__(self):
        return [self.id,self.commodity_type_received,]


class CommodityUtilized(models.Model):
    entity_details = models.ForeignKey(EntityDetails,related_name= 'commodityutilized',on_delete =models.CASCADE)
    commodity_issued_date = models.DateField(verbose_name='Commodity Issued Date',blank=True, null=True)
    commodity_type_issued= models.CharField(verbose_name='Commodity Type Issued',max_length=300,blank=True,null = True)
    quantity_issued = models.CharField(verbose_name='Quantity Issued',max_length=300,blank=True,null = True)
    requisition_number = models.CharField(verbose_name='Requisition Number',max_length=300,blank=True,null = True)
    user_department = models.CharField(verbose_name='User Department',max_length=300,blank=True,null = True)
    remarks_on_commodity_issued = models.CharField(verbose_name='Remarks on Commodity Issued',max_length=300,blank=True,null = True)

    def __str__(self):
        return [self.id,self.requisition_number,]


class FundsUtilized(models.Model):
    entity_details = models.ForeignKey(EntityDetails,related_name = 'fundsutilized',on_delete =models.CASCADE)
    expense_date = models.DateField(verbose_name='Expense Date',blank=True, null=True)
    closing_balance = models.DecimalField(verbose_name='Closing Balance',max_digits=8, decimal_places=2,blank=True,null = True)
    payment_voucher_number = models.CharField(verbose_name='Payment Voucher Number',max_length=300,blank=True,null = True)
    amount_spent =  models.DecimalField(verbose_name='Amount Spent',max_digits=8, decimal_places=2,blank=True,null = True)
    cheque_number = models.CharField(verbose_name='Cheque Number',max_length=300,blank=True,null = True)
    description = models.CharField(verbose_name='Description',max_length=300,blank=True,null = True)
    source_of_funds = models.CharField(verbose_name='Source of Funds',max_length=300,blank=True,null = True)
    payee = models.CharField(verbose_name='Payee Name',max_length=300,blank=True,null = True)
    remarks = models.CharField(verbose_name='Remarks',max_length=300,blank=True,null = True)

    def __str__(self):
        return [self.id,self.payment_voucher_number,]

class UnpresentedPaymentVouchers(models.Model):
    entity_details = models.ForeignKey(EntityDetails,related_name = 'unpresentedpaymentvouchers',on_delete =models.CASCADE)
    payment_date = models.DateField(verbose_name='Payment Date',blank=True, null=True)
    voucher_number = models.CharField(verbose_name='Payment Voucher Number',max_length=300,blank=True,null = True)
    cheque_num = models.CharField(verbose_name='Cheque Number',max_length=300,blank=True,null = True)
    amount =  models.DecimalField(verbose_name='Amount Paid',max_digits=8, decimal_places=2,blank=True,null = True)
    payee_name = models.CharField(verbose_name='Payee Name',max_length=300,blank=True,null = True)
    purpose_of_payment = models.CharField(verbose_name='Purpose of Payment',max_length=300,blank=True,null = True)
    
    def __str__(self):
        return [self.id,self.voucher_number,]


class BankLodgment(models.Model):
    entity_details = models.ForeignKey(EntityDetails,related_name = 'banklodgment',on_delete =models.CASCADE)
    lodgment_date = models.DateField(verbose_name='Lodgment Date',blank=True, null=True)
    pay_in_slip_number = models.CharField(verbose_name='Pay-in-slip Number',max_length=300,blank=True,null = True)
    amount_paid =  models.DecimalField(verbose_name='Amount Paid',max_digits=8, decimal_places=2,blank=True,null = True)
    bank_name = models.CharField(verbose_name='Bank Name',max_length=300,blank=True,null = True)
    account_number = models.CharField(verbose_name='Account Number',max_length=300,blank=True,null = True)
    type_of_fund = models.CharField(verbose_name='Type of Fund',max_length=300,blank=True,null = True)

    def __str__(self):
        return [self.bank_name,self.account_number,]

class ExpensesCategory(models.Model):
    category_name = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return self.category_name

class ExpensesType(models.Model):
    category = models.ForeignKey(ExpensesCategory,related_name ='expensestype', on_delete=models.CASCADE,blank = True, null = True)
    type_name = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return self.type_name

class AuditScope(models.Model):
    auditee_name = models.ForeignKey(EntityDetails,related_name ='audit_scope',on_delete =models.CASCADE,blank = True, null = True)
    review_date = models.DateField(verbose_name='Review Date',blank=False,null = False)
    period_covered = models.CharField(verbose_name='Period Covered',max_length=300,blank=False,null = False)
    audit_objective = models.TextField(verbose_name='Specific Audit Objective',blank=False,null = False)

    def __str__(self):
        return (self.period_covered)


class Observation(models.Model):
    finding_name = models.CharField(verbose_name='Observation',max_length=1000,blank=False,null = False)

    def __str__(self):
        return (self.finding_name)


class Expenditure(models.Model):
    scope_covered = models.ForeignKey(AuditScope,related_name ='expenditure',on_delete =models.CASCADE,blank = True, null = True)
    expense_date = models.DateField(verbose_name='Expense Date',blank=True, null=True)
    payment_voucher = models.CharField(max_length=100, null=True, blank=False)
    cheque_number = models.CharField(max_length=100, null=True, blank=False)
    payee = models.CharField(max_length=100, null=True, blank=False)
    description = models.CharField(max_length=100,null=True, blank=False)
    category = models.ForeignKey(ExpensesCategory, on_delete=models.SET_NULL,blank = False, null=True)
    expense_type = models.ForeignKey(ExpensesType, on_delete=models.SET_NULL,blank = False, null=True)
    amount = models.DecimalField(max_length=100, null=True, blank=False, max_digits=12,decimal_places=2)
    tax_withheld = models.DecimalField(verbose_name='Withheld Tax', max_length=100, null=True, blank=True, max_digits=12,decimal_places=2)
    #remarks = models.CharField(verbose_name='Remarks',max_length=1000, null=True, blank=True,)
    remarks = models.ManyToManyField(Observation,verbose_name='Remarks')

    
    def __str__(self):
        return (self.scope_covered.period_covered)

    def get_scope(self):
        return (self.scope_covered.period_covered)
