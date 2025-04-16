from django.core.exceptions import PermissionDenied
from django.http import Http404
from django.shortcuts import render


class AdUpdateOrDelete:
    """Сервисный слой, для обработки запросов с ошибками 403 и 404, иначе, вывод корректной формы."""
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
