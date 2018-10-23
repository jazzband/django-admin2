from django.views.generic import ListView, DetailView

from .models import Post


class BlogListView(ListView):
    model = Post
    template_name = 'blog_list.html'
    paginate_by = 10


class BlogDetailView(DetailView):
    model = Post
    template_name = 'blog_detail.html'
