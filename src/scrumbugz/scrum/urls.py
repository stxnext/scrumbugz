from django.conf.urls import patterns, url

from scrum.views import (CheckRecentUpdates, CreateBZProductView,
                         CreateProjectView, CreateSprintView, CreateTeamView,
                         DeleteBZProductView, EditProjectView, EditSprintView,
                         EditTeamView, ListProjectsView, ListTeamsView,
                         ManageProjectBugsView, ManageSprintBugsView,
                         ProjectView, ProjectBacklogView, RedirectOldURLsView,
                         SprintView, TeamView)

from scrum.views.auth import LoginView
from scrum.views.bugs import HardRefreshView


urlpatterns = patterns('',
    url(r'^p/$', ListProjectsView.as_view(), name='scrum_projects_list'),
    url(r'^t/$', ListTeamsView.as_view(), name='scrum_teams_list'),
    url(r'^p/new/$', CreateProjectView.as_view(), name='scrum_project_new'),
    url(r'^t/new/$', CreateTeamView.as_view(), name='scrum_team_new'),
    url(r'^p/product/(?P<pk>\d+)/delete/$', DeleteBZProductView.as_view(),
        name='scrum_product_delete'),
    url(r'^p/(?P<slug>[-\w\.]+)/$', ProjectView.as_view(),
        name='scrum_project'),
    url(r'^t/(?P<slug>[-\w\.]+)/$', TeamView.as_view(), name='scrum_team'),
    url(r'^t/(?P<slug>[-\w\.]+)/new/$', CreateSprintView.as_view(),
        name='scrum_sprint_new'),
    url(r'^p/(?P<slug>[-\w\.]+)/edit/$', EditProjectView.as_view(),
        name='scrum_project_edit'),
    url(r'^t/(?P<slug>[-\w\.]+)/edit/$', EditTeamView.as_view(),
        name='scrum_team_edit'),
    url(r'^p/(?P<slug>[-\w\.]+)/products/$', CreateBZProductView.as_view(),
        name='scrum_project_products'),
    url(r'^p/(?P<slug>[-\w\.]+)/bugs/$', ManageProjectBugsView.as_view(),
        name='scrum_project_bugs'),
    url(r'^p/(?P<slug>[-\w\.]+)/backlog/$', ProjectBacklogView.as_view(),
        name='scrum_project_backlog'),
    url(r'^t/(?P<slug>[-\w\.]+)/(?P<sslug>[-\w\.]+)/$', SprintView.as_view(),
        name='scrum_sprint'),
    url(r'^t/(?P<slug>[-\w\.]+)/(?P<sslug>[-\w\.]+)/edit/$',
        EditSprintView.as_view(), name='scrum_sprint_edit'),
    url(r'^t/(?P<slug>[-\w\.]+)/(?P<sslug>[-\w\.]+)/bugs/$',
        ManageSprintBugsView.as_view(), name='scrum_sprint_bugs'),
    url(r'^projects/(?P<path>.*)', RedirectOldURLsView.as_view()),
    url(r'^bugs_updated/$', CheckRecentUpdates.as_view(),
        name='scrum_bugs_updated'),

    url(r'^b/fetch/$', HardRefreshView.as_view(), name='hard-refresh'),


    url(r'^login$', LoginView.as_view(), name='login'),
)
