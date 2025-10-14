from django.db import models
from django.utils import timezone
from users.models import User
from livestock.models import Livestock

class KirchaGroup(models.Model):
    GROUP_TYPES = [('Half Kircha', 'Half Kircha'), ('Full Kircha', 'Full Kircha')]
    SLAUGHTER_METHODS = [('self-slaughter', 'Self Slaughter'), ('company-managed', 'Company Managed')]
    STATUS_CHOICES = [('open', 'Open'), ('closed', 'Closed')]
    PRIVACY_CHOICES = [('public', 'Public'), ('private', 'Private')]

    organizer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="organized_kircha_groups")
    livestock = models.ForeignKey(Livestock, on_delete=models.CASCADE, related_name="kircha_group")
    group_type = models.CharField(max_length=50, choices=GROUP_TYPES)
    max_members = models.IntegerField()
    group_name = models.CharField(max_length=50, blank=True, null=True)
    slaughter_date = models.DateField()
    slaughter_time = models.TimeField()
    slaughter_method = models.CharField(max_length=50, choices=SLAUGHTER_METHODS)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES)
    privacy = models.CharField(max_length=20, choices=PRIVACY_CHOICES, default='public')

    price_half = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    price_full = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.group_name if self.group_name else f"Kircha Group {self.id}"

    def can_add_member(self):
        return self.members.count() < self.max_members



PAYMENT_STATUS_CHOICES = [
    ('pending', 'Pending'),
    ('paid', 'Paid'),
    ('failed', 'Failed'),
]

class GroupMember(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="group_memberships")
    group = models.ForeignKey(KirchaGroup, on_delete=models.CASCADE, related_name="members")
    member_full_name = models.CharField(max_length=50)
    member_phone_number = models.CharField(max_length=50)
    member_delivery_address = models.CharField(max_length=100)
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES)
    invited_by = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, related_name='invitations_sent')
    is_approved = models.BooleanField(default=False)
    joined_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.member_full_name

class GroupInvitation(models.Model):
    group = models.ForeignKey(KirchaGroup, on_delete=models.CASCADE, related_name='invitations')
    invited_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='group_invitations')
    invited_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_invitations')
    is_accepted = models.BooleanField(default=False)
    invited_at = models.DateTimeField(auto_now_add=True)
    responded_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Invite: {self.invited_user} to {self.group} by {self.invited_by}"
