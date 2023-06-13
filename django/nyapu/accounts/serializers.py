from rest_framework import serializers
from accounts.models import CustomUser, Relationship


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username']


class RelationshipSerializer(serializers.ModelSerializer):
    follower = CustomUserSerializer()
    following = CustomUserSerializer()

    class Meta:
        model = Relationship
        fields = ['id', 'follower', 'following']
