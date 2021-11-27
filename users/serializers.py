from rest_framework_gis.serializers import GeoModelSerializer

from .models import SearchSetting, User
from core.serializers import AddressSerializer


class UserSerializer(GeoModelSerializer):
    address = AddressSerializer(many=False, read_only=True)
        
    class Meta:
        model = User
        fields = (
            'id',
            'telegram_user_id',
            'telegram_chat_id',
            'telegram_username',
            'username',
            'type',
            'first_name',
            'last_name',
            'photo',
            'location',
            'is_verified',
            'date_joined',
            'address',
        )

    def create(self, validated_data):
        user = User(
            telegram_user_id=validated_data['telegram_user_id'],
            telegram_chat_id=validated_data['telegram_chat_id'],
            telegram_username=validated_data['telegram_username'],
            username=validated_data['telegram_username'],
            type=User.REGULAR,
            first_name=validated_data['first_name'],
        )
        if 'last_name' in validated_data:
            user.last_name = validated_data['last_name']

        user.is_staff = False
        user.is_verified = False
        user.set_password(validated_data['telegram_user_id'])
        user.save()

        return user


class SearchSettingSerializer(GeoModelSerializer):
    
    class Meta:
        model = SearchSetting
        exclude = ['user']