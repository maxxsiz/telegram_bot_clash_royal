from parsing_clashstat import main_parsing
from databaze_create_update import update_dane
from databaze_create_main_clan import main_dcm
from databaze_create_main_war import main_dcmw
from stat_ranking_update import stat_main
import datetime
import time


def do_update():
    update_dane()
    main_dcm()
    main_dcmw()
    stat_main()

def main():
    a = 0
    while a == 0:
        try:
            do_update()
            do_update()
            log = open('log.txt','a')
            tim = datetime.datetime.now()
            text = tim.strftime("\n%d-%m-%Y %H:%M") + " ---- " + " Обновлення статистики пройшло успішно."
            log.write(text)
            log.close()
            time.sleep(10800)
        except:
            log = open('log.txt','a')
            tim = datetime.datetime.now()
            text = tim.strftime("\n%d-%m-%Y %H:%M") + " ---- " + " Виникла помилка, обновлення не вдалось."
            log.write(text)
            log.close()
            break
if __name__ == '__main__':
    main()
