import telebot
import urllib.request, json
from time import sleep


# ---KO part---
def get_artist_wallet():
    global full_list
    global eth_artist_dict
    eth_artist_dict = {}
    common_url = (
        "https://dapp.knownorigin.io/api/network/1/feed/latest?limit=100000000"
    )  # ?limit=10'
    with urllib.request.urlopen(common_url) as url:
        my_dict_common = json.loads(url.read().decode())
        new_list_common = my_dict_common["data"]
        full_list = []
        for x in new_list_common:
            temp_list = []
            temp_list.append(x["artist"]["name"])
            temp_list.append(x["name"])

            remain = int(x["totalAvailable"]) - int(x["totalSupply"])
            temp_list.append(remain)
            temp_list.append(x["priceInEther"])
            temp_list.append(x["id"])
            temp_list.append(x["artist_deeplink_url"])
            temp_list.append(x["marketplace_deeplink_url"])
            full_list.append(temp_list)

    return full_list


def last_10_created():
    global full_list_10c
    common_url = "https://dapp.knownorigin.io/api/network/1/feed/latest?limit=10"
    with urllib.request.urlopen(common_url) as url:
        my_dict_common = json.loads(url.read().decode())

        new_list_common = my_dict_common["data"]
        full_list_10c = []
        for x in new_list_common:
            temp_list = []
            temp_list.append(x["artist"]["name"])
            temp_list.append(x["name"])

            remain = int(x["totalAvailable"]) - int(x["totalSupply"])
            temp_list.append(remain)
            temp_list.append(x["priceInEther"])
            temp_list.append(x["id"])
            temp_list.append(x["artist_deeplink_url"])
            temp_list.append(x["marketplace_deeplink_url"])
            full_list_10c.append(temp_list)

    return full_list_10c


def last_10_active():
    global full_list_10activ
    common_url = "https://dapp.knownorigin.io/api/network/1/feed/trending?limit=10"
    with urllib.request.urlopen(common_url) as url:
        my_dict_common = json.loads(url.read().decode())

        new_list_common = my_dict_common["data"]
        full_list_10activ = []
        for x in new_list_common:
            temp_list = []
            temp_list.append(x["artist"]["name"])
            temp_list.append(x["name"])

            remain = int(x["totalAvailable"]) - int(x["totalSupply"])
            temp_list.append(remain)
            temp_list.append(x["priceInEther"])
            temp_list.append(x["id"])
            temp_list.append(x["artist_deeplink_url"])
            temp_list.append(x["marketplace_deeplink_url"])
            full_list_10activ.append(temp_list)

    return full_list_10activ


def most_expensive():
    global most_expencive2_list
    common_url = "https://dapp.knownorigin.io/api/network/1/edition/gallery/list?limit=10&order=desc"
    with urllib.request.urlopen(common_url) as url:
        my_dict_common = json.loads(url.read().decode())

        new_list_common = my_dict_common["data"]
        most_expencive2_list = []
        for x in new_list_common:
            temp_list = []
            temp_list.append(x["artist"]["name"])
            temp_list.append(x["name"])

            remain = int(x["totalAvailable"]) - int(x["totalSupply"])
            temp_list.append(remain)
            temp_list.append(x["priceInEther"])
            temp_list.append(x["id"])
            temp_list.append(x["artist_deeplink_url"])
            temp_list.append(x["marketplace_deeplink_url"])
            most_expencive2_list.append(temp_list)
    return most_expencive2_list


def least_expensive():
    global least_expencive2_list
    common_url = "https://dapp.knownorigin.io/api/network/1/edition/gallery/list?limit=10&order=asc"
    with urllib.request.urlopen(common_url) as url:
        my_dict_common = json.loads(url.read().decode())

        new_list_common = my_dict_common["data"]
        least_expencive2_list = []
        for x in new_list_common:
            temp_list = []
            temp_list.append(x["artist"]["name"])
            temp_list.append(x["name"])

            remain = int(x["totalAvailable"]) - int(x["totalSupply"])
            temp_list.append(remain)
            temp_list.append(x["priceInEther"])
            temp_list.append(x["id"])
            temp_list.append(x["artist_deeplink_url"])
            temp_list.append(x["marketplace_deeplink_url"])
            least_expencive2_list.append(temp_list)
    return least_expencive2_list


# ---END of KO part----


# ----Telegram BOT part----------------
from telebot import types

bot_token = "FIXME"

bot = telebot.TeleBot(bot_token)

my_separator = " || "


