from typing import Any
from urllib import request
from venv import create
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.contrib import auth, messages, sessions
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, TemplateView, UpdateView

from users.forms import ProfileForm, UserRegistrationForm, UserLoginForm
from watchlist.models import UserCollections


class UserLoginView(LoginView):
    template_name = 'users/login.html'
    form_class = UserLoginForm
    success_url = reverse_lazy('main:index')

    # def get_success_url(self) -> str:
    #     redirect_page = self.request.POST.get('next')

    #     if redirect_page and redirect_page != reverse('user:logout'):
    #         return redirect_page
        
    #     return reverse_lazy('main:index')

    def form_valid(self, form):
        session_key = self.request.session.session_key
        user = form.get_user()

        if user:
            auth.login(self.request, user)
            if session_key:
                # Не работает если есть дубликаты в названиях коллекций есть вариант обработать ошибку которая возникнет в таком случае
                # collections = UserCollections.objects.filter(session_key=session_key).update(user=user)

                session_collections = UserCollections.objects.filter(session_key=session_key).all()
                for session_collection in session_collections:
                    auth_user_collection, _ = UserCollections.objects.get_or_create(name=session_collection.name, user=user)
                    
                    for pool in session_collection.pools.all():
                        auth_user_collection.pools.add(pool)
                    
                UserCollections.objects.filter(session_key=session_key).delete()

            messages.success(self.request, f"{user.username}, Вы вошли в аккаунт")
            return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['title'] = 'Login'
        return context


class UserRegistrationView(CreateView):
    template_name = 'users/registration.html'
    form_class = UserRegistrationForm
    success_url = reverse_lazy('main:index')

    def form_valid(self, form):
        session_key = self.request.session.session_key
        user = form.instance
        
        if user:
            form.save()
            auth.login(self.request, user)

            if session_key:
                UserCollections.objects.filter(session_key=session_key).update(user=user)

            UserCollections.objects.get_or_create(name='Favorites', user=user)

            messages.success(self.request, f'{user.username}, Вы успешно зарегистрированы и вошли в аккаунт')
            return HttpResponseRedirect(self.success_url)
    

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['title'] = 'Registration'
        return context
    

class UserProfileView(LoginRequiredMixin, UpdateView):
    template_name = 'users/profile.html'
    form_class = ProfileForm
    success_url = reverse_lazy('user:profile')

    def get_object(self, queryset=None):
        return self.request.user
    
    def form_valid(self, form):
        messages.success(self.request, "Профайл успешно обновлен")
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request, "Произошла ошибка")
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["title"] = "Profile"
        return context
    


@login_required
def logout(request):
    auth.logout(request)
    return redirect(reverse('main:index'))
    