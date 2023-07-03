import pytz
from django.urls import reverse
from django.views.generic import CreateView, DetailView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from datetime import datetime
from .filters import AdvertFilter
from .forms import PostForm
from .models import Advert, Response


# Представление для главной страницы
class AdvertListView(LoginRequiredMixin, ListView):
    model = Advert
    # указываем способ сортировки
    ordering = '-created_at'
    # указываем шаблон представления
    template_name = 'ads/advert_list.html'
    # указываем переменную, которую будем использовать в шаблоне news.html
    context_object_name = 'advert-list'
    paginate_by = 6

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = AdvertFilter(self.request.GET, queryset)
        return self.filterset.qs

    # забираем отфильтрованные объекты переопределяя метод get_context_data у наследуемого класса
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_now'] = datetime.utcnow()
        context['is_author'] = self.request.user.groups.filter(name='authors').exists()
        return context


class AdvertCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    raise_exception = True
    permission_required = 'ads.add_post'
    form_class = PostForm
    model = Advert
    # fields = ['title', 'content', 'category', 'upload']
    template_name = 'ads/advert_create.html'
    success_url = ''

    def form_valid(self, form):
        post = form.save(commit=False)
        post.is_news = True
        post.author = self.request.user.author
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('post', kwargs={'pk': self.object.pk})

    # def form_valid(self, form):
    #     form.instance.author = self.request.user
    #     form.instance.user = self.request.user
    #     return super().form_valid(form)


class AdvertDetailView(DetailView):
    model = Advert
    template_name = 'ads/advert_detail.html'


class ResponseCreateView(LoginRequiredMixin, CreateView):
    model = Response
    fields = ['response_text']
    template_name = 'ads/response_create.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.user = self.request.user.customuser
        form.instance.article = Advert.objects.get(pk=self.kwargs['pk'])
        return super().form_valid(form)


class ResponseDetailView(DetailView):
    model = Response
    template_name = 'ads/response_detail.html'
