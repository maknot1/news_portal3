from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from .models import News
from .filters import NewsFilter
from django.urls import reverse_lazy
from .forms import NewsForm


class NewsList(ListView):
    model = News
    template_name = 'news_list.html'
    context_object_name = 'news_list'
    ordering = ['-created_at']
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = NewsFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context

class NewsSearch(ListView):
    model = News
    template_name = 'news_search.html'
    context_object_name = 'news_list'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = NewsFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context

class NewsCreate(CreateView):
    form_class = NewsForm
    model = News
    template_name = 'news_edit.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class NewsUpdate(UpdateView):
    model = News
    form_class = NewsForm
    template_name = 'news_edit.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class NewsDelete(DeleteView):
    model = News
    template_name = 'news_delete.html'
    success_url = reverse_lazy('news_list')

class NewsDetail(DetailView):
    model = News
    template_name = 'news_detail.html'
    context_object_name = 'news'
