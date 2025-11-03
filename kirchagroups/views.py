from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .models import KirchaGroup, GroupMember, GroupInvitation
from .serializers import KirchaGroupSerializer, GroupMemberSerializer, GroupInvitationSerializer
from .permissions import CanJoinGroup 

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated


class KirchaGroupCreateView(generics.ListCreateAPIView):
    queryset = KirchaGroup.objects.all()
    serializer_class = KirchaGroupSerializer
   


class JoinGroupView(generics.ListCreateAPIView):
    queryset = GroupMember.objects.all()
    serializer_class = GroupMemberSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return GroupMember.objects.filter(user=user)

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

class InviteMemberView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = GroupInvitationSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.validated_data['invited_by'] = request.user
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, invite_code=None):
        if not invite_code:
            return Response({"error": "Invite code is required"}, status=status.HTTP_400_BAD_REQUEST)
        serializer = GroupInvitationSerializer( context={'request': request})
        return Response(serializer.data)
class GroupMembersListView(generics.ListAPIView):
    serializer_class = GroupMemberSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        group_id = self.kwargs['group_id']
        return GroupMember.objects.filter(group_id=group_id)
