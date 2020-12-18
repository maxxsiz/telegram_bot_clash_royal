import telebot
import config
from telebot import types
from bot_func import addteg, stat_player_id, stat_player_teg, showclan, ranking
import sys
import datetime
from bot_grafiks import grafik_player_id, grafik_player_teg
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import sqlite3

textinfo = """<b>Мої можливості:</b>
    <b>/info або /help - всі команди бота;</b>
    <b>/join - прив'язка акаунта до телеграма;</b>
    <b>/ranking - рейтинг учасників клану;</b>
    <b>/mystat - статистика вашого акаунта
              (діє після прив'язки акаунта);</b>
    <b>/rules - правила клану та телеграм чату;</b> 
    <b>/aboutbot- інформація по боту;</b>
    <b>/rankinginfo - алгоритм обчислення рейтингу;</b>
    <b>/showclan - показує актуальний за добу стан клану;</b>
                         """
textrankinginfo = """<i>Алгоритм обчислення очків рейтингу:</i>
    <code>(a + b + c)*K + E</code>
    <code>a</code><b> - очки за перемогу (+10 за кожну) </b>
    <code>b</code><b> - очки за поразку (-5 за кожну) </b>
    <code>c</code><b> - очки за неатаку (-20 за кожну) </b>
    <code>K</code><b> - процент участі на кв</b>
    <code>E</code><b> - екстра пункти, які залежать від
    кількості карт, що ви набили за війну
    (можна отримати від -5 до +5 очків)</b>
                        """
textrules = """<b>Правила телеграм чату і чату гри:</b>
    1.1 Заборонені будь-які образи в сторону інших учасників.
    1.2 Заборонений надмірний флуд.
    1.3 Заборонений надмірний мат.
    1.4 Заборонена реклама сторонніх кланів та комерційна реклама.
    1.5 Заборонене розповсюдження порнографічного контенту.
        <b>Правила клану:</b>
    2.1 Кланові війни є обов'язковими. Їх може почати любий сорук.
    2.2 Кік будь-яких осіб без відома глави заборонені.
    2.3 Підвищення будь-яких осіб без відома глави заборонені.
    2.4 Зміну шапки клану виконує глава, як і регулювання
        налаштувань клану.
    2.5 Крім загальних соруків по заслугам, нище поданий
        список довірених соруків, яким присвоєні
        права глави і вони є рівносильні йому:
        \U0001F4CC Hord1k
        \U0001F4CC Avradacadavra
        \U0001F4CC Вовасик
    <b>Додаткові інформації:</b>
        Kлан має чорний список, в який будуть добавлені ігроки
        які сильно порушували правила і були вигнані з клану.
        Такі при поновному вступі в клан будуть вигнані повторно.
        Всі справи можна рішити напряму з главою клану.
        Такими справами можуть бути:
        \U0001F4CCЗміни в роботі клану, чату, бота
        \U0001F4CCЗапрошення друзів, які є нище кубків клану
    <b>Підвищення/кік та пониження:</b>
    2.7 Забороняється "клянчити" підвищення.
            Вимоги для підвищення:
            \U0001F4CC Час проведений в клані: не визначено.
            \U0001F4CC Мінімальний рейтинг: не визначено.
    2.8 Довіренні соруки та глава, лишають право за собою,
        понизити особу по іншій причині не вказаній в правилах.
        <i>Не все реально прописати в правилах.</i>
            Причини пониження/кіку:
            \U0001F4CC Порушення правил в клані.
            \U0001F4CC Неучасть в клановій війні.
            \U0001F4CC Рейтинг меньше: -30 
        """
textaboutbot = """<code> Mr.Bot V1.0 Pre Alpha 30.03.2020  by maxxsiz </code>
    <b>  Бот створенний виключно під клан Clash Royale
    Жодна приватна інформація про учасників чату
    або клану не використовується. Вся інформація,
    яка обробляється є загально доступною.
    Бот знаходиться в <u>Альфа</u> тестуванні, тому можливі
    багаточисленні баги та тимчасові неполадки бота.
    З радістю приймаються <u>адекватнi</u> пропозиції по розвитку бота:
    \U0001F4CC добавлення нових функцій
    \U0001F4CC апгрейд старих
    \U0001F4CC еліміування багів та дрібних проблем</b>
    <i> Р.S. Бот активно розробляється,тому не думайте,
    що робота стоїть;)</i>
    """
main_chat_id = -1001307161525


