
def recommend(name):

    rec = {
    "Non Payment of SSF Contribution For Casual/Temporary Staff":"We recommend that, management should as a matter of urgency pay all outstanding SSNIT contributions of the affected casual / temporary workers and produce evidence of payment for audit verification and authentication",  
    "Payment Vouchers without Requisite Supporting Documents":"We recommend that the Management should ensure that the supporting documents are made available for audit inspection. Failure which the amount should be refunded by the authorizing and approving offices and necessary sanction preferred against them",
    "Payments not Accounted for":"Management should provide evidence of the amount not accounted for, for verification and authentication failure which the amount be refunded by the Head Finance",
    "Payment Vouchers not signed by recipient":"We recommend that all those payments are signed by the payees or their designated persons and the payment vouchers are produced for audit verification failure which the said amount should be refunded by the accounts department",
    "Cash payments to Suppliers":"We recommend that management should desist from these practices but however they should educate and encourage their Artisans and suppliers to register and open Bank accounts for their businesses. Also, the head of finance must adhere to financial rules and disciplines. Failure which the amount should be surcharged against him as required by regulation 8.",
    "Payment Vouchers not Pre-Audited":"We therefore recommended that, in order to ensure effective and efficient management and control of funds, management should ensure that payment vouchers are pre–audited before payments are made in compliance with the regulation",
    "No evidence of receipt by beneficiaries":"We recommend that the Accountant should ensure that the payees append their signatures to authenticate the payments or such monies refunded",
    "Unapproved Payment Vouchers":"We recommend to management to have the payment vouchers appropriately certified and approved by the required officer of {} for our verification. Failure which the amount involved should be refunded by the head of Finance.".format(name),
    "Payments without memo":"Management should produce the memos for audit scrutiny and authentication failure the amount be refunded by the approving, authorizing authority and necessary sanction preferred against them",
    "Failure to obtain fuel receipts":"Management should as a matter of urgency impress on the accounts department to obtain those receipts from the beneficiaries to authenticate the payments failure which the amount should be refunded by the beneficiaries.",
    "Unjustified payments":"We recommend that management should provide evidence of invitation letters, minutes or reports of such meetings for authentication failure which the beneficiaries should refund the amount or the authorizing and approving officers should be surcharged with the amount involved.",
    "Failure to deduct withholding tax":"We urge management to recover the amount from the suppliers involved and remit same to Ghana Revenue Authority, failing which the revenue loss should be surcharged against the Approving and Authorizing officers",
    "Double Payment":"Management should retrieve the said amount from the supplier. Failure which the authorizing and approving officer should be surcharged for willfully causing financial loss to {} with the said amount and a penalty as required by regulation 8.".format(name),
    }
    return rec


def observations(q):
    info = {}
    exp = q.objects.all()
    for item in range(0,len(exp)):
        for dt in exp[item].remarks.all():
            if str(dt.finding_name) in info:
                info[str(dt.finding_name)] = info[str(dt.finding_name)] + exp[item].amount
            else:
                info.update({str(dt.finding_name) : exp[item].amount})
    return sorted(info.items())


def attachments(query):
    res = {}
    exp = query.objects.all()
    for ite in range(0,len(exp)):
        for dt in exp[ite].remarks.all():
            if str(dt.finding_name) in res:
                res[str(dt.finding_name)] = res[str(dt.finding_name)].extend([exp[ite].payment_voucher,exp[ite].cheque_number])
                print("keys found")
                print(res)
            else:
                print("keys not found")
                res.update({
                    str(dt.finding_name):[exp[ite].payment_voucher,exp[ite].cheque_number]
                    })
    return res
