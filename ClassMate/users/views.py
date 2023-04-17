from django.shortcuts import render

# Create your views here.
from django.views.generic import CreateView, DetailView, ListView
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin

from django.contrib.auth.decorators import login_required
# Import User UpdateForm, ProfileUpdatForm
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm


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


# Update it here
@login_required
def profile(request, username):
    user = get_object_or_404(User, username=username)
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=user)
        p_form = ProfileUpdateForm(
            request.POST, request.FILES, instance=user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your account has been updated!')
            # Redirect back to profile page
            return redirect('user:profile', username=user.username)
    else:
        u_form = UserUpdateForm(instance=user)
        p_form = ProfileUpdateForm(instance=user.profile)
    context = {
        'user': user,
        'u_form': u_form,
        'p_form': p_form
    }
    return render(request, 'users/profile.html', context)
