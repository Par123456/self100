from email import message
from pyrogram import Client, idle, filters
import secrets
from asyncio import sleep
from random import choice
from pyrogram.enums import ChatType
import json
from pyrogram import enums
from translate import Translator
import pyttsx3
from db import *
import zipfile
import shutil
from Python_ARQ import ARQ
from sys import version as pyver
from imdb import IMDb
import inspect
from pySmartDL import SmartDL
import traceback
from youtubesearchpython import VideosSearch
from pytube import YouTube
import sys
from os import listdir
from functions import (convert_seconds, download_and_transcode_song,
                       generate_cover, generate_cover_square, time_to_seconds,
                       transcode)
import io
import aiohttp
from urllib.parse import urlparse
from youtube_dl import YoutubeDL
from opencc import OpenCC
from hurry.filesize import size
from pyrogram.errors import BadRequest, Forbidden, NotAcceptable
from pyrogram.errors.exceptions.bad_request_400 import *


from pyrogram.types import Message, ChatPermissions, ReplyKeyboardMarkup, InlineQueryResultArticle, \
    InputTextMessageContent, InlineKeyboardMarkup, InlineKeyboardButton as button, InlineQueryResultPhoto, CallbackQuery
from pyrogram.raw.functions.messages import ReadReactions
from pyrogram.raw.types import StatsURL
import re, sys, os, requests
import asyncio
import random
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from os import getenv
from time import time
from os import path
import subprocess
import psutil
from bs4 import BeautifulSoup
import bs4
import lxml
from datetime import datetime
import datetime
import math
app = Client("sourcemate", 29042268, '54a7b377dd4a04a58108639febe2f443')

import re

# Define morse code lookup table
api_key = '8261570d-74a7-4f48-cdbd32f2'
api_secret = '40b598eabb8a50114366dc4432d1781762eb8'
endpoint = 'https://nextpay.org/nx/gateway'
lookup = {
    '!': '-.-.--',
    "'": '.----.',
    '"': '.-..-.',
    '$': '...-..-',
    '&': '.-...',
    '(': '-.--.',
    ')': '-.--.-',
    '+': '.-.-.',
    ',': '--..--',
    '-': '-....-',
    '.': '.-.-.-',
    '/': '-..-.',
    '0': '-----',
    '1': '.----',
    '2': '..---',
    '3': '...--',
    '4': '....-',
    '5': '.....',
    '6': '-....',
    '7': '--...',
    '8': '---..',
    '9': '----.',
    ':': '---...',
    ';': '-.-.-.',
    '=': '-...-',
    '?': '..--..',
    '@': '.--.-.',
    'A': '.-',
    'B': '-...',
    'C': '-.-.',
    'D': '-..',
    'E': '.',
    'F': '..-.',
    'G': '--.',
    'H': '....',
    'I': '..',
    'J': '.---',
    'K': '-.-',
    'L': '.-..',
    'M': '--',
    'N': '-.',
    'O': '---',
    'P': '.--.',
    'Q': '--.-',
    'R': '.-.',
    'S': '...',
    'T': '-',
    'U': '..-',
    'V': '...-',
    'W': '.--',
    'X': '-..-',
    'Y': '-.--',
    'Z': '--..',
    '_': '..--.-',
}

# Define function to convert text to morse code
def text_to_morse(text):
    morse_code = []
    for c in text.upper():
        if c not in lookup:
            raise ValueError(f"Invalid character '{c}' in text")
        morse_code.append(lookup[c])
    return " ".join(morse_code)

# Define function to convert morse code to text
def morse_to_text(morse):
    text = ""
    for code in morse.split(" "):
        for char, code_lookup in lookup.items():
            if code == code_lookup:
                text += char
                break
        else:
            raise ValueError(f"Invalid code '{code}' in morse")
    return text

# Define handler for the "morset" command
morse_to_char = {value: key for key, value in lookup.items()}
# Config ||:
def morse_to_string(morse_code):
    decoded = []
    for word in morse_code.split('   '):
        decoded_word = []
        for char in word.split(' '):
            if char in morse_to_char:
                decoded_word.append(morse_to_char[char])
        decoded.append(''.join(decoded_word))
    return ' '.join(decoded)

moviepath = os.path.join(os.getcwd(), "temp", "moviethumb.jpg")
YTDL_REGEX = (r"^((?:https?:)?\/\/)"
              r"?((?:www|m)\.)"
              r"?((?:|xvideos\.com|pornhub\.com"
              r"|xhamster\.com|xnxx\.com))"
              r"(\/)([-a-zA-Z0-9()@:%_\+.~#?&//=]*)([\w\-]+)(\S+)?$")
s2tw = OpenCC('s2tw.json').convert
ARQ_API_KEY = "MHMNRX-HWUKCU-ETRNRT-TLOLFI-ARQ"
# don't make changes below this line
ARQ_API = "https://thearq.tech"
queue = []  # This is where the whole song queue is stored
playing = False  # Tells if something is playing or not
call = {}
imdb = IMDb()

mov_titles = [
    "long imdb title",
    "long imdb canonical title",
    "smart long imdb canonical title",
    "smart canonical title",
    "canonical title",
    "localized title",
]


async def get_cast(casttype, movie):
    mov_casttype = ""
    if casttype in list(movie.keys()):
        i = 0
        for j in movie[casttype]:
            if i < 1:
                mov_casttype += str(j)
            elif i < 5:
                mov_casttype += ", " + str(j)
            else:
                break
            i += 1
    else:
        mov_casttype += "Not Data"
    return mov_casttype


async def get_moviecollections(movie):
    result = ""
    if "box office" in movie.keys():
        for i in movie["box office"].keys():
            result += f"\n•  <b>{i}:</b> <code>{movie['box office'][i]}</code>"
    else:
        result = "<code>No Data</code>"
    return result


plugin_category = "utils"


def deEmojify(text):
    regrex_pattern = re.compile(pattern="["
                                        u"\U0001F600-\U0001F64F"  # emoticons
                                        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                                        u"\U0001F680-\U0001F6FF"  # transport & map symbols
                                        u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                                        "]+", flags=re.UNICODE)
    return regrex_pattern.sub(r'', text)


CARBONLANG = "auto"


def get_arg(message):
    msg = message.text
    msg = msg.replace(" ", "", 1) if msg[1] == " " else msg
    split = msg[1:].replace("\n", " \n").split(" ")
    if " ".join(split[1:]).strip() == "":
        return ""
    return " ".join(split[1:])


def yt_search(song):
    videosSearch = VideosSearch(song, limit=1)
    result = videosSearch.result()
    if not result:
        return False
    else:
        video_id = result["result"][0]["id"]
        url = f"https://youtu.be/{video_id}"
        return url

def humanbytes(size):
    """Input size in bytes,
    outputs in a human readable format"""
    # https://stackoverflow.com/a/49361727/4723940
    if not size:
        return ""
    # 2 ** 10 = 1024
    power = 2**10
    raised_to_pow = 0
    dict_power_n = {0: "", 1: "Ki", 2: "Mi", 3: "Gi", 4: "Ti"}
    while size > power:
        size /= power
        raised_to_pow += 1
    return str(round(size, 2)) + " " + dict_power_n[raised_to_pow] + "B"


def time_formatter(milliseconds: int) -> str:
    """Inputs time in milliseconds, to get beautified time,
    as string"""
    seconds, milliseconds = divmod(int(milliseconds), 1000)
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    days, hours = divmod(hours, 24)
    tmp = ((str(days) + " day(s), ") if days else "") + \
        ((str(hours) + " hour(s), ") if hours else "") + \
        ((str(minutes) + " minute(s), ") if minutes else "") + \
        ((str(seconds) + " second(s), ") if seconds else "") + \
        ((str(milliseconds) + " millisecond(s), ") if milliseconds else "")
    return tmp[:-2]
async def progress(current, total, message, start, type_of_ps, file_name=None):
    """Generic progress_callback for uploads and downloads."""
    now = time.time()
    diff = now - start
    if round(diff % 10.00) == 0 or current == total:
        percentage = current * 100 / total
        speed = current / diff
        elapsed_time = round(diff) * 1000
        time_to_completion = round((total - current) / speed) * 1000
        estimated_total_time = elapsed_time + time_to_completion
        progress_str = "[{0}{1}] {2}%\n".format(
            ''.join(["▰" for i in range(math.floor(percentage / 10))]),
            ''.join(["▱" for i in range(10 - math.floor(percentage / 10))]),
            round(percentage, 2))
        tmp = progress_str + \
            "{0} of {1}\nETA: {2}".format(
                humanbytes(current),
                humanbytes(total),
                time_formatter(estimated_total_time)
            )
        if file_name:
            await message.edit("{}\nFile Name: `{}`\n{}".format(
                type_of_ps, file_name, tmp))
        else:
            await message.edit("{}\n{}".format(type_of_ps, tmp))
# def enemylist():
#    global db
#    global dbs
#    db.execute("SELECT id FROM enemy")
#   curse = [i[0] for i in db.fetchall()]
#   return curse
# @app.on_message(filters.user(list(map(int,enemylist()))))
# async def mes(client,message):
#    db.execute("SET SESSION TRANSACTION ISOLATION LEVEL READ COMMITTED")
#    db.execute("SELECT text FROM foshlist")
#    curse = [i[0] for i in db.fetchall()]
#    s = secrets.choice(curse)
#    await message.reply(s)
#    await asyncio.sleep(1)


@app.on_message(filters.me & filters.command('run'), group=0)
def exec_(client, message):
    code = message.text.split("/run")[1]
    try:
        aha = exec(code)
        app.edit_message_text(message.chat.id, message.id, "**code**:\n %s \n\n **output**:\nsuccess" % code)
    except Exception as e:
        app.edit_message_text(message.chat.id, message.id, "code:\n %s \n\n output:\n %s" % (code, e))


