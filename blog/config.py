import os

basedir = os.path.abspath(os.path.dirname(__file__))

# sqlalchemy static configuration
# change the following line 'sqlite:///' to 'mysql' is also ok to run
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir,'blog,db')

# static writing in Flask
DEBUG = True   