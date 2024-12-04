from django import forms
from .models import Subscribers, SubscriberMembership
class SubscriberMembershipForm(forms.ModelForm):
    class Meta:
        model = SubscriberMembership
        fields = ['SubscriberID', 'TierID']

# subscriptions/forms.py
from django import forms
from .models import Subscribers, MembershipTiers

class SubscribersForm(forms.ModelForm):
    class Meta:
        model = Subscribers
        fields = ['Name', 'Email', 'MembershipTier']

    MembershipTier = forms.ModelChoiceField(queryset=MembershipTiers.objects.all(), empty_label="Select a Membership Tier")
