import sqlite3
from before_procesing import war_clans
from databaze_create_main_clan import new_list
conn = sqlite3.connect("clanstat.db")
cursor = conn.cursor()
cursor1 =  conn.cursor()
def create_war_main():
    cursor1.execute("DROP TABLE IF EXISTS main_war")
    cursor1.execute("""CREATE TABLE IF NOT EXISTS main_war(
                        war_number INTEGER NOT NULL,
                        teg TEXT NOT NULL,
                        active INTEGER NOT NULL,
                        battle INTEGER NOT NULL,              
                        win INTEGER NOT NULL,
                        cards INTEGER NOT NULL)""")
    cursor1.execute("DROP TABLE IF EXISTS war_list")
    cursor1.execute("""CREATE TABLE IF NOT EXISTS war_list(
                        war_number INTEGER NOT NULL,
                        wins INTEGER NOT NULL,
                        active_player INTEGER NOT NULL,              
                        cards_mid INTEGER NOT NULL,
                        war_clans TEXT NOT NULL)""")
def create_update(teg):
    cursor1.execute("SELECT * FROM war_list")
    b = len(cursor1.fetchall())
    cursor1.execute("SELECT teg FROM clan_main WHERE status = 1")
    a = cursor1.fetchall()[0]
    cursor1.execute("SELECT fight FROM war_update WHERE teg = ?",(teg,))
    fight = cursor1.fetchone()[0]
    cursor1.execute("SELECT win FROM war_update WHERE teg = ?",(teg,))
    win = cursor1.fetchone()[0]
    cursor1.execute("SELECT cards FROM war_update WHERE teg = ?",(teg,))
    cards = cursor1.fetchone()[0] 
    cursor1.execute("INSERT INTO main_war VALUES(?,?,?,?,?,?)", (b+1,teg,1,fight,win,cards,))
    conn.commit()
    
def other_update():
    cursor1.execute("SELECT * FROM war_list")
    r = len(cursor1.fetchall())
    if r == 0:
        print("pierwsza wojna")
    else:
        cursor1.execute("SELECT * FROM war_list")
        b = len(cursor1.fetchall())
        cursor1.execute("SELECT teg FROM war_update")
        tab1 = cursor1.fetchall()
        cursor1.execute("SELECT teg FROM clan_update")
        tab2 = cursor1.fetchall()
        res = list(set(tab1) ^ set(tab2))
        tab3 = new_list()
        resu = []
        for i in res:
            a = str(i).replace("'",'').replace('(','').replace(')','').replace(',','')
            resu.append(a)
        result = list(set(tab3) ^ set(resu))
        #print(result)
        for j in result:
            print(j)
            cursor1.execute("INSERT INTO main_war VALUES(?,?,?,?,?,?)", (b+1,j,0,0,0,0,))
            conn.commit()
        
def warlist_update():
    cursor1.execute("SELECT * FROM war_list")
    a = len(cursor1.fetchall())
    cursor1.execute("SELECT active FROM main_war WHERE war_number = ?",(int(a+1),))
    act_war = cursor1.fetchall()
    aw = 0
    for k in act_war:
        aw += int(str(k).replace("'",'').replace('(','').replace(')','').replace(',',''))
    cursor1.execute("SELECT win FROM main_war WHERE war_number = ?",(int(a+1),))
    win_war = cursor1.fetchall()
    ww = 0
    for g in win_war:
        ww += int(str(g).replace("'",'').replace('(','').replace(')','').replace(',',''))
    cursor1.execute("SELECT cards FROM main_war WHERE war_number = ?",(int(a+1),))
    cards_war = cursor1.fetchall()
    wc = 0
    for t in cards_war:
        wc += int(str(t).replace("'",'').replace('(','').replace(')','').replace(',',''))
    m_wc = int(wc/aw)
    k = war_clans()
    cursor1.execute("INSERT INTO war_list VALUES(?,?,?,?,?)", (int(a+1),ww,aw,m_wc,k))
    conn.commit()
    
def main_dcmw():
    #create_war_main()
    cursor1.execute("SELECT max(war_number) FROM war_list")
    num_of_war = cursor1.fetchone()[0]
    if num_of_war == None:
        cursor.execute("SELECT * FROM war_update")
        a = 0
        row = cursor.fetchall()
        for r in row:
            a  = r[0]
            create_update(a)
        other_update()
        warlist_update()
    else:
        cursor1.execute("SELECT war_clans FROM war_list WHERE war_number = ?",(num_of_war,))
        d = cursor1.fetchone()[0]
        k = war_clans()
        if d != k:
            cursor.execute("SELECT * FROM war_update")
            a = 0
            row = cursor.fetchall()
            for r in row:
                a  = r[0]
                create_update(a)
            other_update()
            warlist_update()
        else:
            return print("повторенна версія\n__________________________________________")
            






if __name__ == '__main__':
    main_dcmw()
