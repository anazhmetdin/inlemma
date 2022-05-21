import threading
from django.contrib.auth.models import User
import string
import random
import re
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import PasswordResetTokenGenerator
import six
from django.core.mail import EmailMultiAlternatives
from django.conf import settings

def validUsername(username, created=False):
    if re.compile(r'.*[@\.\+-]',).match(username) != None:
        raise Exception("Username contains invalid characters")
    
    elif len(username) > 16 or len(username) < 4:
        raise Exception("Username length is outside the range")

    elif not created and User.objects.filter(username__iexact=username).exists():
        raise Exception(f'Username "{username}" is not available')

def randomUsername(size=16, chars=string.ascii_letters + string.digits + '_'):
    return ''.join(random.choice(chars) for _ in range(size))

def emailIsValid(email):
    if re.match(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', email) == None:
        return False
    else:
        return True

class ConfirmationTokenGenerator(PasswordResetTokenGenerator):
    
    def _make_hash_value(self, user, timestamp: int) -> str:
        return six.text_type(user.id)+six.text_type(timestamp)+six.text_type(user.profile)


class EmailThread(threading.Thread):
    def __init__(self, email):
        self.email = email
        threading.Thread.__init__(self)

    def run(self):
        self.email.send()

def sendConfirmationMail(request, user):
    currentSite = get_current_site(request)
    emailSubject = 'Confirm your email'
    
    emailContext = {'user': user,
                    'site': currentSite,
                    'uid': urlsafe_base64_encode(force_bytes(user.id)),
                    'token': ConfirmationTokenGenerator().make_token(user)}

    emailBody = render_to_string('accounts/confirmation.html', emailContext)

    email = EmailMultiAlternatives(subject=emailSubject,
                                   from_email=settings.EMAIL_FROM_USER,
                                   to=[user.email]
                                  )
    
    email.attach_alternative(emailBody, "text/html")
    EmailThread(email).start()