def gen_markup(): #main keyboard
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    markup.add(InlineKeyboardButton("Cтатистики клану", callback_data="stat_clan"),InlineKeyboardButton("Статистика ігрока", callback_data="stat_player"),InlineKeyboardButton("Підключення", callback_data="connect"),InlineKeyboardButton("Інше", callback_data="other"))
    return markup
def stat_markup():#stat keyboard
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    markup.add(InlineKeyboardButton("Моя статистика", callback_data="mystat"),InlineKeyboardButton("Графік 10 кв", callback_data="last10"),InlineKeyboardButton("Інше", callback_data="other_stat"),InlineKeyboardButton("Назад", callback_data="to_main"))
    return markup
def stat_clan_markup():#stat keyboard
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    markup.add(InlineKeyboardButton("Рейтинг клану", callback_data="clanranking"),InlineKeyboardButton("Учасники клану", callback_data="clanplayers"),InlineKeyboardButton("График", callback_data="clan_grafik"),InlineKeyboardButton("Назад", callback_data="to_main"))
    return markup
def conn_markup():#connect keyboard
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    markup.add(InlineKeyboardButton("Підключення акаунта", callback_data="conn_akk"),InlineKeyboardButton("Зміна акаунта", callback_data="change_akk"),InlineKeyboardButton("Назад", callback_data="to_main"))
    return markup
def other_markup():#other keyboard
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    markup.add(InlineKeyboardButton("Правила", callback_data="rules"),InlineKeyboardButton("About bot", callback_data="about_bot"),InlineKeyboardButton("Всі команди", callback_data="all_commands"),InlineKeyboardButton("Назад", callback_data="to_main"))
    return markup