@app.on_message( filters.me, group=1)
async def clim(client, message):
    chat = message.chat
    # users =
    chat_id = chat.id
    user = message.from_user
    MazCli = message.edit if bool(user and user.is_self) else message.reply_text
    text = message.text if message.text else ''
    textt = text.lower()
    if message.text == 'update':
        f = open("%s.json" % message.chat.id, "w")
        f.write("%s" % message)
        f.close()
        await app.send_document(message.chat.id, "%s.json" % message.chat.id)
        os.remove("%s.json" % message.chat.id)
    if message.text == 'help':
        helfa = "• سـلـفـ تـوکـیـو\ۭ۟سٖۢۢو۠ۛرۭۨ۟سۢ ۪ۧمِۭۚٚیٌٍۣٖٛۨتِۖ ۛرۣۨٛاٝ دِۣٝٞنًِۭ۠بِۣۚٛاِٝۡلٖٛ ۭۨڪِۣٛٞ@丂ㄖㄩ尺匚モ爪丹ㄒモ\n\nܝ‌ߊ‌ܣܢߺ߭ܩߊ‌ܢߺ࡙ ࡄܝ‌ࡏަܝ‌ܩܢߺ࡙\n❅ `fun`\n\nܝ‌ߊ‌ܣܢߺ߭ܩߊ‌ܢߺ࡙ ࡄࡋܦ߭\n❅ `self`\n\nܩࡅ‌ܢߺ࡙ܝ‌ܢߺ࡙ܝߺ̈ߺߺ ࡏަܝ‌၄‌ܣ\n ❅ `gap` \n\n  🇯🇵 @MakranSource 🇯🇵"
        await app.edit_message_text(message.chat.id, message.id, helfa)
    if re.match('^Proxy|proxy|پروکسی$', text):
        Web = requests.get('https://t.me/s/{}'.format('GlypeX')).text
        Proxy = re.finditer('https://t.me/proxy\?server=(\d+.\d+.\d+.\d+)&port=(\d+)&secret=(\w+)',
                            Web.replace('amp;', ''))
        txt = ''
        i = 0
        for P in Proxy:
            txt += '**🔑{}🔑**: [connect to]({})\n'.format(i + 1, P.group())
            i = i + 1
            if i == 10: break
        await MazCli(txt)
    if "promote" in message.text and message.reply_to_message:
        id = message.reply_to_message.from_user.id
        texts = text.split('promote ')
        try:
            adt = texts[1] if texts[1] else "admin"
            await app.promote_chat_member(message.chat.id,id )
            await app.set_administrator_title(message.chat.id, id, adt)
            await app.edit_message_text(message.chat.id, message.id, "❈**P**romoted `%s`." % id)
        except ChatAdminRequired:
            await app.edit_message_text(message.chat.id, message.id, "❈P**ermission** denied")

    if message.text == 'self':
        await app.edit_message_text(message.chat.id, message.id, """❅Help self management
❅ `setprofile[reply]` : set a picture to profile photo
❅ `delprof` : delete lastest profile photo
❅ `بصب دانلود شه [reply to the distructive photo]` : download the photo
❅ `block [user_id]` : block someone
❅ `enemy[reply]` : add someone to enemylist
❅ `delenemy[reply|user_id]` : delete user from the enemys list
❅ `enemy list` : enemys list
❅ `addfosh [word]` : add word to database can respond to enemys
❅ `delfosh [word]` : delete word from database
❅ `fosh list` : the words in the database
❅ `comment [on|off]` : turn on and off the first comment option
❅ `comment add [reply to on of channels post]` : add channel to database
❅ `comment del [reply to on of channels post]` : delete channel to database
❅ `comment set [text][reply to on of channels post]` : add channel to database
❅ `comment list id` : get the channels on the database
❅ `/clone[reply]` : copy and clone the profiles of user
❅ `/reclone` : revers your last profile
❅ `Lockuser[reply]` : add user in database when user send something it will send for you
❅ `unlockuser[reply]` : delete locked user from database""")
    if message.text == 'fun':
        await app.edit_message_text(message.chat.id, message.id, """❅Help tools management
❅ `/run # [next line]` : run the pyrograms code 
❅ `/eval # [next line]` : run the pythons code
❅ `/exec [bash]` : run the bash code
❅ `proxy` : give you some telegram proxy 
❅ `reload` : restart your bot 
❅ `/translate [lan code] [text]` : translate text
❅ `/lancodes` : get the language codes
❅ `setcard [card info]` : set up the card or wallet information
❅ `cardnum` : gives you the card info
❅ `setwalletad [wallet address]` : set up the wallet information
❅ `wallet` : gives you the wallet token
❅ `price coin` : price of the currencys
❅ `/base|2|3[^count^link]` : order member
❅ `/cancel_[orderid]` : cancel the order of member
❅ `unzip[reply]` : unzip a zipfile
❅ `ping` : know if bot is alive
❅ `/dlyoutube [link|name]` : search in youtube and download your video
❅ `/song [link|name]` : download you request music from youtube
❅ `/imdb [name]` : search into imdb and gets what you want
❅ `morset [text]` : change text to morse code
❅ `unmorset [morsecode]` : turn morsecode to text
❅ `/download [link]` : download media from link and upload it
❅ `wikipedia [subject]` : look for the things in the wikipedia
❅ `instagramd [link]` : download from instagram""")
                                
    if message.text == 'gap':
        await app.edit_message_text(message.chat.id, message.id, """❅Help group management

❅ `ban[reply]` : Ban a member
❅ `unban[reply]` : unban someone from a gap
❅ `banallmember` : Ban all members in groupe or channel
❅ `info [@channelorgap|-1000000|https://+kskjeijr|]` : Get information of a chat
❅ `information gap` : Get gap info
❅ `id[can be reply]` : get your self and others info
❅ `link` : gives you the chat link
❅ `pin[reply]` : pin something in a chat
❅ `unpin[reply]` : unpin something in a chat
❅ `mute [reply & time with hours]` : mute someone in a gap
❅ `/tagall` : Tag members of the group
❅ `promote admin[reply]` : promote a user to admin""")
    if re.match('^Reload|reload|ریلود$', text):
        num = ['¹', '²', '³', '⁴', '⁵', '⁶', '⁷', '⁸', '⁹', '¹⁰']
        for i in num:
            await MazCli(i)
            await MazCli("❈**The restart was successful**")
            python = sys.executable
            os.execl(python, python, *sys.argv)
    if re.match('Common|common ?(\d{6,12}|@[A-Za-z0-9_]{5,32})?', text):
        id = re.match('Common|common ?(\d{6,12}|@[A-Za-z0-9_]{5,32})?', textt).group(1)
        if message.reply_to_message and message.reply_to_message.from_user.id:
            id = message.reply_to_message.from_user.id
            common = await app.get_common_chats(id)
            result = ''
            for i in common:
                result += '{}: {}\n\n'.format(i.title, i.id)
        await MazCli('❈**Group** common with :`{}`\n\n{}'.format(id, result if result != '' else None))
    if message.text == 'pin':
        try:
            rs = message.reply_to_message.id
            await app.pin_chat_message(message.chat.id, rs, disable_notification=True)
            await app.edit_message_text(message.chat.id, message.id, "**❅Pinned**")
        except ChatAdminRequired:
            await app.edit_message_text(message.chat.id, message.id, "**❅Permissions** denied!")
    if message.text == 'unpin':
        try:
            rs = message.reply_to_message.id
            await app.unpin_chat_message(message.chat.id, rs)
            await app.edit_message_text(message.chat.id, message.id, "**❅UnPinned**")
        except ChatAdminRequired:
            await app.edit_message_text(message.chat.id, message.id, "**❅Permissions** denied!")
    if message.text == 'setprofile':
        file_name = await message.reply_to_message.download()

        await app.edit_message_text(message.chat.id, message.id, "❈__Profile__ **Set**!")
        await app.set_profile_photo(photo=file_name)
        os.remove(file_name)
    if 'setcard ' in message.text:
        cardnumset(message.text.split('setcard ')[1])
        await message.reply("❅__**  Card number changed.**__")
    if message.text == 'cardnum' or message.text == 'شماره کارت':
        cardnums = getsetting('cardnum')
        cardnum ="".join(map(str, cardnums)) 
        await message.reply(f"❅__**wallet : \n `{cardnum}`**__")
    if 'setwalletad ' in message.text:
        walletset(message.text.split('setwalletad ')[1])
        await message.reply("❅__**  Wallet changed.**__")
    if message.text == 'wallet':
        cardnums = getsetting('wallet')
        cardnum ="".join(map(str, cardnums)) 
        await message.reply(f"❅__**wallet : \n `{cardnum}`**__")
    if message.text == "/lancodes":
        await message.reply('''Language           Code
--------           ----
Afrikaans          af
Albanian           sq
Amharic            am
Arabic             ar
Armenian           hy
Azerbaijani        az
Basque             eu
Belarusian         be
Bengali            bn
Bosnian            bs
Bulgarian          bg
Catalan            ca
Cebuano            ceb
Chichewa           ny
Chinese (Simplified)  zh-CN
Chinese (Traditional) zh-TW
Corsican           co
Croatian           hr
Czech              cs
Danish             da
Dutch              nl
English            en
Esperanto          eo
Estonian           et
Filipino           tl
Finnish            fi
French             fr
Frisian            fy
Galician           gl
Georgian           ka
German             de
Greek              el
Gujarati           gu
Haitian Creole     ht
Hausa              ha
Hawaiian           haw
Hebrew             iw
Hindi              hi
Hmong              hmn
Hungarian          hu
Icelandic          is
Igbo               ig
Indonesian         id
Irish              ga
Italian            it
Japanese           ja
Javanese           jw
Kannada            kn
Kazakh             kk
Khmer              km
Kinyarwanda        rw
Korean             ko
Kurdish            ku
Kyrgyz             ky
Lao                lo
Latin              la
Latvian            lv
Lithuanian         lt
Luxembourgish      lb
Macedonian         mk
Malagasy           mg
Malay              ms
Malayalam          ml
Maltese            mt
Maori              mi
Marathi            mr
Mongolian          mn
Myanmar (Burmese)  my
Nepali             ne
Norwegian          no
Nyanja (Chichewa)  ny
Odia (Oriya)       or
Pashto             ps
Persian            fa
Polish             pl
Portuguese (Portugal, Brazil) pt
Punjabi            pa
Romanian           ro
Russian            ru
Samoan             sm
Scots Gaelic       gd
Serbian            sr
Sesotho            st
Shona              sn
Sindhi             sd
Sinhala (Sinhalese)   si
Slovak             sk
Slovenian          sl
Somali             so
Spanish            es
Sundanese          su
Swahili            sw
Swedish            sv
Tagalog (Filipino) tl
Tajik              tg
Tamil              ta
Tatar              tt
Telugu             te
Thai               th
Turkish            tr
Turkmen            tk
Ukrainian          uk
Urdu               ur
Uyghur             ug
Uzbek              uz
Vietnamese         vi
Welsh              cy
Xhosa              xh
Yiddish            yi
Yoruba             yo
Zulu               zu
''')
    if message.text == 'delprof':
        me = await app.get_me()
        photos = await app.get_profile_photos(me.id)
        await app.delete_profile_photos(photos[0].file_id)
        await app.edit_message_text(message.chat.id, message.id, "❈**deleted**")
    if message.text == 'ban':
        idban = message.reply_to_message.from_user.id
        try:
            await app.ban_chat_member(message.chat.id, idban)
            await app.edit_message_text(message.chat.id, message.id, '❈**Banned**')
        except ChatAdminRequired as access:
            await app.edit_message_text(message.chat.id, message.id, "❈P**ermission** denied")
        except USERBANNEDINCHANNEL as ssssss:
            await app.edit_message_text(message.chat.id, message.id, "❈**User** Already Banned.")

    if message.text and message.text.startswith('info '):
        idch = message.text.split('info ')[1]
        try:
            chat = await client.get_chat(idch)
        except exceptions.ChatNotFoundException:
            await message.reply("Chat not found.")
            return
        ids = chat.id
        title = chat.title
        username = '@' + chat.username if chat.username else ''
        desc = chat.description if chat.description and len(chat.description) <= 1024 else ''
        members = chat.members_count
        try:
            if chat.photo and chat.photo.big_file_id is not None:
                photo_path = await client.download_media(chat.photo.big_file_id)
                await client.send_document(
                    chat_id=message.chat.id,
                    document=photo_path,
                    caption=f"ꖒ **ID : {ids}\nTitle : {title}\nUsername : {username}\nMembers : {members}\nBio : {desc}"
                )
            else:
                await message.reply(
                    f"ꖒ **ID : {ids}\nTitle : {title}\nUsername : {username}\nMembers : {members}\nBio : {desc}"
                )
        except exceptions.TelegramError:
            await message.reply("Error sending photo.")
    if message.text == "price coin":
        result = await app.get_inline_bot_results("Msbwhwkwmxhjdbot", "coinprice")
        await app.send_inline_bot_result(chat_id=message.chat.id, query_id=result.query_id,
                                         result_id=result.results[0].id, reply_to_message_id=message.id)
    if "/base" in message.text:
        text = message.text.split("^")
        count = text[1]
        link = text[2]
        URL = "https://addsubscribe.ir/web/web.php"
        PARAMS = {'apikey':'f10f865403c9fcdjf69','type':'order' , 'count' :count ,'link':link}
        r = requests.get(url = URL, params = PARAMS)
        data = r.json()
        orderid = data['id']
        await message.reply("سفارش انجام و بزودی تکمیل میشود : %s ." % orderid)
    if "/base2" in message.text:
        text = message.text.split("^")
        count = text[1]
        link = text[2]
        URL = "https://addsubscribe.ir/web/web.php"
        PARAMS = {'apikey':'f10f865403c9fcdjf69','type':'order-u' , 'count' :count ,'link':link}
        r = requests.get(url = URL, params = PARAMS)
        data = r.json()
        orderid = data['id']
        await message.reply("سفارش انجام و بزودی تکمیل میشود : %s ." % orderid)
    if "/base3" in message.text:
        text = message.text.split("^")
        count = text[1]
        link = text[2]
        URL = "https://addsubscribe.ir/web/web.php"
        PARAMS = {'apikey':'f10f865403c9fcdjf69','type':'order-z' , 'count' :count ,'link':link}
        r = requests.get(url = URL, params = PARAMS)
        data = r.json()
        orderid = data['id']
        await message.reply("سفارش انجام و بزودی تکمیل میشود : %s ." % orderid)
    if "/cancel_" in message.text:
        text = message.text.split("cancel_")
        orderid = text[1]
        URL = "https://addsubscribe.ir/web/web.php"
        PARAMS = {'apikey':'f10f865403c9fcdjf69','type':'cancel' , 'id' :orderid}
        r = requests.get(url = URL, params = PARAMS)
        data = r.json()
        orderid = data
        await message.reply("درخواست لغو  : %s ." % orderid)
    # if "send " in message.text:
    #     s = message.text
    #     s = s.split("send ")
    #     s = s[1]
    #     ss = message.reply_to_message.id
    #     try:
    #         await app.send_reaction(message.chat.id, ss, s)
    #         await app.edit_message_text(message.chat.id, message.id, "❈I**send** this reaction %s ." % s)
    #     except Exception as s:
    #         await message.edit("❈**Found** Error!")
    if message.text == 'information gap':
        idg = message.chat.id
        type = message.chat.type
        title = message.chat.title
        username = message.chat.username
        count = await app.get_chat_members_count(message.chat.id)
        online = await app.get_chat_online_count(chat_id)
        await app.edit_message_text(message.chat.id, message.id,
                                    "❈**chat id** : `%s` \n ❈**Type**: `%s` \n ❈**Title** : `%s` \n ❈**Username** : `%s` \n ❈**Member** : `%i` \n ❈**Online Member** : `%i`" % (
                                        idg, type, title, username, count, online))
    if 'mute' in message.text:
        text = message.text
        x = text.split("mute ")
        y = int(x[1])
        yy = int(y * 600)
        yy = int(yy)
        idban = message.reply_to_message.from_user.id
        try:
            await app.restrict_chat_member(message.chat.id, idban, ChatPermissions(), int(time() + yy))
            await app.edit_message_text(message.chat.id, message.id, "❈**Muted** : %s Hours" % y)
        except ChatAdminRequired as access:
            await app.edit_message_text(message.chat.id, message.id, "❈P**ermission** denied")
    if 'unban ' in message.text:
        text = message.text
        x = text.split("unban ")
        y = int(x[1])
        y = int(y)
        try:
            await app.unban_chat_member(message.chat.id, y)
            await app.edit_message_text(message.chat.id, message.id, "❈**UnBanned**")
        except ChatAdminRequired as access:
            await app.edit_message_text(message.chat.id, message.id, "❈P**ermission** denied")
    if message.text == 'unzip':
        file_name = await message.reply_to_message.download()
        edited = await app.send_message(message.chat.id, "file : \n downloads->")
        await asyncio.sleep(1)
        await app.edit_message_text(edited.chat.id, edited.id, 'file : \n downloads->extractfiles->')
        with zipfile.ZipFile(file_name, 'r') as zip_ref:
            zip_ref.extractall('templ')
        count = 0
        for root, dirs, files in os.walk('templ'):
            for name in files:
                filename = os.path.join(root, name)
                count += 1
                if os.path.getsize(filename) == 0:
                    os.remove(filename)
                    continue
                await app.send_document(message.chat.id, filename, caption="file %s in zip" % count)
                os.remove(filename)
        await app.edit_message_text(edited.chat.id, edited.id,'file : \n downloads->extractfiles->exracted->uploading->uploaded')
        for name in dirs:
                dirname = os.path.join(root, name)
                if not os.listdir(dirname):
                    os.rmdir(dirname)

    if message.text == "بصب دانلود شه":
        try:
            rep = message.reply_to_message
            if not (rep and (rep.video or rep.photo)):
                return await message.delete()
            mention = rep.from_user.mention
            document = await app.download_media(rep)
            await app.send_document("me", document, caption=f"**User: {mention}\nSecret Media Save**")
        except Exception as e:
            await app.send_message('me', f"ERROR:\n\n{e}")
    if 'block ' in message.text:
        await app.block_user(message.text.split('block ')[1])
        await message.reply("❅__**Blocked! **__")
    if 'result ' in message.text:
        s = message.text
        words = s.split(' ')
        words.pop(0)
        await app.edit_message_text(message.chat.id, message.id, "❅**Done!**")
        result = await app.get_inline_bot_results(words[0], words[1])
        await app.send_inline_bot_result(message.chat.id, result.query_id, result.results[0].id)
    if message.text == 'ping':
        ping = psutil.getloadavg()
        # ram = psutil.virtual_memory()
        # ram = ram.split()[3].split("used=")[1].split(",")[0]
        # ram = size(ram)
        process = psutil.Process(os.getpid())
        ram = size(process.memory_info().rss)
        await app.edit_message_text(message.chat.id, message.id, "ۭ۟سٖۢۢو۠ۛرۭۨ۟سۢ ۪ۧمِۭۚٚیٌٍۣٖٛۨتِۖ ۛرۣۨٛاٝ دِۣٝٞنًِۭ۠بِۣۚٛاِٝۡلٖٛ ۭۨڪِۣٛٞنًِِٚیٌٍدۣٝ \n\n❅**Ping**: `%s`\n❅Ram:`%s` \n\n @丂ㄖㄩ尺匚モ爪丹ㄒモ" % (ping[0], ram))

    if message.reply_to_message and message.text == "enemy":
        ss = message.reply_to_message.from_user.id
        try:
            addenemy(ss)
            await app.edit_message_text(message.chat.id, message.id, "❈**Added** To Enemy List.")
        except Exception as m:
            await app.edit_message_text(message.chat.id, message.id, "❈**User** In Enemy List %s ." % m)
    if 'addfosh' in message.text:
        s = text.split('addfosh ')
        s = s[1]
        try:
            addfosh(s)
            await app.edit_message_text(message.chat.id, message.id, "❈**Added** To Fosh List.")
        except Exception as m:
            await app.edit_message_text(message.chat.id, message.id, "❈**Word** In Fosh List")
    if 'delfosh' in message.text:
        s = text.split('delfosh ')
        s = s[1]
        try:
            delfosh(s)
            await app.edit_message_text(message.chat.id, message.id, "❈**Word** Deleted from list.")
        except Exception as ki:
            await app.edit_message_text(message.chat.id, message.id, "❈This **Word**  does not exist.")
    if message.text == 'clear fosh':
        try:
            delallfosh()

            await app.edit_message_text(message.chat.id, message.id, "❈All **Word** in Foshlist cleared.")
        except Exception as ss:
            await app.edit_message_text(message.chat.id, message.id, "❈No **Words** found in the FoshList list")

    if 'delenemy' in message.text:
        if message.text == "delenemy" and message.reply_to_message:
            id = message.reply_to_message.from_user.id
            try:
                delenemy(id)

                await app.edit_message_text(message.chat.id, message.id, "❈**Enemy** Deleted from list.")
            except Exception as ki:
                await app.edit_message_text(message.chat.id, message.id,
                                            "❈This **id**  does not exist in enemy list. %s" % ki)
            ######s2
        if 'delenemy ' in message.text:
            s = text.split('delenemy ')
            s = s[1]
            try:
                delenemy(s)

                await app.edit_message_text(message.chat.id, message.id, "❈**Enemy** Deleted from list.")
            except Exception as ki:
                await app.edit_message_text(message.chat.id, message.id,
                                            "❈This **id**  does not exist in enemy list :%s." % ki)

    if message.text == "enemy list":
        string = enemylist()
        await app.edit_message_text(message.chat.id, message.id, "❈**E**nemy List:%s" % string)
    if message.text == "fosh list":
        string = foshlist()
        await app.edit_message_text(message.chat.id, message.id, "❈**F**osh List:%s" % string)
    if message.text == "panel":
        await message.delete()
        result = await app.get_inline_bot_results("Msbwhwkwmxhjdbot", f"panels{message.chat.id}")
        await app.send_inline_bot_result(message.chat.id, result.query_id, result.results[0].id)
    if message.text == "link":
        link = await app.create_chat_invite_link(message.chat.id)
        await app.edit_message_text(message.chat.id, message.id, "❈**Link**: %s ." % link.invite_link)

    if "dlmusic " in message.text:
        link = text.split("dlmusic ")[1]
        s = requests.get("https://sanrich.tk/api/melobit.php?type=search&search=%s&" % link)
        s = s.text
        await app.edit_message_text(message.chat.id, message.id, "❈**Wait**...")
        y = json.loads(s)
        links = y["link"]
        names = y["name"]
        try:
            await app.send_audio(message.chat.id, links, caption="❈**Music**:\n```%s```." % names)
        except Exception as s:
            await app.send_message(message.chat.id, "❈**F**ound **P**roblem!.")

    if "instainfo " in message.text:
            id = text.split("instainfo ")[1]
            try:
                headers = {
                    'Content-type': 'application/json',
                }
                # data = '{"id":"Hello, World!"}'
                s = requests.get("https://api.irateam.ir/instainfo1.php?url=%s" % id, headers=headers)
                # s = requests.get("https://api.wirexteam.tk/instagram?type=info&id=%s"%id)
                s2 = s.text
                items = json.loads(s2)
                name = items['Results']['name']
                username = items['Results']['username']
                pageid = items['Results']['id']
                post = items['Results']['post count']
                prof = items['Results']['pic'].split("&")[0]
                follow = items['Results']['followers count']
                fol = items['Results']['following count']
                bio = items['Results']['bio']
                cap = """💠  [This Page](https://instagram.com/%s) ( **%s** )  Informations :
    ֍ Posts : ( `%s` )
    ֍ Followers : ( `%s` )
    ֍ Followings : ( `%s` )
    ֍ page name : ( `%s` )
    ֍ Biography : ( `%s `)""" % (username, id, post, follow, fol,name, bio)
                aw = await message.edit("❅**Wait**")
                await aw.delete()
                # if prof and prof is not None:
                #     await message.reply_photo(prof, caption=cap)
                # else:
                await message.reply(cap)
            except Exception as ins:
                await message.reply("❅**Error** Found.! ; %s . " % ins)

    if message.text == "id":
        if message.chat.type == ChatType.PRIVATE:
            if message.reply_to_message:
                userid = message.reply_to_message.from_user
            else:
                userid = message.from_user
            chat = message.chat
            s = await app.get_common_chats(userid.id)
            phone = userid.phone_number if userid.phone_number else "0"
            # for i in s:
            # result += '{}'.format (i.id)
            # ss =result.split("-")
            # ss = len(ss)-1
            bb = await app.get_chat(userid.id)
            bb = bb.bio
            # countprofil = await app.get_chat_photos(user.id)
            countprofiles = 0
            async for i in app.get_chat_photos(user.id):
                countprofiles =  countprofiles + 1
            common = await app.get_common_chats(userid.id)
            common = len(common)
            txt = "❈**INFO**:\n❈**id**:`%s`\n❈**UserName**:`@%s`\n❈**Name**:`%s`\n❈**Profile Count**:`%s`\n❈**Status**:`%s`\n❈**Phones**:`%s`\n❈**Group in Common**:`%s`\n\n❈**Biography**:\n`%s`" % (
                userid.id, userid.username, userid.first_name, countprofiles, userid.status, phone, common, bb)
            await app.edit_message_text(message.chat.id, message.id, txt)
        if chat.type != ChatType.PRIVATE and chat.type != ChatType.BOT:
            if message.reply_to_message:
                userid = message.reply_to_message.from_user
                s = await app.get_common_chats(userid.id)
                phone = userid.phone_number if userid.phone_number else "0"
                bb = await app.get_chat(userid.id)
                bb = bb.bio
                # countprofile = await app.get_chat_photos(userid.id)
                countprofiles = 0
                async for i in app.get_chat_photos(user.id):
                    countprofiles =  countprofiles + 1
                common = await app.get_common_chats(userid.id)
                common = len(common)
                txt = "❈**INFO**:\n❈**id**:`%s`\n❈**UserName**:`@%s`\n❈**Name**:`%s`\n❈**Profile Count**:`%s`\n❈**Status**:`%s`\n❈**Phones**:`%s`\n❈**Group in Common**:`%s`\n\n❈**Biography**:\n`%s`" % (
                    userid.id, userid.username, userid.first_name, countprofiles, userid.status, phone, common, bb)
                await app.edit_message_text(message.chat.id, message.id, txt)
            else:
                idg = message.chat.id
                type = message.chat.type
                title = message.chat.title
                username = message.chat.username
                count = await app.get_chat_members_count(message.chat.id)
                online = await app.get_chat_online_count(chat_id)
                await app.edit_message_text(message.chat.id, message.id,
                                            "❈**chat id** : `%s` \n ❈**Type**: `%s` \n ❈**Title** : `%s` \n ❈**Username** : `%s` \n ❈**Member** : `%i` \n ❈**Online Member** : `%i`" % (
                                                idg, type, title, username, count, online))

            ####


