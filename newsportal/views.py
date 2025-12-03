from django.views.generic import (ListView,
                                  DetailView,
                                  CreateView,
                                  UpdateView,
                                  DeleteView,
                                  TemplateView)
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required


from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import render, redirect
from django.contrib.auth.models import Group

from .models import News
from .filters import NewsFilter
from django.urls import reverse_lazy
from .forms import NewsForm


def home(request):
    return render(request, 'theme/index.html')

@login_required
def become_author(request):

    authors = Group.objects.get(name='authors')

    if request.user.groups.filter(name='authors').exists():
        messages.warning(request, "Вы уже автор")
    else:
        authors.user_set.add(request.user)
        messages.success(request, "Вы стали автором!")

    return redirect('/news/')




class NewsList(ListView):
    model = News
    template_name = 'news_list.html'
    context_object_name = 'news_list'
    ordering = ['-created_at']
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()

        content_type = self.request.GET.get('type')
        if content_type not in ['news', 'article']:
            content_type = 'news'

        if content_type == 'article':
            queryset = queryset.filter(type=News.ARTICLE)
        else:
            queryset = queryset.filter(type=News.NEWS)

        self.filterset = NewsFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_type'] = self.request.GET.get('type', 'news')
        context['filterset'] = self.filterset

        context['is_author'] = (
            self.request.user.groups.filter(name='authors').exists()
            if self.request.user.is_authenticated else False
        )

        return context



class ArticlesList(ListView):
    model = News
    template_name = 'articles_list.html'
    context_object_name = 'articles_list'

    def get_queryset(self):
        return News.objects.filter(type=News.ARTICLE)

class NewsSearch(ListView):
    model = News
    template_name = 'news_search.html'
    context_object_name = 'news_list'
    paginate_by = 10

    def dispatch(self, request, *args, **kwargs):
        """
        Здесь один раз жёстко определяем current_type
        и потом используем в get_queryset и get_context_data.
        """
        self.current_type = request.GET.get('type')
        if self.current_type not in ['news', 'article']:
            self.current_type = 'news'
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        # базовый queryset
        base_qs = News.objects.all()

        # фильтрация по типу публикации
        if self.current_type == 'article':
            base_qs = base_qs.filter(type=News.ARTICLE)
        else:
            base_qs = base_qs.filter(type=News.NEWS)

        # применяем фильтр django-filters
        self.filterset = NewsFilter(self.request.GET, queryset=base_qs)

        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_type'] = self.request.GET.get('type', 'news')
        context['filterset'] = self.filterset

        context['is_author'] = (
            self.request.user.groups.filter(name='authors').exists()
            if self.request.user.is_authenticated else False
        )

        return context


class NewsCreate(PermissionRequiredMixin, CreateView):
    permission_required = ('newsportal.add_news',)
    raise_exception = True

    model = News
    form_class = NewsForm
    template_name = 'news_edit.html'
    success_url = '/news/'

    def form_valid(self, form):
        content_type = self.request.GET.get('type', 'news')

        if content_type == 'article':
            form.instance.type = News.ARTICLE
        else:
            form.instance.type = News.NEWS

        return super().form_valid(form)

class NewsDelete(PermissionRequiredMixin, DeleteView):
    permission_required = ('newsportal.delete_news',)
    raise_exception = True

    model = News
    template_name = 'news_delete.html'
    success_url = reverse_lazy('news_list')

class NewsUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = ('newsportal.change_news',)
    raise_exception = True

    model = News
    form_class = NewsForm
    template_name = 'news_edit.html'
    success_url = '/news/'

class NewsDetail(DetailView):
    model = News
    template_name = 'news_detail.html'
    context_object_name = 'news'

class ProtectedView(LoginRequiredMixin, TemplateView):
    template_name = 'prodected_page.html'
