import json
import os
import urllib.request

import telegram
import logging

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.DEBUG
)

logger = logging.getLogger(__name__)

bot = telegram.Bot(token=os.environ["TELEGRAM_TOKEN"])


def telegram_webhook(request):
    if request.method == "POST":
        update = telegram.Update.de_json(request.get_json(force=True), bot)
        print("executing function")
        print(update)

        if update and update.callback_query:
            # Reply with the same message
            chat_id = update.callback_query.message.chat.id
            message = update.callback_query.data
        else:
            # Reply with the same message
            chat_id = update.message.chat.id
            message = update.message.text

        # bot.sendMessage(chat_id=chat_id, text=update.message.text)

        if message.lower() == "latest activity":
            latest_activity(chat_id)

        elif message.lower() == "latest creations":
            latest_creations(chat_id)

        # elif message.lower() == "artworks by artist":
        #     artist_works_menu(chat_id)

        elif message.lower() == "all artists":
            all_artists(chat_id)

        elif message.lower() == "least expensive":
            least_expensive(chat_id)

        elif message.lower() == "most expensive":
            most_expensive(chat_id)

        elif message.lower() == "/start" or message.lower() == "start":
            start(chat_id)

        else:
            bot.sendMessage(chat_id=chat_id, text="Hi, start to begin")
            start(chat_id)

    return "ok"


def start(chat_id):
    button_list = [
        [
            telegram.KeyboardButton("latest activity"),
            telegram.KeyboardButton("latest creations"),
            # telegram.InlineKeyboardButton("artworks by artist", callback_data="artworks by artist"),
        ],
        [
            telegram.KeyboardButton("least expensive"),
            telegram.KeyboardButton("most expensive"),
            # telegram.KeyboardButton("all artists"),
        ],
    ]
    # reply_markup = telegram.InlineKeyboardMarkup(button_list)
    reply_markup = telegram.ReplyKeyboardMarkup(button_list, resize_keyboard=True)
    bot.sendMessage(chat_id=chat_id, text="Choose option:", reply_markup=reply_markup)


#
# def artist_works_menu(chat_id):
#     print("artist works menu")
#     button_list = []
#     for artist in all_artists_lookup():
#         if artist['enabled'] and len(artist['ethAddress']) > 0:
#             button_list.append(
#                 telegram.InlineKeyboardButton(
#                     text=artist['name'],
#                     callback_data="eth_address_lookup=" + artist['ethAddress'][0]
#                 )
#             )
#
#     reply_markup = telegram.InlineKeyboardMarkup(inline_keyboard=list(chunks(button_list, 4)))
#     bot.sendMessage(chat_id=chat_id, text="Artists", reply_markup=reply_markup)


def all_artists(chat_id):
    print("All artist")
    high_works = ""
    for artist in all_artists_lookup():
        if artist['enabled'] and len(artist['ethAddress']) > 0:
            high_works += '<a href="https://dapp.knownorigin.io/artists/' + artist['ethAddress'][
                0] + '">' + artist['name'] + '</a>\n'

    bot.sendMessage(chat_id=chat_id, text=high_works, parse_mode="HTML")


def least_expensive(chat_id):
    print("Finding least expensive")
    high_works = ""
    for edition in least_expensive_lookup():
        high_works += build_edition_list(edition) + "\n"

    bot.sendMessage(chat_id=chat_id, text=high_works, parse_mode="HTML")


def most_expensive(chat_id):
    print("Finding most expensive")
    high_works = ""
    for edition in most_expensive_lookup():
        high_works += build_edition_list(edition) + "\n"

    bot.sendMessage(chat_id=chat_id, text=high_works, parse_mode="HTML")


def latest_creations(chat_id):
    print("Finding latest creations")
    high_works = ""
    for edition in latest_creations_lookup():
        high_works += build_edition_list(edition) + "\n"

    bot.sendMessage(chat_id=chat_id, text=high_works, parse_mode="HTML")


def latest_activity(chat_id):
    print("Finding latest activity")
    high_works = ""
    for edition in latest_activity_lookup():
        high_works += build_edition_list(edition) + "\n"

    bot.sendMessage(chat_id=chat_id, text=high_works, parse_mode="HTML")


def build_edition_list(data):
    high_works = ""
    artist_name = str(data[0])
    artwork_name = str(data[1])
    deep_link = str(data[6])

    price = "FREE" if data[3] == 0 else str(data[3]) + "ETH"
    remaining = "SOLD OUT" if data[2] == 0 else "(" + str(data[2]) + " remaining)"
    html_link = '<a href="' + deep_link + '">' + artwork_name + '</a>'

    high_works = high_works + "- " + html_link
    high_works = high_works + " by " + artist_name
    high_works = high_works + " - " + price
    return high_works + " " + remaining


def chunks(l, n):
    """Yield successive n-sized chunks from l."""
    for i in range(0, len(l), n):
        yield l[i:i + n]


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


def all_artists_lookup():
    common_url = "https://dapp.knownorigin.io/api/artist/all"
    with urllib.request.urlopen(common_url) as url:
        raw_artists = json.loads(url.read().decode())
        return raw_artists