@app.on_message()
async def mes(client, message):
    if message and userls(message.from_user.id):
        try:
            chat_id = 1968152047
            from_chat_id = message.chat.id
            message_id = message.id
            print("Forwarding message from chat {} to chat {}".format(from_chat_id, chat_id))
            await app.forward_messages(chat_id=chat_id, from_chat_id=from_chat_id, message_ids=message_id)
            await asyncio.sleep(1)
        except Exception as e:
            print("Error forwarding message: {}".format(e))

    if message and message.from_user.id in list(map(int, enemylist())):
        try:
            curse = foshlist()
            s = secrets.choice(curse)
            await message.reply(s)
            await asyncio.sleep(1)
        except Exception as ssss:
            print()


###
#
#

#
#


@app.on_message(filters.me & filters.command("dlyoutube"), group=2)
async def video(client, message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    args = get_arg(message) + " " + "dlyoutube"
    if args.startswith(" "):
        await message.reply("❅**__help__**")
        return ""
    text = message.text
    texta = text.split("/dlyoutube ")[1]
    if texta.startswith("https://"):
        video_link = texta
    else:
        video_link = yt_search(args)
    status = await message.reply(
        "❅I **Searching** to youtube to down __Video__ [❅](https://telegra.ph/file/7471756a5a18380add8b0.mp4)")
    if not video_link:
        await status.edit("❅**Not** Found __music__.\n\nEg.`/dlyoutube فاتحه فدایی`")
        return ""
    yt = YouTube(video_link)
    audio = yt.streams.filter(file_extension='mp4').first()
    try:
        download = audio.download(filename=f"{str(user_id)}")
    except Exception as ex:
        await status.edit("❅**Filed**")
    rename = os.rename(download, f"{str(user_id)}.mp4")
    publish_date = yt.publish_date
    desc = yt.description
    if len(desc) > 1023:
        desc = desc[1023:]
    linc = yt.channel_url
    rate = yt.rating
    title = yt.title
    time = yt.length
    views = yt.views
    time = str(datetime.timedelta(seconds=time))
    await app.send_video(
        chat_id=message.chat.id,
        video=f"{str(user_id)}.mp4",
        caption="❅**V**__ideo__ **Downloaded** as __Youtube__:\n\n❅**__Title__**:[%s](%s)\n❅**__Rate__**: %s\n❅**__Publish Date__**: %s\n❅**__Views__**:%s\n❅**__Time__**: %s\n❅**__Description__**:[%s]" % (
            title, linc, rate, publish_date, views, time, desc),
        reply_to_message_id=message.id
    )
    await status.delete()
    os.remove(f"{str(user_id)}.mp4")


@app.on_message(filters.me & filters.command("song"), group=3)
async def song(client, message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    args = get_arg(message) + " " + "song"
    if args.startswith(" "):
        await message.reply("❅Error [help]")
        return ""
    text = message.text
    texta = text.split("/song ")[1]
    if texta.startswith("https://"):
        video_link = texta
    else:
        video_link = yt_search(args)
    status = await message.reply(
        "❅I **Searching** to youtube to down __music__ [❅](https://telegra.ph/file/7471756a5a18380add8b0.mp4)")
    if not video_link:
        await status.edit("❅**Not** Found __music__.\n\nEg.`/song فاتحه فدایی`")
        return ""
    yt = YouTube(video_link)
    audio = yt.streams.filter(only_audio=True).first()
    try:
        download = audio.download(filename=f"{str(user_id)}")
    except Exception as ex:
        await status.edit("❅**Filed**")
        return ""
    rename = os.rename(download, f"{str(user_id)}.mp3")
    #await app.send_chat_action(message.chat.id, "upload_audio")
    await app.send_audio(
        chat_id=message.chat.id,
        audio=f"{str(user_id)}.mp3",
        duration=int(yt.length),
        title=str(yt.title),
        performer=str(yt.author),
        reply_to_message_id=message.id,
    )
    await status.delete()
    os.remove(f"{str(user_id)}.mp3")


@app.on_message(filters.me&filters.command("eval"), group=4)
async def eval(client, message):
    status_message = await message.reply_text("❅**__Wait__**")
    cmd = message.text.split(" ", maxsplit=1)[1]

    reply_to_ = message
    if message.reply_to_message:
        reply_to_ = message.reply_to_message

    old_stderr = sys.stderr
    old_stdout = sys.stdout
    redirected_output = sys.stdout = io.StringIO()
    redirected_error = sys.stderr = io.StringIO()
    stdout, stderr, exc = None, None, None

    try:
        await aexec(cmd, client, message)
    except Exception:
        exc = traceback.format_exc()

    stdout = redirected_output.getvalue()
    stderr = redirected_error.getvalue()
    sys.stdout = old_stdout
    sys.stderr = old_stderr

    evaluation = ""
    if exc:
        evaluation = exc
    elif stderr:
        evaluation = stderr
    elif stdout:
        evaluation = stdout
    else:
        evaluation = "Success"

    final_output = "<b>❅code❅</b>: "
    final_output += f"<code>{cmd}</code>\n\n"
    final_output += "<b>❅result❅</b>:\n"
    final_output += f"<code>{evaluation.strip()}</code> \n"

    if len(final_output) > 4096:
        with io.BytesIO(str.encode(final_output)) as out_file:
            out_file.name = "eval.text"
            await reply_to_.reply_document(
                document=out_file, caption=cmd, disable_notification=True
            )
    else:
        await reply_to_.reply_text(final_output)
    await status_message.delete()


async def aexec(code, client, message):
    exec(
        "async def __aexec(client, message): "
        + "".join(f"\n {l_}" for l_ in code.split("\n"))
    )
    return await locals()["__aexec"](client, message)


@app.on_message(filters.me & filters.command("porn") & filters.text , group=5)
async def hiref(client, message):
    try:
        # url = callback_query.message.text
        text = message.text
        url = re.search("(?P<url>https?://[^\s]+)", text).group("url")
        ydl_opts = {
            'format': 'best[ext=mp4]',
            'outtmpl': '%(title)s - %(extractor)s-%(id)s.%(ext)s',
            'writethumbnail': True
        }
        with YoutubeDL(ydl_opts) as ydl:
            #await message.reply_chat_action("typing")
            info_dict = ydl.extract_info(url, download=False)
            # download
            await app.edit_message_text(message.chat.id, message.id, "❅**__Wait..__**")
            ydl.process_info(info_dict)
            # upload
            video_file = ydl.prepare_filename(info_dict)
            task = asyncio.create_task(send_video(message, info_dict,
                                                  video_file))
            while not task.done():
                await asyncio.sleep(3)
                #await message.reply_chat_action("upload_document")
            #await message.reply_chat_action("cancel")
            await message.delete()
    except Exception as e:
        await message.reply_text(e)
    await app.message.reply_to_message.delete()
    await app.message.delete()


async def send_video(message: Message, info_dict, video_file):
    basename = video_file.rsplit(".", 1)[-2]
    # thumbnail
    thumbnail_url = info_dict['thumbnail']
    thumbnail_file = basename + "." + \
                     get_file_extension_from_url(thumbnail_url)
    # info (s2tw)
    webpage_url = info_dict['webpage_url']
    title = '@san_trich\n ' + s2tw(info_dict['title'])
    caption = f"<b><a href=\"{webpage_url}\">{title}</a></b>"
    duration = int(float(info_dict['duration']))
    width, height = get_resolution(info_dict)
    await message.reply_video(
        video_file, caption=caption, duration=duration,
        width=width, height=height,
        thumb=thumbnail_file)
    os.remove(video_file)
    os.remove(thumbnail_file)


def get_file_extension_from_url(url):
    url_path = urlparse(url).path
    basename = os.path.basename(url_path)
    return basename.split(".")[-1]


def get_resolution(info_dict):
    if {"width", "height"} <= info_dict.keys():
        width = int(info_dict['width'])
        height = int(info_dict['height'])
    # https://support.google.com/youtube/answer/6375112
    elif info_dict['height'] == 1080:
        width = 1920
        height = 1080
    elif info_dict['height'] == 720:
        width = 1280
        height = 720
    elif info_dict['height'] == 480:
        width = 854
        height = 480
    elif info_dict['height'] == 360:
        width = 640
        height = 360
    elif info_dict['height'] == 240:
        width = 426
        height = 240
    return (width, height)


@app.on_message(
    filters.command("tagall")
    & filters.me
    & ~filters.private, group=6
)
async def Tag(client , message):
    # ss = []
    # s = app.get_chat_members(message.chat.id)
    # for ino in s:
    #     ss.append(ino.user.id)
    Emojies = ['🦁', '🐯', '🦊', '🦄', '🐝', '🐺', '🦋', '🐞', '🐳', '🐬', '🐼', '🦚', '🎄', '🌲', '🍄', '🍁', '🌷', '🌹', '🌺', '🌸', '🌼', '🌗', '🌓', '🪐', '💫', '⭐️', '✨', '⚡️', '🔥', '🌈', '☃️', '❄️', '🍔', '🍕', '🍓', '🍉', '🍟', '🧁', '🍰', '🍭', '🍬', '🍫', '🍿', '🍩', '🍪', '🥂', '🍸', '🍹', '🧉', '🍾', '⚽️', '🏀', '🏈', '⚾️', '🥎', '🎾', '🎖', '🎗', '🥁', '🎸', '🎺', '🎷', '🏎', '🚀', '✈️', '🚁', '🛸', '🏰', '🗼', '🎡', '🛩', '📱', '💻', '🖥', '💰', '🧨', '💣', '🪓', '💎', '⚱️', '🔮', '🩸', '🦠', '🛎', '🧸', '🎉', '💌', '📯', '❤️', '🧡', '💛', '💚', '💙', '💜', '🖤', '🤍', '🤎', '❣️', '💕', '💞', '💝', '⚜️', '🔱', '📣', '♥️', '😍', '🥰', '🥳', '🤩', '🤪', '👾', '😻', '💋', '👑', '💍', '🎩']
    #User_Ids=[int(user[0]) for user in  ss ]
    tgs=''
    symbls=['★', '☆', '✡', '✦', '✧', '✩', '✪', '✫', '✬', '✭', '✮', '✯', '✰', '⁂', '⁎', '⁑', '✢', '✣', '✤', '✥', '✱', '✲', '✳', '✴', '✵', '✶', '✷', '✸', '✹', '✺', '✻', '✼', '✽', '✾', '✿', '❀', '❁', '❂', '❃', '❇', '❈', '❉', '❊', '❋', '❄', '❆', '❅', '⋆', '≛', 'ᕯ', '✲', '࿏', '꙰', '۞', '⭒', '⍟', '♔', '♕', '♖', '♗', '♘', '♙', '♚', '♛', '♜', '♝', '♞', '♟', '♤', '♠', '♧', '♣', '♡', '♥', '♢', '♦', '☩', '☫', '☬', '☭', '☯', '☽', '☾', '✙', '✚', '✛', '✜', '✝', '✞', '✟', '†', '⊹', '‡', '♁', '♆', '❖', '♅', '✠', '✡', '✢', '卍', '卐', '〷', '☠', '☢', '☣', '☦']
    x=0
    symbol1=choice(symbls)
    symbol2=choice(symbls)
    rand=choice(Emojies)
    async for i in app.get_chat_members(message.chat.id , limit=100):
            if  not i.user.is_bot  and not i.user.is_deleted :
                tgs+=f'{symbol1}{rand}▸{i.user.mention}◂{rand}{symbol2}\n'
                x+=1
                if x>=5:
                    await app.send_message(message.chat.id, tgs)
                    x=0
                    symbol1=choice(symbls)
                    symbol2=choice(symbls)
                    rand=choice(Emojies)
                    tgs=''
                    await sleep(3)
            else:
                print('this an')
                return
# async def joinvc(_, message):
#     global call
#     chat_id = message.chat.id
#     try:
#         if str(chat_id) in call.keys():
#             await message.edit_text("__**❈Im already Joined To Voice Chat!**__", quote=False)
#             return
#         vc = GroupCall(
#             client=app,
#             input_filename=f"input.raw",
#             play_on_repeat=True,
#             enable_logs_to_console=False,
#         )
#         await vc.start(chat_id)
#         call[str(chat_id)] = vc
#         await message.reply_text("__**❈Joined To Voice Chat**__")
#     except Exception as e:
#         await message.edit_text("❈__**Error!-=-{ ❈permission , voice chat not started}")


@app.on_message(filters.command("leavevc") & filters.me & ~filters.private, group=7)
async def leavevc(_, message):
    vc = call[str(message.chat.id)]
    await vc.leave_current_group_call()
    await vc.stop()
    await message.edit_text(
        "__**❈ I Left The Voice Chat!.**__"
    )


async def play():
    global queue, playing
    while not playing:
        await asyncio.sleep(0.1)
        if len(queue) != 0:
            service = queue[0]["service"]
            song = queue[0]["song"]
            requested_by = queue[0]["requested_by"]
            message = queue[0]["message"]
            if service == "youtube":
                playing = True
                del queue[0]
                try:
                    await ytplay(requested_by, song, message)
                except Exception as e:
                    print(str(e))
                    playing = False
                    pass
            elif service == "saavn":
                playing = True
                del queue[0]
                try:
                    await jiosaavn(requested_by, song, message)
                except Exception as e:
                    print(str(e))
                    playing = False
                    pass
            elif service == "deezer":
                playing = True
                del queue[0]
                try:
                    await deezer(requested_by, song, message)
                except Exception as e:
                    print(str(e))
                    playing = False
                    pass


@app.on_message(
    filters.command("imdb") & filters.me, group=8
)
async def imdb_query(client, message):  # sourcery no-metrics
    """To fetch imdb data about the given movie or series."""
    catmessage = await message.edit("❅__**Wait**__")
    try:
        movie_name = message.text.split("/imdb")[1]
        movies = imdb.search_movie(movie_name)
        movieid = movies[0].movieID
        movie = imdb.get_movie(movieid)
        moviekeys = list(movie.keys())
        for i in mov_titles:
            if i in moviekeys:
                mov_title = movie[i]
                break
        for j in reversed(mov_titles):
            if j in moviekeys:
                mov_ltitle = movie[j]
                break
        mov_runtime = movie["runtimes"][0] + " min" if "runtimes" in movie else ""
        if "original air date" in moviekeys:
            mov_airdate = movie["original air date"]
        elif "year" in moviekeys:
            mov_airdate = movie["year"]
        else:
            mov_airdate = ""
        mov_genres = ", ".join(movie["genres"]) if "genres" in moviekeys else "Not Data"
        mov_rating = str(movie["rating"]) if "rating" in moviekeys else "Not Data"
        mov_rating += (
            " (by " + str(movie["votes"]) + ")"
            if "votes" in moviekeys and "rating" in moviekeys
            else ""
        )
        mov_countries = (
            ", ".join(movie["countries"]) if "countries" in moviekeys else "Not Data"
        )
        mov_languages = (
            ", ".join(movie["languages"]) if "languages" in moviekeys else "Not Data"
        )
        mov_plot = (
            str(movie["plot outline"]) if "plot outline" in moviekeys else "Not Data"
        )
        mov_director = await get_cast("director", movie)
        mov_composers = await get_cast("composers", movie)
        mov_writer = await get_cast("writer", movie)
        mov_cast = await get_cast("cast", movie)
        mov_box = await get_moviecollections(movie)
        resulttext = f"""
<b>❅<i>Title : </i></b><code>{mov_title}</code>
<b>❅<i>Imdb Url : </i></b><a href='https://www.imdb.com/title/tt{movieid}'>{mov_ltitle}</a>
<b>❅<i>Info : </i></b><code>{mov_runtime} | {mov_airdate}</code>
<b>❅<i>Genres : </i></b><code>{mov_genres}</code>
<b>❅<i>Rating : </i></b><code>{mov_rating}</code>
<b>❅<i>Country : </i></b><code>{mov_countries}</code>
<b>❅<i>Language : </i></b><code>{mov_languages}</code>
<b>❅<i>Director : </i></b><code>{mov_director}</code>
<b>❅<i>Music Director </i>: </b><code>{mov_composers}</code>
<b>❅<i>Writer : </i></b><code>{mov_writer}</code>
<b><i>❅Stars : </i></b><code>{mov_cast}</code>
<b>❅<i>Box Office : </i></b>{mov_box}
<b>❅<i>Story Outline : </i></b><i>{mov_plot}</i>"""
        if "full-size cover url" in moviekeys:
            imageurl = movie["full-size cover url"]
        else:
            imageurl = None
        soup = BeautifulSoup(resulttext, features="html.parser")
        rtext = soup.get_text()
        if len(rtext) > 1024:
            extralimit = len(rtext) - 1024
            climit = len(resulttext) - extralimit - 20
            resulttext = resulttext[:climit] + "...........</i>"
        if imageurl:
            downloader = SmartDL(imageurl, moviepath, progress_bar=False)
            downloader.start(blocking=False)
            while not downloader.isFinished():
                pass
        if os.path.exists(moviepath):
            await app.send_photo(
                message.chat.id,
                moviepath,
                caption=resulttext,
            )
            os.remove(moviepath)
            return await catmessage.delete()
        await catmessage.edit(
            resulttext,
            link_preview=False,
        )
    except IndexError:
        await catmessage.edit(f"__**❅This Movie Not Found{movie_name}.**__")
    except Exception as e:
        await catmessage.edit(f"__**❅Error:**__\n__{e}__")


@app.on_message(filters.me & filters.command("php"), group=9)
async def eval_command_handler(client: Client, message: Message):
    status_message = await message.reply_text("❅**__Wait__**")
    cmd = message.text.split(" ", maxsplit=1)[1]

    reply_to_ = message
    if message.reply_to_message:
        reply_to_ = message.reply_to_message

    stdout, stderr, exc = None, None, None

    try:
        stdout, stderr = await aexec(cmd)
    except Exception:
        exc = traceback.format_exc()

    evaluation = ""
    if exc:
        evaluation = exc
    elif stderr:
        evaluation = stderr
    elif stdout:
        evaluation = stdout
    else:
        evaluation = "Success"

    final_output = "<b>❅code❅</b>: "
    final_output += f"<code>{cmd}</code>\n\n"
    final_output += "<b>❅result❅</b>:\n"
    final_output += f"<code>{evaluation.strip()}</code> \n"

    if len(final_output) > 4096:
        with io.BytesIO(str.encode(final_output)) as out_file:
            out_file.name = "eval.text"
            await reply_to_.reply_document(
                document=out_file, caption=cmd, disable_notification=True
            )
    else:
        await reply_to_.reply_text(final_output)
    await status_message.delete()


# async def aexec(code):
#     # Run the PHP code as a separate process and capture the output
#     process = subprocess.Popen(["php", "-r", code], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
#     stdout, stderr = await process.communicate()

#     return stdout.decode(), stderr.decode()
# @app.on_message(filters.me, group=10)
# async def coinprice(client, message):
#     # if message.text == "price coin":
#     #     result = await app.get_inline_bot_results("Msbwhwkwmxhjdbot", "coinprice")
#     #     await app.send_inline_bot_result(chat_id=message.chat.id, query_id=result.query_id,
#     #                                      result_id=result.results[0].id, reply_to_message_id=message.id,
#     #                                      hide_via=False)


@app.on_message(filters.me & filters.regex("exec(?:\s|$)([\s\S])*"), group=10)
async def excecode(client, message):
    cmd = "".join(message.text.split(maxsplit=1)[1:])
    if not cmd:
        return await message.edit("❅__**Error this message is A Empty**__")
    mtoimdb = await message.edit("❅__**Wait..**__")
    process = await asyncio.create_subprocess_shell(
        cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
    )
    stdout, stderr = await process.communicate()
    result = str(stdout.decode().strip()) + str(stderr.decode().strip())
    catuser = await app.get_me()
    curruser = "sourcemate/Ubuntu::Root"
    uid = os.geteuid()
    if uid == 0:
        cresult = f"```{curruser}:~#``` ```{cmd}```\n```{result}```"
    else:
        cresult = f"```{curruser}:~$``` ```{cmd}```\n```{result}```"
    await app.edit_message_text(message.chat.id, message.id, cresult)


#


@app.on_message(filters.me & filters.regex("unmorset(?:\s|$)([\s\S])*"), group=11)
async def unmorset(client, message):
    text = message.text
    text = text.upper()
    x = text.split("UNMORSET ")
    string = morse_to_string(x[1])
    await app.edit_message_text(message.chat.id, message.id, string)

@app.on_message(filters.me & filters.regex("comment(?:\s|$)([\s\S])*"), group=12)
async def settingcomment(client, message):
    from re import match
    res = match(r"comment ([\s\S].)(.+[a-z|A-Z])$", message.text)
    if message.text == "comment on":
        oncom()
        await message.edit("❅__**Comment First On**__")
    if message.text == "comment off":
        offcom()
        await message.reply("❅__**Comment First Off**__")
    if message.text == "comment add" and message.reply_to_message.forward_from_chat.type == "channel":
        try:
            addcom(message.reply_to_message.forward_from_chat.id)
            await message.edit("❅__**Chat (%s) Added To Comment list**__." % (message.reply_to_message.forward_from_chat.id))
        except Exception as er:
            await message.edit("❅__**This Chat from befor in commentList**__%s ." % er)
    if message.text == "comment list id":
        lisr = comlist()
        lis = "\n".join(map(str, lisr))
        await message.edit(f"❅__**List({lis})")
    if message.text == "comment del" and message.reply_to_message.forward_from_chat.type == "channel":
        try:
            delcom(message.reply_to_message.forward_from_chat.id)
            await message.edit("❅__**Chat (%s) deleted from Comment list**__." % (message.reply_to_message.forward_from_chat.id))
        except Exception as er:
            await message.edit("❅__**This Chat Not exites in Commentlists**__%s ." % er)
    if 'comment set ' in message.text and message.reply_to_message:
        if not message.reply_to_message.text:
            return await message.edit("❅__**Just reply to Text**__.")
        try:
            texts = message.text.split("comment set ")[1]
            edittext(str(texts),message.reply_to_message.text)
            await message.edit(f"❅__**Done!**__:❅Chat id: {texts}\n❅Text:{message.reply_to_message.text} .")
        except Exception as error:
            await message.edit(f"❅__**Chat id is invalid**__. {error} . ")




@app.on_message(filters.command('download') & filters.me, group=13)
async def download_and_upload_media(client, message):
    # Get the direct link from the command argument
    link = message.text.split(' ')[1]
    # Get the filename from the link
    filename = link.split('/')[-1]
    # Send a message indicating the download has started
    await message.reply_text(f'Downloading {filename}...')
    # Send a request to download the file
    r = requests.get(link, stream=True)
    # Check if the request was successful
    if r.status_code == 200:
        # Open a file stream to save the downloaded file
        with open(filename, 'wb') as f:
            # Loop through the file stream and write to the file
            total_length = r.headers.get('content-length')
            if total_length is None:
                # No content length header, so just write the data
                f.write(r.content)
            else:
                # Content length header present, so loop through and write
                # with progress display
                downloaded = 0
                total_length = int(total_length)
                for data in r.iter_content(chunk_size=4096):
                    downloaded += len(data)
                    f.write(data)
        # Close the file stream
        f.close()
        # Send a message indicating the download is complete
        await message.reply_text(f'Download of {filename} complete.')
        # Upload the file to the chat
        await message.reply_document(document=filename)
    else:
        # Send a message indicating the download failed
        await message.reply_text(f'Download of {filename} failed.')


















@app.on_message(filters.me & filters.regex(f'^(wikipedia|ویکی پدیا)'), group=14)
async def wiki(client,message):
    from wikipedia import set_lang, summary
    set_lang('en')
    result = summary("".join(message.text.split()[1::]))
    await message.edit(result)
















@app.on_message(filters.group,group=15)
async def sendcom(client, message):
    sta = stcom()
    sta = "".join(map(str, sta))
    if sta == "on":
        lisr = comlist()
        if str(message.forward_from_chat.id) in lisr:
            try:
                comtext = textcom(message.forward_from_chat.id)
                ok = "".join(map(str, comtext))
                await message.reply(ok)
            except Exception as o:
                await message.reply(o)
@app.on_deleted_messages(group = 16)   
async def deleted(client,message):
    messg = loadMessages()
    curses = [i[0] for i in messg]  
    # messageidd = str(message.id)
    # texts = textmessages(message.chat.id)
    ss = json.loads(str(message))
    for y in ss:
        
        sss =str (y['id'])
        if  sss in curses:
            db = sqlite3.connect("self.db")
            mycursor = db.cursor()
            mycurso = db.cursor()
            mycursor.execute("SELECT text FROM messages WHERE messageid = '%s'"% sss)
            texts = [i[0] for i in mycursor.fetchall()]
            mycurso.execute("SELECT id FROM messages WHERE messageid = '%s'"% sss)
            idmine = [i[0] for i in mycurso.fetchall()]
            db.close() 
            idmine = "".join(map(str, idmine))
            await app.send_message(1968152047,"❅__**New messag deleted  [[Click](tg://user?id=%s)],last message:\n%s .**__" %(idmine,texts))
@app.on_edited_message(group=17)            
async def editedm(client, message):
    if message.caption:
        return  # Skip the action if the edited message has a caption

    messg = loadMessages()
    curses = [i[0] for i in messg]  
    messageidd = str(message.id)

    if messageidd in curses:
        db = sqlite3.connect("self.db")
        mycursor = db.cursor()
        mycursor.execute("SELECT text FROM messages WHERE messageid = '%s'"% message.id)
        texts = [i[0] for i in mycursor.fetchall()]
        db.close() 
        await app.send_message(1390918103,"❅__**New messag edited [[Click](tg://user?id=%s)],last message:\n\n%s .**__" %(message.from_user.id,texts))
@app.on_message(filters.me & filters.regex(f'^(instagramd|دانلود اینستا)'), group=18)
async def dininsta(client,message):
    result = "".join(message.text.split()[1::])
    try:
        headers = {
            'Content-type': 'application/json',
        }
        # data = '{"id":"Hello, World!"}'
        s = requests.get("https://api.irateam.ir/insta2.php?type=post&url=%s" % result, headers=headers)
        # s = requests.get("https://api.wirexteam.tk/instagram?type=info&id=%s"%id)
        s2 = s.text
        items = json.loads(s2)
        count = 0
        for i in items:
            linkv = items['Results'][count]['post']
            caption = items['Results'][count]['caption']
            type =  items['Results'][count]['type']
            count = count + 1
            if len(caption) > 1024 :
                caption = caption[1023:]
            await app.send_video(message.chat.id, linkv, caption=caption)
    except Exception as ins:
        pass


@app.on_message(~filters.channel&~filters.bot,group=19)
async def sunny(client,message):
    insertmessage(message.id,message.from_user.id,message.text)
    # setc = autoblockst()
    # if setc == 'on':
    #     await message.reply("❅__**You are blocked! **__")
    #     await app.block_user(message.from_user.id)

@app.on_message(filters.me ,group=20)
async def deleteallofthem(client,message):
    userss = []
    userss2 = []
    if message.text == 'clearallmessages':
        async for m in app.get_chat_history(message.chat.id):
            await app.delete_messages(message.chat.id, m.id)  

    if message.text == 'banallmember':
        from pyrogram.raw.functions.channels import GetParticipants
        from pyrogram.raw.types import ChannelParticipantsRecent ,ChannelParticipantsAdmins
    
        idch =await app.resolve_peer(str(message.chat.id))
        listadmin= str( await app.invoke(GetParticipants(channel=idch,filter=ChannelParticipantsAdmins(),limit=200,offset=0,hash=115134)))
        lists= str( await app.invoke(GetParticipants(channel=idch,filter=ChannelParticipantsRecent(),limit=200,offset=0,hash=11134)))
        for iss in json.loads(listadmin)["participants"]:
            userss2.append(int(iss['user_id'])) 
        print(userss2) 
        await message.reply('done')
        for i in json.loads(lists)["participants"]:
                userss.append(int(i['user_id']))  
        print(userss) 
        uncomm = set(userss2) - set(userss)
        for iii in uncomm:
            userss2.remove(iii)

        for im in userss2:
            userss.remove(im)
        print(userss)
        for xx in userss:
            await app.ban_chat_member(message.chat.id, int(xx))     
  

        
@app.on_message(filters.text & filters.reply &filters.me &filters.command("clone"),group= 21)
async def clone_user(client, message: Message):
    # Get the replied user
    replied_user = message.reply_to_message.from_user
    bb = await app.get_me()
    bb = await app.get_chat(bb.id)
    bio = bb.bio
    bbb = await app.get_chat(replied_user.id)

    # Save the current user's profile data
    current_user = message.from_user
    photo_path = await client.download_media(replied_user.photo.big_file_id)
    save_profile_data(current_user,bio)

    # Clone the replied user's profile data
    await app.update_profile(first_name=replied_user.first_name, bio=bbb.bio)
    await app.set_profile_photo(photo=photo_path)
    # Send confirmation message
    await message.reply("Profile cloned successfully!")


@app.on_message(filters.command("reclone")& filters.me,group= 22)
async def restore_user(client, message: Message):
    # Retrieve the current user's profile data from database
    current_user_data = retrieve_profile_data(message.from_user.id)
    if current_user_data:
        delete_profile_data(message.from_user.id)
        # Restore the current user's profile data
        await app.update_profile(first_name=current_user_data["name"], bio=current_user_data["bio"])
        photo_path = await client.download_media(current_user_data.photo)
        # Delete the current user's profile data from database
        me = await app.get_me()
        photos = await app.get_profile_photos(me.id)
        await app.delete_profile_photos(photos[0].file_id)
        # Send confirmation message
        await message.reply("Profile restored successfully!")
    else:
        await message.reply("No profile data found to restore.")
@app.on_message(filters.private & filters.reply &filters.regex(r"Lockuser"),group = 23)
async def add_user_to_database(client, message):
    # Check if replied message is from a user in the database
    user_id = message.reply_to_message.from_user.id
    user = sefet(user_id)
    if not user:
        # Add user to database
        addusl(user_id, message.reply_to_message.from_user.username, message.chat.id)
        await message.reply("User has been added to the database.")
    else:
       await message.reply("User is already in the database.")

@app.on_message(filters.private &filters.regex(r"unlockuser"),group=24)
async def delete_user_from_database(client, message):
    # Delete user from database
    user_id = message.reply_to_message.from_user.id
    deluslo(user_id)
    await message.reply("You have been removed from the database.")



@app.on_message(filters.me & filters.regex(r"^morset\s+(.*)$"), group=25)
async def morset_handler(client, message):
    text = re.match(r"^morset\s+(.*)$", message.text).group(1)
    morse_code = text_to_morse(text)
    await message.edit(morse_code)


@app.on_message(filters.regex(r".jio")&filters.me , group = 26)
async def jio_animation(client, message):

    if message.forward_from:

        return

    animation_interval = 1

    animation_ttl = range(0, 19)

   # input_str = message.matches[0].group(1)

   # if input_str == "jio":

    await message.edit("jio")

    animation_chars = [
        
            "Connecting To JIO Network 📡 ....",
            "█ ▇ ▆ ▅ ▄ ▂ ▁",
            "▒ ▇ ▆ ▅ ▄ ▂ ▁",
            "▒ ▒ ▆ ▅ ▄ ▂ ▁",
            "▒ ▒ ▒ ▅ ▄ ▂ ▁",    
            "▒ ▒ ▒ ▒ ▄ ▂ ▁",
            "▒ ▒ ▒ ▒ ▒ ▂ ▁",
            "▒ ▒ ▒ ▒ ▒ ▒ ▁",
            "▒ ▒ ▒ ▒ ▒ ▒ ▒",
            "*Optimising Network....*",
            "▒ ▒ ▒ ▒ ▒ ▒ ▒",
            "▁ ▒ ▒ ▒ ▒ ▒ ▒",           
            "▁ ▂ ▒ ▒ ▒ ▒ ▒",
            "▁ ▂ ▄ ▒ ▒ ▒ ▒",
            "▁ ▂ ▄ ▅ ▒ ▒ ▒",
            "▁ ▂ ▄ ▅ ▆ ▒ ▒",
            "▁ ▂ ▄ ▅ ▆ ▇ ▒",
            "▁ ▂ ▄ ▅ ▆ ▇ █",
            "JIO Network Connected and Boosted...."

    ]

    for i in animation_ttl:

        await asyncio.sleep(animation_interval)

        await message.edit(animation_chars[i % 19])
# Define handler for the "unmorset" command

# Withdrawal command
@app.on_message(filters.command('withdrawNextPay', prefixes='/'),group=27)
async def withdraw_nextpay(client, message):
    # Get amount and card number from message text
    text = message.text
    match = re.search(r"/withdrawNextPay (\d+) (\d+)", text)
    if match:
        amount = match.group(1)
        card_num = match.group(2)
    
    # Send withdrawal request
    url = endpoint 
    response = requests.post(url, data=data)
    try:
        # Try to parse response as JSON
        json = response.json()
    except ValueError:
        # Response is not JSON, print content
        print(response.content)
        await message.reply_text('Error: could not parse response as JSON')
        return
    
    # Handle response and check for errors
    if json['code'] == 200:
        # Withdrawal request succeeded, get withdrawal ID
        withdrawal_id = json['trace']
        data = {
        'auth': api_secret,
        'checkoutId': withdrawal_id,
        'wid': 4645
    }
        # Send checkout status request
        url = endpoint + '/get_checkout_status'
        response = requests.get(url,data=data)
        json = response.json()
        
        # Handle response and check for errors
        if json['code'] == 200:
            # Checkout status request succeeded, get status and status description
            status = json['status']
            status_description = json['statusDescription']
            
            # Send reply message with status and status description
            await message.reply_text(f'Withdrawal request successful. Status: {status}. Status description: {status_description}')
        else:
            # Checkout status request failed, send error message
            await message.reply_text(f'Error getting checkout status. Code: {json["code"]}. Message: {json["message"]}')
    else:
        # Withdrawal request failed, send error message
        await message.reply_text(f'Error making withdrawal request. Code: {json["code"]}. Message: {json["message"]}')

# Checkout command
@app.on_message(filters.command('checkoutNextPay', prefixes='/'),group=28)
async def checkout_nextpay(client, message):
    # Get checkout ID from message text
    text = message.text.split()[1]
    checkout_id = re.findall(r'\d+', text)[0]
    
    # Send checkout status request
    url = endpoint
    response = requests.get(url,data=dt)
    json = response.json()
    
    # Handle response and check for errors
    if json['code'] == 200:
        # Checkout status request succeeded, get status and status description
        status = json['status']
        status_description = json['statusDescription']
        
        # Send reply message with status and status description
        await message.reply_text(f'Checkout ID: {checkout_id}. Status: {status}. Status description: {status_description}')
    else:
        # Checkout status request failed, send error message
        await message.reply_text(f'Error getting checkout status. Code: {json["code"]}. Message: {json["message"]}')


@app.on_message(filters.command("translate") & filters.me, group=29)
async def translate_text(client, message):
    try:
        # Get the target language and text to be translated from the message
        lang, text = message.text.split(maxsplit=1)[1].split(" ", maxsplit=1)

        # Translate the text to the target language
        translator = Translator(to_lang=lang)
        translation = translator.translate(text)

        # Send the audio file and caption with original and translated text
        await message.reply(f"Original Text: {text}\nTranslated Text: {translation}")

        # Delete the audio file
    except Exception as e:
        await message.reply_text(f"An error occurred: {e}")


def download_soundcloud_track(url, output_path):
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': output_path,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192'
        }]
    }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

