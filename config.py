import os
basedir = os.path.abspath(os.path.dirname(__name__))

class Config:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')


class ProductionConfig(Config):
    pass


class DevelopmentConfig(Config):
    DEBUG = True


config = {
'development': DevelopmentConfig,
'production': ProductionConfig,
'default': DevelopmentConfig
}