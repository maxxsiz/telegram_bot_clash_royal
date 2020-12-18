import sqlite3

conn = sqlite3.connect("clanstat.db")
cursor = conn.cursor()
cursor1 = conn.cursor()
cursor2 = conn.cursor()
def create_stat():
    cursor.execute("DROP TABLE IF EXISTS clan_stat")
    cursor.execute("""CREATE TABLE clan_stat (
                        teg TEXT NOT NULL,
                        win INTEGER NOT NULL,              
                        lose INTEGER NOT NULL,
                        was_in_clan INTEGER NOT NULL,
                        was_in_wars INTEGER NOT NULL,
                        point_for_win INTEGER NOT NULL ,
                        point_for_lose INTEGER NOT NULL,
                        point_for_no_atack INTEGER NOT NULL,
                        point_extra INTEGER NOT NULL,
                        num_changer REAL NOT NULL,
                        point_changer INTEGER NOT NULL,
                        final_point INTEGER NOT NULL)
                        """)
def per_win():# обновляэмо загальну статистику кількості перемог програшів неактивів 
    cursor.execute("SELECT max(war_number) FROM main_war") #
    war_numb = cursor.fetchone()[0]
    for row in cursor.execute("SELECT teg FROM main_war WHERE war_number = ?", (war_numb,)):
        player = str(row).replace("'",'').replace('(','').replace(')','').replace(',','')
        cursor1.execute("SELECT teg FROM main_war WHERE teg = ?", (player,))
        st = len(cursor1.fetchall())
        if st == 0:
            continue
        else:
            cursor1.execute("SELECT SUM(win) FROM main_war WHERE teg = ? AND battle>0",(player,)) #ilość wygranych ogólna
            a = cursor1.fetchone()[0]
            cursor1.execute("SELECT SUM(battle) FROM main_war WHERE teg = ?",(player,))#ilość bitw ogólna
            b = cursor1.fetchone()[0]
            if b > 0:
                p_win = int(a/b*100)
                cursor1.execute("UPDATE clan_main SET p_win = ? WHERE teg = ?",(p_win, player,))
                conn.commit()
            cursor1.execute("SELECT SUM(active) FROM main_war WHERE teg = ? ",(player,)) #ilość KW gdzie był gracz 
            c = cursor1.fetchone()[0]
            cursor1.execute("SELECT COUNT(teg) FROM main_war WHERE teg = ? ",(player,))#ilość wspominek danej osoby w liśćie KW
            f = cursor1.fetchone()[0]
            p_act = int(c/f*100)
            cursor1.execute("UPDATE clan_main SET p_activ = ? WHERE teg = ?",(p_act, player,))
            conn.commit()
            cursor1.execute("SELECT COUNT(active) FROM main_war WHERE teg = ? and battle = 0 AND active = 1",(player,))
            d = cursor1.fetchone()[0]
            cursor1.execute("UPDATE clan_main SET p_no_atack = ? WHERE teg = ?",(d, player,))
            conn.commit()

def mmr():
    cursor.execute("SELECT max(war_number) FROM main_war")
    war_number = cursor.fetchone()[0]
    for row in cursor.execute("SELECT teg FROM main_war WHERE war_number = ?",(war_number,)):
        player = str(row).replace("'",'').replace('(','').replace(')','').replace(',','')
        cursor1.execute("SELECT teg FROM clan_stat WHERE teg = ?", (player,))
        st = len(cursor1.fetchall())
        if st == 0:
            cursor1.execute("INSERT INTO clan_stat VALUES (?,?,?,?,?,?,?,?,?,?,?,?)", (player,0,0,0,0,0,0,0,0,0,0,0,))
            conn.commit()
            win = func_win(player)[0]
            lose = func_lose(player)[0]
            was_in_clan =func_active(player)[0]
            was_in_war = func_active(player)[1]
            point_for_win = func_win(player)[1]
            poin_for_lose = func_lose(player)[1]
            point_for_no_atack = no_atack(player)
            point_extra = extra_point(player)
            num_changer = func_active(player)[2]
            cursor1.execute("""UPDATE clan_stat SET
                            win = ?,              
                            lose = ?,
                            was_in_clan = ?,
                            was_in_wars = ?,
                            point_for_win = ? ,
                            point_for_lose = ?,
                            point_for_no_atack = ?,
                            point_extra = ?,
                            num_changer = ?
                            WHERE teg = ?""",(win,lose,was_in_clan,was_in_war,point_for_win,poin_for_lose,point_for_no_atack,point_extra,num_changer,player,))
            conn.commit()
            befor_final = point_for_win + poin_for_lose + point_for_no_atack + point_extra
            if befor_final>0:              
                final = int(befor_final * num_changer)
                point_changer = befor_final - final
            else:
                final = int(befor_final * num_changer)
                point_changer = final - befor_final
            cursor1.execute("""UPDATE clan_stat SET
                            point_changer = ?,
                            final_point = ?
                            WHERE teg = ?""",(point_changer,final,player,))
            conn.commit()
        else:
            win = func_win(player)[0]
            lose = func_lose(player)[0]
            was_in_clan =func_active(player)[0]
            was_in_war = func_active(player)[1]
            point_for_win = func_win(player)[1]
            poin_for_lose = func_lose(player)[1]
            point_for_no_atack = no_atack(player)
            point_extra = extra_point(player)
            num_changer = func_active(player)[2]
            cursor1.execute("""UPDATE clan_stat SET
                            win = ?,              
                            lose = ?,
                            was_in_clan = ?,
                                was_in_wars = ?,
                            point_for_win = ? ,
                            point_for_lose = ?,
                            point_for_no_atack = ?,
                            point_extra = ?,
                            num_changer = ?
                            WHERE teg = ? """,(win,lose,was_in_clan,was_in_war,point_for_win,poin_for_lose,point_for_no_atack,point_extra,num_changer,player,))
            conn.commit()
            befor_final = point_for_win + poin_for_lose + point_for_no_atack + point_extra
            final = int(befor_final * num_changer)
            point_changer = befor_final - final
            cursor1.execute("""UPDATE clan_stat SET
                            point_changer = ?,
                            final_point = ?
                            WHERE teg = ?""",(point_changer,final,player,))
        conn.commit()
        cursor1.execute("""UPDATE clan_main SET
                            MMR = ?
                            WHERE teg = ?""",(final,player,))
        conn.commit()
            #кожeна перемога це 10 очків
            #кожна поразка це -5 очків
            #кожна неатака на кв -20 очків
            #проц участі множимо на загальну кількість очків
            #обчислення співідношення карт клану до середнього значення (картиігрока/середня
            #>0,5  >0,6  >0,7  >0,8   >0,9   0,9-1,1  1,1>  1,2>  1,3>  1,4>  1,5>
            #-5     -4     -3    -2    -1     0        +1    +2    +3    +4    +5
