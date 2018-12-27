import telegram
import psutil
from pprint import pprint as pp
from hurry.filesize import size
import time 
from pass_tw import TOKEN_BOT


bot = telegram.Bot(token=TOKEN_BOT)
chat_id = "-352161746"

while True:
    stream = False 
    timeline = False 
    news = False 

    msg = "Running Proccess: \n"
    for process in psutil.process_iter():
        if process.name() == 'python': 
            if process.cmdline()[1] == 'stream_db_twitter.py':
                stream = True                
            if process.cmdline()[1] == 'timeline_fetch.py':
                timeline = True
            if process.cmdline()[1] == 'news_paper_fetch.py':
                news = True
    if (not stream or not timeline or not news ):    
        msg = msg + "Stream: " + str(stream) + "\n" + "Timeline: " + str(timeline) + "\n" + "News: " + str(news)
        bot.send_message(chat_id=chat_id, text=msg)
        time.sleep(600)
    time.sleep(30)


#space = psutil.disk_usage('/')
#msg = "USED: " + size(space.used) + "\n" + "FREE: " + size(space.free) + "\n" + "TOTAL: " + size(space.total)




#msg = "Running Proccess: \n"
#for process in psutil.process_iter():
#    if process.name() == 'python': 
#        msg = msg + str(process.cmdline()) + "\n"     



