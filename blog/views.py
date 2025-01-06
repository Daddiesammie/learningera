from django.views.generic import ListView, DetailView
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Post, Comment

class PostListView(ListView):
    model = Post
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'
    paginate_by = 6
    queryset = Post.objects.filter(is_published=True)

class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comments'] = self.object.comments.filter(parent=None)
        return context

@login_required
def add_comment(request, post_id):
    if request.method == 'POST':
        content = request.POST.get('content')
        parent_id = request.POST.get('parent_id')
        
        post = Post.objects.get(id=post_id)
        parent = Comment.objects.get(id=parent_id) if parent_id else None
        
        comment = Comment.objects.create(
            post=post,
            user=request.user,
            content=content,
            parent=parent
        )
        
        return JsonResponse({
            'success': True,
            'comment_id': comment.id,
            'user': comment.user.username,
            'content': comment.content,
            'created_at': comment.created_at.strftime('%B %d, %Y %H:%M'),
            'parent_id': parent_id
        })
