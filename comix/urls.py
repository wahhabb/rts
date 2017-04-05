from django.conf.urls import url
from comix.views import *

urlpatterns = [
    url(r'^$', IssueList.as_view(), name='issue_list'),

    url(r'^genres/$', GenreListView.as_view(),
        name='genre_list'),

    url(r'^issue/(?P<cat_id>.+)/$', issue_detail,
        name='issue_detail'),

    url(r'^issues/$',
        IssueList.as_view(),
        name='issue_list'),

    url(r'^publishers/$',
        PublisherList.as_view(),
        name='publisher_list'),

    url(r'about/$', AboutPage.as_view(), name='about'),

    url(r'ordering/$', OrderingPage.as_view(), name='ordering'),

    url(r'get-catalog/$', GetCatalogPage.as_view(), name='get_catalog'),

    url(r'photojournals/$', PhotoJournalPage.as_view(), name='photojournals'),

    url(r'guarantee/$', GuaranteePage.as_view(), name='guarantee'),

    url(r'update_session/', update_session, name='update_session'),

    url(r'^get-titles/$', SearchAutocompleteView.as_view(), name='get_titles'),
]