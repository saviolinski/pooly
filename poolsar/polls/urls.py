from django.conf.urls import include, url

from views import (
    polls_index,
    polls_create,
    polls_delete,
    polls_detail,
    polls_edit,
    polls_results,
    get_chart,
    vote,
    add_choice

)

app_name = 'polls'
urlpatterns = [
    url(r'^$', polls_index, name='index'),
    url(r'^create$', polls_create, name='create'),
    url(r'^api/index/data/$', get_chart, name='api-index'),
    url(r'^(?P<slug>[\w-]+)/$', polls_detail, name='detail'),
    url(r'^(?P<slug>[\w-]+)/edit/$', polls_edit, name='edit'),
    url(r'^(?P<slug>[\w-]+)/delete/$', polls_delete, name='delete'),
    url(r'^(?P<slug>[\w-]+)/results/$', polls_results, name='results'),
    url(r'^(?P<slug>[\w-]+)/vote/$', vote, name='vote'),
    url(r'^(?P<slug>[\w-]+)/add_choice/$', add_choice, name='add-choice'),

]