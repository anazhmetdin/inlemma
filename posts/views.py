from django.http import Http404
from django.views.generic.list import ListView
from .models import post, comment

class postView(ListView):
    model= comment
    paginate_by= 1
    template_name= 'posts/postPage.html'
    context_object_name= 'comments'

    def get_queryset(self):
        post_query = post.objects.filter(id=self.kwargs['pid'])
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
                comments = comment.objects.filter(post=postInstance).all()
                comments = comments.order_by('-id')
            else:
                raise Http404
        except comment.DoesNotExist:
            comments = []
        except Http404:
            raise Http404
        
        return comments

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['isOwner'] = self.isOwner
        context['postInstance'] = self.postInstance
        return context