from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.db.models import Q
from django.http import HttpResponseForbidden, Http404
from django.shortcuts import redirect, render
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


class AdUpdateView(LoginRequiredMixin, UpdateView):
    """Контроллер изменения объявления."""
    model = Ad
    template_name = "platform_for_sharing/ad_create.html"
    context_object_name = "ad_create"
    form_class = AdForm

    def get(self, request, *args, **kwargs):
        try:
            return super().get(request, *args, **kwargs)
        except Http404:
            return render(request, 'platform_for_sharing/403_or_404.html', status=404)
        except PermissionDenied:
            return render(request, 'platform_for_sharing/403_or_404.html', status=403)

    def get_form_class(self):
        user = self.request.user
        if user == self.object.user:
            return super().get_form_class()
        raise PermissionDenied

    def get_success_url(self):
        return reverse('platform_for_sharing:ad_detail', args=[self.kwargs.get('pk')])


class AdDeleteView(LoginRequiredMixin, DeleteView):
    """Контроллер удаления объявления."""
    model = Ad
    context_object_name = "ad_delete"
    success_url = reverse_lazy("platform_for_sharing:home")

    def get(self, request, *args, **kwargs):
        try:
            return super().get(request, *args, **kwargs)
        except Http404:
            return render(request, 'platform_for_sharing/403_or_404.html', status=404)
        except PermissionDenied:
            return render(request, 'platform_for_sharing/403_or_404.html', status=403)

    def get_form_class(self):
        user = self.request.user
        if user == self.object.user:
            return super().get_form_class()
        raise PermissionDenied


class ExchangeProposalListView(LoginRequiredMixin, ListView):
    """Список всех предложений об обмене."""
    model = ExchangeProposal
    template_name = "platform_for_sharing/exchange_list.html"
    context_object_name = "exchanges"

    def get_context_data(self, *, object_list=None, **kwargs):
        user = self.request.user
        context = super().get_context_data(**kwargs)

        context["ad_sender_id"] = ExchangeProposal.objects.filter(ad_sender_id__user=user)
        context["ad_receiver_id"] = ExchangeProposal.objects.filter(ad_receiver_id__user=user)

        return context

    def get_queryset(self):
        user = self.request.user
        return ExchangeProposal.objects.filter(
            Q(ad_sender_id__user=user) |
            Q(ad_receiver_id__user=user)
        )


class ExchangeProposalCreateView(LoginRequiredMixin, CreateView):
    """Представление создание обмена объявлениями."""
    model = ExchangeProposal
    template_name = "platform_for_sharing/exchange_create.html"
    context_object_name = "exchange"
    success_url = reverse_lazy("platform_for_sharing:exchange_list")
    form_class = ExchangeProposalForm

    def get_initial(self):
        """В GET запросе забираем pk объекта Ad и по дефолту устанавливаем в форме для обмена."""
        initial = super().get_initial()
        ad_id = self.request.GET.get('ad_id')
        if ad_id:
            initial['ad_receiver_id'] = ad_id
        return initial

    def form_valid(self, form):
        """В GET запросе забираем pk объекта Ad и передаем в форму для создания."""
        if form.instance.pk is None:
            ad_id = self.request.GET.get('ad_id')
            if ad_id:
                form.instance.ad_receiver_id = Ad.objects.get(pk=ad_id)
        return super().form_valid(form)

    def get_form_kwargs(self):
        """Передаем в форму текущего пользователя,
        чтобы предоставить выбор на обмен товаров текущего пользователя."""
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs


class ExchangeProposalDetailView(LoginRequiredMixin, DetailView):
    """Представление просмотра обмена."""
    model = ExchangeProposal
    template_name = "platform_for_sharing/exchange_detail.html"
    context_object_name = "exchange"

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        exchange = self.object

        # Проверяем, что пользователь участвует в обмене
        if request.user != exchange.ad_sender_id.user and request.user != exchange.ad_receiver_id.user:
            return HttpResponseForbidden()

        action = request.POST.get('action')

        if action == 'accept':
            # Меняем статус
            exchange.status = 'принят'
            # Меняем местами ad_sender_id и ad_receiver_id
            sender = Ad.objects.get(pk=exchange.ad_sender_id.pk)
            sender.user = exchange.ad_receiver_id.user
            sender.save()

            receiver = Ad.objects.get(pk=exchange.ad_receiver_id.pk)
            receiver.user = exchange.ad_sender_id.user
            receiver.save()
        elif action == 'reject':
            exchange.status = 'отклонён'

        exchange.save()
        return redirect('platform_for_sharing:exchange_list')
