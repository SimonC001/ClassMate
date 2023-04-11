# Create your views here.
from django.shortcuts import get_object_or_404
from django.core.exceptions import PermissionDenied
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, FormView, RedirectView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from .models import Photo, BlogComment
from .forms import NewCommentForm
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

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)

        comments_connected = BlogComment.objects.filter(
            blogpost_connected=self.get_object()).order_by('-date_posted')
        data['comments'] = comments_connected
        if self.request.user.is_authenticated:
            data['comment_form'] = NewCommentForm(instance=self.request.user)

        return data

    def post(self, request, *args, **kwargs):
        new_comment = BlogComment(content=request.POST.get('content'),
                                  author=self.request.user,
                                  blogpost_connected=self.get_object())
        new_comment.save()
        return self.get(self, request,args, **kwargs)


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