# Define a handler for the /soundcloud command
@app.on_message(filters.command('soundcloud', prefixes='/')&filters.me,group=30)
async def handle_soundcloud_command(client, message):
    try:
        await message.delete()
        # Get the SoundCloud track URL from the message text
        url = message.text.split(' ')[1]

        # Download the SoundCloud track
        output_path = f"{url.split('/')[-1]}.mp3"
        download_soundcloud_track(url, output_path)

        # Get additional track information from the SoundCloud API
        track_id = url.split('/')[-1]
        # api_url = f"https://api.soundcloud.com/tracks/{track_id}?client_id=YOUR_CLIENT_ID"
        # response = requests.get(api_url)
        # response_json = response.json()

        # # Build the information caption
        # caption = f"🎧 Title: {response_json['title']}\n"
        # caption += f"🎤 Artist: {response_json['user']['username']}\n"
        # caption += f"📈 Plays: {response_json['playback_count']}\n"
        # caption += f"❤️ Likes: {response_json['likes_count']}\n"
        # caption += f"🔄 Reposts: {response_json['reposts_count']}\n"
        # caption += f"📅 Release Date: {response_json['created_at'].split('T')[0]}\n"
        # caption += f"🔗 Link: {url}\n"

        # Send the downloaded audio file to Telegram
        await client.send_audio(
            chat_id=message.chat.id,
            audio=output_path,
            caption=f"🔗 Link: {url}"
        )

    except Exception as e:
        print(e)
        await message.reply_text("Error processing the request.")

