from django.http import Http404
from django.views.generic.list import ListView
from django.contrib.auth.models import User
from posts.models import Post

class profileView(ListView):
    model= Post
    paginate_by= 10
    template_name= 'profiles/profile.html'
    context_object_name= 'posts'

    def get_queryset(self):
        user_query = User.objects.filter(username__iexact=self.kwargs['username'])
        isOwner = False
        user = None

        if user_query:
            user = user_query.get()
            isOwner = user.username == self.request.user.username
        else:
            raise Http404

        self.profileUser = user
        self.isOwner = isOwner
        
        try:
            if isOwner:
                posts = Post.objects.filter(user=user).all()
            else:
                posts = Post.objects.filter(user=user, anonymous=False, published=True).all()
            posts = posts.order_by('-id')
        except Post.DoesNotExist:
            posts = []
        
        return posts

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['isOwner'] = self.isOwner
        context['profileUser'] = self.profileUser
        return context