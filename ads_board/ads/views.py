from datetime import datetime

from django.urls import reverse
from django.views.generic import CreateView, DetailView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import render, redirect
from django.views import View

from .filters import AdvertFilter
from .forms import PostForm
from .models import Advert, Response


# Представление для главной страницы
class AdvertListView(LoginRequiredMixin, ListView):
    model = Advert
    ordering = '-created_at'
    template_name = 'ads/advert_list.html'
    context_object_name = 'advert_list'
    paginate_by = 6

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = AdvertFilter(self.request.GET, queryset)
        return self.filterset.qs

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
    template_name = 'ads/advert_create.html'
    success_url = 'ads/advert/<int:pk>/'

    def form_valid(self, form):
        advert = form.save(commit=False)
        advert.user = self.request.user
        advert.save()
        form.instance.author = self.request.user
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('ads:advert-detail', kwargs={'pk': self.object.pk})


class AdvertDetailView(DetailView):
    model = Advert
    template_name = 'ads/advert_detail.html'


class ResponseCreateView(LoginRequiredMixin, CreateView):
    model = Response
    fields = ['author', 'response_text']
    template_name = 'ads/response_create.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.user = self.request.user
        form.instance.article = Advert.objects.get(pk=self.kwargs['pk'])
        return super().form_valid(form)


class ResponseDetailView(DetailView):
    model = Response
    template_name = 'ads/response_detail.html'


class PrivatePageView(LoginRequiredMixin, View):
    def get(self, request):
        user = request.user
        adverts = Advert.objects.filter(user=user)
        responses = Response.objects.filter(advert__in=adverts)
        return render(request, 'ads/private_page.html', context={'responses': responses})


class AcceptResponseView(LoginRequiredMixin, View):
    def get(self, request, response_id):
        response = Response.objects.get(pk=response_id)
        response.accepted = True
        response.save()
        return redirect('ads:private')


class DeleteResponseView(LoginRequiredMixin, View):
    def get(self, request, response_id):
        response = Response.objects.get(pk=response_id)
        response.delete()
        return redirect('ads:private')


class LikeView(View):
    def post(self, request, pk):
        response = Response.objects.get(pk=pk)
        response.like()
        return redirect('ads:like', response_id=pk)


class DislikeView(View):
    def post(self, request, pk):
        response = Response.objects.get(pk=pk)
        response.dislike()
        return redirect('ads:dislike', response_id=pk)
