from django.urls import path
from rest_framework.permissions import IsAuthenticated
from rest_framework.routers import DefaultRouter

from platform_for_sharing.apps import PlatformForSharingConfig
from platform_for_sharing.views import HomeView, AdCreateView, AdDetailView, AdUpdateView, AdDeleteView, AdListView, \
    ExchangeProposalCreateView, ExchangeProposalListView, ExchangeProposalDetailView, AdViewSet, AdListAPIView, \
    ExchangeProposalCreateAPIView, ExchangeProposalUpdateAPIView, ExchangeProposalListAPIView

app_name = PlatformForSharingConfig.name
router = DefaultRouter()
router.register(prefix=r"ad", viewset=AdViewSet, basename='ad')

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("ad_list/", AdListView.as_view(), name="ad_list"),
    path("ad_create/", AdCreateView.as_view(), name="ad_create"),
    path("ad_<int:pk>/", AdDetailView.as_view(), name="ad_detail"),
    path('ad_<int:pk>/update/', AdUpdateView.as_view(), name='ad_update'),
    path('ad_<int:pk>/delete/', AdDeleteView.as_view(), name='ad_delete'),

    path('exchange_list/', ExchangeProposalListView.as_view(), name='exchange_list'),
    path('exchange_create/', ExchangeProposalCreateView.as_view(), name='exchange_create'),
    path('exchange_<int:pk>/', ExchangeProposalDetailView.as_view(), name='exchange_detail'),

    path('ad_api_list/', AdListAPIView.as_view(), name='ad_api_list'),
    path('exchange_api_create/', ExchangeProposalCreateAPIView.as_view(), name='exchange_api_create'),
    path('exchange_api_update/<int:pk>/', ExchangeProposalUpdateAPIView.as_view(), name='exchange_api_update'),
    path('exchange_api_list/', ExchangeProposalListAPIView.as_view(), name='exchange_api_list'),
] + router.urls
