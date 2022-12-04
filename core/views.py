from django.shortcuts import render,redirect
from .models import *
from django.core.paginator import Paginator
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .config import pay_eth
from django.contrib.auth import login,logout,authenticate

def index(request):
    context = {}

    dept = Department.objects.filter(raised=False)
    paginator = Paginator(dept, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context['data'] = page_obj

    return render(request, 'core/index.html',context)

@login_required()
def dashboard(request):
    context = {}
    user = request.user
    context['user'] = user
    inverst = Inverst.objects.filter(user=request.user)
    context['inverst'] = inverst
    profile = InversterProfile.objects.get(user=request.user)
    context['profile'] = profile
    print(inverst)
    return render(request, 'core/dashboard.html',context)

@login_required()
def gen_bond(request,id):
    context = {}
    user = request.user
    inverst = Inverst.objects.get(id=id)
    context['inverst'] = inverst
    profile = InversterProfile.objects.get(user=request.user)
    context['profile'] = profile

    return render(request, 'core/bond.html',context)


@login_required()
def dept_detail(request,id):
    context = {}
    data = Department.objects.get(id=id)
    context['data'] = data
    context['amt_req'] = float(data.allocation_amount) - float(data.fund)

    context['amt_eth'] = round(context['amt_req'] * 0.00023,2)
    return render(request, 'core/detail.html',context)

@login_required()
def inverst(request,id):
    context = {}
    data = Department.objects.get(id=id)
    context['data'] = data
    context['profile'] = InversterProfile.objects.get(user=request.user)

    if request.method == 'POST':
        dept = id
        name = request.POST.get('name','')
        org = request.POST.get('org','')

        amount = request.POST.get('amount',0)
        email = request.POST.get('email','')
        
        id_proff = request.FILES.get('id_proff')
        income_certificate = request.FILES.get('ic')
        passbook_copy = request.FILES.get('passbook')
        print(id_proff)

        obj = Inverst.objects.create(
            user=request.user,
            dept=data,
            name=name,
            org=org,
            amount = amount,
            id_proff=id_proff,
            is_approved=False,
            income_certificate = income_certificate,
            email=email,
            passbook_copy=passbook_copy
        )
        return redirect('pay',obj.id)

    return render(request, 'core/inverst.html',context)

@login_required
def pay_inverst(request,id):
    context = {}
    
    inverst = Inverst.objects.get(id=id)
    department = inverst.dept
    context['inverst'] = inverst
    context['department'] = department
    context['amt_eth'] = (float(department.allocation_amount) * 0.00023) - float(department.eth)

    user = request.user

    if request.POST:
        meta_acc = request.POST.get('meta_account','')
        private_key = request.POST.get('private_key','')
        amt = request.POST.get('amt',0.0)
        inverst.metamask_id = meta_acc
        inverst.amount = amt
        
        res = pay_eth(inverst.metamask_id, department.metamask_id, private_key, amt)
        print(res)
        if res['transction']:
            transction_id = res['hash']
            inverst.is_approved = True
            inverst.amount = float(amt)
            inverst.transction_hash = transction_id
            inverst.save()
            department.fund += float(amt) * 4412.52 
            department.eth +=float(amt)
            if department.fund >= department.allocation_amount:
                department.raised = True
            department.save() 
            
            return redirect('dash')
        else:
            print("Transation Faild")
        print(meta_acc,private_key)

    return render(request, 'core/pay.html',context)

def login_user(request):

    if request.method == 'POST':
        name = request.POST.get('username','')
        passwd = request.POST.get('password','')

        user = authenticate(request,username=name,password=passwd)

        if user:
            login(request, user)
            return redirect('index')

    return render(request, 'auth/login.html')

def register_profile(request):
    context = {}

    if request.POST:
        username = request.POST.get("username",'')
        fname = request.POST.get('fname','')
        lname = request.POST.get('lname','')
        email = request.POST.get('email','')
        dob = request.POST.get('dob')
        phone = request.POST.get('phone','')
        address = request.POST.get('address','')
        org = request.POST.get('org')
        id_proff = request.FILES.get('id_proff')
        social = request.POST.get('url','')
        profile = request.FILES.get('img')
        
        p1 = request.POST.get('passwd')
        p2 = request.POST.get('cpassword')
        print(id_proff)
        if p1==p2:
            obj = User.objects.create(first_name=fname,last_name=lname,email=email,username=username,password=p1)
            obj.set_password(p1)
            obj.save()
            InversterProfile.objects.create(
                user=obj,
                fname=fname,
                lname=lname,
                profile=profile,
                dob=dob,email=email,phone=phone,address=address,org=org,
                id_proff=id_proff,
                social_media=social,

            )
            auth = authenticate(request,username=username,password=p2)
            if auth is not None:
                login(request, auth)
                return redirect('dash')
        else:
            print("Went wrong")
    return render(request, 'auth/register.html',context)

@login_required()
def logout_inverst(request):
    logout(request)
    return redirect('login')   