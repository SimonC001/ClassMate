from django.shortcuts import render

# Create your views here.
from django.views.generic import CreateView, DetailView, ListView
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import UserProfile
from .forms import UserProfileForm

class SignUpView(CreateView):

    model = User

    template_name = 'users/signup.html'

    form_class = UserCreationForm

    success_url = reverse_lazy('photo:list')

    def form_valid(self, form):
        to_return = super().form_valid(form)

        user = authenticate(
            username=form.cleaned_data["username"],
            password=form.cleaned_data["password1"],
        )

        login(self.request, user)

        return to_return

class CustomLoginView(LoginView):

    template_name = 'users/login.html'

def logout_request(request):
    logout(request)
    messages.info(request, "You have successfully logged out.")
    return redirect("login")

# # CHANGE THIS FROM LOGIN TO DETAIL WHEN PROFILES ARE MADE
# class ProfileView(LoginView):

#     template_name = 'users/profile.html'


class UserProfileView(LoginRequiredMixin, DetailView):
    model = UserProfile
    template_name = 'users/profile.html'

    def get_object(self):
        return self.request.user.userprofile

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['form'] = UserProfileForm(self.request.POST, instance=self.object)
        else:
            context['form'] = UserProfileForm(instance=self.object)
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = UserProfileForm(request.POST, instance=self.object)
        if form.is_valid():
            form.save()
            return redirect(reverse_lazy('profile'))
        else:
            return self.render_to_response(self.get_context_data(form=form))
