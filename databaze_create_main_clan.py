import sqlite3


conn = sqlite3.connect("clanstat.db")
cursor = conn.cursor()
cursor1 = conn.cursor()
tablica_forwar = []
def new_list():
    return tablica_forwar
def database_main_create():
    cursor.execute("DROP TABLE IF EXISTS clan_main")
    cursor.execute("""CREATE TABLE clan_main (
                        teg TEXT NOT NULL PRIMARY KEY,
                        status INTEGER NOT NULL,              
                        nikname TEXT NOT NULL,
                        rank TEXT NOT NULL,
                        donate INTEGER NOT NULL,
                        time TEXT NOT NULL ,
                        MMR INTEGER NOT NULL,
                        date_entry DATE NOT NULL,
                        date_leave DATE NOT NULL,
                        time_at_clan TEXT NOT NULL,
                        p_win INTEGER NOT NULL,
                        p_activ INTEGER NOT NULL,
                        no_atack INTEGER NOT NULL,
                        id_telegram INTEGER NOT NULL)
                        """)
    
def check_player(teg):
    cursor1.execute("SELECT teg FROM clan_main WHERE teg = ?", (teg,))
    a = cursor1.fetchall()
    cursor1.execute("SELECT * FROM clan_update WHERE teg = ?", (teg,))
    b = cursor1.fetchall()[0]
    cursor1.execute("SELECT time_at_clan FROM clan_main WHERE teg = ?", (teg,))
    time_at_clan = cursor1.fetchone()
    cursor1.execute("SELECT date_entry FROM clan_main WHERE teg = ?", (teg,))
    date_entry = cursor1.fetchone()
    cursor1.execute("SELECT date_leave FROM clan_main WHERE teg = ?", (teg,))
    date_leave = cursor1.fetchone()
    if len(a)==False:
        tablica_forwar.append(teg)
        print("NEW PLAYER - {0}".format(teg))
        cursor1.execute("INSERT INTO clan_main VALUES(?,?,?,?,?,?,?,datetime('now','localtime'),?,?,?,?,?)",(b[0],1,b[1],b[2],b[3],b[4],0,0,0,0,0,0))
        conn.commit()
    else:
        cursor1.execute("SELECT status FROM clan_main WHERE teg = ?", (teg,))
        st = cursor1.fetchone()[0]
        cursor1.execute("SELECT strftime('%s','now','localtime') - strftime('%s',?)",(date_entry))
        de=cursor1.fetchone()[0]
        if st == 1:
            print("AKTUALIZATION - {0}".format(teg))
            cursor1.execute("""UPDATE clan_main SET nikname = ?,
                            rank = ?,
                            donate = ?,
                            time = ?,
                            MMR = ?,
                            time_at_clan = ?,
                            p_win = ?,
                            p_activ = ?,
                            p_no_atack = ?
                            WHERE teg = ? """,(b[1],b[2],b[3],b[4],0,de,0,0,0,teg,))
            conn.commit()      
        else: # nie była obecna ale już jest więć aktualicacjia dannych
            tablica_forwar.append(teg)
            print("AKTIVATION - {0}".format(teg))
            cursor1.execute("""UPDATE clan_main SET nikname = ?,
                            status = 1,
                            rank = ?,
                            donate = ?,
                            time = ?,
                            MMR = ?,
                            date_entry = datetime('now','localtime'),
                            date_leave = 0,
                            p_win = ?,
                            p_activ = ?,
                            p_no_atack = ?
                            WHERE teg = ?""",(b[1],b[2],b[3],b[4],0,0,0,0,teg,))
            conn.commit()      
def do_offline():
    
    cursor1.execute("SELECT teg FROM clan_main WHERE status = 1")
    tab1 = cursor1.fetchall()
    cursor1.execute("SELECT teg FROM clan_update")
    tab2 = cursor1.fetchall()
    result = list(set(tab1) ^ set(tab2))
    for i in result:
        i = str(i).replace("'",'').replace('(','').replace(')','').replace(',','')
        cursor1.execute("SELECT time_at_clan FROM clan_main WHERE teg = ?", (i,))
        time_at_clan = cursor1.fetchone()[0]
        cursor1.execute("SELECT date_entry FROM clan_main WHERE teg = ?", (i,))
        date_entry = cursor1.fetchone()[0]
        cursor1.execute("SELECT ? + strftime('%s','now','localtime') - strftime('%s',?)",(time_at_clan,date_entry,))
        de = cursor1.fetchone()[0]
        cursor1.execute("""UPDATE clan_main SET
                            status = 0,
                            time_at_clan = ?,
                            date_leave = datetime('now','localtime')                  
                            WHERE teg = ?""",(de,i,))  
        conn.commit()
def main_dcm():
    #database_main_create()
    cursor.execute("SELECT * FROM clan_update")
    a = 0
    row = cursor.fetchall()
    for r in row:
        a  = r[0]
        check_player(a)
    do_offline()
    
if __name__ == '__main__':
    main_dcm()

