from django.shortcuts import redirect, render
from django.views import View
from posts.forms import PostForm
from profiles.models import Settings
from django.contrib import messages
# from django.conf import settings

class homeView(View):
    def get(self, request):
        if request.user.is_authenticated:
            if request.user.profile.mail_activated or not request.user.has_usable_password():
                userSettings = Settings.objects.get(user=request.user)
                context = {'form': PostForm(),
                           'anonymous': userSettings.anonymous_posts,
                           'comments': userSettings.posts_comments,
                           'post_messages': userSettings.posts_messages,
                        #    'config': settings.CKEDITOR_CONFIGS
                           }
                return render(request, 'home/homespace.html', context)
            else:
                return render(request, 'home/activate.html')
        else:
            return render(request, 'home/landing.html')

    
    def post(self, request):
        form = PostForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect("home")
        else:
            for error in form.errors:
                messages.error(request, error+form.errors[error].as_text())
            context = {'form': PostForm(data=request.POST)}
            return render(request, 'home/homespace.html', context)