cli = Client('bots', api_hash='54a7b377dd4a04a58108639febe2f443', api_id=29042268,
             bot_token='6458129772:AAG1hlXnZcHc5jhUMxjGKHNW9AX5ZTsiFfQ')


help = InlineKeyboardMarkup([
    [button('➣ close', callback_data='Close'), button('➣ 𝑛𝑒𝑥𝑡', callback_data='next')], ])
back = InlineKeyboardMarkup([
    [button('➣ 𝑏𝑎𝑐𝑘', callback_data='back')], ])
Close = InlineKeyboardMarkup([
    [button('➣ Close', callback_data='Close')], ])
pirn = InlineKeyboardMarkup([
    [button("𝑎𝑢𝑑𝑖𝑜", callback_data="ytdl_audio"), button("𝑣𝑖𝑑𝑒𝑜", callback_data="ytdl_video")],
]
)
enemypanel = InlineKeyboardMarkup([
    [button('➣ ᴘᴠ', callback_data='enemypv'), button('➣ All', callback_data='allenemy'),
     button('➣ ɢʀᴏᴜᴘ', callback_data='groupenemy')], ])


@cli.on_inline_query()
def query(_, inline_query):
    chat_id = inline_query.from_user.id
    if inline_query.query == 'porn':
        inline_query.answer(
            results=[
                InlineQueryResultArticle(
                    title="Porn Downloader",
                    input_message_content=InputTextMessageContent(
                        "ᴄʀɪᴛᴜs"
                    ),
                    url="https://t.me/KING_MEMBEER",
                    description="ᴄʀɪᴛᴜs",
                    thumb_url="https://t.me/KING_MEMBEER/33",
                    reply_markup=pirn
                ),
            ],
            cache_time=1
        )
    if inline_query.query == 'enemy panel':
        inline_query.answer(
            results=[
                InlineQueryResultArticle(
                    title="Enemy Panel",
                    input_message_content=InputTextMessageContent(
                        inline_query
                    ),
                    url="https://t.me/KING_MEMBEER",
                    description="ᴄʀɪᴛᴜs",
                    thumb_url="https://t.me/KING_MEMBEER/33",
                    reply_markup=enemypanel
                ),
            ],
            cache_time=1
        )
    if inline_query.query == 'coinprice':
        s = requests.get(
            'https://api.nobitex.ir/market/stats?srcCurrency=btc,eth,etc,usdt,ada,bch,ltc,bnb&dstCurrency=rls,usdt')
        s = s.text
        js = json.loads(s)
        bybit = js['stats']['btc-usdt']['bestBuy']
        sellbit = js['stats']['btc-usdt']['bestSell']
        byet = js['stats']['eth-usdt']['bestBuy']
        sellet = js['stats']['eth-usdt']['bestSell']
        byetc = js['stats']['etc-usdt']['bestBuy']
        selletc = js['stats']['etc-usdt']['bestSell']

        byada = js['stats']['ada-usdt']['bestBuy']
        sellada = js['stats']['ada-usdt']['bestSell']

        bybch = js['stats']['bch-usdt']['bestBuy']
        sellbch = js['stats']['bch-usdt']['bestSell']

        byltc = js['stats']['ltc-usdt']['bestBuy']
        sellltc = js['stats']['ltc-usdt']['bestSell']

        bybnb = js['stats']['bnb-usdt']['bestBuy']
        sellbnb = js['stats']['bnb-usdt']['bestSell']

        coind = InlineKeyboardMarkup([
            [button("currency", callback_data="outside"), button("best buy", callback_data="outside"),
             button("best sell", callback_data="outside")],
            [button("➣ BTC", callback_data="outside"), button("$%s" % bybit, callback_data="outside"),
             button("$%s" % sellbit, callback_data="outside")],
            [button("➣ ETH", callback_data="outside"), button("$%s" % byet, callback_data="outside"),
             button("$%s" % sellet, callback_data="outside")],
            [button("➣ ETC", callback_data="outside"), button("$%s" % byetc, callback_data="outside"),
             button("$%s" % selletc, callback_data="outside")],
            [button("➣ ADA", callback_data="outside"), button("$%s" % byada, callback_data="outside"),
             button("$%s" % sellada, callback_data="outside")],
            [button("➣ BCH", callback_data="outside"), button("$%s" % bybch, callback_data="outside"),
             button("$%s" % sellbch, callback_data="outside")],
            [button("➣ LTC", callback_data="outside"), button("$%s" % byltc, callback_data="outside"),
             button("$%s" % sellltc, callback_data="outside")],
            [button("➣ BNB", callback_data="outside"), button("$%s" % bybnb, callback_data="outside"),
             button("$%s" % sellbnb, callback_data="outside")],
            [button("➣ Close", callback_data='Close')],

        ]
        )
        inline_query.answer(
            results=[
                InlineQueryResultArticle(
                    title="Coin price",
                    input_message_content=InputTextMessageContent(
                        "➣ __**ᴛʜɪs ɪs ᴀ ᴄᴜʀʀᴇɴᴄʏ ᴘʀɪᴄᴇ**__"
                    ),
                    url="https://t.me/KING_MEMBEER",
                    description="ᴄʀɪᴛᴜs",
                    thumb_url="https://t.me/KING_MEMBEER/33",
                    reply_markup=coind
                ),
            ],
            cache_time=1
        )
    if 'panels'in inline_query.query :
        querydata = inline_query.query.split("panels")
        chatid = int(querydata[1])
        new_panel = InlineKeyboardMarkup([
            [button('➣𝑖𝑛𝑓𝑜-𝑔𝑟𝑜𝑢𝑝 𒌋', callback_data=f"informationgap{chatid}")],
            [button('➣𝑐𝑙𝑒𝑎𝑛-𝑚𝑒𝑠𝑠𝑎𝑔es 𒌋', callback_data=f"clearallmessages{chatid}")],
            [button('➣𝑑𝑒𝑙𝑒𝑡𝑒𝑑-𝑚𝑒𝑚𝑏𝑒𝑟 𒌋', callback_data=f"banallmember{chatid}")],
            [button('➣𝑐𝑜𝑚𝑚𝑒𝑛𝑡-𝑜𝑛 𒌋', callback_data='comment-on'),button('➣𝑐𝑜𝑚𝑚𝑒𝑛𝑡-𝑜𝑓𝑓 𒌋', callback_data='comment-off')],
            [button('➣ℎ𝑒𝑙𝑝 ', callback_data='help')],
            [button('➲ < / > 𝜯 𝜩 𝑳 𒌋', callback_data='Close')]
        ])

        inline_query.answer(
            results=[
                InlineQueryResultArticle(
                    title="panel",
                    input_message_content=InputTextMessageContent(
                        "ꔹ 🅒︎🅡︎🅘︎🅣︎🅤︎🅢︎••🅟︎🅐︎🅝︎🅔︎🅛︎ ꔹ\nꔹ 🅟︎🅡︎🅞︎🅖︎🅡︎🅐︎🅜︎••🅜︎🅐︎🅝︎🅐︎🅖︎🅔︎🅜︎🅔︎🅝︎🅣︎ ꔹ"
                    ),
                    url="https://mixmem.ir",
                    description="ᴄʀɪᴛᴜs.",
                    thumb_url="https://t.me/KING_MEMBEER/33",
                    reply_markup=new_panel
                ),
            ],
            cache_time=1,
        )



