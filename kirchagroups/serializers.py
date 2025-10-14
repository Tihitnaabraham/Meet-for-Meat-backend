from rest_framework import serializers
from .models import KirchaGroup, GroupMember, GroupInvitation

class KirchaGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = KirchaGroup
        fields = '__all__'

class GroupMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = GroupMember
        fields = '__all__'

class GroupInvitationSerializer(serializers.ModelSerializer):
    class Meta:
        model = GroupInvitation
        fields = '__all__'
