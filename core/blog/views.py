from django.shortcuts import render
from django.views.generic.base import TemplateView, RedirectView
from django.views.generic import ListView, FormView, CreateView, UpdateView,DeleteView,DetailView
from django.shortcuts import get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin

from blog.forms import CustomGeneralPostForm
from .models import Post


# Create your views here.
def indexView(request):
    return render(request, "index.html")


class IndexView(TemplateView):
    template_name = "index.html"

    def get_context_data(self, **kwargs):
        contenxt = super().get_context_data(**kwargs)
        contenxt["name"] = "Moka"
        return contenxt


class RedirectToMaktabkhoonehView(RedirectView):
    url = "https://maktabkhooneh.com"

    def get_redirect_url(self, *args, **kwargs):
        pk = kwargs.get("pk")
        print(f"Redirecting to Maktabkhooneh with pk: {pk}")

        post = get_object_or_404(Post, pk=pk)
        print(f"Post Title: {post.title}")
        return super().get_redirect_url(*args, **kwargs)


class PostListView(LoginRequiredMixin, ListView):
    model = Post
    # queryset = Post.objects.all()
    # def get_queryset(self):
    #     posts = Post.objects.filter(status=True).order_by('created_date')
    #     print (posts[0].category)
    #     return posts

    # paginate_by = 2
    ordering = "-id"
    context_object_name = "posts"


"""
class PostCreateView(FormView):
    template_name = "blog/contact.html"
    form_class = CreatePostForm
    success_url = "/blog/post/"

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)
"""


class PostCreateView(LoginRequiredMixin,CreateView):
    model = Post
    fields = ["title", "content", "status", "category"]
    template_name = "blog/contact.html"
    success_url = "/blog/post/"

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin,UpdateView):
    model = Post
    form_class = CustomGeneralPostForm
    success_url = "/blog/post/"

class PostDeleteView(LoginRequiredMixin,DeleteView):
    model = Post
    success_url = "/blog/post/"

class PostDetailView(DetailView):
    model = Post