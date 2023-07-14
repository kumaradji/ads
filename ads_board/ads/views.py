from datetime import datetime

from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.models import Group
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404, render
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, DetailView, ListView, DeleteView, UpdateView
from django.shortcuts import redirect
from django.views import View

from ads_board import settings
from users.models import Profile
from .filters import AdvertFilter
from .forms import PostForm, AdvertForm
from .models import Advert, Response

from django.dispatch import Signal

# Определите сигнал для отправки e-mail
send_response_email_signal = Signal()


# Представление для главной страницы
class AdvertListView(LoginRequiredMixin, ListView):
    model = Advert
    ordering = '-created_at'
    template_name = 'ads/advert_list.html'
    context_object_name = 'advert_list'
    paginate_by = 15

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = AdvertFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_now'] = datetime.utcnow()
        context['is_author'] = self.request.user.groups.filter(name='authors').exists()
        return context


class AdvertCreateView(PermissionRequiredMixin, CreateView):
    raise_exception = True
    permission_required = 'ads.add_advert'
    form_class = PostForm
    model = Advert
    template_name = 'ads/advert_create.html'

    def form_valid(self, form):
        advert = form.save(commit=False)
        advert.user = self.request.user
        advert.author = self.request.user
        advert.save()
        form.instance.author = self.request.user
        form.instance.user = self.request.user

        # Отправка e-mail
        subject = 'Новое объявление'
        message = f'Ваше объявление "{advert.title}" успешно опубликовано.'
        from_email = settings.DEFAULT_FROM_EMAIL
        recipient_list = [self.request.user.email]
        send_mail(subject, message, from_email, recipient_list)

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
    form_class = AdvertForm
    success_url = reverse_lazy('ads:advert-list')


class ResponseCreateView(PermissionRequiredMixin, CreateView):
    raise_exception = True
    permission_required = 'ads.response_create'
    model = Response
    ordering = '-createDate'
    context_object_name = 'responses'
    fields = ['response_text']
    template_name = 'ads/response_create.html'
    paginate_by = 5

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.article = Advert.objects.get(pk=self.kwargs['pk'])

        user_email = 'user@example.com'
        advert_title = 'Название объявления'
        send_response_email_signal.send(
            sender=None,
            user_email=user_email,
            advert_title=advert_title)

        return super().form_valid(form)


class ResponseDetailView(DetailView):
    model = Response
    template_name = 'ads/response_detail.html'


class PrivatePageView(LoginRequiredMixin, View):
    template_name = 'ads/private_page.html'

    def get(self, request):
        user = request.user
        adverts = Advert.objects.filter(user=user)
        responses = Response.objects.filter(advert__user=user)
        is_author = Profile.objects.filter(user=user, is_author=True).exists()

        context = {
            'adverts': adverts,
            'responses': responses,
            'is_author': is_author,
        }
        return render(request, self.template_name, context)

    def post(self, request):
        user = request.user

        if not Profile.objects.filter(user=user, is_author=True).exists():
            author_group = Group.objects.get_or_create(name='Авторы')[0]
            user.groups.add(author_group)
            user.save()
            is_author = True
        else:
            is_author = False

        adverts = Advert.objects.filter(user=user)
        responses = Response.objects.filter(advert__user=user)

        context = {
            'adverts': adverts,
            'responses': responses,
            'is_author': is_author,
        }
        return render(request, self.template_name, context)


class AcceptResponseView(LoginRequiredMixin, View):
    def get(self, request, response_id):
        response = get_object_or_404(Response, pk=response_id)
        response.accepted = True
        response.save()
        return redirect('ads:private')

    def post(self, request, response_id):
        response = get_object_or_404(Response, pk=response_id)
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
