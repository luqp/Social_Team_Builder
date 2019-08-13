from django.urls import path, re_path

from . import views

app_name = "projects"

urlpatterns = [
    path(
        '', views.ProjectsListView.as_view(),
        name="all"),
    path(
        'create/',
        views.CreateProject.as_view(),
        name="create_project"),
    path(
        'applications/', views.UserApplications.as_view(),
        name="applications"),
    re_path(
        r'applications/delete/(?P<pk_app>\d+)',
        views.DeleteApplication.as_view(),
        name="app_delete"),
    re_path(
        r'project/(?P<pk>\d+)/apply/(?P<pk_object>\d+)/(?P<status>\d+)/',
        views.UpdateStatusApplicationView.as_view(),
        name='apply_position'),
    re_path(
        r'project/(?P<pk>\d+)/delete/',
        views.DeleteProject.as_view(),
        name='delete_project'),
    re_path(r'project/(?P<pk>\d+)/detail/',
            views.ProjectView.as_view(),
            name='detail_project'),
    re_path(r'project/(?P<pk>\d+)/edit/',
            views.EditProjectView.as_view(),
            name='edit_project'),
    re_path(r'search/(?P<q>.+)/',
            views.ProjectsListView.as_view(),
            name="search"),
]
