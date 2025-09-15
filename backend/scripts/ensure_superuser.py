import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'travel_agency.settings')
import django
django.setup()
from django.contrib.auth import get_user_model
User = get_user_model()
username = 'admin'
email = 'admin@example.com'
password = 'admin'
if not User.objects.filter(is_superuser=True).exists():
    print('No superuser found — creating default admin user')
    if User.objects.filter(username=username).exists():
        u = User.objects.get(username=username)
        u.is_superuser = True
        u.is_staff = True
        u.email = email
        u.set_password(password)
        u.save()
        print('Updated existing user to superuser:', username)
    else:
        User.objects.create_superuser(username=username, email=email, password=password)
        print('Created superuser:', username)
else:
    print('Superuser already exists:')
    for u in User.objects.filter(is_superuser=True):
        print('-', u.username, u.email)
print('Done')
