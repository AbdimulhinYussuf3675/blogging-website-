import os
import re 

class Config:
    SQLALCHEMY_TRACK_MODIFICATIONS=True
    SECRET_KEY='SECRET_KEY'
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get("MAIL_USERNAME")
    MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD")
    UPLOADED_PHOTOS_DEST ='app/static/photos'
    SENDER_EMAIL = 'abdimulhin.yussuf@student.moringaschool.com'
    

# class ProdConfig(Config):
#     SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")

class ProdConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL","")
    
    if SQLALCHEMY_DATABASE_URI.startswith("postgres://"):
        SQLALCHEMY_DATABASE_URI =SQLALCHEMY_DATABASE_URI.replace("postgres://","postgresql://",1)
  
class TestConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://moringa:access@localhost/adam_test'


class DevConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://moringa:access@localhost/adam'
    DEBUG = True



config_options = {
'development':DevConfig,
'production':ProdConfig,
'test':TestConfig
}