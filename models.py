# subscriptions/models.py
from django.db import models
from django.utils.timezone import now

class TierIntersection(models.Model):
    tier_1_id = models.IntegerField()
    tier_2_id = models.IntegerField()
    intersection_count = models.IntegerField(default=0)

    class Meta:
        db_table = 'tierintersection'  # Ensure this matches your table name

class TierUnion(models.Model):
    tier_1_id = models.IntegerField()
    tier_2_id = models.IntegerField()
    union_count = models.IntegerField(default=0)

    class Meta:
        db_table = 'tierunion'  # Ensure this matches your table name


class SubscriberMembership(models.Model):
    SubscriberMembershipID = models.AutoField(primary_key=True)
    SubscriberID = models.ForeignKey('Subscribers', on_delete=models.CASCADE)  # String reference to Subscribers model
    TierID = models.ForeignKey('MembershipTiers', on_delete=models.CASCADE)  # String reference to MembershipTiers model

    class Meta:
        db_table = 'subscribermembership'  # Table name in lowercase


class Subscribers(models.Model):
    SubscriberID = models.AutoField(primary_key=True)
    Name = models.CharField(max_length=255, default="")
    Email = models.CharField(max_length=255, default="")
    MembershipTier = models.CharField(max_length=50, default="Basic")  # Default tier
    JoinDate = models.DateField(default=now)

    class Meta:
        db_table = 'subscribers'  # Table name in lowercase


class MembershipTiers(models.Model):
    TierID = models.AutoField(primary_key=True, default="")
    TierName = models.CharField(max_length=50, default="DefaultTier")  # Default tier name
    Description = models.CharField(max_length=255, null=True, blank=True)
    Price = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        db_table = 'membershiptiers'  # Table name in lowercase

    def __str__(self):
        return self.TierName  # Display the tier name in dropdowns and other representations

