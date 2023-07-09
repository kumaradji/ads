from datetime import datetime

from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, DetailView, ListView, DeleteView, UpdateView
from django.shortcuts import redirect
from django.views import View

from .filters import AdvertFilter
from .forms import PostForm
from .models import Advert, Response
from ads_board.tasks.tasks import send_registration_email, send_response_email


# Представление для главной страницы
class AdvertListView(LoginRequiredMixin, ListView):
    model = Advert
    ordering = '-created_at'
    template_name = 'ads/advert_list.html'
    context_object_name = 'advert_list'
    paginate_by = 10

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
        advert.author = self.request.user  # Фиксация автора
        advert.save()
        form.instance.author = self.request.user
        form.instance.user = self.request.user

        # Вызов задачи отправки e-mail
        send_registration_email.delay(self.request.user.email, advert.title)

        return super().form_valid(form)

    def get_success_url(self):
        return reverse('ads:advert-detail', kwargs={'pk': self.object.pk})


class AdvertDetailView(DetailView):
    model = Advert
    template_name = 'ads/advert_detail.html'


class AdvertDeleteView(DeleteView):
    model = Advert
    template_name = 'ads/advert_delete.html'
    success_url = reverse_lazy('ads:advert-list')


class AdvertUpdateView(UpdateView):
    model = Advert
    template_name = 'ads/advert_update.html'
    fields = ['title', 'content', 'category']
    success_url = reverse_lazy('ads:advert-list')


class ResponseCreateView(LoginRequiredMixin, CreateView):
    raise_exception = True
    model = Response
    ordering = ' -createDate'
    context_object_name = 'responses'
    fields = ['response_text']
    template_name = 'ads/response_create.html'
    paginate_by = 5

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.article = Advert.objects.get(pk=self.kwargs['pk'])
        # Вызов задачи отправки e-mail
        send_response_email.delay(self.request.user.email, form.instance.article.title)

        return super().form_valid(form)


class ResponseDetailView(DetailView):
    model = Response
    template_name = 'ads/response_detail.html'


class PrivatePageView(LoginRequiredMixin, ListView):
    template_name = 'ads/private_page.html'
    context_object_name = 'adverts'
    paginate_by = 10

    def get_queryset(self):
        user = self.request.user
        return Advert.objects.filter(user=user)


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

    def post(self, request, response_id):
        try:
            response = Response.objects.get(pk=response_id)
        except Response.DoesNotExist:
            return redirect('ads:private')

        response.delete()
        return redirect('ads:private')


class LikeView(View):
    def post(self, request, pk):
        response = get_object_or_404(Response, pk=pk)
        response.likes += 1
        response.save()
        return redirect('ads:advert-detail', pk=response.article.pk)


class DislikeView(View):
    def post(self, request, pk):
        response = get_object_or_404(Response, pk=pk)
        response.dislikes += 1
        response.save()
        return redirect('ads:advert-detail', pk=response.article.pk)
