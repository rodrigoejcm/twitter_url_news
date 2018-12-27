import telegram
import psutil
from pprint import pprint as pp
from hurry.filesize import size
import time 


bot = telegram.Bot(token='')
chat_id = "-352161746"

while True:
    stream = True 
    timeline = True 
    news = True 

    msg = "Running Proccess: \n"
    for process in psutil.process_iter():
        if process.name() == 'python': 
            if process.cmdline()[1] == 'stream_db_twitter.py':
                stream = False                
            if process.cmdline()[1] == 'timeline_fetch.py':
                timeline = False
            if process.cmdline()[1] == 'news_paper_fetch.py':
                news = False
    if (not stream or not timeline or not news ):    
        msg = "Stream: " + str(stream) + "\n" + "Timeline: " + str(timeline) + "\n" + "News: " + str(news)
        bot.send_message(chat_id=chat_id, text=msg)
        time.sleep(600)
    time.sleep(30)


#space = psutil.disk_usage('/')
#msg = "USED: " + size(space.used) + "\n" + "FREE: " + size(space.free) + "\n" + "TOTAL: " + size(space.total)




#msg = "Running Proccess: \n"
#for process in psutil.process_iter():
#    if process.name() == 'python': 
#        msg = msg + str(process.cmdline()) + "\n"     



