# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        "NAME": "videoback",
        "USER": "videoback",
        "PASSWORD": "videobacklocal",
        "HOST": "localhost"
    }
}

# AWS credentials
AWS_ACCESS_KEY_ID = "..."
AWS_SECRET_ACCESS_KEY = "..."
AWS_DEFAULT_REGION = "eu-west-1"