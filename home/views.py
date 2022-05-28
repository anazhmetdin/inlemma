from django.shortcuts import redirect, render
from django.views import View
from posts.forms import PostForm
from profiles.models import Settings
from django.contrib import messages
from django.forms.utils import ErrorList
from django.http import JsonResponse
# from django.conf import settings

class homeView(View):
    def get_context_data(self, request, **kwargs):
        userSettings = Settings.objects.get(user=request.user)
        context = {'form': PostForm(),
                   'anonymous': userSettings.anonymous_posts,
                   'comments': userSettings.posts_comments,
                   'post_messages': userSettings.posts_messages,
                #  'config': settings.CKEDITOR_CONFIGS
                  }
        return context
    
    def get(self, request):
        if request.user.is_authenticated:
            if request.user.profile.mail_activated or not request.user.has_usable_password():
                context = self.get_context_data(request)
                return render(request, 'home/homespace.html', context)
            else:
                return render(request, 'home/activate.html')
        else:
            return render(request, 'home/landing.html')

    
    def post(self, request):
        form = PostForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            # return redirect("home")
            
            response = {
                'message':'Your post has been submitted successfully.'
            }
            status_code = 200
        else:
            # if form.errors:
            #     for error in form.errors:
            #         messages.error(request, error+form.errors[error].as_text())
            # else:
            #     messages.error(request, ErrorList(["Something went wrong, please try again"]))

            # context = self.get_context_data(request)
            # context["title"] = form.data.get("title")
            # context["form"] = form

            response = {
                'message':'Something went wront, please try again.'
            }
            status_code = 400
            # return render(request, 'home/homespace.html', context)
        return JsonResponse(response, status=status_code)