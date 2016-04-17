SECRET_KEY = 'fake-key'
INSTALLED_APPS = [
    "tests",
]

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
    }
}


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
    }
}

