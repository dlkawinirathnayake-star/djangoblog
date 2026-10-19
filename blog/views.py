
from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Q
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from blog.forms import PostForm, RegisterForm
from .models import Post, Category


# Home page - Sri Lanka travel blog
class PostListView(ListView):
    model = Post
    template_name = "blog/home.html"
    context_object_name = "posts"
    paginate_by = 6

    def get_queryset(self):
        queryset = (
            Post.objects
            .filter(status="published")
            .select_related("author", "category")
            .order_by("-created_at")
        )

        category_name = self.request.GET.get("category")

        if category_name:
            queryset = queryset.filter(
                category__name__iexact=category_name
            )

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = Category.objects.all()
        return context


# Single blog post detail
class PostDetailView(DetailView):
    model = Post
    template_name = "blog/post_detail.html"
    context_object_name = "post"
    slug_field = "slug"
    slug_url_kwarg = "slug"

    def get_queryset(self):
        queryset = Post.objects.select_related("author", "category")

        if self.request.user.is_authenticated:
            return queryset.filter(
                Q(status="published") |
                Q(author=self.request.user)
            )

        return queryset.filter(status="published")


# Create a new post
class PostCreateView(
    LoginRequiredMixin,
    SuccessMessageMixin,
    CreateView
):
    model = Post
    form_class = PostForm
    template_name = "blog/post_form.html"
    login_url = "login"
    success_message = "Your story was created successfully!"

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy(
            "post_detail",
            kwargs={"slug": self.object.slug}
        )


# Update a post - author only
class PostUpdateView(
    LoginRequiredMixin,
    UserPassesTestMixin,
    SuccessMessageMixin,
    UpdateView
):
    model = Post
    form_class = PostForm
    template_name = "blog/post_form.html"
    login_url = "login"
    success_message = "Your story was updated successfully!"

    def test_func(self):
        return self.get_object().author == self.request.user

    def get_success_url(self):
        return reverse_lazy(
            "post_detail",
            kwargs={"slug": self.object.slug}
        )


# Delete a post - author only
class PostDeleteView(
    LoginRequiredMixin,
    UserPassesTestMixin,
    DeleteView
):
    model = Post
    template_name = "blog/post_confirm_delete.html"
    login_url = "login"
    success_url = reverse_lazy("home")

    def test_func(self):
        return self.get_object().author == self.request.user

    def form_valid(self, form):
        messages.success(
            self.request,
            "Your story was deleted successfully!"
        )
        return super().form_valid(form)


# Logged-in user's posts
class MyPostsView(LoginRequiredMixin, ListView):
    model = Post
    template_name = "blog/my_posts.html"
    context_object_name = "posts"
    paginate_by = 6
    login_url = "login"

    def get_queryset(self):
        return (
            Post.objects
            .filter(author=self.request.user)
            .select_related("category")
            .order_by("-created_at")
        )


# User registration
class RegisterView(CreateView):
    form_class = RegisterForm
    template_name = "blog/register.html"
    success_url = reverse_lazy("home")

    def form_valid(self, form):
        response = super().form_valid(form)
        login(self.request, self.object)
        return response


# About page
def about(request):
    return render(
        request,
        "blog/about.html",
        {"team": "Discover Sri Lanka"}
    )


# Contact page
def contact(request):
    return render(request, "blog/contact.html")


# Custom permission error page
def custom_403(request, exception=None):
    return render(
        request,
        "blog/403.html",
        status=403
    )
