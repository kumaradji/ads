from django.views.generic import CreateView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Advert, Response


class AdvertCreateView(LoginRequiredMixin, CreateView):
    model = Advert
    fields = ['title', 'content', 'category', 'upload']
    template_name = 'ads/advert_create.html'
    success_url = '/'

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.user = self.request.user
        return super().form_valid(form)


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
