import requests as req
from config import clan_url, war_url
from bs4 import BeautifulSoup
from selenium import webdriver

def update_clash(url):
    driver = webdriver.Chrome()
    driver.get(url)
    driver.find_element_by_xpath('//*[@id="refresh-clan"]/button').click()


def get_html(url):
    r = req.get(url)
    return r.text
    
def get_all_players(html):
    soup = BeautifulSoup(html, 'lxml')
    tab_nikname = []
    tab_url = []
    tab_donate = []
    tab_rank = []
    tab_lasttime = []
    
    for tag in soup.find_all('a', class_="ui__blueLink"):
        tab_nikname.append(tag.text)
        tab_url.append(tag.attrs['href'])
    for tag in soup.find_all('div', class_="clan__donation"):
        tab_donate.append(tag.text)     
    for tag in soup.find_all('div', class_="clan__memberRoleInner"):
        tab_rank.append(tag.text)
    for tag in soup.find_all('div', class_="clan__lastSeenInner"):
        tab_lasttime.append(tag.text)
    for i in range( len(tab_nikname) ):
        print(str(i+1) + str('****') + "{0}___{1}___{2}___{3}_____{4}".format(tab_nikname[i],tab_donate[i],tab_rank[i],tab_lasttime[i],tab_url[i]))
    return tab_nikname,tab_url,tab_donate,tab_rank,tab_lasttime

def get_stat_player(html):
    soup = BeautifulSoup(html, 'lxml')
    tab_clans = []
    tab_name = []
    tab_fight = []
    tab_win = []
    tab_cards = []
    tab_url = []
    k1 = 0
    k2 = 0
    for tag in soup.find_all('a', class_="ui__blueLink"):
        a = tag.attrs['href']
        if 'profile' in a:
            tab_name.append(tag.text)
            tab_url.append(tag.attrs['href'])
        else:
            tab_clans.append(tag.text)
            k1 +=1

        if k1 == 6:
            tab_clans.pop()
            break
        
    l = len(tab_name)
    for tag in soup.find_all('div', class_="clanParticipants__rowContainer"):
        if k2 != l:
            tab_fight.append(tag.attrs['data-battles'])
            tab_win.append(tag.attrs['data-wins'])
            tab_cards.append(tag.attrs['data-cards'])
        else: break
        k2 += 1
    return tab_name,tab_url,tab_fight,tab_win,tab_cards,tab_clans
    
    #for i in range( len(tab_name) ):
        #print("{0}___{1}___{2}___{3}__{4}".format(tab_name[i],tab_fight[i],tab_win[i],tab_cards[i],tab_url[i]))
    
def main_parsing():
    update_clash(clan_url)
    a = get_all_players(get_html(clan_url))
    b = get_stat_player(get_html(war_url))
    return a,b

if __name__ == '__main__':
    main_parsing()
