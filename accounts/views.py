from django.shortcuts import render, redirect
from .forms import PasswordResetForm, OTPConfirmForm
from .utils import gen_sen_otp
from hashlib import md5
from django.contrib.auth.forms import SetPasswordForm
from django.contrib.auth import get_user_model

User = get_user_model()

def password_reset(request):
    if request.method == "POST":
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            phone = form.cleaned_data['phone']
            otp = gen_sen_otp(phone)
            if otp:
                request.session['phone'] = phone
                request.session['otp-code'] = md5(otp.encode()).hexdigest()
                request.session['otp-status'] = False
                return redirect('verify-otp')
    else:
        form = PasswordResetForm()
    return render(request, 'account/password_reset.html', {'form':form})


def verify_otp(request):
    if request.method =='POST':
        form= OTPConfirmForm(request.POST)
        if form.is_valid():
            ent_code = form.cleaned_data['code']
            if md5(ent_code.encode()).hexdigest() == request.session['otp-code']:
                request.session['otp-status']=True
                return redirect('set-new-password')
            else:
                form.add_error('code','Invalid OTP code.')
    else:
        form = OTPConfirmForm()

    return render(request, 'accounts/otp-confirm.html', {"form":form})


def set_new_password(request):
    if not request.session.get('otp-status'):
        return redirect('account_reset_password')
    phone = request.session['phone']
    user = User.objects.get(phone=phone)
    if request.method == "POST":
        form = SetPasswordForm(user, request.POST)
        if form.is_valid():
            form.save()
            del request.session['otp-status']
            del request.session['phone']
            del request.session['otp-code']
            return redirect('account_login')
    else:
        form = SetPasswordForm(user)
    return render(request, 'accounts/new_password_set.html', {'form':form})