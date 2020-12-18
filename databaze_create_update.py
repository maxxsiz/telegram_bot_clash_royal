import sqlite3
from before_procesing import clan_name, clan_url, clan_donate, clan_rank, clan_time, war_name, war_teg, war_fight, war_win, war_cards, clan_teg
def update_dane():
    conn = sqlite3.connect("clanstat.db")
    cursor = conn.cursor()
    cursor.execute("DROP TABLE IF EXISTS clan_update")
    cursor.execute("""CREATE TABLE clan_update (
                    teg TEXT NOT NULL,
                    nikname TEXT NOT NULL,
                    rank TEXT NOT NULL,
                    donate INTEGER NOT NULL,
                    time TEXT NOT NULL ,
                    url TEXT NOT NULL)
                    """)
    cl_name = clan_name()
    cl_url = clan_url()
    cl_donate = clan_donate()
    cl_rank = clan_rank()
    cl_time = clan_time()
    cl_teg = clan_teg()
    for i in range(len(cl_name)):
        cursor.execute("INSERT INTO clan_update VALUES (?,?,?,?,?,?)",(cl_teg[i],cl_name[i],cl_rank[i],cl_donate[i],cl_time[i],cl_url[i]))
        conn.commit()
        
    w_name = war_name()
    w_teg = war_teg()
    w_fight = war_fight()
    w_win = war_win()
    w_cards = war_cards()
    cursor.execute("DROP TABLE IF EXISTS war_update")
    cursor.execute("""CREATE TABLE war_update (
                    teg TEXT NOT NULL,
                    nikname TEXT NOT NULL,
                    fight INTEGER NOT NULL,
                    win INTEGER NOT NULL,
                    cards INTEGER NOT NULL)
                    """)
    for i in range(len(w_name)):
        cursor.execute("INSERT INTO war_update VALUES (?,?,?,?,?)",(w_teg[i],w_name[i],w_fight[i],w_win[i],w_cards[i]))
        conn.commit()     
    conn.close()

if __name__ == '__main__':
    update_dane()
    
