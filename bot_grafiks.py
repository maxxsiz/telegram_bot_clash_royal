import plotly.graph_objects as go
import sqlite3

def grafik_player_id(userid):
    grafik_player_teg(get_teg(userid))
   
def get_teg(userid):
    conn = sqlite3.connect("clanstat.db")
    cursor = conn.cursor()
    cursor.execute("SELECT teg FROM telegram_main WHERE id_telegram = ?",(userid,))
    teg = cursor.fetchone()[0]
    return teg




def grafik_player_teg(teg):
    conn = sqlite3.connect("clanstat.db")
    cursor = conn.cursor()
    cursor.execute("SELECT active, battle, win, cards FROM main_war WHERE teg = ? LIMIT 10",(teg,))
    wars_info = cursor.fetchall()
    cursor.execute("SELECT cards_mid FROM war_list LIMIT 10")
    midl = cursor.fetchall()   
    wins = []
    lose = []
    no_atack = []
    no_war = []
    y_win = []
    y_lose = []
    y_atack = []
    y_war = []
    player_cards = []
    midl_cards = []
    size_m = 40
    a =[]
    title_st = "Останні 10 КВ ігрока: " + str(teg)
    for i in range(len(wars_info)):
        if wars_info[i][0] == 1:#sprawdzamy czy był na kw
            if wars_info[i][1] == 0:#nie było ataku
                no_atack.append(i+1)
                y_atack.append(wars_info[i][3])
            else:
                if wars_info[i][2] > 0:
                    wins.append(i+1)
                    y_win.append(wars_info[i][3])
                else:
                    lose.append(i+1)
                    y_lose.append(wars_info[i][3])
        else:# jeśli nie był na kw
            no_war.append(i+1)
            y_war.append(wars_info[i][3])
        midl_cards.append(midl[i][0])
        a.append(i+1)
        player_cards.append(wars_info[i][3])
    fig = go.Figure()
    fig.add_trace(go.Scatter(x = a,y = player_cards, name="Карти ігрока",mode='lines+markers',))
    fig.add_trace(go.Scatter(x = a,y = midl_cards, name="Cереднє значення карт",mode='lines+markers',))
    fig.add_trace(go.Scatter(mode = "markers+text",
                             x = wins,
                             y=y_win,
                             text=y_win,
                             textposition="bottom center",
                             textfont=dict(
                                            family="sans serif",
                                            size=18,
                                            color="Green"),
                             marker=dict(color='Green',
                                        size=size_m,
                                        line=dict(
                                                color='Black',
                                                width=2,)),
                             name="Перемога",))
    fig.add_trace(go.Scatter(mode = "markers+text",
                             x = lose,
                             y=y_lose,
                             text=y_lose,
                             textposition="bottom center",
                             textfont=dict(
                                            family="sans serif",
                                            size=18,
                                            color="gold",),
                             marker=dict(
                                            color='gold',
                                            size=size_m,
                                            line=dict(
                                                    color='Black',
                                                    width=2,)),
                             name="Поразка",))
    fig.add_trace(go.Scatter(mode = "markers+text",
                             x = no_war,
                             y=y_atack,
                             text=y_atack,
                             textposition="bottom center",
                             textfont=dict(
                                            family="sans serif",
                                            size=18,
                                            color="Red"),
                             marker=dict(
                                            color='Red',
                                            size=size_m,
                                            line=dict(
                                                    color='Black',
                                                    width=2,)),
                             name="Неучасть в КВ",))
    fig.add_trace(go.Scatter(mode = "markers+text",
                             x = no_atack,
                             y=y_war,
                             text=y_war,
                             textposition="bottom center",
                             textfont=dict(
                                            family="sans serif",
                                            size=18,
                                            color="Purple"),
                             marker=dict(
                                        color='Purple',
                                        size=size_m,
                                        line=dict(
                                                    color='Black',
                                                    width=2)),
                             name="Незроблена атака на КВ",))
    fig.update_layout(title=title_st,titlefont=dict(
                                            family="sans serif",
                                            size=30,
                                            color="White"),
                      yaxis=dict(title_text ="Кількість карт набитих на кв",titlefont=dict(
                                            family="sans serif",
                                            size=30,
                                            color="White")),
                      template="plotly_dark",
                      legend_orientation="h",)
    fig.update_yaxes(showline=True,linewidth=2, linecolor='black',mirror=True,automargin=True)
    fig.update_xaxes(showline=True,linewidth=2, linecolor='black',mirror=True,automargin=True)







    fig.write_image("fig1.png")

