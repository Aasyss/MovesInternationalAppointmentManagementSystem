import random
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User, Group
from userregistration.models import UserProfile, Certificate
from appointment_management.models import Setup_Availability
from faker import Faker

fake = Faker()

EXPERTISE_CHOICES = ['Visa Counselor', 'Career Counselor', 'Migration Counselor', 'Stress Counselor']

class Command(BaseCommand):
    help = 'Populate random data for consultants'

    def handle(self, *args, **kwargs):
        # Get the "consultant" group
        consultant_group, _ = Group.objects.get_or_create(name='consultant')

        for _ in range(10):
            user = User.objects.create_user(
                username=fake.user_name(),
                password='password',
                first_name=fake.first_name(),
                last_name=fake.last_name(),
                email=fake.email()
            )

            # Assign the "consultant" group to the user
            user.groups.add(consultant_group)

            user_profile = UserProfile.objects.create(
                user=user,
                profile_picture=fake.image_url(),
                bio=fake.text(),
                cv=fake.file_name(),
                date_of_birth=fake.date_of_birth(),
                education_history=fake.text(),
                expertise=random.choice(EXPERTISE_CHOICES),
                is_verified=True
            )

            Certificate.objects.create(
                user_profile=user_profile,
                certificate_file=fake.file_name()
            )

            availability = Setup_Availability.objects.create(
                consultant=user_profile,
                start_date=fake.date_this_decade(),
                monday_start_time=fake.time(),
                monday_end_time=fake.time(),
                tuesday_start_time=fake.time(),
                tuesday_end_time=fake.time(),
                wednesday_start_time=fake.time(),
                wednesday_end_time=fake.time(),
                thursday_start_time=fake.time(),
                thursday_end_time=fake.time(),
                friday_start_time=fake.time(),
                friday_end_time=fake.time(),
                saturday_start_time=fake.time(),
                saturday_end_time=fake.time(),
                sunday_start_time=fake.time(),
                sunday_end_time=fake.time()
            )

            print(f'Consultant {user.username} created.')
