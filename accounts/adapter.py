from allauth.account.adapter import DefaultAccountAdapter
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from kavenegar import *
from django.conf import settings
from .forms import CustomPhoneField
from django.utils import timezone

User = get_user_model()

class CustomDefaultAccountAdapter(DefaultAccountAdapter):
    def phone_form_field(self, **kwargs):
        return CustomPhoneField(**kwargs)
    
    def clean_phone(self, phone):
        if self.request and 'login' in self.request.path:
            user = self.get_user_by_phone(phone)
            if user:
                return phone
            else:
                raise ValidationError("This phone number is not registered")
        if self.request and 'signup' in self.request.path:
            if User.objects.filter(phone=phone).exists():
                raise ValidationError("This phone number is already registered.")
            return phone
        if self.request and 'phone/change' in self.request.path:
            if self.request.user.phone == phone:
                raise ValidationError("This is your current phone number!")
            if User.objects.filter(phone=phone).exists():
                raise ValidationError("This phone number is already in use.")
        return phone    

    def set_phone(self, user, phone: str, verified: bool):
        user.phone = phone
        user.phone_verified = verified
        user.save()

    def get_phone(self, user):
        return (user.phone, user.phone_verified)

    def set_phone_verified(self, user, phone: str):
        if not self.request.user.is_anonymous and self.request.user.phone != phone:
            if not user.phone_history:
                user.phone_history = {}
            user.phone_history[user.phone]=timezone.now().isoformat()
            user.phone = phone
        user.phone_verified = True
        user.save()

    def get_user_by_phone(self, phone: str):
        try:
            return User.objects.get(phone=phone)
        except User.DoesNotExist:
            return None

    def generate_phone_verification_code(self):
        return self._generate_code(length=10) 

    def send_verification_code_sms(self, user, phone, code, **kwargs):
        if settings.DEBUG:
            print(f"{code} is sent to {phone}")
        else:
            try:
                api = KavenegarAPI(settings.KAVENEGAR_API_KEY)
                params = {
                    'receptor': phone,
                    'template': 'progma-fa',
                    'token': code,
                    'type': 'sms',
                }
                response = api.verify_lookup(params)
                print(response)
            except APIException as e: 
                print(e)
            except HTTPException as e: 
                print(e)

    def send_unknown_account_sms(self, phone, **kwargs):
        pass