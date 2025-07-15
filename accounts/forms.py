from django import forms
from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _
from allauth.account.adapter import get_adapter
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError


User = get_user_model()

class CustomPhoneField(forms.CharField):
    e164_validator = RegexValidator(
        regex=r"^(\+\d{1,3})?\d{10,13}",
        message=_("Please Enter a Valid Phone Number"),
        code="invalid_phone",
    )

    def __init__(self, *args, **kwargs):
        widget = forms.TextInput(
            attrs={"placeholder": _("Phone"), "autocomplete": "tel", "type": "tel"}
        )
        kwargs.setdefault("validators", [self.e164_validator])
        kwargs.setdefault("widget", widget)
        kwargs.setdefault("label", _("Phone"))
        super().__init__(*args, **kwargs)

    def clean(self, value):
        value = super().clean(value)
        if value:
            value = value.replace(" ", "").replace("-", "")
            value = get_adapter().clean_phone(value)
        return value
    

class PasswordResetForm(forms.Form):
    phone = CustomPhoneField()

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if not User.objects.filter(phone=phone).exists():
            raise ValidationError("This phone number is not registered!")
        
        return phone

class OTPConfirmForm(forms.Form):
    code = forms.CharField(max_length=5)