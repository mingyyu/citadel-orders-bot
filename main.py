# -*- coding: utf-8 -*-

import requests
import time
import uuid
from time import gmtime, strftime
import random
import MySQLdb
import re
import json
import asyncio
#from json import loads
#from asynckafka import Consumer

log_channel = -1001175100654

def mysqlconnect():
    print('Trying to connect...')
    global db_connection
    db_connection = None
    try:
        db_connection= MySQLdb.connect(
        "censored","censored","censored","censored"
        )
    except:
        print("Can't connect to database")
        exit()
        return 0
    print("Connected")
    print('Making cursor...')
    global cursor
    cursor=db_connection.cursor()
    print('Cursor connected.')

# Function Call For Connecting To Our Database
mysqlconnect()

class BotHandler:
    def __init__(self, token):
            self.token = token
            self.api_url = "https://api.telegram.org/bot{}/".format(token)

    #url = "https://api.telegram.org/bot<token>/"

    def get_updates(self, offset=0, timeout=30):
        method = 'getUpdates'
        params = {'timeout': timeout, 'offset': offset}
        try:
            resp = requests.get(self.api_url + method, params)
            if 'result' in resp.json():
                result_json = resp.json()['result']
            else:
                result_json = {}
        except:
            print('cannot connect to telegram')
            time.sleep(100)
            result_json = {}
        return result_json

    def send_message(self, chat_id, text, **kwargs):
        params = {'chat_id': chat_id, 'text': text, 'parse_mode': 'HTML'}
        method = 'sendMessage'
        resp = requests.post(self.api_url + method, params)
        print('\n'+str(resp.text)+'\n')
        try:
            if chat_id in guild_info:
                msg_id_by_bot = int(json.loads(resp.text)["result"]["message_id"])
                ccordersbot.send_message(-1001354774898, '['+str(chat_id)+'] ('+str(msg_id_by_bot)+'): '+text+' '+guild_info[chat_id]['tag'])
                if len(kwargs)!=0:
                    ikeyboard = [[{"text": '📌', "callback_data": 'pin_'+str(chat_id)+'_'+str(msg_id_by_bot)}, {"text": '🗑', "callback_data": 'del_'+str(chat_id)+'_'+str(msg_id_by_bot)}]]
                    ccordersbot.inline_keyboard_markup(kwargs['return_id'], '✅✉️-->['+guild_info[chat_id]['tag']+'] ('+str(chat_id)+'): \n'+text, ikeyboard, '')
        except:
            ccordersbot.send_message(-1001354774898, 'An error occurred when sending message: \nError code: '+str(resp.status_code)+'\nReason: '+str(resp.reason)+'\nDetails: '+str(resp.text))
            if len(kwargs)!=0:
                ccordersbot.send_message(kwargs['return_id'], 'An error occurred when sending message: \nError code: '+str(resp.status_code)+'\nReason: '+str(resp.reason)+'\nDetails: '+str(resp.text))
        if "parameters" in json.loads(resp.text):
            if 'retry_after' in json.loads(resp.text)["parameters"]:
                time.sleep(int(json.loads(resp.text)["parameters"]['retry_after'])+3)
                resp = ccordersbot.send_message(chat_id, text)
        return resp

    def reply_to_message(self, chat_id, msg_id, text):
        params = {'chat_id': chat_id, 'reply_to_message_id': msg_id, 'text': text, 'parse_mode': 'HTML'}
        method = 'sendMessage'
        resp = requests.post(self.api_url + method, params)
        print(resp.text)
        return resp

    def proper_message(self, chat_id, text, wided):
        params = {'chat_id': chat_id, 'text': text, 'parse_mode': 'HTML'}
        method = 'sendMessage'
        resp = requests.post(self.api_url + method, params)
        if resp.status_code != 200:
            ccordersbot.send_message(wided, 'An error occurred: \nError code: '+str(resp.status_code)+'\nReason: '+str(resp.reason)+'\nDetails: '+str(resp.text))
            doipinornot[0] = False
        else:
            ccordersbot.send_message(wided, 'No errors, message successfully sent.')
            doipinornot[0] = True
        return resp

    def reply_keyboard_markup(self, chat_id, text, keyboard, is_one_time=True, is_selective=True):
        method = 'sendMessage'
        params = {"chat_id": chat_id, "text": text, "reply_markup": {"keyboard": keyboard, "resize_keyboard": True, "one_time_keyboard": False, "selective": is_selective}, 'parse_mode': 'HTML'}
        resp = requests.post(self.api_url + method, json=params)
        return resp

    def inline_keyboard_markup(self, chat_id, text, ikeyboard, sreply):
        method = 'sendMessage'
        params = {"chat_id": chat_id, "text": text, "reply_markup": {"inline_keyboard": ikeyboard}, 'parse_mode': 'HTML'}
        resp = requests.post(self.api_url + method, json=params)
        if sreply!='':
            if resp.status_code != 200:
                ccordersbot.send_message(sreply, 'An error occurred: \nError code: '+str(resp.status_code)+'\nReason: '+str(resp.reason)+'\nDetails: '+str(resp.text))
                doipinornot[0] = False
            else:
                ccordersbot.send_message(sreply, 'No errors, message successfully sent.')
                doipinornot[0] = True
        return resp

    def answer_callback_query(self, chat_id, text, callback_query_id, itext):
        method = 'answerCallbackQuery'
        print(itext)
        if itext!='':
            if 't.me/' in itext:
                params = {"callback_query_id": callback_query_id, "text": itext, "show_alert": True}
            else:
                params = {"callback_query_id": callback_query_id, "text": itext}
        else:
            params = {"callback_query_id": callback_query_id}
        if text!='':
            ccordersbot.send_message(chat_id, text)
        resp = requests.post(self.api_url + method, json=params)
        print(resp.status_code)
        print(resp.reason)
        print(resp.text)
        return resp

    def pin_chat_message(self, chat_id, message_id, notif):
        method = 'pinChatMessage'
        params = {"chat_id": chat_id, "message_id": message_id, "disable_notification": notif}
        resp = requests.post(self.api_url + method, json=params)
        needtodelete[message_id] = chat_id
        return resp

    def unpin(self, chat_id):
        method = 'unpinChatMessage'
        params = {"chat_id": chat_id}
        resp = requests.post(self.api_url + method, json=params)
        return resp
        #send sticker function not in use
    def send_sticker(self, chat_id, text):
        method = 'sendMessage'
        params = {'file_id': 'AAMCAgADGQEAAgMxXsjSRF5KTvnO6-lY5lqin-qLduYAAmoAA62NWwXRdOXH1CwiKXtWrQ4ABAEAB20ABG8AAhkE', 'file_unique_id': 'AQADe1atDgAFbwAC', 'file_size': 3090, 'width': 128, 'height': 128, 'is_animated': False}
        ccordersbot.send_message(chat_id, text)
        resp = requests.post(self.api_url + method, json=params)
        return resp

    def answer_inline_query(self, results, inline_query_id):
        method = 'answerInlineQuery'
        params = {"inline_query_id": inline_query_id, "results": results}
        resp = requests.post(self.api_url + method, json=params)
        print(resp.text)
        return resp

    def edit_message(self, chat_id, message_id, text):
        params = {'chat_id': int(chat_id), 'message_id': int(message_id), 'text': str(text), 'parse_mode': 'HTML'}
        method = 'editMessageText'
        resp = requests.post(self.api_url + method, params)
        print(resp.text)
        return resp

    def send_picture(self, chat_id, photo, caption):
        method = 'sendPhoto'
        params = {"chat_id": chat_id, "photo": photo, "caption": caption}
        resp = requests.post(self.api_url + method, json=params)
        print(resp.text)
        return resp

    def delete_message(self, chat_id, msgid):
        method = 'deleteMessage'
        params = {"chat_id": chat_id, "message_id": msgid}
        resp = requests.post(self.api_url + method, json=params)
        return resp

    def get_first_update(self):
        get_result = self.get_updates()

        if len(get_result) > 0:
            last_update = get_result[0]
        else:
            last_update = None

        return last_update

token = '🌝<insert token here> censored' #Token of bot
ccordersbot = BotHandler(token)

#handle duels not implemented (because kafka problems)
def handle_duels(duel):
    sql = "INSERT INTO DUELS VALUES ('"+str(offset['duels'])+"', '"+str(duel['winner']['id'])+"', '"+str(duel['loser']['id'])+"', '"+str(duel['winner']['name'])+"', '"+str(duel['loser']['name'])+"', '"+str(duel['winner']['level'])+"', '"+str(duel['loser']['level'])+"', '"+str(duel['winner']['castle'].encode('unicode-escape').decode('ASCII'))+"', '"+str(duel['loser']['castle'].encode('unicode-escape').decode('ASCII'))+"', '0')"
    duels[offset['duels']] = {'age': 0, 'winner': {'id': str(duel['winner']['id']), 'ign': str(duel['winner']['name']), 'lvl': int(duel['winner']['level']), 'castle': str(duel['winner']['castle'])}, 'loser': {'id': str(duel['loser']['id']), 'ign': str(duel['loser']['name']), 'lvl': int(duel['loser']['level']), 'castle': str(duel['loser']['castle'])}}
    botdb.comm(sql, 'unable to add duel to db')
    offset['duels']+=1
    #CREATE TABLE OFFSET (NAME  CHAR(15), VALUE  CHAR(10));
    sql = "UPDATE OFFSET SET VALUE = '"+str(offset['duels'])+"' WHERE NAME = 'duels'"
    botdb.comm(sql, 'unable to change duel offset')

