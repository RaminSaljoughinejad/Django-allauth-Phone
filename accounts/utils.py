from random import randint
from django.conf import settings
from kavenegar import *

def gen_sen_otp(phone):
    code = str(randint(10000,99999))
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
            # print(response)
        except APIException as e: 
            print(e)
        except HTTPException as e: 
            print(e)
    return code