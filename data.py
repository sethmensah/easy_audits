def get_file(files):
	with open(files,'r') as f:
		lines = f.readlines()
	period = []
	exp_date = []
	voucher = []
	cheq = []
	payee = []
	desc = []
	cat = []
	ty = []
	amt = []
	tax = []
	pv = []
	memo = []
	for e in range(0,len(lines)):
		exp_date.append(lines[e].strip('\n').split(',')[0])
		voucher.append(lines[e].strip('\n').split(',')[1])
		cheq.append(lines[e].strip('\n').split(',')[2])
		payee.append(lines[e].strip('\n').split(',')[3])
		desc.append(lines[e].strip('\n').split(',')[4])
		cat.append(lines[e].strip('\n').split(',')[5])
		ty.append(lines[e].strip('\n').split(',')[6])
		amt.append(lines[e].strip('\n').split(',')[7])
		tax.append(lines[e].strip('\n').split(',')[8])
		pv.append(lines[e].strip('\n').split(',')[9])
		memo.append(lines[e].strip('\n').split(',')[10])
		period.append(lines[e].strip('\n').split(',')[11])
		
	return (exp_date, voucher, cheq, payee, desc, cat, ty, amt, tax, pv, memo,period)
	
def insert_data(files):
	from app.models import AuditScope,Expenditure, ExpensesCategory, ExpensesType
	exp_date, voucher, cheq, payee, desc, cat, ty, amt, tax, pv, memo,period = get_file(files)
	for item in range(1,len(cat)):
		
		try:
			ent = AuditScope.objects.get(id = 1)
			category = ExpensesCategory.objects.filter(category_name = cat[item].strip()).first()
			types = ExpensesType.objects.filter(type_name = ty[item].strip()).first()
			dis = Expenditure(
				scope_covered = ent,
				expense_date = exp_date[item],
				payment_voucher = voucher[item],
				cheque_number = cheq[item],
				payee = payee[item],
				description = desc[item],
				category = ExpensesCategory.objects.get(id = int(category.id)),
				expense_type = ExpensesType.objects.get(id = int(types.id)),
				amount = amt[item],
				tax_withheld = tax[item],
				memo_approved = memo[item],
				pv_approved = pv[item],)
			dis.save()
		except Exception as err:
			print(err)
			print(ty[item])
		
	
