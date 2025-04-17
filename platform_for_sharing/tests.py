from django.test import TestCase, Client
from django.urls import reverse
from platform_for_sharing.models import Ad, ExchangeProposal
from django.http import Http404

from users.models import User


class ViewTests(TestCase):

    def setUp(self):
        # Создаем пользователей
        self.user1 = User.objects.create_user(username='user1', password='pass')
        self.user2 = User.objects.create_user(username='user2', password='pass')
        self.client = Client()

        # Создаем объявления
        self.ad1 = Ad.objects.create(title='Объявление 1', description='desc', user=self.user1, category='cat', condition='new')
        self.ad2 = Ad.objects.create(title='Объявление 2', description='desc', user=self.user2, category='cat', condition='used')

        # Создаем предложение об обмене
        self.exchange = ExchangeProposal.objects.create(
            ad_sender_id=self.ad1,
            ad_receiver_id=self.ad2,
            comment='Обмен',
            status='ожидает'
        )

    def test_home_view(self):
        response = self.client.get(reverse('platform_for_sharing:home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Объявление 1')

    def test_ad_list_view_authenticated(self):
        self.client.login(username='user1', password='pass')
        response = self.client.get(reverse('platform_for_sharing:ad_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Объявление 1')
        self.assertNotContains(response, 'Объявление 2')  # только свои объявления

    def test_ad_create_and_detail(self):
        self.client.login(username='user1', password='pass')
        response = self.client.post(reverse('platform_for_sharing:ad_create'), {
            'title': 'Новое объявление',
            'description': 'desc',
            'category': 'cat',
            'condition': 'new'
        })
        self.assertEqual(response.status_code, 200)

    def test_ad_update_permission(self):
        self.client.login(username='user1', password='pass')
        # Попытка редактировать чужое объявление
        response = self.client.get(reverse('platform_for_sharing:ad_update', args=[self.ad2.pk]))
        self.assertEqual(response.status_code, 403)

        # Редактировать свое объявление
        response = self.client.get(reverse('platform_for_sharing:ad_update', args=[self.ad1.pk]))
        self.assertEqual(response.status_code, 200)

    def test_exchange_detail_and_post_accept(self):
        self.client.login(username='user1', password='pass')
        url = reverse('platform_for_sharing:exchange_detail', args=[self.exchange.pk])
        # Проверка доступа
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        # Одобрение обмена (принятие)
        response = self.client.post(url, {'action': 'accept'})
        self.exchange.refresh_from_db()
        self.assertEqual(self.exchange.status, 'принят')

        # Проверка, что владельцы поменялись
        self.ad1.refresh_from_db()
        self.ad2.refresh_from_db()
        self.assertEqual(self.ad1.user, self.user2)
        self.assertEqual(self.ad2.user, self.user1)

    def test_exchange_reject(self):
        self.client.login(username='user2', password='pass')
        url = reverse('platform_for_sharing:exchange_detail', args=[self.exchange.pk])
        response = self.client.post(url, {'action': 'reject'})
        self.exchange.refresh_from_db()
        self.assertEqual(self.exchange.status, 'отклонён')

    def test_exchange_access_for_non_participant(self):
        # Создаем другого пользователя, который не участник
        user3 = User.objects.create_user(username='user3', password='pass')
        self.client.login(username='user3', password='pass')
        url = reverse('platform_for_sharing:exchange_detail', args=[self.exchange.pk])
        response = self.client.post(url, {'action': 'accept'})
        self.assertEqual(response.status_code, 403)

    def test_delete_ad_permission(self):
        self.client.login(username='user1', password='pass')
        response = self.client.get(reverse('platform_for_sharing:ad_delete', args=[self.ad1.pk]))
        self.assertEqual(response.status_code, 200)

        # Попытка удалить чужое объявление
        response = self.client.get(reverse('platform_for_sharing:ad_delete', args=[self.ad2.pk]))
        self.assertEqual(response.status_code, 403)

    def test_delete_ad_success(self):
        self.client.login(username='user1', password='pass')
        response = self.client.post(reverse('platform_for_sharing:ad_delete', args=[self.ad1.pk]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Ad.objects.filter(pk=self.ad1.pk).exists())
