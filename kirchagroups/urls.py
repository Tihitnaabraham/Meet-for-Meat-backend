from django.urls import path
from .views import KirchaGroupCreateView, JoinGroupView, InviteMemberView

urlpatterns = [
    path('groups/create/', KirchaGroupCreateView.as_view(), name='create_kircha_group'),
    path('groups/join/', JoinGroupView.as_view(), name='join_kircha_group'),
    path('groups/invite/', InviteMemberView.as_view(), name='invite_kircha_member'),
    path('groups/invite/<uuid:invite_code>/', InviteMemberView.as_view(), name='invite_kircha_member_detail'),
]
