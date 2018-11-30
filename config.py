import os
basedir = os.path.abspath(os.path.dirname(__name__))

class Config:
    SQLALCHEMY_DATABASE_URI = os.environ["DATABASE_URL"]
    SECRET_KEY = '36356e9db87405fd84fb18d0bd8380ff6ed47b74f1f578df'
    MAIL_SERVER = "smtp.gmail.com"
    MAIL_PORT = 465
    MAIL_USERNAME = os.environ["MAIL_USERNAME"]
    MAIL_PASSWORD = os.environ["MAIL_PASSWORD"]
    MAIL_DEFAULT_SENDER = os.environ["MAIL_DEFAULT_SENDER"]
    MAIL_USE_SSL = True

class ProductionConfig(Config):
    DEBUG = False


class DevelopmentConfig(Config):
    DEBUG = True


config = {
'development': DevelopmentConfig,
'production': ProductionConfig,
'default': DevelopmentConfig
}