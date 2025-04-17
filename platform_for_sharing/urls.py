from django.urls import path

from platform_for_sharing.apps import PlatformForSharingConfig
from platform_for_sharing.views import HomeView, AdCreateView, AdDetailView, AdUpdateView, AdDeleteView, AdListView, \
    ExchangeProposalCreateView, ExchangeProposalListView, ExchangeProposalDetailView

app_name = PlatformForSharingConfig.name

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
]
