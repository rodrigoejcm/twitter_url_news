from decimal import Decimal
from datetime import date
from datetime import datetime


import json

from pony.orm.core import *

db = Database()



class User(db.Entity):
    id = PrimaryKey(int,size=64)
    screen_name_usuario = Optional(str,nullable=True)
    name_usuario = Optional(str,nullable=True)


class Extra_User_Tweet(db.Entity):
    id = PrimaryKey(int,size=64, auto=True)
    id_usuario = Required(int, size=64)
    text_full = Optional(LongUnicode, nullable=True)
    created_at = Optional(datetime)
    tweet_reply_ref = Required(int, size=64)
    
    
class Tweet(db.Entity):
    id = PrimaryKey(int, size=64)
    id_str = Required(str)
    id_usuario = Required(int, size=64)
    id_str_usuario = Required(str)
    name_usuario = Optional(str,nullable=True)
    created_at = Optional(datetime)
    text_full = Optional(LongUnicode, nullable=True)
    url = Set("Url")
    
class Tweet_Reply(db.Entity):
    id = PrimaryKey(int, size=64)
    id_str = Required(str)
    id_usuario = Required(int, size=64)
    id_str_usuario = Required(str)
    
    in_reply_to_user_id = Optional(int, size=64)
    in_reply_to_status_id = Optional(int, size=64)
    
    text_full = Optional(LongUnicode, nullable=True)

    created_at = Optional(datetime)

    fetch_status = Optional(str, default="To Fetch")

class Url(db.Entity):
    id = PrimaryKey(int, auto=True)
    expanded_url = Optional(LongUnicode)
    url = Optional(LongUnicode)
    display = Optional(LongUnicode)
    tweet = Optional(Tweet)

    fetch_status = Optional(str, default="To Fetch")

class News(db.Entity):
    id = PrimaryKey(int, auto=True)
    url_source =  Required(str)
    url_original = Required(str)
    tweet_id = Required(int, size=64)
    url_id = Required(int, size=32)
    authors = Optional(str, nullable=True)
    date = Optional(str, nullable=True)
    meta = Optional(str, nullable=True)
    title = Optional(str, nullable=True)
    text = Optional(LongStr, nullable=True)
    html_file = Optional(str, nullable=True)
    #status = Required(str)
                
       

#sql_debug(True)  # Output all SQL queries to stdout



params = dict(
    #sqlite=dict(provider='sqlite', filename='university1.sqlite', create_db=True),
    mysql=dict(provider='mysql', host="localhost", user="twitter_user", passwd="twitter_pass", db="twitter_new")
    #postgres=dict(provider='postgres', user='pony', password='twitter_user', host='localhost', database='twitter'),
    #oracle=dict(provider='oracle', user='c##pony', password='pony', dsn='localhost/orcl')
)

db.bind(**params['mysql'], charset='utf8mb4', use_unicode=True)


if __name__ == '__main__':
    print("GERANDO TABELAS....")
    db.generate_mapping(create_tables=True)
    with db_session:
        db.execute("SET NAMES utf8mb4;")
    #    db.execute("ALTER DATABASE twitter CHARACTER SET = utf8mb4;")
  
    
else:
    db.generate_mapping(create_tables=False)
    with db_session:
        db.execute("SET NAMES utf8mb4;")
