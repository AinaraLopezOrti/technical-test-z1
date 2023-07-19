# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        "NAME": "testz1",
        "USER": "videoback",
        "PASSWORD": "videobacklocal",
        "HOST": "localhost"
    }
}

# Also... in localhost
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         "NAME": 'db.sqlite3',
#     }
# }