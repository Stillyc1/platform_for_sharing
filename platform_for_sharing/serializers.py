from rest_framework.serializers import ModelSerializer

from platform_for_sharing.models import Ad, ExchangeProposal


class AdSerializer(ModelSerializer):
    """Класс сериализатор привычки."""

    class Meta:
        model = Ad
        fields = "__all__"


class AdCreateSerializer(ModelSerializer):
    """Класс сериализатор привычки."""

    class Meta:
        model = Ad
        exclude = ("user",)


class ExchangeProposalSerializer(ModelSerializer):
    """Класс сериализатор привычки."""

    class Meta:
        model = ExchangeProposal
        fields = ("id", "ad_sender_id", "ad_receiver_id", "comment",)


class ExchangeProposalUpdateSerializer(ModelSerializer):
    """Класс сериализатор привычки."""

    class Meta:
        model = ExchangeProposal
        fields = ("status",)
