# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        "NAME": "dbname",
        "USER": "username",
        "PASSWORD": "password",
        "HOST": "localhost"
    }
}
