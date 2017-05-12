from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http.response import HttpResponse
from django.shortcuts import render
from django.template import loader, Context
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.list import ListView, View
from django.db.models import Q
from django.http import JsonResponse
import re, string
from itertools import chain


from comix.models import Genre, Issue, Publisher, Tag, Series, PubCount
from orders.cart import get_cart_issues, get_cart_items, get_wish_list_issues
import logging


log = logging.getLogger(__name__)


# Create your views here.
####### Comix Related ######


@csrf_exempt
def update_session(request):
    if not request.is_ajax() or not request.method=='POST':
        return HttpResponseNotAllowed(['POST'])

    request.session['per_page'] = request.POST['count']
    return HttpResponse(request.POST['count'])


class PublisherList(View):
    template_name = 'comix/publisher_list.html'

    def get(self, request):
        publishers = PubCount.objects.all().order_by('name')
        col_count = (publishers.count() + 3 ) // 4
        cart_issues = get_cart_items(request)
        cart_item_count = cart_issues.count()
        context = {'publishers': publishers,
                   'col_breaks': [col_count, 2*col_count, 3*col_count],
                   'cart_item_count': cart_item_count,
                   }
        return render(
            request, self.template_name, context
        )


class IssueList(View):
    page_kwarg = 'page'
    genre_kwarg = 'category'
    template_name = 'comix/issue_list.html'

    def get(self, request):
        per_page = per_page_ct = request.session.get('per_page', 12)
        if per_page == '200L':
            per_page_ct = 200
        genre_slug = self.request.GET.get(self.genre_kwarg)
        publisher_slug = self.request.GET.get('publisher')
        sort_order = self.request.GET.get('sort')
        search_text = self.request.GET.get('search')
        tag_slug = self.request.GET.get('tag')
        issues = Issue.objects.all().filter(status='available')
        issues = issues.filter(Q(variants__isnull=True) | Q(variants='')) # V means has variants but selected
        tags = Tag.objects.all()
        query_string = ""
        cart_issues = get_cart_issues(request)
        cart_items = get_cart_items(request)
        cart_item_count = cart_items.count()
        wish_list_issues = get_wish_list_issues(request)
        issues_following = None

        if tag_slug != None:
            tag = Tag.objects.get(slug=tag_slug)
            issues = tag.issue_set.all()
        if genre_slug != None:
            genre = Genre.objects.get(slug=genre_slug)
            genre_text = genre.genre
            issues = issues.filter(genre_id=genre.id)
            query_string += "&" + self.genre_kwarg + "=" + genre_slug
        else:
            genre_text = None
        if publisher_slug != None:
            publisher = PubCount.objects.get(slug=publisher_slug)
            publisher_text = publisher.name
            query_string += "&publisher=" + publisher_slug
            issues = issues.filter(publisher_name=publisher.name)
        else:
            publisher_text = None

        if search_text != None:
            issues1 = issues.filter(gcd_series_id__name__icontains=search_text)
            issues_following = issues.filter(Q(tags__name__icontains=search_text) |
                                   Q(publisher_name__icontains=search_text) |
                                   Q(notes__icontains=search_text))
            issues_following = issues_following.exclude(gcd_series_id__name__icontains=search_text)
            issues = issues1
            query_string += "&search=" + search_text
            log.debug("Search: " + search_text)

        if sort_order != None:
            query_string += "&sort=" + sort_order
        sort_seq = {'price-up': 'price', 'price-down': '-price', None: 'alpha'}
        if (sort_order == 'alpha') or (sort_order == None):
            issues = issues.order_by('gcd_series__sort_name', 'gcd_series__year_began', 'volume', 'number',
                                     'hrn_number', 'edition', 'inserts', 'issue_text', 'numerical_grade', 'price')
            if issues_following != None:
                issues_following = issues_following.order_by('gcd_series__sort_name', 'gcd_series__year_began', 'volume', 'number',
                                     'hrn_number', 'edition', 'inserts', 'issue_text', 'numerical_grade', 'price')
        else:
            issues = issues.order_by(sort_seq[sort_order])
            if issues_following != None:
                issues_following = issues_following.order_by(sort_seq[sort_order])

        if issues_following != None:
            issues = list(chain(issues, issues_following))
        genres = Genre.objects.all().order_by('slug')

        paginator = Paginator(issues, per_page_ct)
        page_no = request.GET.get(self.page_kwarg)

        try:
            page = paginator.page(page_no)
            page_no = int(page_no)
        except PageNotAnInteger:
            page = paginator.page(1)
            page_no = 1
        except EmptyPage:
            page = paginator.page(paginator.num_pages)
            page_no = paginator.num_pages

        page_list = list(range(1, paginator.num_pages + 1))
        if paginator.num_pages - page_no > 2 and paginator.num_pages > 4:
            if page_no == 1:
                page_list[3:paginator.num_pages - 1] = ['...']
            else:
                page_list[page_no + 1:paginator.num_pages - 1] = ['...']
        if page_no > 3 and paginator.num_pages > 4:
            if paginator.num_pages - page_no < 2:
                page_list[1:paginator.num_pages - 3] = ['...']
            else:
                page_list[1:page_no - 2] = ['...']


        is_home = False
        if request.path == '/' and page_no == None:
            is_home = True

        context = {'issues': page,
                   'paginator': paginator,
                   'is_paginated': page.has_other_pages(),
                   'genres': genres,
                   'genre_text': genre_text,
                   'query_string': query_string,
                   'publisher_name': publisher_text,
                   'sort_order': sort_order,
                   'tags': tags,
                   'cart_issues': cart_issues,
                   'cart_item_count': cart_item_count,
                   'wish_list_issues': wish_list_issues,
                   'per_page': per_page,
                   'is_home': is_home,
                   'page_list': page_list,
                   }
        return render(
            request, self.template_name, context
        )

