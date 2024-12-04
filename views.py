from django.shortcuts import render, redirect
from django.db.models import Count, Q
from django.db import connection
from .models import SubscriberMembership, MembershipTiers
from .forms import SubscribersForm
from django.http import HttpResponse

def home(request):
    return render(request, 'subscriptions/home.html')


def update_intersection_and_union():
    with connection.cursor() as cursor:
        try:
            cursor.execute('''
            -- Update intersection counts
                UPDATE TierIntersection
                SET intersection_count = (
                SELECT COUNT(DISTINCT sm.SubscriberID_id)
                FROM subscribermembership sm
                WHERE sm.TierID_id = TierIntersection.tier_1_id
                AND sm.SubscriberID_id IN (
                    SELECT SubscriberID_id FROM subscribermembership WHERE TierID_id = TierIntersection.tier_2_id
                )
            )
            WHERE EXISTS (
                SELECT 1
                FROM subscribermembership sm
                WHERE sm.TierID_id = TierIntersection.tier_1_id
                AND sm.SubscriberID_id IN (
                    SELECT SubscriberID_id FROM subscribermembership WHERE TierID_id = TierIntersection.tier_2_id
                )
            );

            -- Update union counts
            UPDATE TierUnion
            SET union_count = (
                SELECT COUNT(DISTINCT sm.SubscriberID_id)
                FROM subscribermembership sm
                WHERE sm.TierID_id = TierUnion.tier_1_id
                OR sm.TierID_id = TierUnion.tier_2_id
            )
            WHERE EXISTS (
                SELECT 1
                FROM subscribermembership sm
                WHERE sm.TierID_id = TierUnion.tier_1_id
                OR sm.TierID_id = TierUnion.tier_2_id
            );
        ''')
            connection.commit()  # Make sure to commit
        except Exception as e:
            print(f"Error executing raw SQL: {e}")
            connection.rollback()  # Rollback in case of error


def add_subscriber(request):
    if request.method == 'POST':
        form = SubscribersForm(request.POST)
        if form.is_valid():
            subscriber = form.save()  # Save the subscriber

            # Create the SubscriberMembership
            tier = form.cleaned_data['MembershipTier']
            SubscriberMembership.objects.create(
                SubscriberID=subscriber,  # Reference the saved subscriber
                TierID=tier  # Reference the selected tier
            )

        return redirect('calculate')  # Change this to the URL name for your calculate view

    else:
        form = SubscribersForm()

    return render(request, 'subscriptions/add_subscriber.html', {'form': form})
    #         # Update intersection and union tables after saving
    #         update_intersection_and_union()

    #         return redirect('home')  # Redirect after saving
    # else:
    #     form = SubscribersForm()
    # return redirect('calculate')

def subscriber_form(request):
    if request.method == 'POST':
        form = SubscribersForm(request.POST)
        if form.is_valid():
            # Save the new subscriber
            new_subscriber = form.save()

            # Assign the chosen membership tier
            tier_name = form.cleaned_data['MembershipTier']
            tier = MembershipTiers.objects.get(TierName=tier_name)

            # Create the SubscriberMembership entry
            SubscriberMembership.objects.create(SubscriberID=new_subscriber, TierID=tier)

            # Redirect to the results page after successful submission
            return redirect('subscriptions:calculate_unique_subscriptions')
    else:
        form = SubscribersForm()

    return render(request, 'subscriptions/add_subscriber.html', {'form': form})


def calculate_unique_subscriptions(request):
    with connection.cursor() as cursor:
        # Fetch the count of unique subscribers for Basic membership
        cursor.execute('''
            SELECT COUNT(DISTINCT subscriberid) AS basic_count
            FROM subscribers
            WHERE MembershipTier = 'Basic';
        ''')
        basic_count = cursor.fetchone()[0]

        # Fetch the count of unique subscribers for VIP membership
        cursor.execute('''
            SELECT COUNT(DISTINCT subscriberid) AS vip_count
            FROM subscribers
            WHERE MembershipTier = 'VIP';
        ''')
        vip_count = cursor.fetchone()[0]

        # Fetch the count of unique subscribers for Premium membership
        cursor.execute('''
            SELECT COUNT(DISTINCT subscriberid) AS premium_count
            FROM subscribers
            WHERE MembershipTier = 'Premium';
        ''')
        premium_count = cursor.fetchone()[0]

        # Count subscribers with both Basic and VIP memberships
        cursor.execute('''
            SELECT COUNT(*) AS basic_vip_count
            FROM (
                SELECT COUNT(DISTINCT name)
                FROM subscribers
                WHERE MembershipTier IN ('Basic', 'VIP')
                GROUP BY name
                HAVING COUNT(DISTINCT MembershipTier) = 2
            ) AS subquery;
        ''')
        basic_vip_count = cursor.fetchone()[0]

        # Count subscribers with both VIP and Premium memberships
        cursor.execute('''
            SELECT COUNT(*) AS vip_premium_count
            FROM (
                SELECT COUNT(DISTINCT name)
                FROM subscribers
                WHERE MembershipTier IN ('Premium', 'VIP')
                GROUP BY name
                HAVING COUNT(DISTINCT MembershipTier) = 2
            ) AS subquery;
        ''')
        vip_premium_count = cursor.fetchone()[0]

        # Count subscribers with both Basic and Premium memberships
        cursor.execute('''
            SELECT COUNT(*) AS basic_premium_count
            FROM (
                SELECT COUNT(DISTINCT name)
                FROM subscribers
                WHERE MembershipTier IN ('Basic', 'Premium')
                GROUP BY name
                HAVING COUNT(DISTINCT MembershipTier) = 2
            ) AS subquery;
        ''')
        basic_premium_count = cursor.fetchone()[0]

        # Count subscribers with all three memberships (Basic, VIP, Premium)
        cursor.execute('''
            SELECT COUNT(*) AS all_three_count
            FROM (
                SELECT COUNT(DISTINCT name)
                FROM subscribers
                WHERE MembershipTier IN ('Basic', 'VIP', 'Premium')
                GROUP BY name
                HAVING COUNT(DISTINCT MembershipTier) = 3
            ) AS subquery;
        ''')
        all_three_count = cursor.fetchone()[0]

    # Apply the Inclusion-Exclusion Principle (IEP)
    unique_subscribers = (
        basic_count + vip_count + premium_count
        - basic_vip_count - basic_premium_count - vip_premium_count
        + all_three_count
    )

    # Prepare context for the template
    context = {
        'basic_count': basic_count,
        'vip_count': vip_count,
        'premium_count': premium_count,
        'basic_vip_count': basic_vip_count,
        'basic_premium_count': basic_premium_count,
        'vip_premium_count': vip_premium_count,
        'all_three_count': all_three_count,
        'unique_subscribers': unique_subscribers,
    }

    return render(request, 'subscriptions/results.html', context)
