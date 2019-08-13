from django.contrib.auth.forms import AuthenticationForm, UserChangeForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import (
    login, logout, authenticate, get_user_model
)
from django.shortcuts import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views import generic
from braces.views import PrefetchRelatedMixin

from .models import Skill
from .forms import UserCreationForm, UserUpdateForm, SkillFormSet


class SignUp(generic.CreateView):
    form_class = UserCreationForm
    template_name = "accounts/signup.html"

    def form_valid(self, form):
        form.save()
        username = self.request.POST['email']
        password = self.request.POST['password1']
        user = authenticate(username=username, password=password)
        login(self.request, user)
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        user = self.request.user
        return reverse_lazy("accounts:edit",
                            kwargs={'pk': user.pk})


class SignIn(generic.FormView):
    form_class = AuthenticationForm
    success_url = reverse_lazy("projects:all")
    template_name = "accounts/signin.html"

    def form_valid(self, form):
        login(self.request, form.get_user())
        return super().form_valid(form)


class SignOut(LoginRequiredMixin, generic.RedirectView):
    url = reverse_lazy("projects:all")

    def get(self, request, *args, **kwargs):
        logout(request)
        return super().get(request, *args, **kwargs)


class ProfileView(LoginRequiredMixin, generic.DetailView):
    model = get_user_model()
    template_name = "accounts/profile.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['class_profile'] = 'selected'
        context['class_app'] = ''
        return context


class EditProfileView(
    LoginRequiredMixin,
    PrefetchRelatedMixin,
    generic.edit.UpdateView
):
    model = get_user_model()
    form_class = UserUpdateForm
    template_name = "accounts/edit_profile.html"
    prefetch_related = [u'skills']

    def get_context_data(self, **kwargs):
        user_context = super().get_context_data(**kwargs)
        user_context['form'] = self.get_form()
        if self.request.POST:
            user_context['skill_formset'] = SkillFormSet(
                self.request.POST,
                prefix='skill_form'
            )
        else:
            user_context['skill_formset'] = SkillFormSet(
                queryset=Skill.objects.filter(
                    user_skills=user_context['useraccount']
                ),
                prefix='skill_form'
            )
        return user_context

    def form_valid(self, form):
        user_context = self.get_context_data()
        skill_formset = user_context['skill_formset']
        self.object = form.save(commit=False)
        if skill_formset.is_valid():
            skills = skill_formset.save(commit=False)
            for skill in skills:
                skill.save()
                self.object.skills.add(skill)
            for skill in skill_formset.deleted_objects:
                skill.delete()
            skill_formset.save()
            self.object.save()
        return super(EditProfileView, self).form_valid(form)

    def get_success_url(self):
        user_pk = self.object.pk
        return reverse_lazy('accounts:profile',
                            kwargs={'pk': user_pk})
