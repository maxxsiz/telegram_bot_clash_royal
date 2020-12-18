from parsing_clashstat import main_parsing

pars_all = main_parsing()
pars_clan = pars_all[0]
pars_war = pars_all[1]

def clan_name():
    return pars_clan[0]
def clan_url():
    return pars_clan[1]
def clan_donate():
    return pars_clan[2]
def clan_rank():
    return pars_clan[3]
def clan_time():
    return pars_clan[4]
def war_name():
    return pars_war[0]
def war_teg():
    w_url = pars_war[1]
    w_teg = []
    for a in w_url:
        w_teg.append(a[35:])
    return w_teg

def war_fight():
    return pars_war[2]
def war_win():
    return pars_war[3]
def war_cards():
    return pars_war[4]
def clan_teg():
    c_url = pars_clan[1]
    c_teg = []
    for a in c_url:
        c_teg.append(a[35:])
    return c_teg
def war_clans():
    names_clans = ""
    for j in pars_war[5]:
        names_clans += j
    return names_clans
