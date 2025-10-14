from django.db import models
from users.models import User
from kirchagroups.models import KirchaGroup

class Payment(models.Model):
    payer = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='payments',
        db_column='payer_id',  
        to_field='user_id'    
    )
    group = models.ForeignKey(KirchaGroup, on_delete=models.CASCADE, related_name='payments')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Payment by {self.payer.full_name} - {self.amount}"
