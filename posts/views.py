from django.http import Http404
from django.shortcuts import redirect
from django.views import View
from django.views.generic.list import ListView
from .models import Post, Comment
from .forms import CommentForm
from django.contrib import messages

class postView(ListView):
    model= Comment
    paginate_by= 10
    template_name= 'posts/postPage.html'
    context_object_name= 'comments'

    def get_queryset(self):
        post_query = Post.objects.filter(id=self.kwargs['pid'])
        viewable = False
        isOwner = False
        postInstance = None
        
        if post_query:
            postInstance = post_query.get()

            if self.request.user.is_authenticated:
                isOwner = self.request.user.id == postInstance.user.id
                viewable = isOwner
            if not viewable:
                viewable = postInstance.published and not postInstance.anonymous
        else:
            raise Http404
        
        self.postInstance = postInstance
        self.isOwner = isOwner

        try:
            if viewable:
                comments = Comment.objects.filter(post=postInstance).all()
                comments = comments.order_by('-id')
            else:
                raise Http404
        except Comment.DoesNotExist:
            comments = []
        except Http404:
            raise Http404
        
        return comments

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['isOwner'] = self.isOwner
        context['postInstance'] = self.postInstance
        if self.postInstance.comments and self.request.user.is_authenticated:
            context['commentForm'] = CommentForm(user=self.request.user)
            context['anonymous'] = self.request.user.settings.anonymous_comments
        return context


class commentView(View):
    def post(self, request, pid):
        try:
            post = Post.objects.get(id = pid)
        except Exception as e:
            raise Http404

        form = CommentForm(data=request.POST, user=request.user, post=post)
        if form.is_valid():
            form.save()
        else:
            for error in form.errors:
                messages.error(request, error+form.errors[error].as_text())

        return redirect('post', pid=pid)