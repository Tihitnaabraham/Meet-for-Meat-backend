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

# class IsOrganizerOrAdmin(BasePermission):
#     def has_permission(self, request, view):
#         user = request.user
#         if not user.is_authenticated:
#             return False
#         if user.user_type == 'admin':
#             return True
#         group_id = request.data.get('group_id') or request.query_params.get('group_id')
#         if group_id:
#             from .models import KirchaGroup
#             try:
#                 group = KirchaGroup.objects.get(id=group_id)
#             except KirchaGroup.DoesNotExist:
#                 return False
#             return group.organizer_id == user.pk
#         return False
