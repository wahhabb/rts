from django.shortcuts import render
from django.http.response import HttpResponse
from django.views.generic.list import ListView, View
from django.views.generic.detail import DetailView
from django.template import loader, Template, Context
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from comix.models import Genre, Issue, Series

# Create your views here.
def homepage(request):
    issues = Issue.objects.all()
    template = loader.get_template('comix/issue_list.html')
    context = Context({'issue': issues,} )
    return HttpResponse(template.render(context))

class IssueList(View):
    paginate_by = 9
    page_kwarg = 'page'
    template_name = 'comix/issue_list.html'

    def get(self, request):
        issues = Issue.objects.all().order_by('-price')
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
                   'is_paginated': page.has_other_pages()
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
    #   series = Series.objects.get(id=issue.gcd_series_id)
    template = loader.get_template('comix/issue_detail.html')
    context = Context({'issue': issue, 'series': issue.gcd_series_id})
    return HttpResponse(template.render(context))
