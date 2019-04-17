from flask import Flask
from flask_httpauth import HTTPBasicAuth
import configparser
import psycopg2

try:
    config = configparser.RawConfigParser()
    config.read('settings.properties')
    SLACK_TOKEN = config['bot']['SLACK_TOKEN']
    ADMIN = config['service']['ADMIN']
    PASSWORD = config['service']['PASSWORD']
    APPHOST = config['service']['APPHOST']
    APPPORT = config['service']['APPPORT']
    DEBUG = config['service']['DEBUG']
    USER = config['db']['USER']
    PWD = config['db']['PWD']
    DB = config['db']['DB']
    HOST = config['db']['HOST']
    PORT = config['db']['PORT']
    print("Get config successfully")
except Exception:
    print("Cant read config file")
    SLACK_TOKEN = ""


app = Flask(__name__)
auth = HTTPBasicAuth()
conn = psycopg2.connect(dbname=DB, user=USER, password=PWD, host=HOST)


