from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.db.models import Q
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView

from platform_for_sharing.forms import AdForm, ExchangeProposalForm
from platform_for_sharing.models import Ad, ExchangeProposal
from platform_for_sharing.services import AdUpdateOrDelete


class HomeView(ListView):
    """Представление домашней страницы с выводом всех объявлений пользователя."""
    model = Ad
    template_name = "platform_for_sharing/home.html"
    context_object_name = "ads"

    def get_context_data(self, **kwargs):
        categories_list = list()
        for obj in Ad.objects.all():
            categories_list.append(obj.category)

        context = super().get_context_data(**kwargs)
        context['categories'] = categories_list
        return context

    def get_queryset(self):
        qs = super().get_queryset()

        category = self.request.GET.get('category')
        conditions = self.request.GET.getlist('condition')
        search = self.request.GET.get('search', '').strip()

        if search:
            qs = qs.filter(
                Q(title__icontains=search) | Q(description__icontains=search)
            )
        if category and category != 'Выберите категорию':
            qs = qs.filter(category=category)
        if conditions:
            qs = qs.filter(condition__in=conditions)

        return qs


class AdListView(LoginRequiredMixin, ListView):
    """Представление домашней страницы с выводом всех объявлений пользователя."""
    model = Ad
    template_name = "platform_for_sharing/ad_list.html"
    context_object_name = "ads"

    def get_queryset(self):
        """Получаем объявления текущего пользователя."""
        if self.request.user.is_authenticated:
            return Ad.objects.filter(user=self.request.user)


class AdCreateView(LoginRequiredMixin, CreateView):
    """Представление создания модели объявления."""
    model = Ad
    template_name = "platform_for_sharing/ad_create.html"
    context_object_name = "ad"
    form_class = AdForm

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('platform_for_sharing:ad_detail', args=[self.object.pk])


class AdDetailView(LoginRequiredMixin, DetailView):
    """Представление просмотра объявления."""
    model = Ad
    template_name = "platform_for_sharing/ad_detail.html"
    context_object_name = "ad"


class AdUpdateView(AdUpdateOrDelete, LoginRequiredMixin, UpdateView):
    """Контроллер изменения объявления."""
    model = Ad
    template_name = "platform_for_sharing/ad_create.html"
    context_object_name = "ad_create"

    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('platform_for_sharing:ad_detail', args=[self.kwargs.get('pk')])

    def get_form_class(self):
        """
        Проверка чтобы пользователь был владельцем продукта и тогда может его изменять.
        """
        super().get_form_class()


class AdDeleteView(AdUpdateOrDelete, LoginRequiredMixin, DeleteView):
    """Контроллер удаления объявления."""
    model = Ad
    context_object_name = "ad_delete"
    success_url = reverse_lazy("platform_for_sharing:home")

    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)

    def get_form_class(self):
        super().get_form_class()


class ExchangeProposalListView(LoginRequiredMixin, ListView):
    """Список всех предложений об обмене."""
    model = ExchangeProposal
    template_name = "platform_for_sharing/exchange_list.html"
    context_object_name = "exchanges"

    # def get_queryset(self):
    #     if self.request.user.is_authenticated:
    #         return ExchangeProposal.objects.filter(user=self.request.ad_sender_id.user)


class ExchangeProposalCreateView(LoginRequiredMixin, CreateView):
    """Представление создание обмена объявлениями."""
    model = ExchangeProposal
    template_name = "platform_for_sharing/exchange_create.html"
    context_object_name = "exchange"
    success_url = reverse_lazy("platform_for_sharing:exchange_list")
    form_class = ExchangeProposalForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs
