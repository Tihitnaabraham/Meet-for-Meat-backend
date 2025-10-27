from rest_framework.permissions import BasePermission
from .models import KirchaGroup, GroupMember


class CanJoinGroup(BasePermission):

    def has_permission(self, request, view):
        group_id = request.data.get('group_id') or request.data.get('group')
        user = request.user
        try:
            group = KirchaGroup.objects.get(id=group_id)
        except KirchaGroup.DoesNotExist:
            return False

        if group.privacy == 'public':
            return True
        membership = GroupMember.objects.filter(group=group, user=user, is_approved=True).first()
        return membership is not None


