from django.db import models

from users.models import User


class Ad(models.Model):
    """Модель объявления."""

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="ads", verbose_name="владелец")
    title = models.CharField(max_length=100, verbose_name="Название")
    description = models.TextField(verbose_name="Описание товара")
    image_url = models.URLField(max_length=200, verbose_name="url изображения", blank=True, null=True)
    category = models.CharField(max_length=100, verbose_name="Категория")
    condition = models.CharField(max_length=5, verbose_name="Состояние", choices=[("новый", "новый"), ("б/у", "б/у")])
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Объявление"
        verbose_name_plural = "Объявления"


class ExchangeProposal(models.Model):
    """Класс предложений для обмена объявлениями."""
    CHOICES = [
        ("ожидает", "ожидает"),
        ("принят", "принят"),
        ("отклонён", "отклонён")
    ]

    ad_sender_id = models.ForeignKey(Ad, on_delete=models.CASCADE, related_name="senders", verbose_name="что меняем")
    ad_receiver_id = models.ForeignKey(Ad, on_delete=models.CASCADE, related_name="receivers",
                                       verbose_name="на что меняем")
    comment = models.TextField(verbose_name="комментарий")
    status = models.CharField(max_length=8, choices=CHOICES, default="ожидает", verbose_name="статус")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"'{self.ad_sender_id.title}' обмен на '{self.ad_receiver_id.title}'"

    class Meta:
        verbose_name = "Объявление"
        verbose_name_plural = "Объявления"
