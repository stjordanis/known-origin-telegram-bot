import os
import telegram
import urllib.request, json
from time import sleep

bot = telegram.Bot(token=os.environ["TELEGRAM_TOKEN"])


def telegram_webhook(request):
    if request.method == "POST":
        update = telegram.Update.de_json(request.get_json(force=True), bot)
        print(update)

        chat_id = update.message.chat.id

        # Reply with the same message
        # bot.sendMessage(chat_id=chat_id, text=update.message.text)
        message = update.message.text

        if message.lower() == "least expensive":
            least_expensive(chat_id)

        if message.lower() == "most expensive":
            most_expensive(chat_id)

        if message.lower() == "latest activity":
            latest_activity(chat_id)

        if message.lower() == "latest creations":
            latest_creations(chat_id)

        if message.lower() == "/start" or message.lower() == "start":
            start(chat_id)

        bot.sendMessage(chat_id=chat_id, text=message)

    return "ok"


def start(chat_id):
    button_list = [
        [
            telegram.InlineKeyboardButton("all artists", callback_data="all artists"),
            telegram.InlineKeyboardButton("artworks", callback_data="artworks"),
            telegram.InlineKeyboardButton("latest creations", callback_data="latest creations")
        ],
        [
            telegram.InlineKeyboardButton("latest activity", callback_data="latest activity"),
            telegram.InlineKeyboardButton("least expensive", callback_data="least expensive"),
            telegram.InlineKeyboardButton("most expensive", callback_data="most expensive")
        ],
    ]
    reply_markup = telegram.InlineKeyboardMarkup(button_list)
    bot.sendMessage(chat_id=chat_id, text="Choose option:", reply_markup=reply_markup)


def least_expensive(chat_id):
    print("Finding least expensive")
    high_works = ""
    for y in least_expensive_lookup():
        high_works = high_works + "- Artist: " + str(y[0])
        high_works = high_works + ", work: " + str(y[1])
        high_works = high_works + ", price: " + str(y[3]) + " Eth"
        high_works = high_works + ", remaining works: " + str(y[2])
        html_link = '<a href="' + str(y[6]) + '">link to work</a>'
        high_works = high_works + ", " + html_link
        high_works = high_works + "\n"

    bot.sendMessage(chat_id=chat_id, text=high_works, parse_mode="HTML")


def most_expensive(chat_id):
    print("Finding most expensive")
    high_works = ""
    for y in most_expensive_lookup():
        high_works = high_works + "- Artist: " + str(y[0])
        high_works = high_works + ", work: " + str(y[1])
        high_works = high_works + ", price: " + str(y[3]) + " Eth"
        high_works = high_works + ", remaining works: " + str(y[2])
        html_link = '<a href="' + str(y[6]) + '">link to work</a>'
        high_works = high_works + ", " + html_link
        high_works = high_works + "\n"

    bot.sendMessage(chat_id=chat_id, text=high_works, parse_mode="HTML")


def latest_creations(chat_id):
    print("Finding latest creations")
    high_works = ""
    for y in latest_creations_lookup():
        high_works = high_works + "- Artist: " + str(y[0])
        high_works = high_works + ", work: " + str(y[1])
        high_works = high_works + ", price: " + str(y[3]) + " Eth"
        high_works = high_works + ", remaining works: " + str(y[2])
        html_link = '<a href="' + str(y[6]) + '">link to work</a>'
        high_works = high_works + ", " + html_link
        high_works = high_works + "\n"

    bot.sendMessage(chat_id, high_works, parse_mode="HTML")


def latest_activity(chat_id):
    print("Finding least activity")
    high_works = ""
    for edition in latest_activity_lookup():
        high_works = high_works + "- Artist: " + str(edition[0])
        high_works = high_works + ", work: " + str(edition[1])
        high_works = high_works + ", price: " + str(edition[3]) + " Eth"
        high_works = high_works + ", remaining works: " + str(edition[2])
        html_link = '<a href="' + str(edition[6]) + '">link to work</a>'
        high_works = high_works + ", " + html_link
        high_works = high_works + "\n"

    bot.sendMessage(chat_id=chat_id, text=high_works, parse_mode="HTML")


##
# API Lookups
##

def latest_activity_lookup():
    trending = []
    common_url = "https://dapp.knownorigin.io/api/network/1/feed/trending?limit=10"
    with urllib.request.urlopen(common_url) as url:
        my_dict_common = json.loads(url.read().decode())

        new_list_common = my_dict_common["data"]
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
            trending.append(temp_list)

    return trending


def latest_creations_lookup():
    creations = []
    common_url = "https://dapp.knownorigin.io/api/network/1/feed/latest?limit=10"
    with urllib.request.urlopen(common_url) as url:
        my_dict_common = json.loads(url.read().decode())
        new_list_common = my_dict_common["data"]
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
            creations.append(temp_list)

    return creations


def most_expensive_lookup():
    expensive = []
    common_url = "https://dapp.knownorigin.io/api/network/1/edition/gallery/list?limit=10&order=desc"
    with urllib.request.urlopen(common_url) as url:
        my_dict_common = json.loads(url.read().decode())
        new_list_common = my_dict_common["data"]
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
            expensive.append(temp_list)

    return expensive


def least_expensive_lookup():
    expensive = []
    common_url = "https://dapp.knownorigin.io/api/network/1/edition/gallery/list?limit=10&order=asc"
    with urllib.request.urlopen(common_url) as url:
        my_dict_common = json.loads(url.read().decode())
        new_list_common = my_dict_common["data"]
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
            expensive.append(temp_list)

    return expensive
