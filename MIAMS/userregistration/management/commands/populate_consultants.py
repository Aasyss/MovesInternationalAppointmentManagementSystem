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
                password='@@Apple1234',
                first_name=fake.first_name(),
                last_name=fake.last_name(),
                email=fake.email()
            )

            # Assign the "consultant" group to the user
            user.groups.add(consultant_group)

            user_profile = UserProfile.objects.create(
                user=user,
                profile_picture=fake.image_url(),
                bio=fake.paragraph(nb_sentences=5),
                cv=fake.file_name(),
                date_of_birth=fake.date_of_birth(),
                education_history=fake.paragraph(nb_sentences=5),
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
                monday_start_time='09:00',
                monday_end_time='17:00',
                tuesday_start_time='09:00',
                tuesday_end_time='17:00',
                wednesday_start_time='09:00',
                wednesday_end_time='17:00',
                thursday_start_time='09:00',
                thursday_end_time='17:00',
                friday_start_time='09:00',
                friday_end_time='17:00',
                saturday_start_time='09:00',
                saturday_end_time='17:00',
                sunday_start_time='09:00',
                sunday_end_time='17:00'
            )

            print(f'Consultant {user.username} created.')
