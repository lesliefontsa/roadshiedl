from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(is_superuser=True).exists():
    User.objects.create_superuser('admin','admin@example.com','admin')
    print('Created superuser admin/admin')
else:
    print('Superuser(s) already exist:')
    for u in User.objects.filter(is_superuser=True):
        print('-', u.username, u.email)
