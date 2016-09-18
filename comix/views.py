from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.template import loader, Context
from django.views.generic.list import ListView, View

from comix.models import Genre, Issue, Publisher, Tag
from orders.cart import get_cart_items


# Create your views here.
####### Comix Related ######

def homepage(request):
    return HttpResponseRedirect('/issues/')


class PublisherList(View):
    template_name = 'comix/publisher_list.html'

    def get(self, request):
        publishers = Publisher.objects.all().order_by('name')
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
    paginate_by = 9
    page_kwarg = 'page'
    genre_kwarg = 'category'
    template_name = 'comix/issue_list.html'

    def get(self, request):
        genre_slug = self.request.GET.get(self.genre_kwarg)
        publisher_slug = self.request.GET.get('publisher')
        sort_order = self.request.GET.get('sort')
        search_text = self.request.GET.get('search')
        tag_slug = self.request.GET.get('tag')
        issues = Issue.objects.all().filter(status='available')
        tags = Tag.objects.all()
        query_string = ""
        cart_issues = get_cart_items(request)
        cart_item_count = cart_issues.count()

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
            publisher = Publisher.objects.get(slug=publisher_slug)
            publisher_text = publisher.name
            query_string += "&publisher=" + publisher_slug
            issues = issues.filter(gcd_series_id__gcd_publisher_id=publisher.id)
        else:
            publisher_text = None
        if search_text != None:
            issues = issues.filter(gcd_series_id__name__icontains=search_text )
            query_string += "&search=" + search_text
        if sort_order != None:
            query_string += "&sort=" + sort_order
        sort_seq = {'price-up': 'price', 'price-down': '-price', None: '-price'}
        if sort_order == 'alpha':
            issues = issues.order_by('gcd_series_id__name', 'number')
        else:
            issues = issues.order_by(sort_seq[sort_order])
        genres = Genre.objects.all().order_by('slug')
        paginator = Paginator(
            issues, self.paginate_by
        )
        page_no = request.GET.get(self.page_kwarg)
        try:
            page = paginator.page(page_no)
        except PageNotAnInteger:
            page = paginator.page(1)
        except EmptyPage:
            page = paginator.page(paginator.num_pages)

        context = {'issues': page,
                   'paginator': paginator,
                   'is_paginated': page.has_other_pages(),
                   'genres': genres,
                   'genre_text': genre_text,
                   'query_string': query_string,
                   'publisher_name': publisher_text,
                   'sort_order': sort_order,
                   'tags': tags,
                   'cart_item_count': cart_item_count,
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
    issue = Issue.objects.get(pk=cat_id)
    tags = Tag.objects.all()
    template = loader.get_template('comix/issue_detail.html')
    genres = Genre.objects.all().order_by('slug')
    cart_issues = get_cart_items(request)
    cart_item_count = cart_issues.count()
    context = Context({'issue': issue,
                       'series': issue.gcd_series_id,
                       'genres': genres,
                       'tags': tags,
                       'cart_item_count': cart_item_count,
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



