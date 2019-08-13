from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.core.mail import send_mail
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views import generic

from .forms import ProjectForm, PositionInlineFormSet
from .models import Project, Position, Application
from accounts.models import Skill


class CreateProject(
    LoginRequiredMixin,
    generic.CreateView
):
    form_class = ProjectForm
    success_url = reverse_lazy("projects:all")
    template_name = "projects/project_form.html"

    def get_context_data(self, **kwargs):
        project_context = super().get_context_data(**kwargs)
        project_context['form'] = self.get_form()
        if self.request.POST:
            project_context['position_formset'] = PositionInlineFormSet(
                self.request.POST, prefix='position_form'
            )
        else:
            project_context['position_formset'] = PositionInlineFormSet(
                queryset=Position.objects.none(),
                prefix='position_form'
            )
        return project_context

    def form_valid(self, form):
        project_context = self.get_context_data()
        position_formset = project_context['position_formset']
        form.instance.user = self.request.user
        self.object = form.save()
        if position_formset.is_valid():
            positions = position_formset.save(commit=False)
            for position in positions:
                position.project = self.object
                position.save()
            position_formset.save()
        return super(CreateProject, self).form_valid(form)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({"user": self.request.user})
        return kwargs


class ProjectsListView(generic.ListView):
    model = Project
    template_name = "projects/project_list.html"

    def get_queryset(self):
        q = self.request.GET.get('q')
        if q:
            return Project.objects.filter(
                Q(title__icontains=q)|
                Q(description__icontains=q)
            )
        else:
            query = self.kwargs.get('q')
            if query:
                return Project.objects.filter(
                    position__name=query
                )
        return Project.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        positions = Position.objects.exclude(applications__status=2)
        context['needs'] = [
            name[0]
            for name in positions.values_list('name').distinct()
        ]
        return context


class ProjectView(generic.DetailView):
    model = Project
    template_name = "projects/project.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        project = context['project']
        context['positions'] = project.position_set.all()
        if self.request.user.is_authenticated:
            context['applying_for'] = context['positions'].filter(
                applications__user=self.request.user,
                applications__status=1
            )
            context['applications_accepted'] = context['positions'].filter(
                applications__user=self.request.user,
                applications__status=2
            )
        context['is_admin'] = False
        if project.user == self.request.user:
            context['is_admin'] = True
        return context


class EditProjectView(
    LoginRequiredMixin,
    generic.edit.UpdateView
):
    model = Project
    form_class = ProjectForm
    template_name = "projects/project_form.html"

    def get_context_data(self, **kwargs):
        project_context = super().get_context_data(**kwargs)
        project_context['form'] = self.get_form()
        if self.request.POST:
            project_context['position_formset'] = PositionInlineFormSet(
                self.request.POST, prefix='position_form'
            )
        else:
            project_context['position_formset'] = PositionInlineFormSet(
                queryset=Position.objects.filter(project=self.object),
                prefix='position_form'
            )
        return project_context

    def form_valid(self, form):
        project_context = self.get_context_data()
        position_formset = project_context['position_formset']
        form.instance.user = self.request.user
        self.object = form.save()
        if position_formset.is_valid():
            positions = position_formset.save(commit=False)
            for position in positions:
                position.project = self.object
                skill = Skill.objects.get(pk=1)
                position.skill = skill
                position.save()
        return super(EditProjectView, self).form_valid(form)

    def get_success_url(self):
        project_pk = self.kwargs['pk']
        return reverse_lazy('projects:detail_project',
                            kwargs={'pk': project_pk})


class DeleteProject(
    LoginRequiredMixin,
    generic.RedirectView
):
    pattern_name = 'projects:all'

    def get_redirect_url(self, *args, **kwargs):
        pk = self.kwargs.get('pk')
        project = get_object_or_404(Project, pk=pk)
        project.delete()
        kwargs = {}
        return super(DeleteProject, self
                     ).get_redirect_url(*args, **kwargs)


class UserApplications(generic.ListView):
    model = Application

    def get_queryset(self):
        apps = Application.objects.filter(
            user=self.request.user
        )
        return apps

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['class_profile'] = ''
        context['class_app'] = 'selected'
        return context


class DeleteApplication(
    LoginRequiredMixin,
    generic.RedirectView
):
    pattern_name = 'projects:applications'

    def get_redirect_url(self, *args, **kwargs):
        pk_app = self.kwargs.get('pk_app')
        app = get_object_or_404(Application, pk=pk_app)
        app.delete()
        kwargs = {}
        return super(DeleteApplication, self
                     ).get_redirect_url(*args, **kwargs)


class UpdateStatusApplicationView(
    LoginRequiredMixin,
    generic.base.RedirectView
):
    pattern_name = 'projects:detail_project'

    def applyToPosition(self, pk_object, status):
        position = get_object_or_404(Position, pk=pk_object)
        application = Application.objects.filter(
            position=position,
            user=self.request.user
        )
        if not application.exists():
            Application.objects.create(
                position=position,
                user=self.request.user,
                status=status
            )

    def acceptStatus(self, pk_object, status):
        application = get_object_or_404(Application, pk=pk_object)
        position = application.position
        position.engaged = True
        position.save()
        app_set = Application.objects.filter(
            position=application.position
        )
        for app in app_set:
            if app.pk == application.pk:
                app.status = 2
                self.sendMailtoUser(app)
            else:
                if app.status != 3:
                    app.status = 3
                    self.sendMailtoUser(app)
            app.save()

    def deleteStatus(self, pk_object, status):
        application = get_object_or_404(Application, pk=pk_object)
        if application.status != 3:
            position = application.position
            position.engaged = False
            position.save()
            app_set = Application.objects.filter(
                position=application.position
            )
            for app in app_set:
                if app.pk == application.pk:
                    app.status = 3
                    self.sendMailtoUser(app)
                else:
                    app.status = 1
                app.save()

    def sendMailtoUser(self, application):
        position = application.position
        project = position.project
        send_mail(
            f'Application results from "{ position.name }" position',
            f'Your application was { application.get_status_display() }',
            f'{project.title} (project) <{project.user.email}>',
            [application.user.email]
        )

    def get_redirect_url(self, *args, **kwargs):
        run_application = {
            1: self.applyToPosition,
            2: self.acceptStatus,
            3: self.deleteStatus
        }
        status = self.kwargs.get('status')
        pk_object = self.kwargs.get('pk_object')
        run_application[int(status)](pk_object, status)
        kwargs = {'pk': self.kwargs.get('pk')}
        return super(UpdateStatusApplicationView, self
                     ).get_redirect_url(*args, **kwargs)
