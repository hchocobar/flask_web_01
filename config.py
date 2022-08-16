import os


class Config(object):
    # csrf config
    SECRET_KEY = os.environ.get('MI_CLAVE_SECRETA')
    # mail config
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_SSL = False
    MAIL_USE_TLS = True
    MAIL_USERNAME = 'tucuenta@gmail.com'
    MAIL_PASSWORD = os.environ.get('PASSWORD_EMAIL')


# configuración para el entorno de Desarrollo
class DevelopmentConfig(Config):
    # app config
    DEBUG = True
    # db config
    SQLALCHEMY_DATABASE_URI = 'mysql://db_user:pass@localhost/db_flask'
    SQLALCHEMY_TRACK_MODIFICATIONS = False


# configuración para el entorno de Producción

# configuración para pruebas unitarias
