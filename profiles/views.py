from django.shortcuts import redirect, render
from django.views import View
from django.contrib.auth.models import User

class profileView(View):
    def get(self, request, username):
        user_query = User.objects.filter(username__iexact=username)
        if user_query:
            user = user_query.get()
            context = {'user': user, 'is_owner': username==request.user.username}
            return render(request, 'profiles/profile.html', context)
        else:
            return redirect('home')