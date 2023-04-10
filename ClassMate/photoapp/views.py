# Create your views here.
from django.shortcuts import get_object_or_404
from django.core.exceptions import PermissionDenied
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, FormView, RedirectView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from .models import Photo, Comment
from .forms import CommentForm
from django.db.models import Q
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from taggit.models import Tag
from django.urls import reverse


class PhotoListView(ListView):

    model = Photo

    template_name = 'photoapp/list.html'

    context_object_name = 'photos'


class PhotoTagListView(PhotoListView):

    template_name = 'photoapp/taglist.html'

    # Custom method
    def get_tag(self):
        return self.kwargs.get('tag')

    def get_queryset(self):
        return self.model.objects.filter(tags__slug=self.get_tag())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["tag"] = self.get_tag()
        return context


class PhotoDetailView(DetailView):

    model = Photo

    template_name = 'photoapp/detail.html'

    context_object_name = 'photo'


class PhotoCreateView(LoginRequiredMixin, CreateView):

    model = Photo

    fields = ['title', 'description', 'image', 'thumbnail', 'tags']

    template_name = 'photoapp/create.html'

    success_url = reverse_lazy('photo:list')

    def form_valid(self, form):

        form.instance.submitter = self.request.user

        return super().form_valid(form)


class UserIsSubmitter(UserPassesTestMixin):

    # Custom method
    def get_photo(self):
        return get_object_or_404(Photo, pk=self.kwargs.get('pk'))

    def test_func(self):

        if self.request.user.is_authenticated:
            return self.request.user == self.get_photo().submitter
        else:
            raise PermissionDenied('Sorry you are not allowed here')


class PhotoUpdateView(UserIsSubmitter, UpdateView):

    template_name = 'photoapp/update.html'

    model = Photo

    fields = ['title', 'description', 'tags']

    success_url = reverse_lazy('photo:list')


class PhotoDeleteView(UserIsSubmitter, DeleteView):

    template_name = 'photoapp/delete.html'

    model = Photo

    success_url = reverse_lazy('photo:list')


class PhotoSearchView(ListView):

    template_name = 'photoapp/search.html'

    model = Photo

    context_object_name = 'photos'

    def get_queryset(self):
        query = self.request.GET.get('q')
        return Photo.objects.filter(title__icontains=query)


def post_detail(request, year, month, day, post):
    post = get_object_or_404(Photo, slug=post,
                             status='published',
                             publish__year=year,
                             publish__month=month,
                             publish__day=day)

    # List of active comments for this post
    comments = post.comments.filter(active=True)

    new_comment = None

    if request.method == 'POST':
        # A comment was posted
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            # Create Comment object but don't save to database yet
            new_comment = comment_form.save(commit=False)
            # Assign the current post to the comment
            new_comment.post = post
            # Save the comment to the database
            new_comment.save()
    else:
        comment_form = CommentForm()
    return render(request,
                  'blog/post/detail.html',
                  {'post': post,
                   'comments': comments,
                   'new_comment': new_comment,
                   'comment_form': comment_form})