@bot.message_handler(func=lambda message: True)
def echo_all(message):
    trig_unknown_cmd = 0

    get_artist_wallet()
    chat_id = message.chat.id

    if message.text.lower() == "all artists":
        trig_unknown_cmd = 1
        allartists = []
        check_uniq = []  # to check unique artist
        for x in full_list:
            if x[0] not in check_uniq:
                check_uniq.append(x[0])
                temp = []
                temp.append(x[0])
                html_link = '<a href="' + str(x[5]) + '">link to artist</a>'
                temp.append(html_link)
                allartists.append(temp)

        mes_cutter(chat_id, allartists)

    if message.text.lower() == "10 least expensive":
        least_expensive()
        trig_unknown_cmd = 1
        high_works = ""
        for y in least_expencive2_list:
            high_works = high_works + "- Artist: " + str(y[0])
            high_works = high_works + ", work: " + str(y[1])
            high_works = high_works + ", price: " + str(y[3]) + " Eth"
            high_works = high_works + ", remaining works: " + str(y[2])
            html_link = '<a href="' + str(y[6]) + '">link to work</a>'
            high_works = high_works + ", " + html_link
            high_works = high_works + "\n"

        bot.send_message(chat_id, high_works, parse_mode="HTML")

    if message.text.lower() == "10 most expensive":
        most_expensive()
        trig_unknown_cmd = 1
        high_works = ""
        for y in most_expencive2_list:
            high_works = high_works + "- Artist: " + str(y[0])
            high_works = high_works + ", work: " + str(y[1])
            high_works = high_works + ", price: " + str(y[3]) + " Eth"
            high_works = high_works + ", remaining works: " + str(y[2])
            html_link = '<a href="' + str(y[6]) + '">link to work</a>'
            high_works = high_works + ", " + html_link
            high_works = high_works + "\n"

        bot.send_message(chat_id, high_works, parse_mode="HTML")

    if message.text.lower() == "artworks by artist":
        trig_unknown_cmd = 1
        msg = "Enter artist name in the format like:" + "\n" + "Artist=Picasso"
        bot.send_message(chat_id, msg)

    check_for_artist = message.text.lower()
    if check_for_artist[:7] == "artist=":
        trig_unknown_cmd = 1
        high_works = ""
        my_artist = check_for_artist[7:]
        artist_found = 0
        for y in full_list:
            artist_low_let = y[0]
            artist_low_let = artist_low_let.lower()
            if artist_low_let == my_artist:
                high_works = high_works + "- Artist: " + str(y[0])
                high_works = high_works + ", work: " + str(y[1])
                high_works = high_works + ", price: " + str(y[3]) + " Eth"
                high_works = high_works + ", remaining works: " + str(y[2])
                html_link = '<a href="' + str(y[6]) + '">link to work</a>'
                high_works = high_works + ", " + html_link
                high_works = high_works + "\n"
                artist_found = 1

        if artist_found == 1:
            bot.send_message(chat_id, high_works, parse_mode="HTML")
        else:
            bot.send_message(chat_id, "artist not found")

        bot.send_message(chat_id, "click /start to begin")

    if message.text.lower() == "last 10 created":
        high_works = ""
        trig_unknown_cmd = 1
        last_10_created()
        for y in full_list_10c:
            high_works = high_works + "- Artist: " + str(y[0])
            high_works = high_works + ", work: " + str(y[1])
            high_works = high_works + ", price: " + str(y[3]) + " Eth"
            high_works = high_works + ", remaining works: " + str(y[2])
            html_link = '<a href="' + str(y[6]) + '">link to work</a>'
            high_works = high_works + ", " + html_link
            high_works = high_works + "\n"

        bot.send_message(chat_id, high_works, parse_mode="HTML")

    if message.text.lower() == "last 10 activity":
        high_works = ""
        trig_unknown_cmd = 1
        last_10_active()
        for y in full_list_10activ:
            high_works = high_works + "- Artist: " + str(y[0])
            high_works = high_works + ", work: " + str(y[1])
            high_works = high_works + ", price: " + str(y[3]) + " Eth"
            high_works = high_works + ", remaining works: " + str(y[2])
            html_link = '<a href="' + str(y[6]) + '">link to work</a>'
            high_works = high_works + ", " + html_link
            high_works = high_works + "\n"

        bot.send_message(chat_id, high_works, parse_mode="HTML")

    if message.text.lower() == "/start" or message.text.lower() == "start":
        trig_unknown_cmd = 1

        markup = types.ReplyKeyboardMarkup(row_width=3)
        itembtn1 = types.KeyboardButton("all artists")
        itembtn2 = types.KeyboardButton("artworks by artist")
        itembtn3 = types.KeyboardButton("last 10 created")

        itembtn4 = types.KeyboardButton("last 10 activity")
        itembtn5 = types.KeyboardButton("10 least expensive")
        itembtn6 = types.KeyboardButton("10 most expensive")

        markup.add(itembtn1, itembtn2, itembtn3, itembtn4, itembtn5, itembtn6)
        bot.send_message(chat_id, "Choose button:", reply_markup=markup)

    if trig_unknown_cmd == 0:
        bot.send_message(chat_id, "command unknown, click /start to begin")


def mes_cutter(chat_id, my_message):
    to_sent = ""
    trig_unknown_cmd_sleep = 0
    for x in my_message:
        to_sent = to_sent + x[0] + ", " + x[1] + my_separator
        if len(to_sent) > 3300:
            bot.send_message(chat_id, to_sent, parse_mode="HTML")
            to_sent = ""
            sleep(0.3)  # delay to keep message order
            trig_unknown_cmd_sleep = 1
    if trig_unknown_cmd_sleep == 0:
        sleep(0.3)
    bot.send_message(chat_id, to_sent, parse_mode="HTML")


bot.polling()
