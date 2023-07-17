from datetime import datetime

from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.models import Group
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, DetailView, ListView, DeleteView, UpdateView, View

from ads_board import settings
from users.models import Profile
from .filters import AdvertFilter
from .forms import PostForm, AdvertForm
from .models import Advert, Response

from django.dispatch import Signal

# Define a signal for sending email
send_response_email_signal = Signal()


# View for the homepage
class AdvertListView(LoginRequiredMixin, ListView):
    """
    View representing the list of advertisements.
    """
    model = Advert
    ordering = '-created_at'
    template_name = 'ads/advert_list.html'
    context_object_name = 'advert_list'
    paginate_by = 15

    def get_queryset(self):
        """
        Get the queryset of advertisements, filtered by user input.
        """
        queryset = super().get_queryset()
        self.filterset = AdvertFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        """
        Get the additional context data for the template.
        """
        context = super().get_context_data(**kwargs)
        context['time_now'] = datetime.utcnow()
        context['is_author'] = self.request.user.groups.filter(name='authors').exists()
        return context


class AdvertCreateView(PermissionRequiredMixin, CreateView):
    """
    View for creating an advertisement.
    """
    raise_exception = True
    permission_required = 'ads.add_advert'
    form_class = PostForm
    model = Advert
    template_name = 'ads/advert_create.html'

    def form_valid(self, form):
        """
        Save the form data and send an email notification.
        """
        advert = form.save(commit=False)
        advert.user = self.request.user
        advert.author = self.request.user
        advert.save()
        form.instance.author = self.request.user
        form.instance.user = self.request.user

        # Send email
        subject = 'Новое объявление'
        message = f'Ваше объявление "{advert.title}" успешно опубликовано.'
        from_email = settings.DEFAULT_FROM_EMAIL
        recipient_list = [self.request.user.email]
        send_mail(subject, message, from_email, recipient_list)

        return super().form_valid(form)

    def get_success_url(self):
        """
        Get the URL to redirect to after successful form submission.
        """
        return reverse('ads:advert-detail', kwargs={'pk': self.object.pk})


class AdvertDetailView(DetailView):
    """
    View representing the details of an advertisement.
    """
    model = Advert
    template_name = 'ads/advert_detail.html'


class AdvertDeleteView(DeleteView):
    """
    View for deleting an advertisement.
    """
    model = Advert
    template_name = 'ads/advert_delete.html'
    success_url = reverse_lazy('ads:advert-list')


class AdvertUpdateView(UpdateView):
    """
    View for updating an advertisement.
    """
    model = Advert
    template_name = 'ads/advert_update.html'
    form_class = AdvertForm
    success_url = reverse_lazy('ads:advert-list')


class ResponseCreateView(PermissionRequiredMixin, CreateView):
    """
    View for creating a response to an advertisement.
    """
    raise_exception = True
    permission_required = 'ads.response_create'
    model = Response
    ordering = '-created_at'
    context_object_name = 'responses'
    fields = ['response_text']
    template_name = 'ads/response_create.html'
    paginate_by = 5

    def form_valid(self, form):
        """
        Save the form data and send a signal for sending email.
        """
        form.instance.author = self.request.user
        form.instance.advert = Advert.objects.get(pk=self.kwargs['pk'])
        form.instance.user = self.request.user

        user_email = self.request.user.email
        advert_title = form.instance.advert.title
        send_response_email_signal.send(
            sender=None,
            user_email=user_email,
            advert_title=advert_title
        )

        return super().form_valid(form)


class ResponseDetailView(DetailView):
    """
    View representing the details of a response.
    """
    model = Response
    template_name = 'ads/response_detail.html'


class PrivatePageView(LoginRequiredMixin, View):
    """
    View for the private page of the user.
    """
    template_name = 'ads/private_page.html'

    def get(self, request):
        """
        Handle GET request for the private page.
        """
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
        """
        Handle POST request for the private page.
        """
        user = request.user

        if not Profile.objects.filter(user=user, is_author=True).exists():
            author_group = Group.objects.get_or_create(name='authors')[0]
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
    """
    View for accepting a response.
    """

    def get(self, request, response_id):
        """
        Handle GET request for accepting a response.
        """
        response = get_object_or_404(Response, pk=response_id)
        response.accepted = True
        response.save()
        return redirect('ads:private')

    def post(self, request, response_id):
        """
        Handle POST request for accepting a response.
        """
        response = get_object_or_404(Response, pk=response_id)
        response.accepted = True
        response.save()
        return redirect('ads:private')


class DeleteResponseView(LoginRequiredMixin, View):
    """
    View for deleting a response.
    """

    def get(self, request, response_id):
        """
        Handle GET request for deleting a response.
        """
        response = Response.objects.get(pk=response_id)
        response.delete()
        return redirect('ads:private')

    def post(self, request, response_id):
        """
        Handle POST request for deleting a response.
        """
        try:
            response = Response.objects.get(pk=response_id)
        except Response.DoesNotExist:
            return redirect('ads:private')

        response.delete()
        return redirect('ads:private')


class LikeView(View):
    """
    View for liking a response.
    """

    def post(self, request, pk):
        """
        Handle POST request for liking a response.
        """
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