def extra_point(player):
    cursor2.execute("SELECT MAX(war_number) FROM war_list")# дізнаємось номер останьої кв
    a = cursor2.fetchone()[0]
    cursor2.execute("SELECT cards_mid FROM war_list WHERE war_number = ?",(a,)) #витягуэмо середню карт 
    b = cursor2.fetchone()[0]
    cursor2.execute("SELECT cards FROM main_war WHERE war_number = ? AND teg = ?",(a,player,)) 
    c = cursor2.fetchone()[0]
    extr_ch = c/b
    cursor2.execute("SELECT point_extra FROM clan_stat WHERE teg = ?",(player,))
    old_extra = cursor2.fetchone()[0]
    if extr_ch < (0.5) :
        return old_extra - 5
    elif extr_ch < (0.6):
        return old_extra - 4
    elif extr_ch < (0.7):
        return old_extra - 3
    elif extr_ch < (0.8):
        return old_extra - 2
    elif extr_ch < (0.9):
        return old_extra - 1
    elif (0.9) <= extr_ch <= (1.1):
        return old_extra 
    elif extr_ch > (1.1):
        return old_extra + 1
    elif extr_ch > (1.2):
        return old_extra + 2
    elif extr_ch > (1.3):
        return old_extra + 3
    elif extr_ch > (1.4):
        return old_extra + 4
    elif extr_ch > (1.5):
        return old_extra + 5
    
def func_win(player):#win#point_for_win 
    cursor2.execute("SELECT SUM(win) FROM main_war WHERE teg = ?",(player,))
    win = cursor2.fetchone()[0]
    p_win = win*10
    return win, p_win
    
    cursor2.execute("SELECT COUNT(teg) FROM main_war WHERE teg = ? AND active = 1",(player,)) #was_in_wars
def func_lose(player):#lose#point_for_lose
    cursor2.execute("SELECT SUM(win) FROM main_war WHERE teg = ?",(player,))
    a = cursor2.fetchone()[0]
    cursor2.execute("SELECT SUM(battle) FROM main_war WHERE teg = ?",(player,))
    b = cursor2.fetchone()[0]
    lose = b - a
    p_lose = lose * (-5)
    return lose, p_lose

def no_atack(player):#point_for_no_atack
    cursor2.execute("SELECT COUNT(active) FROM main_war WHERE active = 1 AND battle = 0 AND teg = ?",(player,))
    a = cursor2.fetchone()[0]
    no_atack = a * (-20)
    return no_atack
    
def func_active(player):#num_changer#was_in_clan#was_in_war
    cursor2.execute("SELECT COUNT(teg) FROM main_war WHERE teg = ?",(player,)) #was_in_clan
    a = cursor2.fetchone()[0]
    cursor2.execute("SELECT COUNT(teg) FROM main_war WHERE teg = ? AND active = 1",(player,)) #was_in_war
    b = cursor2.fetchone()[0]
    num_changer = b/a
    return a, b, num_changer
    
def stat_main():
    #create_stat()
    per_win()
    mmr()



if __name__ == '__main__':
    stat_main()
