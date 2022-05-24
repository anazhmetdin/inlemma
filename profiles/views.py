from django.shortcuts import redirect, render
from django.views import View
from django.contrib.auth.models import User
from posts.models import post

class profileView(View):
    def get(self, request, username):
        user_query = User.objects.filter(username__iexact=username)
        if user_query:
            user = user_query.get()
            isOwner = user.username == request.user.username
            # if logged-in user is the profile owner, display anonymous posts
            try:
                if isOwner:
                    posts = post.objects.filter(user=user).all()
                else:
                    posts = post.objects.filter(user=user, anonymous=False, published=True).all()
            except post.DoesNotExist:
                posts = None
            
            context = {'user': user, 'posts': posts, 'isOwner': isOwner}
            return render(request, 'profiles/profile.html', context)
        else:
            return redirect('home')