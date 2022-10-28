from rest_framework import serializers

from .models import Test


class TestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Test
        fields = ['code', 'name', 'unit', 'upper', 'lower', 'ideal_range']
        required_fields = ['name', 'unit']
        read_only_fields = ['code']


class TestCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Test
        fields = ['code', 'name', 'unit', 'upper', 'lower', 'ideal_range']
        required_fields = ['name', 'unit']

    # def validate(self, attrs):
    #     if 'upper' and 'lower' not in attrs:
    #         raise serializers.ValidationError('Lower and upper cannot both be null')
    #     if attrs['upper'] and attrs['upper'] < (attrs['lower'] or 0):
    #         return serializers.ValidationError("Lower value can't exceed upper value")
    #     return attrs
