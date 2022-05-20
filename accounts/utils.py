from django.contrib.auth.models import User
import string
import random
import re

def validUsername(username, created=False):
    if re.compile(r'.*[@\.\+-]',).match(username) != None:
        raise Exception("Username contains invalid characters")
    
    elif len(username) > 16 or len(username) < 4:
        raise Exception("Username length is outside the range")

    elif not created and User.objects.filter(username__iexact=username).exists():
        raise Exception(f'Username "{username}" is not available')

def randomUsername(size=16, chars=string.ascii_letters + string.digits + '_'):
    return ''.join(random.choice(chars) for _ in range(size))