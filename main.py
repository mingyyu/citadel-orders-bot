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
import datetime
from nltk.chat.eliza import eliza_chatbot
from random_word import RandomWords
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
#from json import loads
#from asynckafka import Consumer

log_channel = -1001175100654

def mysqlconnect():
    print('Trying to connect...')
    global db_connection
    db_connection = None
    try:
        db_connection= MySQLdb.connect(
        "mingyu201712.mysql.pythonanywhere-services.com","mingyu201712","welovedolphins142857","mingyu201712$tgorderbot"
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

    def send_message(self, chat_id, text):
        params = {'chat_id': chat_id, 'text': text, 'parse_mode': 'HTML', "disable_web_page_preview": True}
        method = 'sendMessage'
        resp = requests.post(self.api_url + method, params)
        print('\n'+str(resp.text)+'\n')
        if "parameters" in json.loads(resp.text):
            if 'retry_after' in json.loads(resp.text)["parameters"]:
                time.sleep(int(json.loads(resp.text)["parameters"]['retry_after'])+3)
                resp = ccordersbot.send_message(chat_id, text)
        return resp

    def send_order(self, chat_id, text, **kwargs):
        if chat_id==0:
            return ''
        params = {'chat_id': chat_id, 'text': text, 'parse_mode': 'HTML'}
        method = 'sendMessage'
        resp = requests.post(self.api_url + method, params)
        print('\n'+str(resp.text)+'\n')
        try:
            if chat_id in guild_info:
                tag = guild_info[chat_id]['tag']
            elif chat_id!=-1001354774898:
                tag = str(chat_id)
            else:
                return False
            msg_id_by_bot = int(json.loads(resp.text)["result"]["message_id"])
            ccordersbot.send_message(-1001354774898, '['+str(chat_id)+'] ('+str(msg_id_by_bot)+'): '+text+' '+tag)
            if len(kwargs)!=0:
                ikeyboard = [[{"text": '📌', "callback_data": 'pin_'+str(chat_id)+'_'+str(msg_id_by_bot)}, {"text": '🗑', "callback_data": 'del_'+str(chat_id)+'_'+str(msg_id_by_bot)}]]
                ccordersbot.inline_keyboard_markup(kwargs['return_id'], '✅✉️-->['+tag+'] ('+str(chat_id)+'): \n'+text, ikeyboard, '')
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
            return False
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

    def send_picture(self, chat_id, photo, **kwargs):
        method = 'sendPhoto'
        params = {"chat_id": chat_id, "photo": photo}
        if 'message' in kwargs:
            params["caption"]=kwargs['message']
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

token = '1293724081:AAGtJg6_uzJy9hV7nOCO_z9iFL46Hu-Bs28' #Token of your bot
ccordersbot = BotHandler(token) #Your bot's name

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
                ccordersbot.send_message(-1001175100654, "Error: unable to fetch data for getdbinfo(), credentials: \n"+str(sql)+"\n\n#error")
                results = ''
        return results

    def change_info(self, liste, thing, value, cond, what):
        if cond=='' and what=='':
            sql = "UPDATE "+str(liste)+" SET "+str(thing)+" = '"+str(value)+"'"
        elif isinstance(cond, list)!=True:
            sql = "UPDATE "+str(liste)+" SET "+str(thing)+" = '"+str(value)+"' WHERE "+str(cond)+" = '"+str(what)+"'"
        else:
            sql = "UPDATE "+str(liste)+" SET "+str(thing)+" = '"+str(value)+"' WHERE "+str(cond[0])+" = '"+str(what[0])+"'"
            for x in cond:
                if cond.index(x)!=0:
                    sql+=' AND '+str(x)+" = '"+str(what[cond.index(x)])+"'"
        botdb.comm(sql, 'unable to change data for changedbinfo()')

    def delete_info(self, table, cond, value):
        sql = "DELETE FROM "+str(table)+" WHERE "+str(cond)+" = '"+str(value)+"'"
        botdb.comm(sql, 'unable to delete db row')

    def add_location(self, name, code, status, typeee, age, owner, dump):
        sql = "INSERT INTO LOCATIONS VALUES ('"+str(name)+"', '"+str(code)+"', '"+str(status)+"', '"+str(typeee)+"', '"+str(age)+"', '"+str(owner)+"', '"+str(dump)+"')"
        botdb.comm(sql, 'unable to add location to db')

    def add_battle_result(self, tyype, battlecode, name, result, dump):
        #CREATE TABLE BATTLE (TYPE  INT, NAME  CHAR(35), RESULT  INT, DUMP  CHAR(255), BATTLE  CHAR(25));
        if battlecode not in battle[int(tyype)]:
            battle[int(tyype)][str(battlecode)] = {}
        battle[int(tyype)][str(battlecode)][str(name)] = {"result": int(result), "dump": str(dump)}
        sql = "INSERT INTO BATTLE VALUES ('"+str(tyype)+"', '"+str(name)+"', '"+str(result)+"', '"+str(dump)+"', '"+str(battlecode)+"')"
        botdb.comm(sql, 'unable to add battle result to db')

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
        for x in guild_info:
            if cht_id==guild_info[x]['leader'] or cht_id==x:
                return guild_info[x]['tag']
        return False

    def member(self, cht_id):
        for x in members:
            try:
                if int(cht_id)==members[x]['id']:
                    return x
            except:
                continue
        return False

clearance = SecurityHandler()

class Utilities:
    def link_command(self, raw_message):
        raw_message = raw_message.replace('</', 'TempOrarY').replace('\/', 'tEmpOrAry')
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
        new_message = new_message.replace('TempOrarY', '</').replace('tEmpOrAry', '/')
        print(new_message)
        return new_message

tools = Utilities()

event ={}
runekeeper = {}
spam_cleanup = []

def initialize():
    global members
    global alliance
    global locations
    global guild_info
    global banlist
    global battle
    global unhandled_locations
    global event
    global runekeeper
    global gatop
    global plotcontrol
    global commanderlist
    global trusted
    members = {}
    alliance = {}
    locations = {}
    guild_info = {}
    banlist = []
    offset = {}
    duels = {}
    gatop = {}
    plotcontrol = {}
    trusted = {}
    unhandled_locations = []
    commanderlist = []
    battle = {0: {}, 1: {}}
    result = botdb.get_info('', "EVENT", '', '')
    for x in result:
        event[int(x[0])] = {'runes': int(x[1]), 'points': int(x[2]), 'ign': x[3]}
    result = botdb.get_info('', "RUNEKEEPER", '', '')
    for x in result:
        runekeeper[x[0]] = x[1]
    runekeeper['points']=int(runekeeper['points'])
    runekeeper['hp']=int(runekeeper['hp'])
    result = botdb.get_info('', "MEMBERS", '', '')
    for x in result:
        members[int(x[0])] = {'ign': x[1], 'atk': x[2], 'def': x[3], 'lvl': x[4], 'id': int(x[5]), 'guild': x[6], 'dump': x[7]}
    result = botdb.get_info('', "LOCATIONS", '', '')
    for x in result:
        if x[1]=='%%%%%%':
            unhandled_locations.append({'name': x[0], 'status': x[2], 'type': x[3], 'age': int(x[4]), 'owner': x[5], 'dump': x[6]})
        else:
            locations[x[1]] = {'name': x[0], 'status': x[2], 'type': x[3], 'age': int(x[4]), 'owner': x[5], 'dump': x[6]}
    result = botdb.get_info('', "ALLIANCES", '', '')
    for x in result:
        alliance[x[1]] = {'name': x[0], 'status': x[2], 'power': x[3], 'dump': x[4]}
    result = botdb.get_info('', "GATOP1", '', '')
    for x in result:
        if x[0] not in gatop:
            gatop[x[0]]={}
        gatop[x[0]][x[2]] = str(x[1])
    result = botdb.get_info('', "PLOTCONTROL", '', '')
    for x in result:
        plotcontrol[str(x[0])] = str(x[1])
    result = botdb.get_info('', "GUILD", '', '')
    for x in result:
        guild_info[int(x[1])] = {'tag': x[0], 'leader': int(x[2]), 'credit': int(x[3]), 'settings': str(x[4])}
    print('Locations: '+str(locations))
    result = botdb.get_info('', "DUELS", '', '')
    for x in result:
        duels[int(x[0])] = {'age': int(x[9]), 'winner': {'id': str(x[1]), 'ign': str(x[3]), 'lvl': int(x[5]), 'castle': str(x[7])}, 'loser': {'id': str(x[2]), 'ign': str(x[4]), 'lvl': int(x[6]), 'castle': str(x[8])}}
    result = botdb.get_info('', "BATTLE", '', '')
    for x in result:
        if x[4] not in battle[int(x[0])]:
            battle[int(x[0])][x[4]] = {}
        battle[int(x[0])][x[4]][str(x[1])] = {"result": int(x[2]), "dump": str(x[3])}
    result = botdb.get_info('', "BANLIST", '', '')
    for x in result:
        banlist.append(int(x[0]))
    print('Banlist: '+str(banlist))
    result = botdb.get_info('', "COMMANDERS", '', '')
    for x in result:
        commanderlist.append(int(x[0]))
    print('commanderlist: '+str(commanderlist))
    result = botdb.get_info('', "OFFSET", '', '')
    for x in result:
        offset[x[0]] = int(x[1])

initialize()

reports = {}
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
needtodelete = {}
wire_tap_message = ''
transferdict = {}
default_tactics = 'deerhorn'

poincomp = {}

rword = RandomWords()

class LocManager:
    def age(self, excepts):
        to_pop=[]
        for x in locations:
            if locations[x]['name'] not in excepts and locations[x]['owner']!='Golem Sentinels':
                locations[x]['age']+=1
                if 'life,' in locations[x]['dump']:
                    max_age = int(locations[x]['dump'].split('life,')[1].split(' ')[0])
                    if max_age==locations[x]['age']:
                        ccordersbot.send_message(-1001344525861, '<b>📍'+locations[x]['name']+'</b> <code>'+x+'</code> reached the end of life. It is deleted!')
                        to_pop.append(x)
                        botdb.delete_info("LOCATIONS", "CODE", x)
                        continue
                botdb.change_info("LOCATIONS", "AGE", locations[x]['age'], "CODE", x)
        for x in to_pop:
            locations.pop(x)
        for x in unhandled_locations:
            if x['name'] not in excepts and x['owner']!='Golem Sentinels':
                unhandled_locations[unhandled_locations.index(x)]['age']+=1
                botdb.change_info("LOCATIONS", "AGE", unhandled_locations[unhandled_locations.index(x)]['age'], ["CODE", "NAME"], ["%%%%%%", x['name']])

    def loot(self, text, **kwargs):
        to_work_with=text.split('\n')
        if len(kwargs)==0:
            typee=gettype(to_work_with[0])
        else:
            typee=kwargs['type']
        datadump = []
        type_of_mine_datasets = {"Coke:": {"symb": 'c', "split": "Coke: "}, "Magic": {"symb": 'm', "split": "Magic stone: "}, "Sapphire:": {"symb": 's', "split": "Sapphire: "}, "Ruby:": {"symb": 'r', "split": "Ruby: "}}
        for x in to_work_with[2:len(to_work_with)]:
            if 'Attractions: ' in x:
                datadump.append('a')
                continue
            if 'Mine' in typee:
                datadump.append(type_of_mine_datasets[x.split(' ')[0]]['symb']+','+x.split(type_of_mine_datasets[x.split(' ')[0]]['split'])[1].split('%')[0])
            elif 'Ruins' in typee:
                datadump.append('i,'+x.split('Items: ')[1].split('%')[0])
            elif 'Glory' in typee:
                datadump.append('g,'+x.split('Glory: ')[1].split('%')[0])
        return [';'.join(datadump), text.split('Code: ')[1].split('.')[0]]

    def read(self, code):
        stuff=locations[code]['dump'].split(' ')
        type_of_datasets = {"g": {"text": 'Glory'}, "i": {"text": 'Items'}, "c": {"text": 'Coke'}, "m": {"text": 'Magic stone'}, "s": {"text": 'Sapphire'}, "r": {"text": 'Ruby'}}
        dict_of_burn={}
        dict_of_now = {}
        dict_of_loots ={}
        attractions=False
        for x in stuff:
            if 'burn:' in x:
                type_and_burn = x.replace('burn:', '').split(';')
                for y in type_and_burn:
                    dict_of_burn[type_of_datasets[y.split(',')[0]]['text']] = float(y.split(',')[1])
            elif '_logged:' in x:
                age_and_loots = x.split('_logged:')
                age_logged = int(age_and_loots[0])
                age_current = locations[code]['age']
                difference_in_age = age_current-age_logged
                loots = age_and_loots[1].split(';')
                for y in loots:
                    if y=='a':
                        attractions = True
                        continue
                    dict_of_loots[type_of_datasets[y.split(',')[0]]['text']] = float(y.split(',')[1])
                if dict_of_burn!={}:
                    for z in dict_of_loots:
                        dict_of_now[z] = round(dict_of_loots[z]-(dict_of_burn[z]*difference_in_age), 2)
        beautyful_text = ' <code>unknown</code>'
        if dict_of_now!={}:
            beautyful_text=''
            for x in dict_of_now:
                beautyful_text+='\n └'+x+': '+(str(dict_of_now[x]) if dict_of_now[x]>0 else '0.00')+'%'
        return [beautyful_text, dict_of_loots, attractions]

    def scout(self):
        msg_to_send_x = '🔭🗺<b>Weak locations from Last War</b>:\n\n<b>No defenders</b>:'
        dict_of_msgs = {}
        weak_list = {40: [], 60: [], 80: []}
        list_of_battlecodes = [x for x in battle[1]]
        max_battlecode = max([int(k.split('_')[2]) for k in list_of_battlecodes])
        real_battlecode = [z for z in list_of_battlecodes if '_'+str(max_battlecode) in z][0]
        for y in locations:
            if locations[y]['name'] not in battle[1][real_battlecode]:
                msg_to_send_x+='\n'+locations[y]['name']+' <code>'+y+'</code> <a href="t.me/share/url?url=/ga_atk_'+y+'">⤴️Check</a>'
                if locations[y]['owner']!='Complex Citadel':
                    lvl_of_loc = int(locations[y]['name'].split('.')[1])
                    for x in weak_list:
                        if lvl_of_loc<=x:
                            weak_list[x].append(y)
                            break
        msg_to_send_x+='\n\n<b>Few defenders:</b>'
        for a in battle[1][real_battlecode]:
            dump_in_question = battle[1][real_battlecode][a]['dump'].split('_')
            bunch_of_codes = [t for t in locations if locations[t]['name']==a]
            if int(dump_in_question[2])<3:
                msg_to_send_x+='\n'+a+' <code>'+str(bunch_of_codes)+'</code> <b>'+dump_in_question[2]+'</b>🛡'
                if len(bunch_of_codes)!=0:
                    if locations[bunch_of_codes[0]]['owner']!='Complex Citadel':
                        lvl_of_loc = int(a.split('.')[1])
                        for x in weak_list:
                            if lvl_of_loc<=x:
                                weak_list[x].append(bunch_of_codes[0])
                                break
        return [msg_to_send_x, weak_list]

loc = LocManager()

#add a piece of location or alliance headquarters to db.
def add_objective(name, code, owner, **kwargs):
    print("'"+name+"' "+code+' '+owner)
    if code=='':
        code='%%%%%%'
        print('code set to %')
    if code!='%%%%%%' and (code in alliance or code in locations):
        print('way1')
        #check if alliance/location code exists in db
        if owner!='-':
            locations[code]['owner']=owner
            botdb.change_info("LOCATIONS", 'OWNER', owner, 'CODE', code)
        if 'lvl' in name:
            statu = locations[code]['status']
            if statu!='active':
                botdb.change_info("LOCATIONS", "STATUS", 'active', "NAME", name)
                locations[code]['status']='active'
    elif code!='%%%%%%':
        if 'lvl.' in name:
            typee = gettype(name)
        else:
            typee = 'hq'
        if typee!='hq':
            list_of_names=[x['name'] for x in unhandled_locations]
            if name in list_of_names:
                botdb.change_info("LOCATIONS", "CODE", code, ["CODE", "NAME"], ['%%%%%%', name])
                locations[code] = {'name': name, 'status': 'active', 'type': typee, 'age': unhandled_locations[list_of_names.index(name)]['age'], 'owner': unhandled_locations[list_of_names.index(name)]['owner'], 'dump': ''}
                del(unhandled_locations[list_of_names.index(name)])
            else:
                botdb.add_location(name, code, 'active', typee, '0', owner, '')
                locations[code] = {'name': name, 'status': 'active', 'type': typee, 'age': 0, 'owner': owner, 'dump': ''}
        else:
            botdb.add_hq(name, code, 'active', '100,100,100', '')
            alliance[code] = {'name': name, 'status': 'active', 'power': '100,100,100', 'dump': ''}
        loc_report='<b>New 📍 found:</b> \n'+name
        if len(kwargs)!=0:
            loc_report+='\n<a href="tg://user?id='+str(kwargs['finder_id'])+'">From</a>'
        loc_report+='\n<b>Code:</b> '+code
        if typee!='hq':
            if locations[code]['owner']!='-':
                loc_report+='\n<b>Owner:</b> '+locations[code]['owner']
        for abccu in commanderlist:
            ccordersbot.send_message(abccu, loc_report)
    else:
        print('way3')
        list_of_correct_owner = [locations[x]['name'] for x in locations if locations[x]['owner']!=owner]
        golems = [locations[x]['name'] for x in locations if locations[x]['owner']=='Golem Sentinels']
        names_of_unhandled = [x['name'] for x in unhandled_locations]
        print(list_of_correct_owner)
        if list_of_correct_owner.count(name)==1:
            print('way31')
            for x in locations:
                if locations[x]['owner']!=owner and locations[x]['name']==name:
                    locations[x]['owner']=owner
                    botdb.change_info("LOCATIONS", "OWNER", owner, "CODE", x)
        elif list_of_correct_owner.count(name)>1:
            print('way32')
            for x in locations:
                if locations[x]['name']==name:
                    locations[x]['owner']='Double Locations'
            #if len([locations[x]['name'] for x in locations if (locations[x]['owner']=='-' or locations[x]['owner']=='Golem Sentinels')])==1:
            #    for x in locations:
            #        if (locations[x]['owner']=='-' or locations[x]['owner']=='Golem Sentinels') and locations[x]['name']==name:
            #            locations[x]['owner']=owner
            #            botdb.change_info("LOCATIONS", "OWNER", owner, "CODE", x)
            #else:
            #    for x in locations:
            #        if locations[x]['name']==name:
            #            locations[x]['owner']=owner
            #            botdb.change_info("LOCATIONS", "OWNER", owner, "CODE", x)
        elif name not in names_of_unhandled:
            print('way33')
            if owner=='Golem Sentinels':
                if golems.count(name)>=1:
                    return
                for abccu in commanderlist:
                    ccordersbot.send_message(abccu, '<b>New 📍 found:</b> \n'+name+'\nFrom reports\n<b>Code:</b> '+code+'\n<b>Owner</b>: '+owner)
            typee = gettype(name)
            botdb.add_location(name, code, 'active', typee, '0', owner, '')
            unhandled_locations.append({'name': name, 'status': 'active', 'type': typee, 'age': 0, 'owner': owner, 'dump': ''})
        elif names_of_unhandled.count(name)==1:
            print('way34')
            typee = gettype(name)
            for x in names_of_unhandled:
                if x==name:
                    botdb.change_info("LOCATIONS", "OWNER", owner, ["NAME", "CODE"], [name, '%%%%%%'])
                    unhandled_locations[names_of_unhandled.index(x)]['owner'] = owner

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
    typee = 'unknown'
    if 'State: ' in office or '%' in office or 'Attractions: ' in office or office=='':
        return typee
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
    elif 'Mine' in office:
        if 'Abandoned' in office:
            typee = 'Mine T3'
        elif 'Collapsed' in office:
            typee = 'Mine T2'
        elif 'Unfinished' in office:
            typee = 'Mine T1'
    return typee

async def main():
    global guild_info
    global guilds
    global doipinornot
    global order
    global reports
    global transferdict
    global battle
    global wire_tap_message
    global poincomp
    new_offset = 0
    print('launching cc orders bot')

    while True:
        all_updates=ccordersbot.get_updates(new_offset)
        await asyncio.sleep(0.2)

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
                poincomp={}
                time.sleep(60)
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
                threspp = ccordersbot.send_message(-1001416833350, '<b>⚔️ Battle is over! ⚔️</b> \n\nSend your battle <a href="t.me/share/url?url=/report">/report</a> to @cwccorderbot')
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

async def update_handler(current_update):
            global guild_info
            global guilds
            global doipinornot
            global order
            global attendlist
            global reports
            global transferdict
            global default_tactics
            global battle
            global wire_tap_message
            global event
            global runekeeper
            global spam_cleanup
            global rword
            global gatop
            global plotcontrol
            global poincomp
            try:
                first_update_id = current_update['update_id']
                new_offset = first_update_id + 1
                iscwbot = False
                isgrp = False
                first_chat_text=''
                first_chat_id=0
                sender_id=0
                first_forward_date=0
                if 'message' in current_update or 'edited_message' in current_update:
                    if 'edited_message' in current_update:
                        print('Trash update---')
                        return
                    if 'from' in current_update['message']:
                        sender_id = current_update['message']['from']['id']
                        if sender_id==1293724081:
                            return
                    else:
                        sender_id = 0
                    first_msg_id = current_update['message']['message_id']
                    if 'forward_from' in current_update['message']:
                        if current_update['message']['forward_from']['id']==408101137:
                            iscwbot = True
                        first_forward_date = int(current_update['message']['forward_date'])
                    if 'chat' in current_update['message']:
                        first_chat_id = current_update['message']['chat']['id']
                        if first_chat_id==-1001354774898:
                            if 'reply_to_message' in current_update['message']:
                                try:
                                    cht_txt = current_update['message']['reply_to_message']['text']
                                    first_chat_text = current_update['message']['text']
                                    msgid = int(first_chat_text.split('(')[1].split(')')[0])
                                    guild_id = first_chat_text.split('[')[1].split(']')[0]
                                    if '/pin' in first_chat_text:
                                        ccordersbot.pin_chat_message(guild_id, msgid, False)
                                    else:
                                        ccordersbot.reply_to_message(guild_id, msgid, first_chat_text.replace('('+str(msgid)+')', '').replace('['+guild_id+']', ''))
                                except:
                                    ccordersbot.send_message(-1001354774898, 'error')
                        if current_update['message']['chat']['type'] == 'supergroup':
                            if 'text' in current_update['message']:
                                first_chat_text = current_update['message']['text']
                            if (('То remember the route you associated it with simple combination' not in first_chat_text and 'Your result on the battlefield:' not in first_chat_text) or iscwbot!=True) and 'update locations' not in first_chat_text:
                                for x in guild_info:
                                    if x==first_chat_id:
                                        wire_tap_message+='\n['+str(first_chat_id)+'] ('+str(current_update['message']['message_id'])+') <a href="tg://user?id='+str(sender_id)+'">'+str(sender_id)+'</a>: '+first_chat_text+' '+guild_info[x]['tag']
                                        if random.randint(1, 8)==8:
                                            ccordersbot.send_message(-1001354774898, wire_tap_message)
                                            wire_tap_message=''
                                if '/' in first_chat_text or sender_id in commanderlist or (('Rating' in first_chat_text or ('#' in first_chat_text and '[' in first_chat_text) or '🤝Alliances top:' in first_chat_text) and iscwbot==True):
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
                    first_chat_text = current_update['channel_post']['text']
                    if first_chat_id!=-1001370689034:
                        print('Trash update---')
                        return
                    if 'forward_date' in current_update['channel_post']:
                        first_forward_date=int(current_update['channel_post']['forward_date'])
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
                                    i_text = i_text+'\n<b>'+locations[dots]["name"]+'</b> <code>'+dots+'</code> \n<b>'+str(locations[dots]["status"])+'</b>, Owner: <b>'+locations[dots]["owner"]+'</b>'
                                desc = 'Get a list of all locations.'
                                resultis.append({"type": "article", "id": str(resultoffset[0]), "title": i_title, "input_message_content": {"message_text": i_text, "parse_mode": "HTML"}, "description": desc})
                                resultoffset[0] = resultoffset[0]+1
                                i_title = "🗺Locations Map"
                                i_text = 'The active <b>Locations:</b>'
                                for dots in locations:
                                    if locations[dots]['status']=='active':
                                        i_text+='\n<b>'+locations[dots]["name"]+'</b> <code>'+dots+'</code> \n<b>'+str(locations[dots]["status"])+'</b>, Owner: <b>'+locations[dots]["owner"]+'</b> \n/deactivate_'+dots+' \n/delete_'+dots
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
                                    i_text+='\n📍<b>'+alliance[dots]["name"]+'</b> <code>'+dots+'</code> \n<b>'+str(alliance[dots]["status"])+'</b> '+acv_msg
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
                if first_chat_id in banlist:
                    return
                clearance_two = not (clearance.guild(first_chat_id)=='' and first_chat_id not in commanderlist and sender_id not in commanderlist)
                first_chat_text=first_chat_text.replace('@cwccorderbot', '')
                if first_chat_id==-1001416833350 and ('/give ' in first_chat_text or first_chat_text=='/status' or first_chat_text=='/mypoints' or first_chat_text=='/top'):
                    if sender_id in event:
                        if '/give ' in first_chat_text:
                            if event[sender_id]['runes']>0:
                                letter_given = first_chat_text.replace('/give ', '')
                                if len(letter_given)==1:
                                    spam_cleanup.append(current_update['message']['message_id'])
                                    runekeeper['word']+=letter_given
                                    botdb.change_info("RUNEKEEPER", "DUMP", runekeeper['word'], "VARIABLE", "word")
                                    event[sender_id]['runes']-=1
                                    botdb.change_info("EVENT", "RUNES", event[sender_id]['runes'], "ID", sender_id)
                                    if runekeeper['current'][len(runekeeper['word'])-1]!=letter_given:
                                        ccordersbot.send_message(-1001416833350, 'Whyyy, you ruined the word '+event[sender_id]['ign']+'!')
                                        runekeeper['word']=''
                                        botdb.change_info("RUNEKEEPER", "DUMP", '', "VARIABLE", "word")
                                        runekeeper['reward']=''
                                        botdb.change_info("RUNEKEEPER", "DUMP", '', "VARIABLE", "reward")
                                    else:
                                        if runekeeper['reward']!='':
                                            runekeeper['reward']+=' '+str(sender_id)
                                        else:
                                            runekeeper['reward']=str(sender_id)
                                        botdb.change_info("RUNEKEEPER", "DUMP", runekeeper['reward'], "VARIABLE", "reward")
                                        if runekeeper['current']==runekeeper['word']:
                                            tries=0
                                            new_word=None
                                            while new_word==None and tries<15:
                                                tries+=1
                                                new_word = rword.get_random_word(maxLength=22)
                                            if new_word==None:
                                                new_word=runekeeper['word']
                                            new_word=new_word.replace(' ', '')
                                            points_to_add = len(runekeeper['word'])
                                            for x in runekeeper['reward'].split(' '):
                                                event[int(x)]['points']+=points_to_add
                                                botdb.change_info("EVENT", "POINTS", event[int(x)]['points'], "ID", x)
                                            runekeeper['points']+=points_to_add**2
                                            botdb.change_info("RUNEKEEPER", "DUMP", runekeeper['points'], "VARIABLE", "points")
                                            runekeeper['current']=new_word
                                            botdb.change_info("RUNEKEEPER", "DUMP", new_word, "VARIABLE", "current")
                                            runekeeper['word']=''
                                            botdb.change_info("RUNEKEEPER", "DUMP", '', "VARIABLE", "word")
                                            runekeeper['reward']=''
                                            botdb.change_info("RUNEKEEPER", "DUMP", '', "VARIABLE", "reward")
                                            if runekeeper['points']>runekeeper['hp']:
                                                ccordersbot.send_message(-1001416833350, '🔮Boss <b>'+runekeeper['boss']+'</b> died☠️! Comgratulations!')
                                                list_of_bosses = ["silverrr", 'suitcasse', 'motheri', 'consequencc', 'onlly', 'floatingv', 'belives', 'desesperandoo', 'quarterrb', 'quando']
                                                runekeeper['boss']=list_of_bosses[random.randint(0, len(list_of_bosses)-1)]
                                                botdb.change_info("RUNEKEEPER", "DUMP", runekeeper['boss'], "VARIABLE", "boss")
                                                runekeeper['hp']=random.randint(500, 2000)
                                                botdb.change_info("RUNEKEEPER", "DUMP", runekeeper['hp'], "VARIABLE", "hp")
                                                runekeeper['points']=0
                                                botdb.change_info("RUNEKEEPER", "DUMP", '0', "VARIABLE", "points")
                                                ccordersbot.send_message(-1001416833350, '🔮🚨Oh no! 😱 A new light appeared from the crystal ball, it seems like a new boss was born!')
                                            current_hp=int((runekeeper['points']/runekeeper['hp'])*20)
                                            #for x in spam_cleanup:
                                                #ccordersbot.delete_message(-1001416833350, x)
                                            spam_cleanup=[]
                                            msg_to_send = 'Well done!\n\n🔮<b>'+runekeeper['boss']+'</b> HP\n['+('-'*(20-current_hp))+'💚'+('-'*current_hp)+']\n\n💫Spell: <b>'+runekeeper['current']+'</b>'
                                            ccordersbot.send_message(-1001416833350, msg_to_send)
                                else:
                                    ccordersbot.send_message(-1001416833350, '/give only 1 letter please')
                            else:
                                ccordersbot.send_message(-1001416833350, 'You have no more runes!')
                        elif first_chat_text=='/status':
                            current_hp=int((runekeeper['points']/runekeeper['hp'])*20)
                            msg_to_send = '🔮<b>'+runekeeper['boss']+'</b> HP\n['+('-'*(20-current_hp))+'💚'+('-'*current_hp)+']\n\nWe need: <b>'+runekeeper['current']+'</b>'
                            ccordersbot.send_message(-1001416833350, msg_to_send)
                        elif first_chat_text=='/top':
                            final_msg = '🎖<b>Top Citadel Players</b>'
                            points_string = [event[x]['points'] for x in event]
                            ids_string = [x for x in event]
                            topindices = sorted(range(len(points_string)), key=lambda i: points_string[i])[-10:]
                            ranking = 0
                            for x in topindices[::-1]:
                                ranking+=1
                                top_name = event[ids_string[x]]['ign']
                                final_msg+='\n<b>'+str(ranking)+'.</b> '+top_name+': <b>'+str(event[ids_string[x]]['points'])+' points </b>'
                            ccordersbot.send_message(first_chat_id, final_msg)
                    else:
                        ccordersbot.send_message(first_chat_id, 'You don\'t have any runes yet. Send your alliance /report to @cwccorderbot to play!')
                elif first_chat_id==536511250 and '/giftrune_' in first_chat_text:
                    first_chat_text=first_chat_text.split('_')
                    event[int(first_chat_text[1])]['runes']+=int(first_chat_text[2])
                    botdb.change_info("EVENT", "RUNES", event[int(first_chat_text[1])]['runes'], "ID", int(first_chat_text[1]))
                    ccordersbot.send_message(first_chat_id, 'Done')
                elif first_chat_id in event and first_chat_text in ['/mypoints', '/myrunes', '/top']:
                    if first_chat_text=='/mypoints':
                        ccordersbot.send_message(first_chat_id, '🎉You have <b>'+str(event[sender_id]['points'])+'</b> points')
                    elif first_chat_text=='/myrunes':
                        ccordersbot.send_message(first_chat_id, '🎉You have <b>'+str(event[sender_id]['runes'])+'</b> runes📜')
                    elif first_chat_text=='/top':
                        final_msg = '🎖<b>Top Citadel Players</b>'
                        points_string = [event[x]['points'] for x in event]
                        ids_string = [x for x in event]
                        topindices = sorted(range(len(points_string)), key=lambda i: points_string[i])[-10:]
                        ranking = 0
                        for x in topindices[::-1]:
                            ranking+=1
                            top_name = event[ids_string[x]]['ign']
                            final_msg+='\n<b>'+str(ranking)+'.</b> '+top_name+': <b>'+str(event[ids_string[x]]['points'])+' points </b>'
                        ccordersbot.send_message(first_chat_id, final_msg)
                elif '/common_chat_link' in first_chat_text and isgrp==True:
                    tag=guild_info[first_chat_id]['tag']
                    if tag!='X':
                        linke = ''
                        if tag=='SEA':
                            linke = 'https://t.me/joinchat/F3c_zynJF_g3ZWM9'
                        elif tag=='BTW':
                            linke = 'https://t.me/joinchat/uwAWa54gPvo1ZDk1'
                        elif tag=='RK':
                            linke = 'https://t.me/joinchat/bhHxoqMU2-MwM2Q1'
                        elif tag=='TGS':
                            linke = 'https://t.me/joinchat/NTwzV4pt9TM2Y2E1'
                        elif tag=='IRL':
                            linke = 'https://t.me/joinchat/0RQnkOpsvP4wMzVl'
                        elif tag=='LR':
                            linke = 'https://t.me/joinchat/yPGC61Qz8TwwZmY9'
                        ccordersbot.send_message(first_chat_id, 'Alliance chat link: '+linke)
                elif '➡️' in first_chat_text and '👝: ' in first_chat_text:
                    pogcount = first_chat_text.split('👝: ')
                    pog_count = int(pogcount[0])
                    fromwho = pogcount[1].split(' ➡️ ')
                    from_who = fromwho[0]
                    towho = fromwho[1].split('\n')
                    to_who = towho[0]
                    if from_who in transferdict:
                        transferdict[from_who]['involved']+=(' '+to_who)
                        transferdict[from_who]['pog']+=pog_count
                        transferdict[from_who]['count']+=1
                    else:
                        transferdict[from_who] = {'involved': to_who, 'pog': pog_count, 'count': 1}
                    if to_who in transferdict:
                        transferdict[to_who]['involved']+=(' '+from_who)
                        transferdict[to_who]['pog']+=pog_count
                        transferdict[to_who]['count']+=1
                    else:
                        transferdict[to_who] = {'involved': from_who, 'pog': pog_count, 'count': 1}
                elif '/gettoptransfers_' in first_chat_text:
                    final_msg = ''
                    tophowmany = int(first_chat_text.split('/gettoptransfers_')[1])
                    pog_string = [transferdict[x]['pog'] for x in transferdict]
                    names_string = [x for x in transferdict]
                    topindices = sorted(range(len(pog_string)), key=lambda i: pog_string[i])[-tophowmany:]
                    ranking = 0
                    for x in topindices[::-1]:
                        ranking+=1
                        tranferrer = names_string[x]
                        final_msg+='\n'+str(ranking)+'. '+tranferrer+' 👝:'+str(transferdict[tranferrer]['pog'])+' 🔨:'+str(transferdict[tranferrer]['count'])+' 👥:'+transferdict[tranferrer]['involved']
                    ccordersbot.send_message(first_chat_id, final_msg)
                elif '/erasetransfers' in first_chat_text:
                    transferdict = {}
                elif '🤝Alliances top:' in first_chat_text and iscwbot==True:
                    current_day = datetime.datetime.utcfromtimestamp(first_forward_date)
                    currenttime = int(str(current_day).split(' ')[1].split(':')[0])
                    if currenttime<7 or currenttime==23:
                        lastwar = '23'
                    elif currenttime<15:
                        lastwar = '07'
                    else:
                        lastwar = '15'
                    if currenttime<7:
                        current_day=current_day-datetime.timedelta(1)
                    target_battlecode = str(current_day).split(' ')[0]+'_'+lastwar
                    if target_battlecode not in gatop:
                        gatop[target_battlecode]={}
                        for x in first_chat_text.replace('🤝Alliances top:\n', '').split('\n'):
                            current_point_parser=x.split(' ')
                            pointss= current_point_parser[len(current_point_parser)-1]
                            namee = ' '.join([p for p in x.replace(' '+pointss, '').split(' ') if not any(char.isdigit() for char in p)])
                            gatop[target_battlecode][namee]=pointss
                            botdb.comm("INSERT INTO GATOP1 VALUES ('"+target_battlecode+"', '"+pointss+"', '"+namee+"')", 'UNABLE TO ADD NEW GATOP1 RESULT TO DB')
                        msg_to_reply='Thank you comrade for updating the latest /ga_top1 situation with me!!!'
                    else:
                        msg_to_reply='We already got the current /ga_top1 situation, but thank you.'
                    if isgrp==False:
                        ccordersbot.send_message(first_chat_id, msg_to_reply)
                elif 'То remember the route you associated it with simple combination' in first_chat_text and iscwbot == True:
                    if current_update['message']['forward_date']<int(time.time())-86400 and 'lvl.' in first_chat_text:
                        ccordersbot.delete_message(first_chat_id, first_msg_id)
                        resp = ccordersbot.send_message(first_chat_id, 'Looks like an old location, please send hidden locations within 24 hours they\'re found next time.')
                        try:
                            msg_id_by_bot = int(json.loads(resp.text)["result"]["message_id"])
                        except:
                            what=1
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
                        add_objective(office, both[1], '-', finder_id=sender_id)
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
                    if sender_id in reports:
                        message_to_send = 'You sent your report already'
                        old_report = True
                    lencheck = first_chat_text.split('[')
                    if len(lencheck)>=2 and old_report!=True:
                        lencheckk = lencheck[1].split(']')
                        if [k for k in guild_info if guild_info[k]['tag']==lencheckk[0]]==[]:
                            if first_chat_id==sender_id:
                                banlist.append(first_chat_id)
                                botdb.comm("INSERT INTO BANLIST VALUES ('"+str(first_chat_id)+"')", "unable to insert id into banlist: "+str(first_chat_id))
                                ccordersbot.send_message(log_channel, 'banned: <a href="tg://user?id='+str(sender_id)+'">'+str(sender_id)+'</a> #banned')
                            return
                        lencheckkk = lencheckk[1].split(' ⚔️:')
                        if len(lencheckkk)==1:
                            lencheckkk = lencheckk[1].split(' ⚔:')
                        lencheckkkk = lencheckkk[1].split(' 🛡:')
                        lencheckkkk[0] = lencheckkkk[0].split('(')[0]
                        lencheckkkkk = lencheckkkk[1].split(' Lvl: ')
                        lencheckkkkk[0] = lencheckkkkk[0].split('(')[0]
                        lencheckkkkkk = lencheckkkkk[1].split('\nYour result on the battlefield:\n')
                        match_for_id = [a for a in members if members[a]['id']==sender_id]
                        tags_in_members = [members[a]['guild'] for a in members]
                        insert_into_members_later=False
                        if match_for_id==[]:
                            if lencheckk[0] not in tags_in_members or lencheckkk[0] not in [members[x]['ign'] for x in members]:
                                insert_into_members_later=True
                            else:
                                for b in members:
                                    if lencheckkk[0]==members[b]['ign']:
                                        members[b]['id'] = sender_id
                                        botdb.change_info("MEMBERS", "DUMP", sender_id, "IGN", lencheckkk[0].replace("'", "''"))
                                        message_to_send+=' Have a nice day!'
                        elif len(match_for_id)==1:
                            if int(lencheckkkkkk[0])!=members[match_for_id[0]]['lvl']:
                                message_to_send+='Gratz on your levelup! '
                                members[match_for_id[0]]['lvl']=int(lencheckkkkkk[0])
                                botdb.change_info("MEMBERS", "LVL", int(lencheckkkkkk[0]), "SNO", match_for_id[0])
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
                        if insert_into_members_later==True:
                            new_serial_no = max([x for x in members])+1
                            members[new_serial_no] = {'ign': lencheckkk[0], 'atk': int(lencheckkkk[0]), 'def': int(lencheckkkkk[0]), 'lvl': int(lencheckkkkkk[0]), 'id': int(sender_id), 'guild': lencheckk[0], 'dump': ''}
                            botdb.comm("INSERT INTO MEMBERS VALUES ('"+str(new_serial_no)+"', '"+lencheckkk[0].replace("'", "''")+"', '"+lencheckkkk[0]+"', '"+lencheckkkkk[0]+"', '"+lencheckkkkkk[0]+"', '"+str(sender_id)+"', '"+lencheckk[0]+"', '')", 'insert into members new values')
                            message_to_send += 'You are now recognised. '
                        if int(gold_no)>0 or int(stock_no)>0 or exp_no<=0:
                            if first_chat_id==sender_id:
                                message_to_send += 'But that does not seem like the alliance one🤔'
                                ccordersbot.send_message(first_chat_id, message_to_send)
                            return
                        if exp_no==1:
                            message_to_send = message_to_send+'🙇‍♂️Sorry for the wall (if any), we will do better next time!!'
                        reports[sender_id] = {'tag': lencheckk[0], 'ign': lencheckkk[0], 'att': lencheckkkk[0], 'def': lencheckkkkk[0], 'lvl': lencheckkkkkk[0], 'exp': exp_no, 'hp': hp_no}
                        rune_count = random.randint(2, 5)
                        if sender_id not in event:
                            botdb.comm("INSERT INTO EVENT VALUES ('"+str(sender_id)+"', '"+str(rune_count)+"', '0', '["+lencheckk[0]+']'+lencheckkk[0].replace("'", "''")+"')", 'unable to insert new event guy')
                            event[sender_id] = {'runes': rune_count, 'points': 0, 'ign': "["+lencheckk[0]+']'+lencheckkk[0]}
                        else:
                            event[sender_id]['runes']+=rune_count
                            botdb.change_info("EVENT", "RUNES", event[sender_id]['runes'], "ID", sender_id)
                        message_to_send+='\n📜+'+str(rune_count)
                    elif old_report==True:
                        print('old report')
                    else:
                        message_to_send=''
                    if message_to_send!='':
                        resp = ccordersbot.send_message(first_chat_id, message_to_send)
                        if isgrp==True:
                            msg_id_by_bot = int(json.loads(resp.text)["result"]["message_id"])
                            await asyncio.sleep(30)
                            if guild_info[first_chat_id]['settings'].split(' ')[1]=='y':
                                ccordersbot.delete_message(first_chat_id, first_msg_id)
                            ccordersbot.delete_message(first_chat_id, msg_id_by_bot)
                elif (first_chat_id not in commanderlist+[guild_info[x]['leader'] for x in guild_info] or first_chat_text=='/secret_request'):
                    if isgrp==False:
                        if clearance.member(first_chat_id)==False:
                            ccordersbot.send_message(first_chat_id, 'Send me your /report 🌝')
                            ccordersbot.send_message(-1001175100654, 'Suspicious new person pm-ed me: '+str(first_chat_id)+' sender: <a href="tg://user?id='+str(sender_id)+'">'+str(sender_id)+'</a>')
                        elif first_chat_text=='/help':
                            ccordersbot.send_message(first_chat_id, '<b>Commands:</b>\n/secret_request\n/orders')
                        elif first_chat_text=='/secret_request':
                            serial_no = clearance.member(first_chat_id)
                            ccordersbot.send_message(first_chat_id, 'secret request sent, await authorisation!')
                            ccordersbot.send_message(536511250, '🌝Secret mission request: <a href="tg://user?id='+str(sender_id)+'">'+str(sender_id)+'</a> \n'+str(members[serial_no])+'\nAllow: /secret_'+str(sender_id))
                        else:
                            if random.randint(1, 9)!=1:
                                message_to_send = eliza_chatbot.respond(first_chat_text)
                                ccordersbot.send_message(-1001175100654, "Usage of eliza by "+str(first_chat_id)+" \n"+message_to_send+'\n#eliza')
                            else:
                                serial_no = clearance.member(first_chat_id)
                                message_to_send='How may I help you today, ['+members[serial_no]['guild']+']'+members[serial_no]['ign']+'?🤵'
                            ccordersbot.send_message(first_chat_id, message_to_send)
                elif '/secret_' in first_chat_text and sender_id==536511250:
                    try:
                        chat_id_in_question = int(first_chat_text.split('_')[1])
                        list_of_match = [x for x in members if members[x]['id']==chat_id_in_question]
                        if list_of_match!=[]:
                            if 'secret' not in members[list_of_match[0]]['dump']:
                                members[list_of_match[0]]['dump']='secret'
                                ccordersbot.send_message(chat_id_in_question, 'Welcome to the secret missions team! Thank you for your participation.')
                            else:
                                members[list_of_match[0]]['dump']=''
                            botdb.change_info("MEMBERS", "REALDUMP", members[list_of_match[0]]['dump'], "DUMP", chat_id_in_question)
                            ccordersbot.send_message(first_chat_id, 'ok '+members[list_of_match[0]]['dump'])
                        else:
                            ccordersbot.send_message(first_chat_id, 'chat id not found')
                    except:
                        ccordersbot.send_message(first_chat_id, '<b>Usage</b>: /secret_{chatID}')
                elif '/interject' in first_chat_text:
                    first_chat_text=first_chat_text.split('_')
                    try:
                        if len(first_chat_text[2])==6 and first_chat_text[1] in ['def', 'atk'] and (set(first_chat_text[3].split(' ')).issubset(set(['1', '2', '3']))) and int(first_chat_text[4])>2:
                            poincomp[first_chat_text[2]] = {"def": 0 if first_chat_text[1]=='def' else 1, "range": [int(x) for x in first_chat_text[3].split(' ')], "points": int(first_chat_text[4]), "type": 'hq', "state": 'preparing'}
                            ccordersbot.send_message(first_chat_id, 'okay interjected:\ncommand: /ga_'+first_chat_text[1]+'_'+first_chat_text[2]+'\nimportance: '+first_chat_text[4]+'\nranges: '+first_chat_text[3])
                        else:
                            ccordersbot.send_message(first_chat_id, '<b>Usage</b>: /interject_{atk|def}_{code}_{range ({1|2|3}) separated with a space, 1:lvl20-39, 2:lvl.40-59, 3:lvl.60+}_{importantness>2}\n<b>Example:</b> /interject_atk_abcdef_1 2_20')
                    except:
                        ccordersbot.send_message(first_chat_id, '<b>Usage</b>: /interject_{atk|def}_{code}_{range ({1|2|3}) separated with a space, 1:lvl20-39, 2:lvl.40-59, 3:lvl.60+}_{importantness>2}\n<b>Example:</b> /interject_atk_abcdef_1 2_20')
                elif '🤝 Your alliance.\n🥔⛰Complex Citadel' in first_chat_text and iscwbot==True and commanderlist.count(first_chat_id)!=0:
                    if yeodet[0]==0:
                        if current_update['message']['forward_date']>= int(time.time())-120:
                            current_day = datetime.datetime.utcnow()
                            currenttime = int(str(current_day).split(' ')[1].split(':')[0])
                            lastwar=''
                            if currenttime<7:
                                lastwar = '23'
                            elif currenttime<15 and currenttime!=7:
                                lastwar = '07'
                            elif currenttime!=7 and currenttime!=15 and currenttime!=23:
                                lastwar = '15'
                            if 'Code: KMDwuF.\n\n' in first_chat_text and lastwar!='':
                                if currenttime<7:
                                    current_day=current_day-datetime.timedelta(1)
                                target_battlecode = str(current_day).split(' ')[0]+'_'+lastwar
                                ccordersbot.send_message(first_chat_id, 'Thank you for updating alliance map with me. \n<b>Next! Send me the Alliance Menu</b>')
                                first_chat_text=first_chat_text.split('Code: KMDwuF.\n\n')[1]
                                first_chat_text = first_chat_text.split('\n\n\n')
                                for difhing in first_chat_text:
                                    namesake = difhing.split('\n')[0]
                                    real_name = namesake[2:len(namesake)]
                                    code = difhing.split('Code: ')[1].split('.')[0]
                                    if code not in locations:
                                        if real_name in [x['name'] for x in unhandled_locations]:
                                            add_objective(real_name, code, '')
                                    if code in locations:
                                        if 'life,' not in locations[code]['dump'] and locations[code]['age']!=0:
                                            loot_li= loc.loot(difhing)
                                            loot_master = {}
                                            loot_master[0]=[]
                                            there_is_attractions=False
                                            if ';a' in loot_li[0]:
                                                loot_li[0]=loot_li[0].replace(';a', '')
                                                there_is_attractions = True
                                            loot_master[locations[code]['age']]=loot_li[0].split(';')
                                            for x in loot_master[locations[code]['age']]:
                                                loot_master[0].append(x.split(',')[0]+',100')
                                            loot_bigmaster={0: {}, locations[code]['age']: {}}
                                            for age in loot_master:
                                                for y in loot_master[age]:
                                                    if ',' in y:
                                                        loot_bigmaster[age][y.split(',')[0]] = float(y.split(',')[1])
                                            both_perc = {}
                                            both_burn = {}
                                            for loottype in loot_bigmaster[locations[code]['age']]:
                                                both_perc[loottype] = abs(loot_bigmaster[locations[code]['age']][loottype]-loot_bigmaster[0][loottype])
                                                both_burn[loottype] = round(both_perc[loottype]/(locations[code]['age']), 3)
                                            maximum_burn = min([both_burn[x] for x in both_burn])
                                            lower_burnt = max([loot_bigmaster[locations[code]['age']][t] for t in loot_bigmaster[locations[code]['age']]])
                                            max_age = int(lower_burnt//maximum_burn)+1+locations[code]['age']
                                            locations[code]['dump'] = 'life,'+str(max_age)+' burn:'+';'.join([x+','+str(both_burn[x]) for x in both_burn])+' '+str(locations[code]['age'])+'_logged:'+loot_li[0]+(';a' if there_is_attractions else '')
                                            botdb.change_info("LOCATIONS", "DUMP", locations[code]['dump'], "CODE", code)
                                    difhing=difhing.split('\n')
                                    office = difhing[0]
                                    typee = gettype(office)
                                    if typee!='unknown':
                                        poin=0
                                        infoneed = difhing[1]
                                        state=infoneed.split('.')[0].replace('State: ', '')
                                        lvlpsr = difhing[0].split('lvl.')[1]
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
                                                poin = poin+2
                                            elif 'T2' in typee:
                                                poin = poin+3
                                            elif 'T3' in typee:
                                                poin = poin+5
                                            try:
                                                targpi = difhing[3]
                                            except:
                                                targpi = 'nice'
                                            if 'Attractions' in targpi:
                                                poin=poin+3
                                        elif 'Mine' in typee:
                                            typ1 = difhing[2]
                                            typ2 = difhing[3]
                                            for botyps in [typ1, typ2]:
                                                if 'Ruby' in botyps and '0.00%' not in botyps:
                                                    if 'T1' in typee:
                                                        poin+=6
                                                    elif 'T2' in typee:
                                                        poin+=8
                                                    elif 'T3' in typee:
                                                        poin+=12
                                                elif 'Magic stone' in botyps and '0.00%' not in botyps:
                                                    if 'T1' in typee:
                                                        poin+=2
                                                    elif 'T2' in typee:
                                                        poin+=4
                                                    elif 'T3' in typee:
                                                        poin+=6
                                                else:
                                                    if 'T1' in typee:
                                                        poin+=2
                                                    elif 'T2' in typee:
                                                        poin+=3
                                                    elif 'T3' in typee:
                                                        poin+=5
                                            try:
                                                targpi = difhing[4]
                                            except:
                                                targpi = 'nice'
                                            if 'Attractions:' in targpi:
                                                poin+=3
                                        if code not in poincomp:
                                            poincomp[code] = {"def": 0, "range": tlv, "points": poin, "type": typee, "state": state}
                                waitinglist.append(first_chat_id)
                                chat.append('caos')
                            else:
                                ccordersbot.send_message(first_chat_id, 'You can\'t use auto orders now wait a bit later.')
                        else:
                            ccordersbot.send_message(first_chat_id, 'Alliance Map must be sent within 2 mins after cwbot sends it to avoid confusion, try again')
                    else:
                        ccordersbot.send_message(first_chat_id, 'Somebody already updated alliance map with me, but thank you.')
                elif first_chat_id in waitinglist and '/cancel' not in first_chat_text:
                    theindex = waitinglist.index(first_chat_id)
                    if '\nOwner: 🥔[BTW]Smartatos\nObjectives:' in first_chat_text and iscwbot==True and chat[theindex]=='caos':
                        poin=0
                        first_chat_text = first_chat_text.split('\n')
                        glptts = int(first_chat_text[8].split('Glory: ')[1])
                        stockpe = int(first_chat_text[7].split('Stock: ')[1])
                        if glptts !=0:
                            poin+=(glptts//100)
                        if stockpe !=0:
                            poin+=(stockpe//30)
                        for difend in poincomp:
                            if poincomp[difend]['state']=='preparing' or poincomp[difend]['def']==1:
                                continue
                            typee = poincomp[difend]['type']
                            tier = poincomp[difend]['range']
                            if 'Ruin' in typee:
                                poin = poin + (tier*50)
                        poincomp['KMDwuF'] = {"def": 0, "range": [1, 2, 3], "points": poin}
                        del(chat[theindex])
                        del(waitinglist[theindex])
                        yeodet[0] = 2
                        guildyay = {}
                        for dy in guild_info:
                            guildyay[guild_info[dy]['tag']] = {'grpid': int(dy)}
                        print(guildyay)
                        currenttime = int(str(datetime.datetime.utcnow()).split(' ')[1].split(':')[0])
                        if currenttime<7 or currenttime==23:
                            nextwar = 7
                        elif currenttime<15:
                            nextwar = 15
                        else:
                            nextwar = 23
                        for sgflyer in guildyay:
                            if sgflyer=='C' or sgflyer=='X':
                                continue
                            text_msg = ''
                            notice = ''
                            toppots = 0
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
                                    diffcator+=poincomp[charders]['points']
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
                                    importanceind=''
                                    if (diffcator//8)!=0:
                                        importanceind = '🕊x'+str(diffcator//8 if (diffcator//8)<4 else 3)
                                        toppots = (diffcator//8) if (diffcator//8)<4 else 3
                                    text_msg +='\n\n<b>'+thixt+'</b> /ga_'+str('def' if poincomp[thecdiw]['def']==0 else 'atk')+'_'+thecdiw+' '+importanceind
                                else:
                                    notice +='\n'+thixt+'can go attend castle war'
                            if toppots!=0:
                                notice+='\n🕊'
                                for x in range(1, toppots+1):
	                                notice+=' /use_p0'+str(x+3)
                            grpppid = guildyay[sgflyer]['grpid']
                            raw_message = '<u>NEXT WAR '+str(nextwar)+'UTC '+sgflyer+'</u> \n<code>Orders generated by Citadel Systems 3.0</code> '+text_msg+'\n'+notice+'\n🔱/tactics_'+default_tactics+'\nℹ️/report to guild chat'
                            new_message = tools.link_command(raw_message)
                            ccordersbot.send_order(grpppid, new_message, return_id=sender_id)
                        ccordersbot.send_message(first_chat_id, 'orders sent')
                elif first_chat_text=='/send_secrets':
                    secret_locs = loc.scout()[1]
                    secret_list = {}
                    for x in [[20, 40], [41, 60], [61, 80]]:
                        secret_list[x[1]] = [members[t]['id'] for t in members if 'secret' in members[t]['dump'] and members[t]['lvl']<=x[1] and members[t]['lvl']>=x[0]]
                    msg_to_sen = '<b>Secret missions for next war:</b>\n'
                    for k in secret_list:
                        keeping_tabs = 4
                        for l in secret_list[k]:
                            if keeping_tabs>=4:
                                try:
                                    secret_mission_code=secret_locs[k][0]
                                    del(secret_locs[k][0])
                                except:
                                    continue
                                keeping_tabs=random.randint(0, 1)
                            ccordersbot.send_order(l, 'Your secret mission for next war:\n\n/ga_atk_'+secret_mission_code, return_id=sender_id)
                            keeping_tabs+=1
                            msg_to_sen+='\n'+['['+members[x]['guild']+']'+members[x]['ign'] for x in members if members[x]['id']==l][0]+': <code>'+secret_mission_code+'</code>'
                    ccordersbot.send_message(first_chat_id, msg_to_sen)
                elif '/set_tactics_' in first_chat_text:
                    default_tactics = first_chat_text.split('/set_tactics_')[1]
                    ccordersbot.send_message(first_chat_id, 'successfully set default tactics: '+default_tactics)
                elif '/collect_fees' in first_chat_text and first_chat_id==536511250:
                    guild_lists = []
                    fee_message = '🤵Dear guild leaders, please /ga_deposit ❤️ the following amounts (calculated based on guild member count, without considering possible rebates):'
                    for x in guild_info:
                        if guild_info[x]['tag']!='X':
                            fee_message+='\n<b>'+guild_info[x]['tag']+'</b>: <a href="t.me/share/url?url=/ga_deposit_25">/ga_deposit_25</a>'
                    ccordersbot.send_message(-1001344525861, fee_message)
                elif iscwbot==True:
                    if current_update['message']['forward_date']<int(time.time())-600:
                        old_msg=True
                    else:
                        old_msg=False
                    g_tag = ''
                    for x in guild_info:
                        if sender_id==guild_info[x]['leader'] or first_chat_id==x:
                            g_tag = guild_info[x]['tag']
                    if g_tag=='' or g_tag=='X':
                        return
                    if '#' in first_chat_text and '[' in first_chat_text:
                        if old_msg==True and isgrp==False:
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
                            temporary_id_dict[members[x]['ign']] = members[x]['id']
                            members.pop(x)
                        allppl = first_chat_text.split('\n')
                        for player in allppl:
                            if '#' not in player:
                                continue
                            char = re.findall("[0-9]", player.split(' ')[1].split(' ')[0])
                            level_of_player = ''
                            for x in char:
                                level_of_player = level_of_player+x
                            try:
                                level_of_player = int(level_of_player)
                            except:
                                return
                            ign = player.split('] ')[1]
                            ign=ign.replace("'", "")
                            idd = '0' if ign not in temporary_id_dict else temporary_id_dict[ign]
                            if list_of_removals!=[]:
                                member_id = list_of_removals[0]
                            else:
                                top_member_no+=1
                                member_id = top_member_no
                            members[member_id] = {'ign': ign, 'atk': 0, 'def': 0, 'lvl': level_of_player, 'id': int(idd), 'guild': g_tag, 'dump': ''}
                            reply_msg = reply_msg+'\n- Added info member#'+str(member_id)+' ign: '+str(ign)
                            botdb.comm("INSERT INTO MEMBERS VALUES ('"+str(member_id)+"', '"+ign+"', '0', '0', '"+str(level_of_player)+"', '"+str(idd)+"', '"+g_tag+"', '')", 'insert into members new values')
                            if list_of_removals!=[]:
                                del(list_of_removals[0])
                        if list_of_removals!=[]:
                            for x in list_of_removals:
                                for k in range(x+1, len(members)):
                                    try:
                                        botdb.change_info("MEMBERS", "SNO", k-1, "SNO", k)
                                        members[k-1] = {'ign': members[k]['ign'], 'atk': members[k]['atk'], 'def': members[k]['def'], 'lvl': members[k]['lvl'], 'id': members[k]['id'], 'guild': members[k]['guild'], 'dump': ''}
                                    except:
                                        print('problem with dummy?')
                        if isgrp!=True:
                            ccordersbot.send_message(first_chat_id, reply_msg+'\n\n--Finished-- \n\nFinish updating /g_atklist and /g_deflist (forward <b>both</b> to me)')
                    elif isgrp==True:
                        return
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
                            is_validated = False
                            for y in guild_info:
                                if guild_info[y]['tag']==g_tag_p:
                                    is_existing_guild.append(g_tag_p)
                                    reply_msg = reply_msg+'\n- Found '+g_tag_p+', skipping'
                                    is_validated = True
                            if is_validated==True:
                                continue
                            reply_msg = reply_msg+'\n- New guild inserted: '+g_tag_p+', finish setup: \nLeader: /gs_'+g_tag_p+'_l_{id} \nChat: /gs_'+g_tag_p+'_cht_{id} \noptional (req. additional perm.s):\n /gs_'+g_tag_p+'_cdt_{id} /gs_'+g_tag_p+'_o{0|1|2}_{y|n} /gs_'+g_tag_p+'_adm_{id}'
                            guild_info[consta] = {'tag': g_tag_p, 'leader': 0, 'credit': 100, 'settings': 'y y y x'}
                            botdb.add_guild(g_tag_p, consta, 0, 100, 'y y y x')
                            for y in guild_info:
                                if guild_info[y]['tag']==g_tag_p:
                                    is_existing_guild.append(g_tag_p)
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
                    elif 'Commander' in first_chat_text and 'Level' in first_chat_text and 'Glory' in first_chat_text:
                        tag = first_chat_text.split('[')[1].split(']')[0]
                        for x in guild_info:
                            if guild_info[x]['tag']==tag:
                                guild_info[x]['credit']=int(first_chat_text.split('👥 ')[1].split('/')[0])
                                botdb.change_info("GUILD", "CREDIT", guild_info[x]['credit'], "TAG", tag)
                                ccordersbot.send_message(first_chat_id, 'ok, size of guild '+tag+' is now '+str(guild_info[x]['credit'])+'in special Citadel Guilds (TM) db')
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
                    if len(set_var[1])<4:
                        for x in guild_info:
                            if set_var[1]==guild_info[x]['tag']:
                                guild_chat_for_process = x
                                existence_of_guild = True
                    else:
                        list_of_needed_chats = [x for x in guild_info if set_var[1] in str(x)]
                        if len(list_of_needed_chats)==1:
                            guild_chat_for_process = list_of_needed_chats[0]
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
                        settings_var = int(set_var[2].replace('o', ''))
                        guild_setting = guild_info[guild_chat_for_process]['settings'].split(' ')
                        if set_var[3] in ['y', 'n'] and settings_var in [0, 1, 2]:
                            guild_setting[settings_var]=set_var[3]
                        else:
                            ccordersbot.send_message(first_chat_id, '<b>Usage:</b> /gs_TAG_o{0|1|2}_{y|n}')
                            return
                        new_settings = ' '.join([x for x in guild_setting])
                        guild_info[guild_chat_for_process]['settings']=new_settings
                        botdb.change_info("GUILD", "SETTINGS", new_settings, "CHAT", guild_chat_for_process)
                    ccordersbot.send_message(first_chat_id, 'ok')
                elif '/chat_settings' in first_chat_text and first_chat_id in guild_info:
                    msg_to_send = '🔧<b>This chat settings</b> ('+str(first_chat_id)+'):'
                    settings_and_descriptions = {0: 'Mini Alliance reports to guild chat: ', 1: 'Delete alliance /reports from guild chat: ', 2: 'Battle is coming! reminders: '}
                    two_states_and_desc = {'y': {'word': 'yes', 'opp': 'n', 'desc': 'off: '}, 'n': {'word': 'no', 'opp': 'y', 'desc': 'on: '}}
                    guild_setting = guild_info[first_chat_id]['settings'].split(' ')
                    for x in settings_and_descriptions:
                        msg_to_send+='\n'+settings_and_descriptions[x]+'<b>'+two_states_and_desc[guild_setting[x]]['word']+'</b>\n └To turn '+two_states_and_desc[guild_setting[x]]['desc']+': /gs_'+str(first_chat_id).replace('-100', '')+'_o'+str(x)+'_'+two_states_and_desc[guild_setting[x]]['opp']
                    ccordersbot.send_message(first_chat_id, msg_to_send)
                elif '/msg' in first_chat_text and first_chat_id in commanderlist:
                    msg_variables = first_chat_text.split('_')
                    try:
                        guild_exis = False
                        cht_idd = []
                        for x in guild_info:
                            if guild_info[x]['tag'] in msg_variables[1]:
                                if x not in cht_idd:
                                    cht_idd.append(x)
                                guild_exis = True
                            elif str(x) in msg_variables[1]:
                                if x not in cht_idd:
                                    cht_idd.append(x)
                                guild_exis = True
                        for x in members:
                            try:
                                if (str(members[x]['id']) in msg_variables[1] or 'sn'+str(x) in msg_variables[1]) and members[x]['id']!=0:
                                    if members[x]['id'] not in cht_idd:
                                        cht_idd.append(members[x]['id'])
                                    guild_exis = True
                            except:
                                plach = 1+1
                        print(cht_idd)
                        if guild_exis==True:
                            for a in cht_idd:
                                raw_message = first_chat_text.replace('/msg_'+msg_variables[1]+'_', '')
                                new_message = tools.link_command(raw_message)
                                new_message = new_message.replace('1 exp', '/hail_Citadel').replace('1exp', '/hail_Citadel').replace('1xp', '/hail_Citadel')
                                ccordersbot.send_order(a, new_message, return_id=sender_id)
                        else:
                            ccordersbot.send_message(first_chat_id, 'No such guild/chat/member ('+msg_variables[1]+') exist in Complex Citadel')
                    except:
                        ccordersbot.send_message(first_chat_id, '<b>Usage:</b> /msg_{TAG/ID}_{message}\nGUILD Available Tag/chatIDs: '+', '.join([guild_info[x]['tag']+'/'+str(x) for x in guild_info])+'\nExample: /msg_BTW LR AYY 536511250 sn11_Hello!!')
                elif '/whois' in first_chat_text:
                    try:
                        space_split = first_chat_text.split(' ')
                        if len(space_split)==1:
                            space_split = space_split.split('_')
                        extra_info = ''
                        for x in members:
                            if int(space_split[1])==members[x]['id']:
                                extra_info = '\nFound a record in members list: '+str(members[x])
                        ccordersbot.send_message(first_chat_id, '👤 <a href="tg://user?id='+space_split[1]+'">'+space_split[1]+'</a>'+extra_info)
                    except:
                        ccordersbot.send_message(first_chat_id, '<b>Usage:</b> /whois {chatID}')
                elif first_chat_text=='/help':
                    ccordersbot.send_message(first_chat_id, '<b>Commands:</b>\n/members\n/reports\n/whois {chatID}\n/msg_{TAG/ID}_{message}\nAvailable Tag/chatIDs: '+str([guild_info[x]['tag']+': '+str(x) for x in guild_info])+'\nExample: /msg_BTW LR AYY_Hello!!\n/interject_{atk|def}_{code}_{range ({1|2|3}) separated with a space, 1:lvl20-39, 2:lvl.40-59, 3:lvl.60+}_{importantness>2}\n<b>Example:</b> /interject_atk_abcdef_1 2_20 \n(only for emergency)\n\nGuild leaders: (only for emergency)\n/g_add_{tag}_{chatIDofGuildChat}_{chatIDofLeader}\n/g_del_{chatIDofGuildChat}\n\nSecret missions:\n/secret_request\n/send_secrets (admin)\n\nLocations management:\n/overview\n/scout\n/survey_{name/code}\nFor alliance codes:\n/activate_{code}\n/deactivate_{code}\nFor location codes:\n/delete_{code}\nFor both:\n/addloc_{exactName}_{6-digitCode}_{Owner} (only use this for emergency)\n\nServer Data:\n/cpu\n/dbrefresh\n\nAdmin commands:\n/cmd_{promote|demote}_{chatID}\n/{ban|unban}_{chatID}')
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
                        mess_to_send+='\n\nLvl.'+str(a)+'-'+str(a+19)+':\n<b><code>Lv|ID        |Atk |Def |Tag</code></b>'
                        for x in members:
                            if int(members[x]['lvl'])>=a and int(members[x]['lvl'])<a+20:
                                processed_values = {}
                                for c in const_of_lvl:
                                    process_phrase = str(members[x][c])
                                    available_chars = const_of_lvl[c]
                                    processed_values[c] = ''
                                    for k in process_phrase:
                                        if available_chars >0:
                                            available_chars-=1
                                            processed_values[c]+=k
                                    if len(processed_values[c])<const_of_lvl[c]:
                                        processed_values[c]+=(' '*(const_of_lvl[c]-len(processed_values[c])))
                                    processed_values[c]+='|'
                                mess_to_send+='\n<code>'+str(members[x]['lvl'])+'|'+processed_values['id']+str(processed_values['atk'])+str(processed_values['def'])+processed_values['guild']+'</code>'
                    ccordersbot.send_message(first_chat_id, mess_to_send)
                elif '/ga_top1' in first_chat_text:
                    current_day = datetime.datetime.utcnow()
                    currenttime = int(str(current_day).split(' ')[1].split(':')[0])
                    if currenttime<7 or currenttime==23:
                        lastwar = '23'
                    elif currenttime<15:
                        lastwar = '07'
                    else:
                        lastwar = '15'
                    if currenttime<7:
                        current_day=current_day-datetime.timedelta(1)
                    target_battlecode = str(current_day).split(' ')[0]+'_'+lastwar
                    if target_battlecode not in plotcontrol:
                        fig = plt.figure()
                        ax = fig.add_subplot(111)
                        preparedhqs={}
                        for x in gatop:
                            date_time_str = x
                            date_time_obj = datetime.datetime.strptime(date_time_str, '%Y-%m-%d_%H')
                            for y in gatop[x]:
                                if y not in preparedhqs:
                                    preparedhqs[y]={}
                                preparedhqs[y][date_time_obj]=gatop[x][y]
                        for x in preparedhqs:
                            listo_dates = sorted([k for k in preparedhqs[x]])
                            listo_points = []
                            for g in listo_dates:
                                listo_points.append(float(preparedhqs[x][g]))
                            ax.plot(listo_dates, listo_points, label=x)
                        fig.autofmt_xdate()
                        plt.xlabel('time')
                        plt.ylabel('points')
                        plt.title('/ga_top1 rankings')
                        fontP = matplotlib.font_manager.FontProperties()
                        fontP.set_size('xx-small')
                        plt.legend(prop=fontP)
                        fig.savefig('1_'+target_battlecode+".png")
                        plotcontrol[target_battlecode]='http://mingyu201712.pythonanywhere.com/static/gatop/1_'+target_battlecode+'.png'
                        botdb.comm("INSERT INTO PLOTCONTROL VALUES ('"+target_battlecode+"', '"+plotcontrol[target_battlecode]+"')", "unable to insert something into plotcontrol")
                    ccordersbot.send_picture(first_chat_id, 'http://mingyu201712.pythonanywhere.com/static/gatop/1_'+target_battlecode+'.png', message='/ga_top1')
                elif '/survey' in first_chat_text or '/s_' in first_chat_text or '/s ' in first_chat_text:
                    try:
                        first_chat_text=first_chat_text.replace('/survey'+first_chat_text[7], '')
                    except:
                        ccordersbot.send_message(first_chat_id, '<b>Usage:</b>\n/survey {code}\n/survey {location name}')
                        return
                    try:
                        loc_name=first_chat_text.replace('/s'+first_chat_text[2], '')
                    except:
                        ccordersbot.send_message(first_chat_id, '<b>Usage:</b>\n/survey {code}\n/survey {location name}')
                        return
                    matches_list=[]
                    if len(loc_name)==6 and (loc_name in alliance or loc_name in locations):
                        if loc_name in alliance:
                            loc_name = alliance[loc_name]['name']
                        elif loc_name in locations:
                            loc_name = locations[loc_name]['name']
                    elif loc_name not in ([locations[x]['name'] for x in locations]+[alliance[x]['name'] for x in alliance]):
                        loc_name = str.title(' '.join(loc_name.split(' ')[0:2]))
                        stuffs_after_that = loc_name.split(' ')[2:]
                        if stuffs_after_that!=[]:
                            loc_name+=' '+' '.join(stuffs_after_that)
                        for x in locations:
                            if loc_name in locations[x]['name']:
                                matches_list.append(x)
                        for x in alliance:
                            if loc_name in alliance[x]['name']:
                                matches_list.append(x)
                        if len(matches_list)==1:
                            loc_name = alliance[matches_list[0]]['name'] if matches_list[0] in alliance else locations[matches_list[0]]['name']
                        else:
                            if len(matches_list)==0:
                                msg_to_send='404 Not found'
                            else:
                                msg_to_send='<b>Search results</b> ('+str(len(matches_list))+')\n<i>(powered by Booble)</i>\n'
                                serial_no=0
                                while serial_no<5 and serial_no<len(matches_list):
                                    x=matches_list[serial_no]
                                    loc_name = alliance[x]['name'] if x in alliance else locations[x]['name']
                                    msg_to_send+='\n'+loc_name+': /s_'+x
                                    serial_no+=1
                                msg_to_send+='\n\nToo many items fit the description. Try narrowing the search.' if len(matches_list)>5 else ''
                            ccordersbot.send_message(first_chat_id, msg_to_send)
                            return
                    statees = ['🛡👌', '🛡', '🛡⚡️', '⚔️⚡️', '⚔️', '⚔️😎']
                    x=0
                    if 'lvl.' in loc_name:
                        x=1
                    msg_to_send = 'survey results for <b>'+loc_name+'</b>:\n'
                    if x==0:
                        loca_message=''
                        for locs in locations:
                            if locations[locs]['owner']==loc_name:
                                loca_message+='\n └'+locations[locs]['name']+' <code>'+locs+'</code>'
                        for stuff in unhandled_locations:
                            if stuff['owner']==loc_name:
                                loca_message+='\n └'+stuff['name']+' <code>unknown_code</code>'
                        if loca_message=='':
                            loca_message+=' <code>none</code>'
                        print(loc_name)
                        spot_guild_msg='\n<code>'+[alliance[x]['dump'] for x in alliance if alliance[x]['name']==loc_name][0]+'</code>'
                        if spot_guild_msg=='\n<code></code>':
                            spot_guild_msg='<code>none</code>'
                        msg_to_send+='HQ code: <code>'+', '.join([x for x in alliance if alliance[x]['name']==loc_name])+'</code>\nGuilds spotted: '+spot_guild_msg+'\n📍Locations:'+loca_message+'\n'
                    else:
                        msg_to_send+='Location(s): <code>'+', '.join([x for x in locations if locations[x]['name']==loc_name])+'</code>\nOwner(s): '+', '.join([locations[x]['owner'] for x in locations if locations[x]['name']==loc_name])
                        read_loc = loc.read([x for x in locations if locations[x]['name']==loc_name][0])
                        msg_to_send+='\n📦🎖Current Loot(s): '+read_loc[0]+'\n🎢Attractions: <code>'+str(read_loc[2])+'</code>\n'
                    for y in battle[x]:
                        battle_details = y.split('_')[0]+' '+y.split('_')[1]
                        for z in battle[x][y]:
                            if loc_name==z:
                                dump = battle[x][y][z]["dump"].split('_')
                                emoji = statees[battle[x][y][z]["result"]-1]
                                if x==0:
                                    loot_tv='' if battle[x][y][z]["result"]<4 else ' -'+dump[1]+'📦 -'+dump[2]+'🎖'
                                    msg_to_send+='\n<b>[⚔️'+str(dump[4])+'|🛡'+str(dump[3])+']</b> <a href="t.me/chtwrsreports/'+y.split('_')[2]+'">'+battle_details+'</a>: '+emoji+loot_tv
                                else:
                                    by_who='' if dump[1]=='none' else ' (by '+dump[1]+')'
                                    msg_to_send+='\n<b>[⚔️'+str(dump[3])+'|🛡'+str(dump[2])+']</b> <a href="t.me/chtwrsreports/'+y.split('_')[2]+'">'+battle_details+'</a>: '+emoji+by_who
                        if battle_details not in msg_to_send:
                            msg_to_send+='\n<b>[⚔️0|🛡0]</b> <a href="t.me/chtwrsreports/'+y.split('_')[2]+'">'+battle_details+'</a>: missing!!!'
                    ccordersbot.send_message(first_chat_id, msg_to_send)
                elif first_chat_text=='/overview':
                    msg_to_send_x = '🌏🗺<b>World Map:</b>'
                    list_of_battlecodes = [x for x in battle[1]]
                    max_battlecode = max([int(k.split('_')[2]) for k in list_of_battlecodes])
                    real_battlecode = [z for z in list_of_battlecodes if '_'+str(max_battlecode) in z][0]
                    for a in battle[1][real_battlecode]:
                        dump_in_question = battle[1][real_battlecode][a]['dump'].split('_')
                    dict_of_msgs = {}
                    for code in alliance:
                        dict_of_msgs[code]={}
                        for locs in locations:
                            if locations[locs]['owner']==alliance[code]['name']:
                                dict_of_msgs[code][locs]={"msg": ' └'+locations[locs]['name']+' <code>'+locs+'</code>', "name": locations[locs]['name']}
                        temp_keeper=123964
                        for x in unhandled_locations:
                            if x['owner']==alliance[code]['name']:
                                dict_of_msgs[code][temp_keeper]={"msg": ' └'+x['name']+' <code>unknown_code</code>', "name": x['name']}
                                temp_keeper+=1
                    for x in dict_of_msgs:
                        if len(dict_of_msgs[x])!=0:
                            msg_to_send_x+='\n\n🏯<b>'+alliance[x]['name']+'</b> <code>'+x+'</code>'
                            for y in dict_of_msgs[x]:
                                msg_to_send_x+='\n'+dict_of_msgs[x][y]['msg']
                                try:
                                    by_whom = battle[1][real_battlecode][dict_of_msgs[x][y]['name']]['dump'].split('_')[1]
                                    if by_whom!='none':
                                        msg_to_send_x+=' ⛳️'
                                except:
                                    print('no such loc from last battle')
                    ccordersbot.send_message(first_chat_id, msg_to_send_x)
                elif first_chat_text=='/scout':
                    msg_to_send_x=loc.scout()[0]
                    ccordersbot.send_message(first_chat_id, msg_to_send_x)
                elif '/addloc_' in first_chat_text:
                    first_chat_text=first_chat_text.split('_')
                    if gettype(first_chat_text[1])!='unknown' and len(first_chat_text[2])==6 and (first_chat_text[3] in [alliance[x]['name'] for x in alliance] or first_chat_text[3]=='Golem Sentinels'):
                        add_objective(first_chat_text[1], first_chat_text[2], first_chat_text[3])
                        ccordersbot.send_message(first_chat_id, 'Successfully added location:\n<b>Name:</b> '+first_chat_text[1]+'\n<b>Code:</b> '+first_chat_text[2]+'\n<b>Owner:</b> '+first_chat_text[3])
                    else:
                        ccordersbot.send_message(first_chat_id, '<b>Usage:</b> /addloc_{exactName}_{6-digitCode}_{Owner}')
                elif '🤝Headquarters news:' in first_chat_text and first_chat_id in [-1001370689034, 536511250]:
                    list_of_gtags = [guild_info[x]['tag'] for x in guild_info if guild_info[x]['tag']!='X']
                    tv_message='📺<b>Citadel TV</b>\n'
                    list_of_hqs=first_chat_text.replace('🤝Headquarters news:\n', '').split('\n\n\n')
                    hqs_prepared = {1: {}, 2: {}, 3: {}, 4: {}, 5: {}, 6: {}}
                    mini_report = '<b>🤝Battle results:</b>'
                    currenttime = int(str(datetime.datetime.utcfromtimestamp(first_forward_date)).split(' ')[1].split(':')[0])
                    if currenttime<7 or currenttime==23:
                        nextwar = '23'
                    elif currenttime<15:
                        nextwar = '07'
                    else:
                        nextwar = '15'
                    cstwar = int(nextwar)+8
                    dayyy=5
                    current_day = str(datetime.datetime.utcfromtimestamp(first_forward_date))
                    delete_battlecode = str(datetime.datetime.utcfromtimestamp(first_forward_date)-datetime.timedelta(5)).split(' ')[0]+'_'+nextwar
                    for x in battle:
                        for y in battle[x]:
                            if delete_battlecode in y:
                                delete_battlecode = y
                                break
                    for x in battle:
                        try:
                            battle[x].pop(delete_battlecode)
                        except:
                            print('no battle to del')
                    botdb.delete_info("BATTLE", "BATTLE", delete_battlecode)
                    if 'channel_post' in current_update:
                        msg_id_from_reports = current_update['channel_post']['forward_from_message_id']
                    else:
                        msg_id_from_reports = current_update['message']['forward_from_message_id']
                    battlecode = current_day.split(' ')[0]+'_'+nextwar+'_'+str(msg_id_from_reports)
                    for x in list_of_hqs:
                        current_hq = x.split('\n')
                        list_of_states = {'easily defended:': {"emoji": '🛡👌', "order": 1}, 'defended successfully:': {"emoji": '🛡', "order": 2}, 'closely defended:': {"emoji": '🛡⚡️', "order": 3}, 'closely breached. ': {"emoji": '⚔️⚡️', "order": 4}, 'breached. ': {"emoji": '⚔️', "order": 5}, 'easily breached. ': {"emoji": '⚔️😎', "order": 6}}
                        emoji = list_of_states[current_hq[0].split('was ')[1]]['emoji']
                        order = list_of_states[current_hq[0].split('was ')[1]]['order']
                        loot_tv = ''
                        stocks=0
                        glory=0
                        if order>3:
                            stocks = x.split('pillaged alliance for ')[1].split('📦 and ')[0]
                            if stocks!='':
                                stocks=int(stocks)
                            glory = x.split('📦 and ')[1].split('🎖:')[0]
                            if glory!='':
                                glory=int(glory)
                            loot_tv = ' -'+str(stocks)+'📦 -'+str(glory)+'🎖'
                        defenders_tv = 0
                        attackers_tv = 0
                        hq_name = current_hq[0].split(' was')[0]
                        for y in current_hq:
                            if current_hq.index(y)==0:
                                continue
                            for g in list_of_gtags:
                                if g in y:
                                    tv_message+='\n📯<b>'+hq_name+'</b>:\n'+y
                                    break
                            if '🎖Defense: ' in y:
                                defenders_tv=len(y.replace('🎖Defense: ', '').split(', '))
                                matching_codes = [x for x in alliance if alliance[x]['name']==hq_name]
                                if len(matching_codes)==1:
                                    original_d = str(alliance[matching_codes[0]]['dump'])
                                    for z in y.split('['):
                                        if ']' in z:
                                            tag=z.split(']')[0]
                                            if tag not in alliance[matching_codes[0]]['dump'].split(' '):
                                                if alliance[matching_codes[0]]['dump']!='':
                                                    alliance[matching_codes[0]]['dump']+=' '+tag
                                                else:
                                                    alliance[matching_codes[0]]['dump']=tag
                                    if alliance[matching_codes[0]]['dump']!=original_d:
                                        botdb.change_info("ALLIANCES", "DUMP", alliance[matching_codes[0]]['dump'], "CODE", matching_codes[0])
                            elif '🎖Attack: ' in y:
                                attackers_tv=len(y.replace('🎖Attack: ', '').split(', '))
                        hq_minitv = '\n<b>[⚔️'+str(attackers_tv)+'|🛡'+str(defenders_tv)+']</b> <i>'+hq_name+':</i> '+emoji+loot_tv
                        hqs_prepared[order][hq_name] = {"emoji": order, 'report': hq_minitv, 'db_string': str(order)+'_'+str(stocks)+'_'+str(glory)+'_'+str(defenders_tv)+'_'+str(attackers_tv)}
                        botdb.add_battle_result(0, battlecode, hq_name, order, hqs_prepared[order][hq_name]['db_string'])
                    for x in hqs_prepared:
                        for y in hqs_prepared[x]:
                            mini_report+=hqs_prepared[x][y]['report']
                    mini_report+='\n\n<a href="t.me/chtwrsreports/'+str(msg_id_from_reports)+'">Battle</a>\n<i>'+current_day.split(' ')[0]+' '+nextwar+':00 UTC ('+str(cstwar)+':00 CST)</i>'
                    for x in guild_info:
                        if guild_info[x]['settings'].split(' ')[0]=='y':
                            ccordersbot.send_message(x, mini_report)
                    ccordersbot.send_message(-1001416833350, tv_message)
                elif '🗺State of map:' in first_chat_text and first_chat_id in [-1001370689034, 536511250]:
                    list_of_gtags = [guild_info[x]['tag'] for x in guild_info if guild_info[x]['tag']!='X']
                    tv_message='📺<b>Citadel TV</b>\n'
                    list_of_hqs=first_chat_text.replace('🗺State of map:\n', '').split('\n\n')
                    locs_prepared = {1: {}, 2: {}, 3: {}, 4: {}, 5: {}, 6: {}}
                    mini_report = '<b>🗺Battle results:</b>'
                    currenttime = int(str(datetime.datetime.utcfromtimestamp(first_forward_date)).split(' ')[1].split(':')[0])
                    if currenttime<7 or currenttime==23:
                        nextwar = '23'
                    elif currenttime<15:
                        nextwar = '07'
                    else:
                        nextwar = '15'
                    cstwar = int(nextwar)+8
                    dayyy=5
                    current_day = str(datetime.datetime.utcfromtimestamp(first_forward_date))
                    delete_battlecode = str(datetime.datetime.utcfromtimestamp(first_forward_date)-datetime.timedelta(5)).split(' ')[0]+'_'+nextwar
                    for x in battle:
                        for y in battle[x]:
                            if delete_battlecode in y:
                                delete_battlecode = y
                                break
                    for x in battle:
                        try:
                            battle[x].pop(delete_battlecode)
                        except:
                            print('no battle to del')
                    botdb.delete_info("BATTLE", "BATTLE", delete_battlecode)
                    if 'channel_post' in current_update:
                        msg_id_from_reports = current_update['channel_post']['forward_from_message_id']
                    else:
                        msg_id_from_reports = current_update['message']['forward_from_message_id']
                    battlecode = current_day.split(' ')[0]+'_'+nextwar+'_'+str(msg_id_from_reports)
                    things_to_deage=[]
                    for x in list_of_hqs:
                        current_hq = x.split('\n')
                        list_of_states = {'easily protected': {"emoji": '🛡👌', "order": 1}, 'was protected': {"emoji": '🛡', "order": 2}, 'closely protected': {"emoji": '🛡⚡️', "order": 3}, '. Easy win:': {"emoji": '⚔️😎', "order": 6}, '. Massacre:': {"emoji": '⚔️⚡️', "order": 4}, 'belongs to ': {"emoji": '⚔️', "order": 5}}
                        for k in list_of_states:
                            if k in current_hq[0]:
                                what_you_need = k
                                break
                        emoji = list_of_states[what_you_need]['emoji']
                        order = list_of_states[what_you_need]['order']
                        loot_tv = ''
                        new_owner = 'none'
                        defenders_tv = 0
                        attackers_tv = 0
                        emojit ='🛡'
                        loc_name = current_hq[0].split(' was')[0].split(' belongs')[0]
                        for y in current_hq:
                            if current_hq.index(y)==0:
                                continue
                            for g in list_of_gtags:
                                if g in y:
                                    tv_message+='\n📯<b>'+loc_name+'</b>:\n'+y
                                    break
                            if '🎖Defense: ' in y:
                                defenders_tv=len(y.replace('🎖Defense: ', '').split(', '))
                                if 'Golem Sentinel lvl' in y:
                                    emojit='📛'
                                    if order<4:
                                        add_objective(loc_name, '%%%%%%', 'Golem Sentinels')
                                owners_of_loc = [locations[x]['owner'] for x in locations if locations[x]['name']==loc_name]
                                if len(owners_of_loc)==1 and 'Golem Sentinels' not in owners_of_loc and 'Double Locations' not in owners_of_loc:
                                    matching_codes = [x for x in alliance if alliance[x]['name']==owners_of_loc[0]]
                                    if len(matching_codes)==1:
                                        original_dump = str(alliance[matching_codes[0]]['dump'])
                                        for z in y.split('['):
                                            if ']' in z:
                                                tag=z.split(']')[0]
                                                if tag not in alliance[matching_codes[0]]['dump'].split(' '):
                                                    if alliance[matching_codes[0]]['dump']!='':
                                                        alliance[matching_codes[0]]['dump']+=' '+tag
                                                    else:
                                                        alliance[matching_codes[0]]['dump']=tag
                                        if alliance[matching_codes[0]]['dump']!=original_dump:
                                            botdb.change_info("ALLIANCES", "DUMP", alliance[matching_codes[0]]['dump'], "CODE", matching_codes[0])
                            elif '🎖Attack: ' in y:
                                attackers_tv=len(y.replace('🎖Attack: ', '').split(', '))
                        if order>3:
                            new_owner = x.split('to ')[1].split('.')[0].split(':')[0]
                            loot_tv = ' (by '+new_owner+')'
                            add_objective(loc_name, '', new_owner)
                            things_to_deage.append(loc_name)
                        elif emojit=='📛':
                            things_to_deage.append(loc_name)
                        hq_minitv = '\n<b>[⚔️'+str(attackers_tv)+'|'+emojit+str(defenders_tv)+']</b> <i>'+loc_name+':</i> '+emoji+loot_tv
                        if loc_name not in locs_prepared[order]:
                            locs_prepared[order][loc_name]=[]
                        locs_prepared[order][loc_name].append({"emoji": order, 'report': hq_minitv, 'db_string': str(order)+'_'+new_owner+'_'+str(defenders_tv)+'_'+str(attackers_tv)})
                        botdb.add_battle_result(1, battlecode, loc_name, order, str(order)+'_'+new_owner+'_'+str(defenders_tv)+'_'+str(attackers_tv))
                    for x in locs_prepared:
                        for y in locs_prepared[x]:
                            for z in locs_prepared[x][y]:
                                mini_report+=z['report']
                    loc.age(things_to_deage)
                    mini_report+='\n\n<a href="t.me/chtwrsreports/'+str(msg_id_from_reports)+'">Battle</a>\n<i>'+current_day.split(' ')[0]+' '+nextwar+':00 UTC ('+str(cstwar)+':00 CST)</i>'
                    for x in guild_info:
                        if guild_info[x]['settings'].split(' ')[0]=='y':
                            ccordersbot.send_message(x, mini_report)
                    ccordersbot.send_message(-1001416833350, tv_message)
                elif 'update locations' in first_chat_text and sender_id in [536511250]:
                    resp = ccordersbot.send_message(first_chat_id, 'updating locations.')
                    msg_id_by_bot = int(json.loads(resp.text)["result"]["message_id"])
                    fullstops=1
                    for x in alliance:
                        fullstops = fullstops+1
                        if fullstops>3:
                            fullstops=1
                        ccordersbot.edit_message(first_chat_id, msg_id_by_bot, 'updating locations'+fullstops*'.')
                    for x in locations:
                        fullstops = fullstops+1
                        if fullstops>3:
                            fullstops=1
                        ccordersbot.edit_message(first_chat_id, msg_id_by_bot, 'updating locations'+fullstops*'.')
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
                            ccordersbot.send_message(first_chat_id, 'Successfully activated '+coooo+' ('+alliance[coooo]['name']+') in database. Have a great day!')
                            botdb.change_info('ALLIANCES', 'STATUS', 'inactive', 'CODE', coooo)
                            locations[coooo]['status'] = 'inactive'
                            whyisthis = whyisthis+1
                    ccordersbot.send_message(first_chat_id, 'Scan through complete, activated '+str(whyisthis)+' locations. Have a great day!')
                elif '/deactivate_' in first_chat_text and commanderlist.count(first_chat_id)!=0 and len(first_chat_text)==18:
                    first_chat_text = first_chat_text.replace('/deactivate_', '')
                    whyisthis = 0
                    inactive_list_l = []
                    inactive_list_a = []
                    for coooo in locations:
                        if coooo == first_chat_text:
                            ccordersbot.send_message(first_chat_id, 'Successfully deactivated '+coooo+' ('+locations[coooo]['name']+') in database. Have a great day!')
                            botdb.change_info('LOCATIONS', 'STATUS', 'inactive', 'CODE', coooo)
                            inactive_list_l.append(coooo)
                            whyisthis = whyisthis+1
                    for coooo in alliance:
                        if coooo == first_chat_text:
                            ccordersbot.send_message(first_chat_id, 'Successfully deactivated '+coooo+' ('+alliance[coooo]['name']+') in database. Have a great day!')
                            botdb.change_info('ALLIANCES', 'STATUS', 'inactive', 'CODE', coooo)
                            inactive_list_a.append(coooo)
                            whyisthis = whyisthis+1
                    for x in inactive_list_l:
                        locations[x]['status'] = 'inactive'
                    for x in inactive_list_a:
                        alliance[x]['status'] = 'inactive'
                    ccordersbot.send_message(first_chat_id, 'Scan through complete, deactivated '+str(whyisthis)+' locations. Have a great day!')
                elif '/delete_' in first_chat_text and commanderlist.count(first_chat_id)!=0 and len(first_chat_text)==14:
                    first_chat_text = first_chat_text.replace('/delete_', '')
                    whyisthis = 0
                    inactive_list_l = []
                    inactive_list_a = []
                    for coooo in locations:
                        if coooo == first_chat_text:
                            ccordersbot.send_message(first_chat_id, 'Successfully removed '+coooo+' ('+locations[coooo]['name']+') from database. Have a great day!')
                            botdb.delete_info("LOCATIONS", "CODE", coooo)
                            inactive_list_l.append(coooo)
                            whyisthis = whyisthis+1
                    for coooo in alliance:
                        if coooo == first_chat_text:
                            ccordersbot.send_message(first_chat_id, 'Successfully removed '+coooo+' ('+alliance[coooo]['name']+') from database. Have a great day!')
                            botdb.delete_info("ALLIANCES", "CODE", coooo)
                            inactive_list_a.append(coooo)
                            whyisthis = whyisthis+1
                    for x in inactive_list_l:
                        locations.pop(x)
                    for x in inactive_list_a:
                        alliance.pop(x)
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
                elif '/cmd_promote_' in first_chat_text:
                    tgid = first_chat_text.replace('/cmd_promote_', '')
                    try:
                        tgid = int(tgid)
                        if tgid in banlist:
                            ccordersbot.send_message(first_chat_id, str(tgid)+' is in ban_list, please remove that first /unban_'+str(tgid))
                        else:
                            if commanderlist.count(tgid)==0:
                                commanderlist.append(tgid)
                                botdb.comm('INSERT INTO COMMANDERS VALUES ('+str(tgid)+')', "can't insert values to banlist")
                                ccordersbot.send_message(first_chat_id, 'Promoted '+str(tgid)+' to commander')
                    except:
                        ccordersbot.send_message(first_chat_id, '<b>Usage:</b>\n/cmd_promote_{chatID}')
                elif commanderlist.count(first_chat_id)!=0 and first_chat_text == '/cpu':
                    username = 'mingyu201712'
                    token = 'e43edb27fff0285e37fdf5cae41351f024c10d60'
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
                elif '/cmd_demote_' in first_chat_text and sender_id in commanderlist:
                    tgid = first_chat_text.replace('/cmd_demote_', '')
                    try:
                        tgid = int(tgid)
                        if commanderlist.count(tgid)>=1:
                            commanderlist.remove(tgid)
                            botdb.delete_info("COMMANDERS", "ID", tgid)
                            ccordersbot.send_message(first_chat_id, 'Demoted '+str(tgid))
                    except:
                        ccordersbot.send_message(first_chat_id, '<b>Usage:</b>\n/cmd_demote_{chatID}')
                elif '/ban_' in first_chat_text and sender_id in commanderlist:
                    tgid = first_chat_text.replace('/ban_', '')
                    try:
                        tgid = int(tgid)
                        if banlist.count(tgid)==0:
                            banlist.append(tgid)
                            botdb.comm('INSERT INTO BANLIST VALUES ('+str(tgid)+')', "can't insert values to banlist")
                            ccordersbot.send_message(first_chat_id, 'Banned '+str(tgid))
                    except:
                        ccordersbot.send_message(first_chat_id, '<b>Usage:</b>\n/ban_{chatID}')
                elif '/unban_' in first_chat_text:
                    tgid = first_chat_text.replace('/unban_', '')
                    try:
                        tgid = int(tgid)
                        if banlist.count(tgid)>=1:
                            banlist.remove(tgid)
                            botdb.delete_info("BANLIST", "ID", tgid)
                            ccordersbot.send_message(first_chat_id, 'Unbanned '+str(tgid))
                    except:
                        ccordersbot.send_message(first_chat_id, '<b>Usage:</b>\n/unban_{chatID}')
                elif isgrp==False:
                    if random.randint(1, 9)!=1:
                        message_to_send = eliza_chatbot.respond(first_chat_text)
                        ccordersbot.send_message(-1001175100654, "Usage of eliza by "+str(first_chat_id)+" \n"+message_to_send+'\n#eliza')
                    else:
                        message_to_send='It seems like you got lost...🤵here\'s some help that you need:\n/help'
                    ccordersbot.send_message(first_chat_id, message_to_send)
            except:
                ccordersbot.send_message(-1001175100654, 'Problem with current update: '+str(current_update))
            return new_offset

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