class GenreListView(ListView):
    model = Genre

    def get_context_data(self, **kwargs):
        context = super(GenreListView, self).get_context_data(**kwargs)
        return context

def issue_detail(request, cat_id):
    issue = Issue.objects.get(catalog_id=cat_id)
    tags = Tag.objects.all()
    template = loader.get_template('comix/issue_detail.html')
    genres = Genre.objects.all().order_by('slug')
    cart_issues = get_cart_issues(request)
    cart_items = get_cart_items(request)
    cart_item_count = cart_items.count()
    wish_list_issues = get_wish_list_issues(request)
    context = Context({'issue': issue,
                       'series': issue.gcd_series,
                       'genres': genres,
                       'tags': tags,
                       'cart_item_count': cart_item_count,
                       'cart_issues': cart_issues,
                       'wish_list_issues': wish_list_issues,
                       'user': request.user,
                       })
    return HttpResponse(template.render(context))


######  Static Pages #######
class StaticPageMixin:
    template_name = ''

    def get(self, request):
        cart_issues = get_cart_items(request)
        cart_item_count = cart_issues.count()
        return render(
            request, self.template_name,
            {'cart_item_count': cart_item_count,}
        )


class AboutPage(StaticPageMixin, View):
    template_name = 'comix/about.html'


class GetCatalogPage(StaticPageMixin, View):
    template_name = 'comix/get_catalog.html'


class PhotoJournalPage(StaticPageMixin, View):
    template_name = 'comix/photojournals.html'


class OrderingPage(StaticPageMixin, View):
    template_name = 'comix/ordering.html'


class GuaranteePage(StaticPageMixin, View):
    template_name = 'comix/guarantee.html'


#   Dropdown for search shows titles, publishers, notes, gcd_notes, tags, genres
#   ToDo: Add Categories
class SearchAutocompleteView(View):
    def get(self, request):
        if request.is_ajax():
            q = request.GET.get('term', '').lower()
            foundset = set()
            publishers = PubCount.objects.filter(name__icontains=q)
            for publisher in publishers:
                foundset.add(string.capwords(publisher.name))
            titles = Series.objects.filter(name__icontains=q)
            results = []
            for title in titles:
                foundset.add(string.capwords(title.name))
            tags = Tag.objects.filter(name__icontains=q)
            for tag in tags:
                foundset.add(string.capwords(tag.name))
            genres = Genre.objects.filter(genre__icontains=q)
            for genre in genres:
                foundset.add(string.capwords(genre.genre))
            if len(q) > 4:
                notes = Issue.objects.filter(notes__icontains=q)
                for note in notes:
                    res = re.search(r'(' + q + r'.*?)(?:\W|$)', note.notes, re.I).group(1)   # extend to end of word
                    foundset.add(string.capwords(res))
                notes = Issue.objects.filter(gcd_notes__icontains=q)
                for note in notes:
                    res = re.search(r'(' + q + r'.*?)(?:\W|$)', note.gcd_notes, re.I).group(1)   # extend to end of word
                    foundset.add(string.capwords(res))
            results = sorted(foundset, key=len)
        else:
            results='fail'
        return JsonResponse(results, safe=False)