class DBHandler:
    def get_info(self, column, liste, tarcolrows, value):
        if column=='' and tarcolrows=='' and value=='':
            sql = "SELECT * FROM "+str(liste)
        else:
            sql = "SELECT "+str(column)+" FROM "+str(liste)+" WHERE "+str(tarcolrows)+" = '"+str(value)+"'"
        try:
            cursor.execute(sql)
            results = cursor.fetchall()
        except:
            mysqlconnect()
            try:
                cursor.execute(sql)
                results = cursor.fetchall()
            except:
                ccordersbot.send_message(log_channel, "Error: unable to fetch data for getdbinfo(), credentials: \n"+str(sql)+"\n\n#error")
                results = ''
        return results

    def change_info(self, liste, thing, value, cond, what):
        if cond=='' and what=='':
            sql = "UPDATE "+str(liste)+" SET "+str(thing)+" = '"+str(value)+"'"
        else:
            sql = "UPDATE "+str(liste)+" SET "+str(thing)+" = '"+str(value)+"' WHERE "+str(cond)+" = '"+str(what)+"'"
        botdb.comm(sql, 'unable to change data for changedbinfo()')

    def delete_info(self, table, cond, value):
        sql = "DELETE FROM "+str(table)+" WHERE "+str(cond)+" = '"+str(value)+"'"
        botdb.comm(sql, 'unable to delete db row')

    def add_location(self, name, code, status, typeee, age, owner, dump):
        sql = "INSERT INTO LOCATIONS VALUES ('"+str(name)+"', '"+str(code)+"', '"+str(status)+"', '"+str(typeee)+"', '"+str(age)+"', '"+str(owner)+"', '"+str(dump)+"')"
        botdb.comm(sql, 'unable to add location to db')

    def add_hq(self, name, code, status, power, dump):
        sql = "INSERT INTO ALLIANCES VALUES ('"+str(name)+"', '"+str(code)+"', '"+str(status)+"', '"+str(power)+"', '"+str(dump)+"')"
        botdb.comm(sql, 'unable to add hq to db')

    def add_guild(self, tag, chat, leader, credit, settings):
        sql = "INSERT INTO GUILD VALUES ('"+str(tag)+"', '"+str(chat)+"', '"+str(leader)+"', '"+str(credit)+"', '"+str(settings)+"')"
        botdb.comm(sql, 'unable to add guild to db')

    def comm(self, sql, error):
        try:
           cursor.execute(sql)
           db_connection.commit()
        except:
            mysqlconnect()
            try:
                cursor.execute(sql)
                db_connection.commit()
            except:
                ccordersbot.send_message(log_channel, "#error: \n"+str(error)+"\n<code>Query:</code> \n"+str(sql))

botdb = DBHandler()

class SecurityHandler:
    def guild(self, cht_id):
        g_tag = ''
        for x in guild_info:
            if cht_id==guild_info[x]['leader'] or cht_id==x:
                g_tag = guild_info[x]['tag']
        return g_tag

    def member(self, cht_id):
        for x in members:
            if int(cht_id)==members[x]['id']:
                return x
        return False

clearance = SecurityHandler()

def initialize():
    global members
    global alliance
    global locations
    global guild_info
    global banlist
    members = {}
    alliance = {}
    locations = {}
    guild_info = {}
    banlist = []
    offset = {}
    duels = {}
    result = botdb.get_info('', "MEMBERS", '', '')
    for x in result:
        members[int(x[0])] = {'ign': x[1], 'atk': x[2], 'def': x[3], 'lvl': x[4], 'id': int(x[5]), 'guild': x[6]}
    result = botdb.get_info('', "LOCATIONS", '', '')
    for x in result:
        locations[x[1]] = {'name': x[0], 'status': x[2], 'type': x[3], 'age': int(x[4]), 'owner': x[5], 'dump': x[6]}
    result = botdb.get_info('', "ALLIANCES", '', '')
    for x in result:
        alliance[x[1]] = {'name': x[0], 'status': x[2], 'power': x[3], 'dump': x[4]}
    result = botdb.get_info('', "GUILD", '', '')
    for x in result:
        guild_info[int(x[1])] = {'tag': x[0], 'leader': int(x[2]), 'credit': int(x[3]), 'settings': str(x[4])}
    print('Locations: '+str(locations))
    result = botdb.get_info('', "DUELS", '', '')
    for x in result:
        duels[int(x[0])] = {'age': int(x[9]), 'winner': {'id': str(x[1]), 'ign': str(x[3]), 'lvl': int(x[5]), 'castle': str(x[7])}, 'loser': {'id': str(x[2]), 'ign': str(x[4]), 'lvl': int(x[6]), 'castle': str(x[8])}}
    result = botdb.get_info('', "BANLIST", '', '')
    for x in result:
        banlist.append(str(x[0]))
    print('Banlist: '+str(banlist))
    result = botdb.get_info('', "OFFSET", '', '')
    for x in result:
        offset[x[0]] = int(x[1])

initialize()

reports = {}

#cache variables... undeleted trash from first&second version of citadel orders bot (we use db now)
commanderlist = [536511250, -1001344525861, 924188734, 286258967]
guildyay = {}
poincomp = {}
waitinglist = []
chat = []
doipinornot = [True]
autoban = [False]
imode = ['A']
reattendance = [False, '✅Tick below to register your attendance']
pinning = [True]
chtgrps = [-1001146688414, -1001304570929, -1001290558528, -1001416110269, -1001201123281, -1001115528574, -1001276952340, -1001194097788, -1001306422833, 0, -1001457920863, -1001376774780, -1001378244959, -1001283488162]
pinrem = [49641, 107640, 145134, 0, 81029, 15293, 9000, 1789, 139537, 0, 131, 0, 0, 0]
footers = ['ℹ️Send your /report to @angrymarsbot']
timing = [0, 36000000, 0, 0]
joiningw = []
antispai = {}
ordereader = {}
order = []
resultoffset = [1323]
results = []
nomoreqclt = {}
yeodet = [0]
qcltest = [True]
importance = ['❗', '❗', '❗️']
needtodelete = {}
attendlist = {}

#add a piece of location or alliance headquarters to db.
def add_objective(name, code, owner):
    no_code = False
    if code=='':
        no_code = True
        try:
            if 'lvl' in name:
                for coder in locations:
                    if locations[coder]['name']==name:
                        code = coder
            else:
                for coder in alliance:
                    if alliance[coder]['name']==name:
                        code = coder
        except:
            return 0
        if code=='':
            return 0
    if code in alliance or code in locations:
        #check if alliance/location code exists in db
        if owner!='-':
            locations[code]['owner']=owner
            botdb.change_info("LOCATIONS", 'OWNER', owner, 'CODE', code)
            if owner not in alliance:
                ccordersbot.send_message(-1001338303651, owner)
        if 'lvl' not in name:
            statu = alliance[code]['status']
        else:
            statu = locations[code]['status']
        if statu!='active' and 'lvl' in name:
            botdb.change_info("LOCATIONS", "STATUS", 'active', "NAME", name)
        if 'lvl' not in name:
            alliance[code]['status']='active'
        else:
            locations[code]['status']='active'
    else:
        if 'lvl.' in name:
            typee = gettype(name)
        else:
            typee = 'hq'
        if typee!='hq':
            botdb.add_location(name, code, 'active', typee, '0', owner, '')
            locations[code] = {'name': name, 'status': 'active', 'type': typee, 'age': 0, 'owner': owner, 'dump': ''}
        else:
            botdb.add_hq(name, code, 'active', '100,100,100', '')
            alliance[code] = {'name': name, 'status': 'active', 'power': '100,100,100', 'dump': ''}
        for abccu in commanderlist:
            ccordersbot.send_message(abccu, '<b>New 📍 found:</b> \n'+name+' \n<b>Code:</b> '+code)

def check_locs(code):
    repeat = False
    for x in locations:
        if locations[x]["code"] == code:
            repeat = True
    for x in alliance:
        if alliance[x]["code"] == code:
            repeat = True
    return repeat

def gettype(office):
    if 'Fort' in office:
        typee = 'Glory T3'
    elif 'Tower' in office:
        typee = 'Glory T2'
    elif 'Outpost' in office:
        typee = 'Glory T1'
    elif 'Ruins' in office:
        if 'Ancient' in office:
            typee = 'Ruins T3'
        elif 'Trusted' in office:
            typee = 'Ruins T3'
        elif 'Dubious' in office:
            typee = 'Ruins T1'
    else:
        if 'Abandoned' in office:
            typee = 'Mine T3'
        elif 'Collapsed' in office:
            typee = 'Mine T2'
        elif 'Unfinished' in office:
            typee = 'Mine T1'
        else:
            ccordersbot.send_message(536511250, 'Mistake? \nLocation Name: '+str(office))
            typee = 'unknown'
    return typee

async def main():
    global guild_info
    global guilds
    global doipinornot
    global order
    global attendlist
    global reports
    new_offset = 0
    print('launching cc orders bot')

    while True:
        all_updates=ccordersbot.get_updates(new_offset)
        await asyncio.sleep(0.1)

        if len(all_updates) > 0:
            async_update = []
            for current_update in all_updates:
                print(current_update)
                first_update_id = current_update['update_id']
                new_offset = first_update_id + 1
                async_update.append(update_handler(current_update))
            await asyncio.gather(*async_update)
        if timing[3]<=time.perf_counter()-45:
            if timing[0]<=time.perf_counter()-1200:
                timing[0] = int(time.perf_counter())
            nicetime = strftime("%H:%M", gmtime())
            if nicetime == '07:00' or nicetime == '15:00' or nicetime == '23:00':
                ccordersbot.send_message(-1001175100654, 'The Wind Is Howling')
                time.sleep(60)
                for x in locations:
                    locations[x]['age']=locations[x]['age']+1
                    botdb.change_info("LOCATIONS", "AGE", locations[x]['age'], "NAME", x)
                #for x in duels:
                    #duels[x]['age']+=1
                    #if duels[x]['age']>21:
                        #needtodelll.append(x)
                #for x in needtodelll:
                #    duels.pop(x)
                #    botdb.delete_info("DUELS", "ID", x)
                for chattts in chtgrps:
                    ccordersbot.unpin(chattts)
                for msggs in needtodelete:
                    ccordersbot.delete_message(needtodelete[msggs], msggs)
                reports = {}
                timing[1] = time.perf_counter()
            if timing[1]+540<=time.perf_counter():
                yeodet[0] = 0
                threspp = ccordersbot.send_message(-1001416833350, '<b>⚔️ Battle is over! ⚔️</b> \n\nSend your battle <a href="t.me/share/url?url=/report">/report</a> to @angrymarsbot')
                ccordersbot.pin_chat_message(-1001416833350, int(threspp.text.split('"message_id":')[1].split(',')[0]), True)
                timing[1]=int(time.perf_counter()+36000000)
            if timing[2]+60<=time.perf_counter():
                gointopop = []
                for peoids in nomoreqclt:
                    if nomoreqclt[peoids]+3600 <= time.perf_counter():
                        gointopop.append(peoids)
                for ppeoids in gointopop:
                    nomoreqclt.pop(ppeoids)
                timing[2]=time.perf_counter()
            timing[3] = time.perf_counter()

