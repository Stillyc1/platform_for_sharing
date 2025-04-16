import re

from django.forms import ModelForm

from platform_for_sharing.models import Ad, ExchangeProposal


class AdForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super(AdForm, self).__init__(*args, **kwargs)

        self.fields['title'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Как называется ваш товар?'
        })
        self.fields['category'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Категория товара'
        })
        self.fields['description'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Описание'
        })
        self.fields['image_url'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Ссылка на фото'
        })
        self.fields['condition'].widget.attrs.update({
            'class': 'form-select',
            'placeholder': 'Состояние'
        })

    class Meta:
        model = Ad
        fields = ('title', 'category', 'description', 'image_url', 'condition',)
        exclude = ('user',)

    def clean_image_url(self):
        """Валидация изображения"""
        cleaned_data = super().clean()
        image_url = cleaned_data.get('image_url')

        if image_url and not re.search("https://\\S+", image_url):
            self.add_error('image_url', f'Изображение должно быть ссылкой на фото и начинаться с https://')


class ExchangeProposalForm(ModelForm):

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(ExchangeProposalForm, self).__init__(*args, **kwargs)

        if user:
            self.fields["ad_sender_id"].queryset = Ad.objects.filter(user=user)

        self.fields['ad_sender_id'].widget.attrs.update({
            'class': 'form-select',
        })
        self.fields['ad_receiver_id'].widget.attrs.update({
            'class': 'form-control',
            'aria-label': 'Disabled select example',
            'disabled': 'disabled',
        })
        self.fields['comment'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Комментарий'
        })

    class Meta:
        model = ExchangeProposal
        fields = ('ad_sender_id', 'ad_receiver_id', 'comment',)
