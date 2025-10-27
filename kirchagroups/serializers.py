from rest_framework import serializers
from .models import KirchaGroup, GroupMember, GroupInvitation

# class KirchaGroupSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = KirchaGroup
#         fields = '__all__'

class KirchaGroupSerializer(serializers.ModelSerializer):
    current_members = serializers.SerializerMethodField()

    class Meta:
        model = KirchaGroup
        fields = '__all__'

    def get_current_members(self, obj):
        return obj.members.filter(is_approved=True).count()
 

class GroupMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = GroupMember
        fields = '__all__'

# class GroupInvitationSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = GroupInvitation
#         fields = '__all__'
class GroupInvitationSerializer(serializers.ModelSerializer):
    invite_link = serializers.SerializerMethodField()

    class Meta:
        model = GroupInvitation
        fields = ['id', 'group', 'invited_user', 'invited_by', 'invite_code', 'invite_link', 'is_accepted', 'invited_at', 'responded_at']
        read_only_fields = ['invited_by', 'invite_code', 'invited_at', 'responded_at']

    def get_invite_link(self, obj):
        # Use local frontend URL since frontend is not hosted
        base_url = 'http://localhost:3000'
        return f"{base_url}/invite/{obj.invite_code}"

    def validate(self, data):
        group = data.get('group')
        if group and group.privacy != 'private':
            raise serializers.ValidationError("Invitations can only be created for private groups.")
        return data