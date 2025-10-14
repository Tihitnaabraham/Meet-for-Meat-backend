from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .models import KirchaGroup, GroupMember, GroupInvitation
from .serializers import KirchaGroupSerializer, GroupMemberSerializer, GroupInvitationSerializer
from .permissions import CanJoinGroup 


class KirchaGroupCreateView(generics.CreateAPIView):
    queryset = KirchaGroup.objects.all()
    serializer_class = KirchaGroupSerializer
    permission_classes = [permissions.IsAuthenticated ]

class JoinGroupView(generics.CreateAPIView):
    serializer_class = GroupMemberSerializer
    permission_classes = [permissions.IsAuthenticated, CanJoinGroup]

    def create(self, request, *args, **kwargs):
        if not request.user:
            return Response({"detail": "Authentication credentials were not provided."}, status=401)
        data = request.data.copy()
        data['user'] = request.user.pk
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        group = serializer.validated_data['group']
        if not group.can_add_member():
            return Response({"detail": "Group is full."}, status=400)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class InviteMemberView(generics.CreateAPIView):
    serializer_class = GroupInvitationSerializer
    permission_classes = [permissions.IsAuthenticated ]

    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        data['invited_by'] = request.user.pk
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