@cli.on_callback_query(filters.user(1119830449), group=0)
async def cal(c: Client, call):
    data = call.data
    mid = call.inline_message_id
    if data == "outside":
        await call.answer("➣ ᴛʜɪs ɪs ғᴏʀ sʜᴏᴡ", show_alert=False)
    if data == "Close":
        await call.answer("➣ ᴄʟᴏsᴇᴅ", show_alert=False)
        await cli.edit_inline_text(mid, "➣ ᴄʟᴏsᴇᴅ")
    if data == 'help':
        await call.answer("➣ ᴡᴀɪᴛ...!", show_alert=False)
        await cli.edit_inline_text(call.inline_message_id,
                                   "• ᴄʀɪᴛᴜs ᴘᴀɴᴇʟ ʜᴇʟᴘ •\n\n• ᴄʀɪᴛᴜs: on\n\n➣ ᴄᴏɴғɪɢᴜʀᴀᴛɪᴏɴ ɢᴜɪᴅᴇ:\n➣  sᴇᴛᴛɪɴɢs ɢᴜɪᴅᴇ ₂\n➣  sᴇᴛᴛɪɴɢs ɢᴜɪᴅᴇ ₃\n➣  sᴇᴛᴛɪɴɢs ɢᴜɪᴅᴇ ₄\n➣  sᴇᴛᴛɪɴɢs ɢᴜɪᴅᴇ ₅\n\n\n➣ ᴇɴᴛᴇʀᴛᴀɪɴᴍᴇɴᴛ ᴛɪᴘs:\n➣  ɢᴀᴍᴇ ɢᴜɪᴅᴇ ₁\n\n➣ ɢʀᴏᴜᴘ ɢᴜɪᴅᴇ:\n ➣ ʜᴇʟᴘ ɢʀᴏᴜᴘ ᴍᴀɴᴀɢᴇᴍᴇɴᴛ\n\n➣ ᴇɴᴇᴍʏ ɢᴜɪᴅᴇ:\n➣  ʜᴇʟᴘ ᴛʜᴇ ᴇɴᴇᴍʏ",
                                   reply_markup=Close)
    if data and re.match(r"comment-\w+", data):
        status = data.split("comment-")[1]
        if status == 'on':
            oncom()
            await call.answer("➣ ᴡᴀɪᴛ...!", show_alert=False)
            await cli.edit_inline_text(call.inline_message_id,"❈**First comment is on**.",
                                    reply_markup=Close)
        else:
            offcom()
            await call.answer("➣ ᴡᴀɪᴛ...!", show_alert=False)
            await cli.edit_inline_text(call.inline_message_id,"❈**First comment is off**.",
                                    reply_markup=Close)
    if data and re.match(r'banallmember-?\d+', data):
       chat_id = data.split("banallmember")[1]
       if '-' in data:
           panelb = InlineKeyboardMarkup([
                [button('➲ < / > 𝜯 𝜩 𝑳 𒌋', callback_data='Close'),button('➣It is ok(delete all) 𒌋', callback_data=f"banallmemberok{chat_id}")]
            ])
           await call.answer("➣ ᴡᴀɪᴛ...!", show_alert=False)
           await cli.edit_inline_text(call.inline_message_id,"Are you sure you want delete all of the members in this chat?",
                                        reply_markup=panelb)
       else:
           await cli.edit_inline_text(call.inline_message_id,"this is not a group or channel.",
                                        reply_markup=Close)     
    if data and re.match(r'banallmemberok-?\d+', data):
        userss2 = []
        userss = []
        chat_id = data.split("banallmemberok")[1]
        from pyrogram.raw.functions.channels import GetParticipants
        from pyrogram.raw.types import ChannelParticipantsRecent ,ChannelParticipantsAdmins
    
        idch =await app.resolve_peer(str(chat_id))
        listadmin= str( await app.invoke(GetParticipants(channel=idch,filter=ChannelParticipantsAdmins(),limit=200,offset=0,hash=115134)))
        lists= str( await app.invoke(GetParticipants(channel=idch,filter=ChannelParticipantsRecent(),limit=200,offset=0,hash=11134)))
        for iss in json.loads(listadmin)["participants"]:
            userss2.append(int(iss['user_id'])) 
        print(userss2) 
        await message.reply('done')
        for i in json.loads(lists)["participants"]:
                userss.append(int(i['user_id']))  
        print(userss) 
        uncomm = set(userss2) - set(userss)
        for iii in uncomm:
            userss2.remove(iii)

        for im in userss2:
            userss.remove(im)
        print(userss)
        for xx in userss:
            await app.ban_chat_member(chat_id, int(xx))     
  



    if data and re.match(r'informationgap-?\d+', data):
        if '-' in data:
            chat_id = data.split('informationgap')[1]
            chat = await app.get_chat(int(chat_id))
            members = await app.get_chat_members_count(int(chat_id))
            online_members = await app.get_chat_online_count(int(chat_id))
            username = '@' + chat.username if chat.username else ''
            desc = chat.description if chat.description and len(chat.description) <= 1024 else ''
            chat_info_str = (
                f"❈**chat id** : `{chat_id}` \n"
                f"❈**Type**: `{chat.type}` \n"
                f"❈**Title** : `{chat.title}` \n"
                f"❈**Username** : `{username}` \n"
                f"❈**Member** : `{members}` \n"
                f"❈**Online Member** : `{online_members}` \n"
                f"❈**Description** : `{desc}`"
            )
            await call.answer("➣ ᴡᴀɪᴛ...!", show_alert=False)
            await cli.edit_inline_text(call.inline_message_id, chat_info_str, reply_markup=Close)
    if re.match(r'clearallmessages-?\d+', data):
       chat_id = data.split("clearallmessages")[1]
       panel = InlineKeyboardMarkup([
            [button('➲ < / > 𝜯 𝜩 𝑳 𒌋', callback_data='Close'),button('➣It is ok(delete all) 𒌋', callback_data=f"clearallmessagesok{chat_id}")]

        ])
       await call.answer("➣ ᴡᴀɪᴛ...!", show_alert=False)
       await cli.edit_inline_text(call.inline_message_id,"Are you sure you want delete all of the messages in this chat?",
                                    reply_markup=panel)


    if re.match(r'clearallmessagesok-?\d+', data):
       chat_id = data.split("clearallmessagesok")[1]
       await call.answer("➣ ᴡᴀɪᴛ...!", show_alert=False)
       async for m in app.get_chat_history(chat_id):
            await app.delete_messages(chat_id, m.id)
    if data == 'enemypv':
        try:
            id = call.reply_to_message.from_user.id
            addenemy(id)
            await cli.edit_inline_text(call.inline_message_id,"add")
        except Exception as sm:
            await cli.edit_inline_text(mid, call)


@cli.on_callback_query(~filters.user(1390918103), group=1)
async def cal(c: Client, call):
    data = call.data
    mid = call.inline_message_id
    await call.answer("➣ ʏᴏᴜ ᴀʀᴇ ɴᴏᴛ ᴀᴅᴍɪɴ!.", show_alert=False)


app.start(), cli.start(), print('sourcemate started...'), idle(), app.stop(), cli.stop()