def bot_main():
    
    non_bmp_map = dict.fromkeys(range(0x10000, sys.maxunicode + 1), 0xfffd)
    botnikname = '@StatMaxClanBot'
    def listener(messages):
        for m in messages:
            a = m.chat.id
            user_id = m.from_user.id
            main_chat_id = -1001307161525
            if m.content_type == 'left_chat_member':
                print( str(m.left_chat_member.id) + ' ' + str(m.left_chat_member.first_name)+ " " + str(m.left_chat_member.last_name) + " [" + str(m.chat.id) + "]: " + 'Left the chat')
            elif m.text == "/start":
                bot.send_message(a,textinfo,parse_mode='html')
            elif m.content_type == 'new_chat_members':
                print( str(m.new_chat_member.id) + ' ' + str(m.new_chat_member.first_name)+ " " + str(m.new_chat_member.last_name) + " [" + str(m.chat.id) + "]: " + 'Join the chat')
                stiker = open('sticker_welcome.webp','rb')
                bot.send_sticker(a, stiker)
                bot.send_message(a, "Привіт, {0}!\n Я -{1.first_name}, бот помічник!\n Пропиши /info, щоб знати. що я можу.\nВелике прохання, користуватися ботом здебільшого\nв приватному чаті з ботом.".format(m.new_chat_member.first_name,bot.get_me()),parse_mode='html')
            elif m.content_type == 'text':
                m_tex = m.text
                m_send = m_tex[5:]
                m_tex = m_tex.translate(non_bmp_map)
                m_add = m_tex[:5]
                if m.chat.id == main_chat_id:
                    print(str(m.from_user.id) + ' ' + str(m.from_user.first_name)+ " " + str(m.from_user.last_name) + " [" + "General chat" + "]: " + m_tex )
                else:
                    print(str(m.from_user.id) + ' ' + str(m.from_user.first_name)+ " " + str(m.from_user.last_name) + " [" + "Private chat" + "]: " + m_tex )
                if m_tex == '/mystat' or m_tex  == '/mystat'+botnikname and m.content_type == 'text':
                    player_stat_run(a, user_id)
                    player_10last_run(a, user_id)
                elif  m_add == "/add#" and m.content_type == 'text' :
                    userid = m.from_user.id
                    teg = m_tex[5:]
                    username = m.from_user.first_name + m.from_user.last_name
                    bot.send_message(m.chat.id,addteg(teg,userid,username),parse_mode='html')
                elif "куку" in m_tex or "привіт" in m_tex or "здарова" in m_tex and m.from_user.id == [887767512,578146202]:
                    bot.send_message(a,"<b>Привіт пупсік</b>", parse_mode='html')

                    
    def admin_listener(messages):
        for mm in messages:
            main_chat_id = -1001307161525
            if mm.from_user.id == 578146202:
                mm_text = mm.text
                text5 = mm_text[:5]
                if text5 == '/send':
                    mm_send = mm_text[5:]
                    bot.send_message(-1001307161525,mm_send,parse_mode = 'html')
                elif text5 == '/stat':
                    mm_teg = mm_text[5:]
                    bot.send_message(mm.chat.id, stat_player_teg(mm_teg),parse_mode='html')
                    bot.send_message(mm.chat.id, "Зачекайте, завантажуємо розширенну статистику...",parse_mode='html')
                    grafik_player_teg(mm_teg)
                    bot.send_photo(mm.chat.id, open('C:/Users/maxxsiz/Desktop/scr/fig1.png', 'rb')) 
            else:
                pass
                
    bot = telebot.TeleBot(config.TOKEN)
    bot.set_update_listener(listener)
    bot.set_update_listener(admin_listener)
    def player_stat_run(chat_id, user_id):
        bot.send_message(chat_id, stat_player_id(user_id),parse_mode='html')
    def player_10last_run(chat_id, user_id):
        bot.send_message(chat_id, "Зачекайте, завантажуємо розширенну статистику...",parse_mode='html')
        grafik_player_id(user_id)
        bot.send_photo(chat_id, open('C:/Users/maxxsiz/Desktop/scr/fig1.png', 'rb'))
    def info_run(chat_id, user_id):
        try:
            bot.send_message(user_id,textinfo,parse_mode='html')
            if chat_id == main_chat_id:
                bot.send_message(chat_id,"<b>Я тобі написав в приватні повідомлення.</b>", parse_mode ='html')
        except:
            bot.send_message(chat_id,textinfo,parse_mode='html')
    def rules_run(chat_id, user_id):
        try:
            bot.send_message(user_id,textrules,parse_mode='html')
            if chat_id == main_chat_id:
                bot.send_message(chat_id,"<b>Я тобі написав в приватні повідомлення.</b>", parse_mode ='html')
        except:
            bot.send_message(chat_id,textrules,parse_mode='html')
    def ranking_info_run(chat_id, user_id):
        try:
            bot.send_message(user_id,textrankinginfo,parse_mode='html')
            if chat_id == main_chat_id:
                bot.send_message(chat_id,"<b>Я тобі написав в приватні повідомлення.</b>", parse_mode ='html')
        except:
            bot.send_message(chat_id,textrankinginfo,parse_mode='html')
    def ranking_run(chat_id, user_id):
        try:
            bot.send_message(user_id,ranking(),parse_mode='html')
            if chat_id == main_chat_id:
                bot.send_message(chat_id,"<b>Я тобі написав в приватні повідомлення.</b>", parse_mode ='html')
        except:
            bot.send_message(chat_id,ranking(),parse_mode='html')
    def aboutbot_run(chat_id, user_id):
        try:
            bot.send_message(user_id,textaboutbot,parse_mode='html')
            if chat_id == main_chat_id:
                bot.send_message(chat_id,"<b>Я тобі написав в приватні повідомлення.</b>", parse_mode ='html')
        except:
            bot.send_message(chat_id,textaboutbot,parse_mode='html')
    def showclan_run(chat_id, user_id):
        try:
            bot.send_message(user_id,showclan(),parse_mode='html')
            if chat_id == main_chat_id:
                bot.send_message(chat_id,"<b>Я тобі написав в приватні повідомлення.</b>", parse_mode ='html')
        except:
            bot.send_message(chat_id,showclan(),parse_mode='html')
    def join_run(chat_id, user_id):
        try:
            bot.send_message(user_id,"<b>Для того, щоб добавити Ваш акаунт з Clash Royale, введіть</b> <pre>/add#ваштег</pre>",parse_mode='html')
            if chat_id == main_chat_id:
                bot.send_message(chat_id,"<b>Я тобі написав в приватні повідомлення.</b>", parse_mode ='html')
        except:
            bot.send_message(chat_id,"<b>Для того, щоб добавити Ваш акаунт з Clash Royale, введіть</b> <pre>/add#ваштег</pre>",parse_mode='html')
        
    @bot.message_handler(commands=['help','info','start','ranking','mystat','rules','aboutbot','showclan','rankinginfo','join','menu','kakaszka'])
    def send_start(message):
        main_chat_id = -1001307161525 #id основного телеграм чата
        chat_id = message.chat.id #a
        mt = message.text #mt
        user_id = message.from_user.id
        user_message_id = message.from_user.id
        if mt == '/info' or mt == '/help' or mt == '/help' + botnikname or mt == '/info' + botnikname:
            info_run(chat_id,user_id)
        elif mt == '/ranking' or mt == '/ranking' + botnikname:
            ranking_run(chat_id, user_id)
        elif mt == '/kakaszka' or mt == '/kakaszka' + botnikname:
            bot.send_photo(chat_id, open('C:/Users/maxxsiz/Desktop/scr/screamer.jpg', 'rb'))
        elif mt == '/rankinginfo' or mt == '/rankinginfo' + botnikname:
            ranking_info_run(chat_id, user_id) 
        elif mt == '/rules' or mt == '/rules' + botnikname:
            rules_run(chat_id, user_id)
        elif mt == '/aboutbot' or mt == '/aboutbot' + botnikname:
            aboutbot_run(chat_id, user_id)
        elif mt == '/showclan' or mt == '/showclan' + botnikname:
            showclan_run(chat_id,user_id)
        elif mt == '/join' or mt == '/join' + botnikname:
            join_run(chat_id, user_id)
        elif mt == '/menu' or mt == '/menu' + botnikname:
            try:
                bot.send_message(user_id, "Виберіть, що Вас цікавить.", reply_markup=gen_markup())
                if chat_id == main_chat_id:
                    bot.send_message(chat_id,"<b>Я тобі написав в приватні повідомлення.</b>", parse_mode ='html')
            except:
                bot.send_message(chat_id,"Виберіть, що Вас цікавить.", reply_markup=gen_markup())

            
    @bot.callback_query_handler(func=lambda call: True)
    def callback_query(call):
        user_id = call.from_user.id
        chat_id = call.message.chat.id
        if call.data == "all_commands":
            info_run(chat_id,user_id)   
            bot.delete_message(call.message.chat.id, call.message.message_id)
        elif call.data == "stat_player":
            bot.send_message(chat_id,"Виберіть, що Вас цікавить.", reply_markup=stat_markup())
            bot.delete_message(call.message.chat.id, call.message.message_id)
        elif call.data == "connect":
            bot.send_message(chat_id, "Виберіть, що Вас цікавить.", reply_markup=conn_markup())
            bot.delete_message(call.message.chat.id, call.message.message_id) 
        elif call.data == "other":
            bot.send_message(chat_id, "Виберіть, що Вас цікавить.", reply_markup=other_markup())
            bot.delete_message(call.message.chat.id, call.message.message_id)
        elif call.data == "to_main":
            bot.send_message(chat_id, "Виберіть, що Вас цікавить.", reply_markup=gen_markup())
            bot.delete_message(call.message.chat.id, call.message.message_id)
        elif call.data == "mystat":
            player_stat_run(chat_id, user_id)
            bot.delete_message(call.message.chat.id, call.message.message_id)
        elif call.data == "last10":
            bot.delete_message(call.message.chat.id, call.message.message_id)
            player_10last_run(chat_id, user_id)
        elif call.data == "other_stat":#!
            bot.answer_callback_query(call.id, "В розробці")
            #bot.delete_message(call.message.chat.id, call.message.message_id)
        elif call.data == "stat_clan":
            bot.send_message(chat_id, "Виберіть, що Вас цікавить.", reply_markup=stat_clan_markup())
            bot.delete_message(call.message.chat.id, call.message.message_id)
        elif call.data == "rules":
            bot.answer_callback_query(call.id, "Answer is No")
            bot.delete_message(call.message.chat.id, call.message.message_id)
        elif call.data == "about_bot":
            aboutbot_run(chat_id, user_id)
            bot.delete_message(call.message.chat.id, call.message.message_id)
        elif call.data == "conn_akk":
            join_run(chat_id, user_id)
            bot.delete_message(call.message.chat.id, call.message.message_id)
        elif call.data == "change_akk":#!
            bot.answer_callback_query(call.id, "В розробці")
            #bot.delete_message(call.message.chat.id, call.message.message_id)
        elif call.data == "clanranking":
            ranking_run(chat_id, user_id)
            bot.delete_message(call.message.chat.id, call.message.message_id)
        elif call.data == "clanplayers":
            showclan_run(chat_id, user_id)
            bot.delete_message(call.message.chat.id, call.message.message_id)
        elif call.data == "clan_grafik":#!
            bot.answer_callback_query(call.id, "В розробці")
            #bot.delete_message(call.message.chat.id, call.message.message_id)
        
            
            
    #bot.polling(none_stop=False, interval=0, timeout=20)
    bot.infinity_polling()
        
def start_restart():
    try:
        bot_main()
    except Exception as e:
        log = open('log.txt','a')
        tim = datetime.datetime.now()
        text = tim.strftime("\n%d-%m-%Y %H:%M") + " ---- " + " Виникла помилка, обновлення не вдалось." + e
        log.write(text)
        log.close()
        start_restart()

start_restart()
