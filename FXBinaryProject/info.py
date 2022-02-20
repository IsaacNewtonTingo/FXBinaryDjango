from decouple import config


EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = config('EMAIL_HOST_PASSWORD')
EMAIL_HOST_PASSWORD = '@HcetOfniYranibxF'
EMAIL_PORT = 587
