import sqlite3



def addteg(teg,userid,username): 
    conn = sqlite3.connect("clanstat.db")
    cursor = conn.cursor()
    cursor.execute("SELECT teg, nikname FROM clan_main WHERE teg = ?",(teg,))
    player = cursor.fetchone()
    if player == None:
        return "<b>Не існує такого учасника клану, спробуйте пізніше</b>."
    else:
        nikname = player[1]
        cursor.execute("SELECT id_telegram FROM telegram_main WHERE id_telegram = ?",(userid,))
        id_t = cursor.fetchone()
        if id_t == None:
            cursor.execute("INSERT INTO telegram_main VALUES(?,?,?,?,?)",(teg, userid, False,username , 0))
            conn.commit()
            text = "<b>Створенно нову прив'язку акаунта з нікнеймом: {0}\nВідтепер легкий доступ до статистики по команді /mystat</b>".format(nikname)
            return text
        else:
            cursor.execute("UPDATE telegram_main SET teg = ? WHERE id_telegram = ?",(teg, userid))
            conn.commit()
            text = " Прив'язано новий акаунт з нікнеймом: {0}\nВідтепер легкий доступ до статистики по команді /mystat".format(nikname)
            return text
        
def get_teg(userid):
    conn = sqlite3.connect("clanstat.db")
    cursor = conn.cursor()
    cursor.execute("SELECT teg FROM telegram_main WHERE id_telegram = ?",(userid,))
    teg = str(cursor.fetchone()[0])
    return teg

def stat_player_id(userid):
    a = get_teg(userid)
    stat_player_teg(a)
    return stat_player_teg(a)
    
def stat_player_teg(teg):
    conn = sqlite3.connect("clanstat.db")
    cursor = conn.cursor()
    if teg == None:
        text = "<b>Вибачте але ми не знаходимо Вас в нашій базі данних, введіть /start</b>"
        return text
    else:
        cursor.execute("SELECT * FROM clan_main WHERE teg = ?", (teg,))
        inform = cursor.fetchone()
        if inform[1] == 1:
            time = int(int(inform[9])/3600)
            days = int(time/24)
            hour = int(time - days*24)
            time_text = "{0} днів {1} годин".format(days,hour)
            text = "<code>Нікнейм: {0}\nПосада: {1}\nДонат: {2}\nРейтинг: {3} \nЧас в клані: {4}\nПроцент перемог: {5}%\nПроцент активності: {6}%\nКількість підстав: {7}</code>".format(inform[2],inform[3],inform[4],inform[6],time_text,inform[10],inform[11],inform[12])
            return text
        else:
            text = "<b>Данний ігрок не являється учасником клану</b>"
            return text
    
def showclan():
    conn = sqlite3.connect("clanstat.db")
    cursor = conn.cursor()
    cursor.execute("SELECT nikname, teg FROM clan_main WHERE status = 1 ")
    clan = cursor.fetchall()
    text_clan = ""
    for i in range(len(clan)):
        position = clan[i]
        text = "<b>{0}) {1} | {2}</b>\n".format(i + 1 ,position[0],position[1])
        text_clan += text
    return text_clan

def ranking():
    conn = sqlite3.connect("clanstat.db")
    cursor = conn.cursor()
    cursor.execute("SELECT nikname,MMR FROM clan_main WHERE status = 1 ORDER BY MMR DESC")
    rank = cursor.fetchall()
    text_rank = ""
    for i in range(len(rank)):
        position = rank[i]
        text = "<b>{0}) {1} | {2}</b>\n".format(i + 1 ,position[0],position[1])
        text_rank += text
    return text_rank