#some stuff in here is unused trash from first&second version of ccordersbot
async def update_handler(current_update):
            global guild_info
            global guilds
            global doipinornot
            global order
            global attendlist
            global reports
            if True: #try:
                first_update_id = current_update['update_id']
                new_offset = first_update_id + 1
                iscwbot = False
                isgrp = False
                first_chat_text=''
                first_chat_id=0
                sender_id=0

                if 'message' in current_update or 'edited_message' in current_update:
                    if 'edited_message' in current_update:
                        print('Trash update---')
                        return
                    if 'from' in current_update['message']:
                        sender_id = current_update['message']['from']['id']
                    else:
                        sender_id = 0
                    first_msg_id = current_update['message']['message_id']
                    if 'forward_from' in current_update['message']:
                        if current_update['message']['forward_from']['id']==408101137:
                            iscwbot = True
                    if 'chat' in current_update['message']:
                        first_chat_id = current_update['message']['chat']['id']
                        if first_chat_id==-1001354774898:
                            if 'reply_to_message' in current_update['message']:
                                try:
                                    cht_txt = current_update['message']['reply_to_message']['text']
                                    first_chat_text = current_update['message']['text']
                                    if '[' in cht_txt:
                                        msgid = int(cht_txt.split('(')[1].split(')')[0])
                                        guild_id = cht_txt.split('[')[1].split(']')[0]
                                    if first_chat_text=='/pin':
                                        ccordersbot.pin_chat_message(guild_id, msgid, False)
                                    else:
                                        ccordersbot.reply_to_message(guild_id, msgid, first_chat_text)
                                except:
                                    ccordersbot.send_message(-1001354774898, 'error')
                        if current_update['message']['chat']['type'] == 'supergroup':
                            if 'text' in current_update['message']:
                                first_chat_text = current_update['message']['text']
                            if (('То remember the route you associated it with simple combination' not in first_chat_text and 'Your result on the battlefield:' not in first_chat_text) or iscwbot!=True) and 'update locations' not in first_chat_text:
                                for x in guild_info:
                                    if x==first_chat_id:
                                        ccordersbot.send_message(-1001354774898, '['+str(first_chat_id)+'] ('+str(current_update['message']['message_id'])+') <a href="tg://user?id='+str(sender_id)+'">'+str(sender_id)+'</a>: '+first_chat_text+' '+guild_info[x]['tag'])
                                if '/' in first_chat_text:
                                    print('parsing grp command...')
                                    isgrp = True
                                else:
                                    print('Trash update---')
                                    return
                            else:
                                print('parsing grp msg...')
                                isgrp = True
                        elif current_update['message']['chat']['id'] in banlist:
                            print('Trash update---')
                            return
                    if 'text' not in current_update['message']:
                        first_chat_text='New member'
                    else:
                        first_chat_text = current_update['message']['text']
                    if 'first_name' in current_update['message']:
                        first_chat_name = current_update['message']['chat']['first_name']
                    elif 'new_chat_member' in current_update['message']:
                        first_chat_name = current_update['message']['new_chat_member']['username']
                elif "channel_post" in current_update:
                    first_chat_id = current_update['channel_post']['chat']['id']
                    if first_chat_id!=-1001338303651:
                        print('Trash update---')
                        return
                    try:
                        first_chat_text=current_update['channel_post']['text']
                    except:
                        return
                    if '/new_battle' in first_chat_text:
                        first_chat_fake_text=json.loads(first_chat_text.split('\n')[1])
                        print('Parsed current new battle: '+str(first_chat_fake_text))
                        if len(first_chat_fake_text)>=17:
                            tempo_loc = []
                            for x in locations:
                                for y in first_chat_fake_text:
                                    if y[0]==locations[x]['name']:
                                        tempo_loc.append(locations[x]['name'])
                                        del(first_chat_fake_text[first_chat_fake_text.index(y)])
                                        break
                            netodel = []
                            temp_locations = []
                            for x in locations:
                                temp_locations.append([x, locations[x]])
                            temp_locations.reverse()
                            for x in temp_locations:
                                if x[1]['name'] in tempo_loc:
                                    del(tempo_loc[tempo_loc.index(x[1]['name'])])
                                else:
                                    netodel.append(x[0])
                            for x in netodel:
                                botdb.delete_info("LOCATIONS", "CODE", x)
                            initialize()
                        return
                    elif '{' not in first_chat_text:
                        print('Trash update---')
                        return
                    first_chat_text=json.loads(first_chat_text.replace('\n', '').replace('    ', ''))
                    print('Parsed current dict: '+str(first_chat_text))
                    if 'key' not in first_chat_text:
                        return
                    try:
                        code_for_add = first_chat_text['code']
                    except:
                        code_for_add = ''
                    owner = '-'
                    if 'last_battle' in first_chat_text:
                        try:
                            yee = ('by' in first_chat_text['last_battle'])
                        except:
                            yee=False
                        if yee:
                            owner = first_chat_text['last_battle'].split('(by ')[1].split(')')[0]
                    if owner!='-':
                        if 'last_battles' in first_chat_text:
                            for x in first_chat_text['last_battles']:
                                if '(by ' not in x[0]:
                                    continue
                                owner = x[0].split('(by ')[1].split(')')[0]
                                break
                    add_objective(first_chat_text['key'], code_for_add, owner)
                    return
                elif 'callback_query' in current_update:
                    first_query_id = current_update['callback_query']['id']
                    first_chat_id = current_update['callback_query']['from']['id']
                    first_chat_name = current_update['callback_query']['from']['first_name']
                    first_chat_text = current_update['callback_query']['data']
                    if 'pin_' in first_chat_text:
                        first_chat_text = first_chat_text.split('_')
                        ccordersbot.pin_chat_message(int(first_chat_text[1]), int(first_chat_text[2]), False)
                        ccordersbot.answer_callback_query(first_chat_id, '', first_query_id, '📌✅')
                        original_text = current_update['callback_query']['message']['text']
                        original_id = current_update['callback_query']['message']['message_id']
                        ccordersbot.edit_message(first_chat_id, original_id, original_text+'\n📌✅')
                    elif 'del_' in first_chat_text:
                        first_chat_text = first_chat_text.split('_')
                        ccordersbot.delete_message(int(first_chat_text[1]), int(first_chat_text[2]))
                        ccordersbot.answer_callback_query(first_chat_id, '', first_query_id, 'Deleted order. 📄➡️🗑')
                        original_text = current_update['callback_query']['message']['text']
                        original_id = current_update['callback_query']['message']['message_id']
                        ccordersbot.edit_message(first_chat_id, original_id, '<s>'+original_text+'</s>\nDeleted order. 📄➡️🗑')
                    return
                elif 'inline_query' in current_update:
                    i_query_id = current_update['inline_query']['id']
                    i_chat_text = current_update['inline_query']['query']
                    i_chat_id = current_update['inline_query']['from']['id']
                    if 'username' in current_update['inline_query']['from']:
                        i_chat_name = current_update['inline_query']['from']['username']
                    elif 'first_name' in current_update['inline_query']['from']:
                        i_chat_name = current_update['inline_query']['from']['first_name']
                    elif 'last_name' in current_update['inline_query']['from']:
                        i_chat_name = current_update['inline_query']['from']['last_name']
                    else:
                        i_chat_name = 'unknown'
                    resultis = []
                    nonononoiwant = True
                    if commanderlist.count(i_chat_id)!=0:
                        if 'map' in i_chat_text or 'dots' in i_chat_text:
                            if 'hq' not in i_chat_text and 'eadquarters' not in i_chat_text and 'HQ' not in i_chat_text and 'Hq' not in i_chat_text:
                                i_title = "🗺All Locations Map"
                                i_text = 'All known <b>Locations:</b> \nTo delete, /delete_code \nTo deactivate, /deactivate_code \nTo activate, /activate_code'
                                for dots in locations:
                                    i_text = i_text+'\n<b>'+locations[dots]["name"]+'</b> <code>'+dots+'</code> \n<b>'+str(locations[dots]["status"])+'</b>, Type: <b>'+locations[dots]["type"]+'</b>'
                                if i_text == 'All known <b>Locations:</b>':
                                    i_text = i_text+'\n\n<i>[no data yet]</i>'
                                desc = 'Get a list of all locations.'
                                resultis.append({"type": "article", "id": str(resultoffset[0]), "title": i_title, "input_message_content": {"message_text": i_text, "parse_mode": "HTML"}, "description": desc})
                                resultoffset[0] = resultoffset[0]+1
                                i_title = "🗺Locations Map"
                                i_text = 'The active <b>Locations:</b>'
                                for dots in locations:
                                    if locations[dots]['status']=='active':
                                        i_text+='\n<b>'+locations[dots]["name"]+'</b> <code>'+dots+'</code> \n<b>'+str(locations[dots]["status"])+'</b>, Type: <b>'+locations[dots]["type"]+'</b> \n/deactivate_'+dots+' \n/delete_'+dots
                                if i_text == 'The active <b>Locations:</b>':
                                    i_text = i_text+'\n\n<i>[no data yet]</i>'
                                desc = 'Get a list of current active locations.'
                                resultis.append({"type": "article", "id": str(resultoffset[0]), "title": i_title, "input_message_content": {"message_text": i_text, "parse_mode": "HTML"}, "description": desc})
                                resultoffset[0] = resultoffset[0]+1
                            if 'ocations' not in i_chat_text:
                                i_title = "🏛Full Headquarters Map"
                                i_text = 'All known <b>Headquarters:</b>'
                                for dots in alliance:
                                    if alliance[dots]["status"]!='inactive':
                                        acv_msg = '/deactivate_'+dots
                                    else:
                                        acv_msg = '/activate_'+dots
                                    i_text+='\n\n📍<b>'+alliance[dots]["name"]+'</b> <code>'+dots+'</code> \n<b>'+str(alliance[dots]["status"])+'</b>'+acv_msg
                                if i_text == 'All known <b>Headquarters:</b>':
                                    i_text = i_text+'\n\n<i>[no data yet]</i>'
                                desc = 'List of all headquarters'
                                resultis.append({"type": "article", "id": str(resultoffset[0]), "title": i_title, "input_message_content": {"message_text": i_text, "parse_mode": "HTML"}, "description": desc})
                                resultoffset[0] = resultoffset[0]+1
                                i_title = "🏛Active Headquarters Map"
                                i_text = 'The Active Alliances <b>Headquarters:</b>'
                                for dots in alliance:
                                    if alliance[dots]["status"]!='inactive':
                                        i_text = i_text+'\n\n📍<b>'+alliance[dots]["name"]+'</b> \nCode: <code>'+dots+'</code> \nStatus: <b>'+str(alliance[dots]["status"])+'</b> \n/deactivate_'+dots
                                if i_text == 'The Active Alliances <b>Headquarters:</b>':
                                    i_text = i_text+'\n\n<i>[no data yet]</i>'
                                desc = 'List of current active alliances headquarters'
                                resultis.append({"type": "article", "id": str(resultoffset[0]), "title": i_title, "input_message_content": {"message_text": i_text, "parse_mode": "HTML"}, "description": desc})
                                resultoffset[0] = resultoffset[0]+1
                        for places in locations:
                            if i_chat_text in locations[places]['name'] and i_chat_text!='' and len(i_chat_text)>=3 and locations[places]['status']=='active':
                                desc = '⚔️Issue the order to attack '+locations[places]['name']
                                resultis.append({"type": "article", "id": str(resultoffset[0]), "title": '⚔️'+locations[places]['name'], "input_message_content": {"message_text": '/ga_atk_'+places, "parse_mode": "HTML"}, "description": desc})
                                resultoffset[0] = resultoffset[0]+1
                                desc = '🛡Issue the order to defend '+locations[places]['name']
                                resultis.append({"type": "article", "id": str(resultoffset[0]), "title": '🛡'+locations[places]['name'], "input_message_content": {"message_text": '/ga_def_'+places, "parse_mode": "HTML"}, "description": desc})
                                resultoffset[0] = resultoffset[0]+1
                        for places in alliance:
                            if i_chat_text in alliance[places]['name'] and i_chat_text!='' and len(i_chat_text)>=3 and alliance[places]['status']=='active':
                                desc = '⚔️Issue the order to attack '+alliance[places]['name']
                                resultis.append({"type": "article", "id": str(resultoffset[0]), "title": '⚔️'+places, "input_message_content": {"message_text": '/ga_atk_'+places, "parse_mode": "HTML"}, "description": desc})
                                resultoffset[0] = resultoffset[0]+1
                        ccordersbot.answer_inline_query(resultis, i_query_id)
                    if nonononoiwant==True:
                        i_title = '❓Inline Help'
                        desc = 'Press here if you need help.'
                        i_text = 'Hello! I\'m the Citadel\'s <b>order bot</b>. \n\nWhen you forward an order to @chtwrsbot, there will be a secret code xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx behind the inline query. Then an order button will pop up. \n\nHowever, if the order is expired, then a 🗺Not found location will pop up. \n\nYou need to press the order button and you will successfully send the order. \n\nFor more information, take a look at <a href="https://t.me/complexcitadelnews/213">this guide</a>.'
                        resultis.append({"type": "article", "id": str(resultoffset[0]), "title": i_title, "input_message_content": {"message_text": i_text, "parse_mode": "HTML"}, "description": desc})
                        resultoffset[0] = resultoffset[0]+1
                        ccordersbot.answer_inline_query(resultis, i_query_id)
                    resultis.clear()
                clearance_two = not (clearance.guild(first_chat_id)=='' and commanderlist.count(first_chat_id)==0 and commanderlist.count(sender_id)==0)
                if 'То remember the route you associated it with simple combination' in first_chat_text and iscwbot == True:
                    if current_update['message']['forward_date']<int(time.time())-86400 and 'lvl.' in first_chat_text:
                        ccordersbot.delete_message(first_chat_id, first_msg_id)
                        resp = ccordersbot.send_message(first_chat_id, 'Looks like an old location, please send hidden locations within 24 hours they\'re found next time.')
                        msg_id_by_bot = int(json.loads(resp.text)["result"]["message_id"])
                        await asyncio.sleep(3)
                        ccordersbot.delete_message(first_chat_id, msg_id_by_bot)
                        return
                    both = first_chat_text.split('\nТо remember the route you associated it with simple combination: ')
                    if 'hidden headquarter' in both[0]:
                        office = both[0].replace('You found hidden headquarter ', '')
                    else:
                        office = both[0].replace('You found hidden location ', '')
                    if 'You noticed' in office:
                        office = office.split('\nYou noticed')[0]
                    repeat = False
                    if both[1] in locations or both[1] in alliance:
                        repeat = True
                    if repeat == False:
                        if 'lvl.' in office:
                            typee = gettype(office)
                        else:
                            typee = 'hq'
                        if office in locations:
                            botdb.change_info("LOCATIONS", "CODE", both[1], "NAME", office)
                        elif typee!='hq':
                            botdb.add_location(office, both[1], 'active', typee, '0', '-', '')
                            locations[both[1]] = {'name': office, 'status': 'active', 'type': typee, 'age': 0, 'owner': '-', 'dump': ''}
                        elif office not in alliance:
                            botdb.add_hq(office, both[1], 'active', '100,100,100', '')
                            alliance[both[1]] = {'name': office, 'status': 'active', 'power': '100,100,100', 'dump': ''}
                        for abccu in commanderlist:
                            ccordersbot.send_message(abccu, '<b>New 📍 found:</b> \n'+office+' \n<a href="tg://user?id='+str(sender_id)+'">From</a>\n<b>Code:</b> '+both[1])
                        if isgrp == True:
                            ccordersbot.delete_message(first_chat_id, first_msg_id)
                            resp = ccordersbot.send_message(first_chat_id, 'Thank you for that location. \n<b>'+office+'</b>')
                            msg_id_by_bot = int(json.loads(resp.text)["result"]["message_id"])
                            await asyncio.sleep(3)
                            ccordersbot.delete_message(first_chat_id, msg_id_by_bot)
                        else:
                            ccordersbot.send_message(first_chat_id, 'Thank you for that location. \n<b>'+office+'</b>')
                    else:
                        if isgrp == True:
                            ccordersbot.delete_message(first_chat_id, first_msg_id)
                            resp = ccordersbot.send_message(first_chat_id, 'We already got <b>'+office+'</b>, but thank you (<b>please send more locations!!!</b>).')
                            msg_id_by_bot = int(json.loads(resp.text)["result"]["message_id"])
                            await asyncio.sleep(3)
                            ccordersbot.delete_message(first_chat_id, msg_id_by_bot)
                        else:
                            ccordersbot.send_message(first_chat_id, 'We already got <b>'+office+'</b>, but thank you.')
                elif 'Your result on the battlefield:' in first_chat_text and iscwbot==True and '👾Encounter' not in first_chat_text:
                    old_report = False
                    if current_update['message']['forward_date']<int(time.time())-600:
                        message_to_send = 'Looks old, please send reports within 10 minute next time.'
                        old_report = True
                    else:
                        message_to_send = 'Thanks for your report! '
                    lencheck = first_chat_text.split('[')
                    if len(lencheck)>=2 and old_report!=True:
                        lencheckk = lencheck[1].split(']')
                        lencheckkk = lencheckk[1].split(' ⚔️:')
                        if len(lencheckkk)==1:
                            lencheckkk = lencheckk[1].split(' ⚔:')
                        lencheckkkk = lencheckkk[1].split(' 🛡:')
                        lencheckkkkk = lencheckkkk[1].split(' Lvl: ')
                        lencheckkkkkk = lencheckkkkk[1].split('\nYour result on the battlefield:\n')
                        if [a for a in members if members[a]['id']==sender_id]==[]:
                            for b in members:
                                if lencheckkk[0]==members[b]['ign']:
                                    members[b]['id'] = sender_id
                                    botdb.change_info("MEMBERS", "DUMP", sender_id, "IGN", lencheckkk[0])
                                    message_to_send+=' saved your name btw '
                        exp_no = -1
                        stock_no = 0
                        gold_no = 0
                        hp_no = 0
                        for x in lencheckkkkkk[1].split('\n'):
                            if 'Gold' in x:
                                gold_no = int(x.split('Gold: ')[1])
                            elif 'Stock' in x:
                                stock_no = int(x.split('Stock: ')[1])
                            elif 'Hp' in x:
                                hp_no = int(x.split('Hp: ')[1])
                            elif 'Exp' in x:
                                exp_no = int(x.split('Exp: ')[1])
                        if int(gold_no)>0 or int(stock_no)>0 or exp_no<0:
                            if first_chat_id==sender_id:
                                message_to_send += 'But that does not seem like the alliance one🤔'
                                ccordersbot.send_message(first_chat_id, message_to_send)
                            return
                        if exp_no==1:
                            message_to_send = message_to_send+'🙇‍♂️Sorry for the wall (if any), we will do better next time!!'
                        reports[sender_id] = {'tag': lencheckk[0], 'ign': lencheckkk[0], 'att': lencheckkkk[0], 'def': lencheckkkkk[0], 'lvl': lencheckkkkkk[0], 'exp': exp_no, 'hp': hp_no}
                    elif old_report==True:
                        print('old report')
                    else:
                        message_to_send=''
                    if message_to_send!='':
                        resp = ccordersbot.send_message(first_chat_id, message_to_send)
                        msg_id_by_bot = int(json.loads(resp.text)["result"]["message_id"])
                        await asyncio.sleep(30)
                        ccordersbot.delete_message(first_chat_id, first_msg_id)
                        ccordersbot.delete_message(first_chat_id, msg_id_by_bot)
                elif clearance.guild(first_chat_id)==False and isgrp==False:
                    ccordersbot.send_message(first_chat_id, 'Send me your /report 🌝')
                    ccordersbot.send_message(-1001175100654, 'Suspicious new person pm-ed me: '+str(first_chat_id)+' sender: '+str(sender_id))
                elif first_chat_text=='/help' and clearance_two==False and isgrp==False:
                    ccordersbot.send_message(first_chat_id, '<b>Commands:</b>\n/orders')
                elif clearance_two==False and isgrp==False:
                    serial_no = clearance.guild(first_chat_id)
                    ccordersbot.send_message(first_chat_id, 'How may I help you today, ['+members[serial_no]['guild']+']'+members[serial_no]['ign']+'?🤵')
                    return
                elif False:#'🤝 Your alliance.\n🥔⛰Complex Citadel' in first_chat_text and iscwbot==True and commanderlist.count(first_chat_id)!=0:
                    if yeodet[0]==0:
                        if current_update['message']['forward_date']>= int(time.time())-120:
                            ccordersbot.send_message(first_chat_id, 'Thank you for updating alliance map with me. \n<b>Next! Send me the Alliance Menu</b>, something like: \n🤝Complex Citadel \nGuilds: 11 👥168\nOwner: 🥔[BTW]Smartatos\nObjectives: 2\nState: Active\nBalance:\n    👝547 💰53 \n    📦Stock: 705\n    🎖Glory: 0')
                            first_chat_text = first_chat_text.split('\n')
                            for removespaces in first_chat_text:
                                if removespaces=='':
                                    first_chat_text.remove('')
                            if len(first_chat_text)>=4:
                                poincomp = {}
                                for difhing in first_chat_text:
                                    if first_chat_text.index(difhing) in [1, 2, 0]:
                                        continue
                                    office = difhing
                                    typee = gettype(office)
                                    if typee=='unknown':
                                        continue
                                    else:
                                        poin=0
                                        infoneed = first_chat_text[(first_chat_text.index(difhing))+1]
                                        code=infoneed.split('Code: ')[1].replace('.', '')
                                        state=infoneed.split('.')[0].replace('State: ', '')
                                        lvlpsr = first_chat_text[first_chat_text.index(difhing)].split('lvl.')[1]
                                        lvlpsr = int(lvlpsr)
                                        if lvlpsr>=20 and lvlpsr<=39:
                                            tlv = 1
                                        elif lvlpsr>=40 and lvlpsr<=59:
                                            tlv = 2
                                        elif lvlpsr>=60 and lvlpsr<=79:
                                            tlv = 3
                                        if 'Ruins' in typee:
                                            poin = poin+12
                                        elif 'Glory' in typee:
                                            if 'T1' in typee:
                                                poin = poin+3
                                            elif 'T2' in typee:
                                                poin = poin+4
                                            elif 'T3' in typee:
                                                poin = poin+6
                                            try:
                                                targpi = first_chat_text[(first_chat_text.index(difhing))+3]
                                            except:
                                                targpi = 'nice'
                                            if 'Attractions' in targpi:
                                                poin=poin+3
                                        elif 'Mine' in typee:
                                            typ1 = first_chat_text[(first_chat_text.index(difhing))+2]
                                            typ2 = first_chat_text[(first_chat_text.index(difhing))+3]
                                            for botyps in [typ1, typ2]:
                                                if 'Magic stone' in botyps and '0.00%' not in botyps:
                                                    if 'T1' in typee:
                                                        poin = poin+3
                                                    elif 'T2' in typee:
                                                        poin = poin+4
                                                    elif 'T3' in typee:
                                                        poin = poin+7
                                                else:
                                                    if 'T1' in typee:
                                                        poin = poin+1
                                                    elif 'T2' in typee:
                                                        poin = poin+1
                                                    elif 'T3' in typee:
                                                        poin = poin+2
                                            try:
                                                targpi = first_chat_text[(first_chat_text.index(difhing))+4]
                                            except:
                                                targpi = 'nice'
                                            if 'Attractions:' in targpi:
                                                poin = poin +3
                                        poincomp[code] = {"range": tlv, "points": poin, "type": typee, "state": state}
                                waitinglist.append(first_chat_id)
                                chat.append('caos')
                        else:
                            ccordersbot.send_message(first_chat_id, 'Alliance Map must be sent within 2 mins after cwbot sends it to avoid confusion, try again')
                    else:
                        ccordersbot.send_message(first_chat_id, 'Somebody already updated alliance map with me, but thank you.')
                elif False: #first_chat_id in waitinglist and '/cancel' not in first_chat_text:
                    theindex = waitinglist.index(first_chat_id)
                    if '\nOwner: 🥔[BTW]Smartatos\nObjectives:' in first_chat_text and iscwbot==True and chat[theindex]=='caos':
                        poin=0
                        first_chat_text = first_chat_text.split('\n')
                        glptts = int(first_chat_text[8].split('Glory: ')[1])
                        stockpe = int(first_chat_text[7].split('Stock: ')[1])
                        if glptts !=0:
                            poin = poin+(glptts//100)
                        if stockpe !=0:
                            poin = poin+1
                        for difend in poincomp:
                            if poincomp[difend]['state']=='preparing':
                                continue
                            typee = poincomp[difend]['type']
                            tier = poincomp[difend]['range']
                            if 'Ruin' in typee:
                                poin = poin + (tier*50)
                        poincomp['KMDwuF'] = {"range": [1, 2, 3], "points": poin}
                        del(chat[theindex])
                        del(waitinglist[theindex])
                        yeodet[0] = 2
                        try:
                            cursor.execute("SELECT * FROM GUILD")
                        except:
                            ccordersbot.send_message(first_chat_id, 'Lost connection to mySQL, reconnecting...')
                            mysqlconnect()
                            try:
                                cursor.execute("SELECT * FROM GUILD")
                            except:
                                ccordersbot.send_message(first_chat_id, 'Can\'t connect.')
                                return
                        result = cursor.fetchall()
                        guildyay = {}
                        for dy in result:
                            guildyay[dy[0]] = {'grpid': int(dy[1]), 'pinmsgid': pinrem[chtgrps.index(int(dy[1]))]+1}
                        print(guildyay)
                        for sgflyer in guildyay:
                            if sgflyer=='CCT' or sgflyer=='SIX' or sgflyer=='GS':
                                continue
                            order = []
                            notice = ''
                            for tiars in [1, 2, 3]:
                                if tiars==3:
                                    thixt = "Lvl.60+ "
                                elif tiars==2:
                                    thixt = "Lvl.40-59 "
                                elif tiars==1:
                                    thixt = "Lvl.20-39 "
                                diffcator = 0
                                whatthechances = {}
                                for charders in poincomp:
                                    try:
                                        corrnot = tiars not in poincomp[charders]['range']
                                    except:
                                        corrnot = poincomp[charders]['range']!=tiars
                                    if corrnot:
                                        continue
                                    whatthechances[charders] = poincomp[charders]['points']+diffcator
                                    diffcator = diffcator+poincomp[charders]['points']
                                if len(whatthechances)!=0:
                                    whatissithe = random.randint(0, diffcator)
                                    calsake = []
                                    for chcalc in whatthechances:
                                        if whatthechances[chcalc]-whatissithe<0:
                                            continue
                                        calsake.append(whatthechances[chcalc])
                                    idealpt = min(calsake)
                                    for chcalc in whatthechances:
                                        if whatthechances[chcalc]!=idealpt:
                                            continue
                                        thecdiw = chcalc
                                    uniqueorder = str(uuid.uuid4())
                                    if diffcator>=15:
                                        importanceind = '❗️'
                                    else:
                                        importanceind = ''
                                    row = [{"text": thixt+importanceind, "switch_inline_query": uniqueorder}]
                                    ordereader[uniqueorder] = {}
                                    ordereader[uniqueorder]['link'] = '/ga_def_'+thecdiw
                                    ordereader[uniqueorder]['guild'] = sgflyer
                                    order.append(row)
                                else:
                                    notice = notice+'\n'+thixt+'can go attend castle war'
                            grpppid = guildyay[sgflyer]['grpid']
                            threspppp = ccordersbot.inline_keyboard_markup(grpppid, '<b>'+sgflyer+'</b> \nThe orders are as follows, click on the button to forward order directly to @chtwrsbot. \n<b>Only press the button that suits your level.</b> \n<a href="https://t.me/complexcitadelnews/237">Generated by Citadel Orders</a> \n'+notice+'\n\n'+footers[0], order, first_chat_id)
                            if guildyay[sgflyer]['pinmsgid']!=1 and pinning[0]==True and doipinornot[0] == True:
                                ccordersbot.pin_chat_message(grpppid, int(threspppp.text.split('"message_id":')[1].split(',')[0]), False)
                            else:
                                print('cannot907')
                elif iscwbot==True:
                    if current_update['message']['forward_date']<int(time.time())-600:
                        old_msg=True
                    else:
                        old_msg=False
                    g_tag = ''
                    for x in guild_info:
                        if sender_id==guild_info[x]['leader'] or first_chat_id==x:
                            g_tag = guild_info[x]['tag']
                    if g_tag=='':
                        return
                    if '#' in first_chat_text and '[' in first_chat_text:
                        if old_msg==True:
                            ccordersbot.send_message(first_chat_id, 'rejected, please send guild roster within 10 mins')
                            return
                        reply_msg = ''
                        list_of_removals = []
                        top_member_no = 0
                        for x in members:
                            if x>top_member_no:
                                top_member_no = x
                            if members[x]['guild']==g_tag:
                                list_of_removals.append(x)
                        temporary_id_dict = {}
                        for x in list_of_removals:
                            reply_msg = reply_msg+'\n- Removed info member#'+str(x)+' ign: '+str(members[x]['ign'])
                            botdb.delete_info("MEMBERS", "SNO", x)
                            temporary_id_dict[members[x]['ign']+str(members[x]['lvl'])] = members[x]['id']
                            members.pop(x)
                        allppl = first_chat_text.split('\n')
                        for player in allppl:
                            if '#' not in player:
                                continue
                            char = re.findall("[0-9]", player.split(' ')[1].split(' ')[0])
                            level_of_player = ''
                            for x in char:
                                level_of_player = level_of_player+x
                            level_of_player = int(level_of_player)
                            ign = player.split('] ')[1]
                            if ign+str(level_of_player) not in temporary_id_dict:
                                idd = '0'
                            else:
                                idd = temporary_id_dict[ign+str(level_of_player)]
                            if list_of_removals!=[]:
                                members[list_of_removals[0]] = {'ign': ign, 'atk': 0, 'def': 0, 'lvl': level_of_player, 'id': int(idd), 'guild': g_tag}
                                reply_msg = reply_msg+'\n- Added info member#'+str(list_of_removals[0])+' ign: '+str(ign)
                                botdb.comm("INSERT INTO MEMBERS VALUES ('"+str(list_of_removals[0])+"', '"+ign+"', '0', '0', '"+str(level_of_player)+"', '"+str(idd)+"', '"+g_tag+"')", 'insert into members new values')
                                del(list_of_removals[0])
                            else:
                                top_member_no = top_member_no+1
                                members[top_member_no] = {'ign': ign, 'atk': 0, 'def': 0, 'lvl': level_of_player, 'id': idd, 'guild': g_tag}
                                reply_msg = reply_msg+'\n- Added info member#'+str(top_member_no)+' ign: '+str(ign)
                                botdb.comm("INSERT INTO MEMBERS VALUES ('"+str(top_member_no)+"', '"+ign+"', '0', '0', '"+str(level_of_player)+"', '"+str(idd)+"', '"+g_tag+"')", 'insert into members new values')
                        if list_of_removals!=[]:
                            for x in list_of_removals:
                                for k in range(x+1, len(members)):
                                    try:
                                        botdb.change_info("MEMBERS", "SNO", k-1, "SNO", k)
                                        members[k-1] = {'ign': members[k]['ign'], 'atk': members[k]['atk'], 'def': members[k]['def'], 'lvl': members[k]['lvl'], 'id': members[k]['id'], 'guild': members[k]['guild']}
                                    except:
                                        print('problem with dummy?')
                        ccordersbot.send_message(first_chat_id, reply_msg+'\n\n--Finished-- \n\nFinish updating /g_atklist and /g_deflist (forward <b>both</b> to me)')
                    elif 'Attack Rating' in first_chat_text:
                        if old_msg==True:
                            ccordersbot.send_message(first_chat_id, 'rejected, please send attack rating roster within 10 mins')
                            return
                        reply_msg = ''
                        allppl = first_chat_text.split('\n')
                        for player in allppl:
                            if '#' not in player:
                                continue
                            char = re.findall("[0-9]", player.split(' ')[1])
                            level_of_player = ''
                            for x in char:
                                level_of_player = level_of_player+x
                            level_of_player = int(level_of_player)
                            ign = player.split(str(level_of_player)+' ')[1]
                            change_info = ''
                            for x in members:
                                if members[x]['ign']==ign:
                                    change_info = x
                            if change_info!='':
                                members[change_info] = {'ign': ign, 'atk': level_of_player, 'def': members[change_info]['def'], 'lvl': members[change_info]['lvl'], 'id': members[change_info]['id'], 'guild': g_tag}
                                botdb.change_info("MEMBERS", "ATK", level_of_player, "SNO", change_info)
                                reply_msg = reply_msg+'\n- Updated info member#'+str(change_info)+' ign: '+str(ign)
                            else:
                                reply_msg = reply_msg+'\n- <b>Error:</b> ign: '+str(ign)+' not in members list\nPlease update guild roster with me first'
                                continue
                        ccordersbot.send_message(first_chat_id, reply_msg+'\n\n--Finished--')
                    elif 'Defence Rating' in first_chat_text:
                        if old_msg==True:
                            ccordersbot.send_message(first_chat_id, 'rejected, please send defence rating roster within 10 mins')
                            return
                        reply_msg = ''
                        allppl = first_chat_text.split('\n')
                        for player in allppl:
                            if '#' not in player:
                                continue
                            char = re.findall("[0-9]", player.split(' ')[1])
                            level_of_player = ''
                            for x in char:
                                level_of_player = level_of_player+x
                            level_of_player = int(level_of_player)
                            ign = player.split(str(level_of_player)+' ')[1]
                            change_info = ''
                            for x in members:
                                if members[x]['ign']==ign:
                                    change_info = x
                            if change_info!='':
                                members[change_info] = {'ign': ign, 'atk': members[change_info]['atk'], 'def': level_of_player, 'lvl': members[change_info]['lvl'], 'id': members[change_info]['id'], 'guild': g_tag}
                                botdb.change_info("MEMBERS", "DEF", level_of_player, "SNO", change_info)
                                reply_msg = reply_msg+'\n- Updated info member#'+str(change_info)+' ign: '+str(ign)
                            else:
                                reply_msg = reply_msg+'\n- <b>Error:</b> ign: '+str(ign)+' not in members list\nPlease update guild roster with me first'
                                continue
                        ccordersbot.send_message(first_chat_id, reply_msg+'\n\n--Finished--')
                    elif '📋Roster:' in first_chat_text:
                        if old_msg==True:
                            ccordersbot.send_message(first_chat_id, 'rejected, please send alliance roster within 10 mins')
                            return
                        reply_msg = ''
                        is_existing_guild = ['X', 'C']
                        consta = 0
                        for x in first_chat_text.replace("📋Roster:\n", '').split('\n'):
                            g_tag_p = x.split('[')[1].split(']')[0]
                            if g_tag_p in guild_info:
                                reply_msg = reply_msg+'\n- Found '+g_tag_p+', skipping'
                                for y in guild_info:
                                    if y==g_tag_p:
                                        is_existing_guild.append(y)
                                continue
                            reply_msg = reply_msg+'\n- New guild inserted: '+g_tag_p+', finish setup: \nLeader: /gs_'+g_tag_p+'_l_{id} \nChat: /gs_'+g_tag_p+'_cht_{id} \noptional (req. additional perm.s):\n /gs_'+g_tag_p+'_cdt_{id} /gs_'+g_tag_p+'_o{0|1|2}_{y|n} /gs_'+g_tag_p+'_adm_{id}'
                            guild_info[consta] = {'tag': g_tag_p, 'leader': 0, 'credit': 100, 'settings': 'y y y x'}
                            botdb.add_guild(g_tag_p, consta, 0, 100, 'y y y x')
                            for y in guild_info:
                                if y==g_tag_p:
                                    is_existing_guild.append(y)
                            consta = consta+1
                        to_pop_guild = []
                        for x in guild_info:
                            if guild_info[x]['tag'] not in is_existing_guild:
                                botdb.delete_info("GUILD", "TAG", guild_info[x]['tag'])
                                to_pop_guild.append(x)
                                reply_msg = reply_msg+'\n- Deleted '+guild_info[x]['tag']+'.'
                        for x in to_pop_guild:
                            guild_info.pop(x)
                        ccordersbot.send_message(first_chat_id, reply_msg+'\n\n--Finished--')
                elif '/g_add_' in first_chat_text:
                    first_chat_text = first_chat_text.split('_')
                    try:
                        if first_chat_text[3] in guild_info:
                            ccordersbot.send_message(first_chat_id, 'Rejected, Reason: Overlapping guild chat '+str(first_chat_text[3]))
                            return
                        for x in guild_info:
                            if first_chat_text[2] in guild_info[x]['tag'] and first_chat_text[2]!='X':
                                ccordersbot.send_message(first_chat_id, 'Rejected, Reason: Guild '+str(first_chat_text[2])+' already exist')
                                return
                        botdb.add_guild(first_chat_text[2], first_chat_text[3], first_chat_text[4], 100, 'y y y x')
                        ccordersbot.send_message(first_chat_id, 'New guild inserted: '+first_chat_text[2]+', finish setup: \nLeader: /gs_'+first_chat_text[2]+'_l_{id} ('+str(first_chat_text[4])+') \nChat: /gs_'+first_chat_text[2]+'_cht_{id} ('+first_chat_text[3]+') \noptional (req. additional perm.s):\n /gs_'+first_chat_text[2]+'_cdt_{id} /gs_'+first_chat_text[2]+'_o{0|1|2}_{y|n} /gs_'+first_chat_text[2]+'_adm_{id}')
                        guild_info[int(first_chat_text[3])] = {'tag': first_chat_text[2], 'leader': int(first_chat_text[4]), 'credit': 100, 'settings': 'y y y x'}
                    except:
                        ccordersbot.send_message(first_chat_id, 'Usage: /g_add_tag_id_leader')
                elif '/g_del_' in first_chat_text:
                    try:
                        botdb.remove_info('GUILD', 'CHAT', first_chat_text[2])
                        guild_info.pop(int(first_chat_text[2]))
                        ccordersbot.send_message(first_chat_id, 'Removed '+first_chat_text[2])
                    except:
                        ccordersbot.send_message(first_chat_id, 'Usage: /g_del_id')
                elif '/gs_' in first_chat_text:
                    set_var = first_chat_text.split('_')
                    existence_of_guild = False
                    for x in guild_info:
                        if set_var[1]==guild_info[x]['tag']:
                            guild_chat_for_process = x
                            existence_of_guild = True
                    if existence_of_guild==False:
                        ccordersbot.send_message(first_chat_id, set_var[1]+' guild does not exist')
                        return
                    try:
                        cht_id_for_gset = int(float(set_var[3]))
                    except:
                        if set_var[3] not in ['y', 'n']:
                            ccordersbot.send_message(first_chat_id, 'id: '+set_var[3]+' in bad format')
                            return
                    if set_var[2]=='l':
                        guild_info[guild_chat_for_process]['leader']=cht_id_for_gset
                        botdb.change_info("GUILD", "LEADER", cht_id_for_gset, "TAG", set_var[1])
                    elif set_var[2]=='cht':
                        guild_info[cht_id_for_gset] = guild_info[guild_chat_for_process]
                        guild_info.pop(guild_chat_for_process)
                        botdb.change_info("GUILD", "CHAT", cht_id_for_gset, "TAG", set_var[1])
                    elif set_var[2]=='cdt':
                        guild_info[guild_chat_for_process]['credit']=cht_id_for_gset
                        botdb.change_info("GUILD", "CREDIT", cht_id_for_gset, "TAG", set_var[1])
                    elif set_var[2]=='adm':
                        new_settings = guild_info[set_var[1]]['settings']+cht_id_for_gset+','
                        guild_info[guild_chat_for_process]['settings']=new_settings
                        botdb.change_info("GUILD", "SETTINGS", new_settings, "TAG", set_var[1])
                    elif 'o' in set_var[2]:
                        settings_var = int(set_var[2].replace('o'))
                        guild_setting = guild_info[guild_chat_for_process]['settings'].split(' ')
                        try:
                            guild_setting[settings_var]=set_var[3]
                        except:
                            ccordersbot.send_message(first_chat_id, 'only o{0|1|2} allowed')
                            return
                        new_settings = ''
                        for x in guild_setting:
                            new_settings = new_settings+x
                        guild_info[guild_chat_for_process]['settings']=new_settings
                        botdb.change_info("GUILD", "SETTINGS", new_settings, "TAG", set_var[1])
                    ccordersbot.send_message(first_chat_id, 'ok')
                elif '/msg' in first_chat_text:
                    msg_variables = first_chat_text.split('_')
                    try:
                        guild_exis = False
                        cht_idd = []
                        if '-' in msg_variables[1]:
                            if int(msg_variables[1]) in guild_info:
                                cht_idd =[int(msg_variables[1])]
                                guild_exis = True
                        else:
                            for x in guild_info:
                                if guild_info[x]['tag'] in msg_variables[1]:
                                    cht_idd.append(x)
                                    guild_exis = True
                        if guild_exis==True:
                            for a in cht_idd:
                                raw_message = first_chat_text.replace('/msg_'+msg_variables[1]+'_', '')
                                raw_message = raw_message.replace('</', 'TempOrarY')
                                new_message = ''
                                cmd_still_exist=True
                                specifi_msg = True
                                while cmd_still_exist==True:
                                    try:
                                        cmd_now = '/'+raw_message.split('/')[1].split('\n')[0].split(' ')[0]
                                        print(cmd_now)
                                    except:
                                        print('error cmd_now')
                                        specifi_msg = False
                                    if specifi_msg==True:
                                        new_message = new_message + raw_message.split(cmd_now)[0]
                                        new_message = new_message +'<a href="t.me/share/url?url='+cmd_now+'">'+cmd_now+'</a>'
                                    else:
                                        new_message = new_message + raw_message
                                    try:
                                        raw_message_part_i = raw_message.split(cmd_now)[1]
                                        raw_message=raw_message_part_i+raw_message.split(raw_message_part_i)[1]
                                    except:
                                        break
                                new_message = new_message.replace('TempOrarY', '</').replace('1 exp', '/hail_Citadel').replace('1exp', '/hail_Citadel').replace('1xp', '/hail_Citadel')
                                print(new_message)
                                ccordersbot.send_message(a, new_message, return_id=sender_id)
                        else:
                            ccordersbot.send_message(first_chat_id, 'No such guild/chat ('+msg_variables[1]+') exist in Complex Citadel')
                    except:
                        ccordersbot.send_message(first_chat_id, '<b>Usage:</b> /msg_{TAG/ID}_{message}\nAvailable Tag/chatIDs: '+', '.join([guild_info[x]['tag']+'/'+str(x) for x in guild_info])+'\nExample: /msg_BTW LR AYY_Hello!!')
                elif '/whois' in first_chat_text:
                    try:
                        space_split = first_chat_text.split(' ')
                        if len(space_split)==1:
                            space_split = space_split.split('_')
                        extra_info = ''
                        for x in members:
                            if int(space_split[1])==members[x]['id']:
                                extra_info = '\nFound a record in members list: '+str(members[x])
                        ccordersbot.send_message(first_chat_id, '👤<a href="tg://user?id='+space_split[1]+'">'+space_split[1]+'</a>'+extra_info)
                    except:
                        ccordersbot.send_message(first_chat_id, '<b>Usage:</b> /whois {chatID}')
                elif first_chat_text=='/help':
                    ccordersbot.send_message(first_chat_id, '<b>Commands:</b>\n/members\n/reports\n/whois {chatID}\n/msg_{TAG/ID}_{message}\nAvailable Tag/chatIDs: '+str([guild_info[x]['tag']+': '+str(x) for x in guild_info])+'\nExample: /msg_BTW LR AYY_Hello!!\n\nGuild leaders:\n/g_add_tag_id_leader\n/g_del_id\n\nLocations management:\n/activate_{code}\n/deactivate_{code}\n/delete_{code}\n\nServer Data:\n/cpu\n/dbrefresh\n\nBan spys:\n/ban_{chat_id}')
                elif '/reports' in first_chat_text:
                    mess_to_send='<b>Reports for last battle:</b>'
                    const_of_lvl = {'ign':9, 'att':5, 'def':5, 'tag':4}
                    for a in [20, 40, 60]:
                        mess_to_send+='\n\n<b>Lvl.'+str(a)+'-'+str(a+19)+':</b>\n<code>Lv|Name     |Atk  |Def  |Tag</code>'
                        total_people=0
                        total_exp=0
                        total_hp=0
                        for x in reports:
                            if int(reports[x]['lvl'])>=a and int(reports[x]['lvl'])<a+20:
                                total_people+=1
                                processed_values = {}
                                for c in const_of_lvl:
                                    processed_values[c] = ''.join([k for k in reports[x][c] if reports[x][c].index(k) <const_of_lvl[c]])
                                    if len(processed_values[c])<const_of_lvl[c]:
                                        processed_values[c]+=(' '*(const_of_lvl[c]-len(processed_values[c])))
                                    processed_values[c]+='|'
                                mess_to_send+='\n<code>'+str(reports[x]['lvl'])+'|'+processed_values['ign']+str(processed_values['att'])+str(processed_values['def'])+processed_values['tag']+'</code>'
                                total_exp+=reports[x]['exp']
                                total_hp+=reports[x]['hp']
                        if total_people!=0:
                            mess_to_send+='\nAverage exp: '+str(int(total_exp/total_people))+' hp: '+str(int(total_hp/total_people))
                    ccordersbot.send_message(first_chat_id, mess_to_send)
                elif '/members' in first_chat_text:
                    mess_to_send='<b>👥Members of Complex Citadel:</b>'
                    const_of_lvl = {'id':10, 'atk':4, 'def':4, 'guild':4}
                    for a in [20, 40, 60]:
                        mess_to_send+='\n\n<b>Lvl.'+str(a)+'-'+str(a+19)+':</b>\n<code>Lv|ID        |Atk |Def |Tag</code>'
                        for x in members:
                            if int(members[x]['lvl'])>=a and int(members[x]['lvl'])<a+20:
                                processed_values = {}
                                for c in const_of_lvl:
                                    process_phrase = str(members[x][c])
                                    processed_values[c] = ''.join([k for k in process_phrase if process_phrase.index(k) <const_of_lvl[c]])
                                    if len(processed_values[c])<const_of_lvl[c]:
                                        processed_values[c]+=(' '*(const_of_lvl[c]-len(processed_values[c])))
                                    processed_values[c]+='|'
                                mess_to_send+='\n<code>'+str(members[x]['lvl'])+'|'+processed_values['id']+str(processed_values['atk'])+str(processed_values['def'])+processed_values['guild']+'</code>'
                    ccordersbot.send_message(first_chat_id, mess_to_send)
                elif 'update locations' in first_chat_text and sender_id in [536511250]:
                    resp = ccordersbot.send_message(first_chat_id, 'updating locations.')
                    msg_id_by_bot = int(json.loads(resp.text)["result"]["message_id"])
                    fullstops=1
                    for x in alliance:
                        fullstops = fullstops+1
                        if fullstops>3:
                            fullstops=1
                        ccordersbot.edit_message(first_chat_id, msg_id_by_bot, 'updating locations'+fullstops*'.')
                        ccordersbot.send_message(-1001338303651, alliance[x]['name'])
                        time.sleep(1)
                    for x in locations:
                        fullstops = fullstops+1
                        if fullstops>3:
                            fullstops=1
                        ccordersbot.edit_message(first_chat_id, msg_id_by_bot, 'updating locations'+fullstops*'.')
                        ccordersbot.send_message(-1001338303651, locations[x]['name'])
                        time.sleep(1)
                    ccordersbot.edit_message(first_chat_id, msg_id_by_bot, 'updating locations... done')
                elif '/activate_' in first_chat_text and commanderlist.count(first_chat_id)!=0 and len(first_chat_text)==16:
                    first_chat_text = first_chat_text.replace('/activate_', '')
                    whyisthis = 0
                    for coooo in locations:
                        if coooo == first_chat_text:
                            ccordersbot.send_message(first_chat_id, 'Successfully activated '+coooo+' ('+locations[coooo]['name']+') in database. Have a great day!')
                            botdb.change_info('LOCATIONS', 'STATUS', 'active', 'CODE', coooo)
                            locations[coooo]['status'] = 'active'
                            whyisthis = whyisthis+1
                    for coooo in alliance:
                        if coooo == first_chat_text:
                            ccordersbot.send_message(first_chat_id, 'Successfully deactivated '+coooo+' ('+alliance[coooo]['name']+') in database. Have a great day!')
                            botdb.change_info('ALLIANCES', 'STATUS', 'inactive', 'CODE', coooo)
                            locations[coooo]['status'] = 'inactive'
                            whyisthis = whyisthis+1
                    ccordersbot.send_message(first_chat_id, 'Scan through complete, activated '+str(whyisthis)+' locations. Have a great day!')
                    initialize()
                elif '/deactivate_' in first_chat_text and commanderlist.count(first_chat_id)!=0 and len(first_chat_text)==18:
                    first_chat_text = first_chat_text.replace('/deactivate_', '')
                    whyisthis = 0
                    for coooo in locations:
                        if coooo == first_chat_text:
                            ccordersbot.send_message(first_chat_id, 'Successfully deactivated '+coooo+' ('+locations[coooo]['name']+') in database. Have a great day!')
                            botdb.change_info('LOCATIONS', 'STATUS', 'inactive', 'CODE', coooo)
                            locations[coooo]['status'] = 'inactive'
                            whyisthis = whyisthis+1
                    for coooo in alliance:
                        if coooo == first_chat_text:
                            ccordersbot.send_message(first_chat_id, 'Successfully deactivated '+coooo+' ('+alliance[coooo]['name']+') in database. Have a great day!')
                            botdb.change_info('ALLIANCES', 'STATUS', 'inactive', 'CODE', coooo)
                            alliance[coooo]['status'] = 'inactive'
                            whyisthis = whyisthis+1
                    ccordersbot.send_message(first_chat_id, 'Scan through complete, deactivated '+str(whyisthis)+' locations. Have a great day!')
                    initialize()
                elif '/delete_' in first_chat_text and commanderlist.count(first_chat_id)!=0 and len(first_chat_text)==14:
                    first_chat_text = first_chat_text.replace('/delete_', '')
                    whyisthis = 0
                    for coooo in locations:
                        if coooo == first_chat_text:
                            ccordersbot.send_message(first_chat_id, 'Successfully removed '+coooo+' ('+locations[coooo]['name']+') from database. Have a great day!')
                            botdb.delete_info("LOCATIONS", "CODE", coooo)
                            whyisthis = whyisthis+1
                    for coooo in alliance:
                        if coooo == first_chat_text:
                            ccordersbot.send_message(first_chat_id, 'Successfully removed '+coooo+' ('+alliance[coooo]['name']+') from database. Have a great day!')
                            botdb.delete_info("ALLIANCES", "CODE", coooo)
                            whyisthis = whyisthis+1
                    initialize()
                    ccordersbot.send_message(first_chat_id, 'Scan through complete, removed '+str(whyisthis)+' locations. Have a great day!')
                elif first_chat_id == 536511250 and first_chat_text == '/dbrefresh':
                    try:
                        db_connection.close()
                        mysqlconnect()
                        initialize()
                        ccordersbot.send_message(first_chat_id, 'Refreshed database connection.')
                    except:
                        ccordersbot.send_message(first_chat_id, 'Refresh failed.')
                elif first_chat_text == '/cancel' and commanderlist.count(first_chat_id)>=1:
                    if waitinglist.count(first_chat_id) >=1:
                        theindex = waitinglist.index(first_chat_id)
                        del(chat[theindex])
                        del(waitinglist[theindex])
                        ccordersbot.send_message(first_chat_id, 'Successfully cancelled operation. ')
                    else:
                        ccordersbot.send_message(first_chat_id, 'Nothing going on in the first place, anything wrong?')
                elif '/set_footer ' in first_chat_text and commanderlist.count(first_chat_id) == 1:
                    footers[0] = first_chat_text.replace('/set_footer ', '')
                    ccordersbot.send_message(first_chat_id, 'Successfully changed default order footer to: \n'+footers[0])
                elif '/cmd_promote_' in first_chat_text:
                    if commanderlist.count(first_chat_id)>=1:
                        tgid = first_chat_text.replace('/cmd_promote_', '')
                        if len(tgid) == len(re.findall("[1-9]", tgid)) and len(tgid)!=0:
                            tgid = int(tgid)
                            if banlist.count(tgid) == 1:
                                ccordersbot.send_message(log_channel, 'To '+str(first_chat_id)+': \nError 001: '+str(tgid)+' is on banlist')
                            else:
                                if commanderlist.count(tgid)>=1:
                                    ccordersbot.send_message(log_channel, 'To '+str(first_chat_id)+': \nError 004: '+str(tgid)+' is already on commander list')
                                else:
                                    commanderlist.append(tgid)
                                    try:
                                        ccordersbot.send_message(tgid, 'You have been promoted to commander status, you can now send orders to guilds')
                                    except:
                                        ccordersbot.send_message(log_channel, 'To '+str(first_chat_id)+': \nError 002: '+str(tgid)+' did not start the bot yet/banned the bot')
                        else:
                            ccordersbot.send_message(first_chat_id, 'It ain\'t a number! I want numbers behind /cmd_promote_!')
                    else:
                        ccordersbot.send_message(first_chat_id, 'You ain\'t the supreme commander with all rights, ask @thegr8person to promote you there first')
                elif commanderlist.count(first_chat_id)!=0 and first_chat_text == '/cpu':
                    username = 'mingyu201712'
                    token = 'censored'
                    response = requests.get(
                        'https://www.pythonanywhere.com/api/v0/user/{username}/cpu/'.format(
                            username=username
                        ),
                        headers={'Authorization': 'Token {token}'.format(token=token)}
                    )
                    if response.status_code == 200:
                        ccordersbot.send_message(first_chat_id, 'CPU quota info: \n'+str(response.content))
                    else:
                        ccordersbot.send_message(first_chat_id, 'Got unexpected status code {}: {!r}'.format(response.status_code, response.content))
                elif '/aordertext' in first_chat_text and commanderlist.count(first_chat_id)!=0:
                    first_chat_text = first_chat_text.replace('/aordertext', '')
                    if first_chat_text == '':
                        ccordersbot.send_message(first_chat_id, '<b>Usage:</b> \n/aordertext 2039/4059/6079 ordertext \n\n<code>ANTISPAI</code> ordertexts: \n<b>2039: </b>'+importance[0]+' \n<b>4059: </b>'+importance[1]+' \n<b>6079: </b>'+importance[2])
                    else:
                        first_chat_text = first_chat_text.split(' ')
                        if len(first_chat_text)==2:
                            noes = -1
                            if first_chat_text[0] == '2039':
                                noes = 0
                            elif first_chat_text[0] == '4059':
                                noes = 1
                            elif first_chat_text[0] == '6079':
                                noes = 2
                            if noes!=-1:
                                if first_chat_text[1] =='del':
                                    importance[noes] = ''
                                    ccordersbot.send_message(first_chat_id, 'Successfully deleted ANTISPAI ordertext of <b>'+first_chat_text[0]+'</b>')
                                else:
                                    importance[noes] = first_chat_text[1]
                                    ccordersbot.send_message(first_chat_id, 'Successfully set ANTISPAI ordertext of <b>'+first_chat_text[0]+'</b> to: \n'+first_chat_text[1])
                elif '/cmd_demote_' in first_chat_text:
                    if commanderlist.count(first_chat_id)>=1:
                        tgid = first_chat_text.replace('/cmd_demote_', '')
                        if len(tgid) == len(re.findall("[1-9]", tgid)) and len(tgid)!=0:
                            tgid = int(tgid)
                            if commanderlist.count(tgid)>=1:
                                del(commanderlist[commanderlist.index(tgid)])
                            else:
                                ccordersbot.send_message(first_chat_id, 'To '+str(first_chat_id)+': \nError 003: '+str(tgid)+' ain\'t a commander in the first place')
                                ccordersbot.send_message(-1001175100654, 'To '+str(first_chat_id)+': \nError 003: '+str(tgid)+' ain\'t a commander in the first place')
                        else:
                            ccordersbot.send_message(first_chat_id, 'It ain\'t a number! I want numbers behind /cmd_demote_!')
                    else:
                        ccordersbot.send_message(first_chat_id, 'You ain\'t the supreme commander with all rights, ask @thegr8person to promote you there first')
                elif '/ban_' in first_chat_text and first_chat_id==536511250:
                    if commanderlist.count(first_chat_id)>=1:
                        tgid = first_chat_text.replace('/ban_', '')
                        if len(tgid) == len(re.findall("[1-9]", tgid)) and len(tgid)!=0:
                            tgid = int(tgid)
                            if banlist.count(tgid)>=1:
                                ccordersbot.send_message(first_chat_id, 'To '+str(first_chat_id)+': \nError 003: '+str(tgid)+' is already on banlist')
                                ccordersbot.send_message(-1001175100654, 'To '+str(first_chat_id)+': \nError 003: '+str(tgid)+' is already on banlist')
                            else:
                                banlist.append(tgid)
                                botdb.comm('INSERT INTO BANLIST VALUES ('+str(tgid)+')', "can't insert values to banlist")
                        else:
                            ccordersbot.send_message(first_chat_id, 'It ain\'t a number! I want numbers behind /ban_!')
                    else:
                        ccordersbot.send_message(first_chat_id, 'You ain\'t the supreme commander with all rights, ask @thegr8person to promote you there first')
                elif '/unban_' in first_chat_text:
                    if commanderlist.count(first_chat_id)>=1:
                        tgid = first_chat_text.replace('/unban_', '')
                        if len(tgid) == len(re.findall("[1-9]", tgid)) and len(tgid)!=0:
                            tgid = int(tgid)
                            if banlist.count(tgid)>=1:
                                ccordersbot.send_message(first_chat_id, 'To '+str(first_chat_id)+': \nError 003: '+str(tgid)+' is already on banlist')
                                ccordersbot.send_message(-1001175100654, 'To '+str(first_chat_id)+': \nError 003: '+str(tgid)+' is already on banlist')
                            else:
                                banlist.remove(tgid)
                                botdb.delete_info("BANLIST", "ID", str(tgid))
                        else:
                            ccordersbot.send_message(first_chat_id, 'It ain\'t a number! I want numbers behind /ban_!')
                    else:
                        ccordersbot.send_message(first_chat_id, 'You ain\'t the supreme commander with all rights, ask @thegr8person to promote you there first')
                elif isgrp==False:
                    ccordersbot.send_message(first_chat_id, 'How may I help you today?🤵')
            #except:
            #    ccordersbot.send_message(-1001175100654, 'Problem with current update: '+str(current_update))
            return new_offset


#kafka section... not done

#async def process_kafka_forever(consumer):
    #async for message in consumer:
        #duel = json.loads(message.payload.decode())
        #await handle_duels(duel)

#consumer = Consumer(
    #brokers='digest-api.chtwrs.com:9092',
    #topics=['cw2-duels'],
    #group_id=str(uuid.uuid4()),
#)
#consumer.start()

#async def main():
    #await asyncio.gather(process_kafka_forever(consumer), thandler())

asyncio.run(main())
#if __name__ == '__main__':
#    try:
#        main()
#    except KeyboardInterrupt:
#       exit()
