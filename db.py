import sqlite3

db = sqlite3.connect("self.db")
mycursor = db.cursor()


# ========================== tables ==========================
def connects():
    db = sqlite3.connect("self.db")
    mycursor = db.cursor()
    mycursor.execute("CREATE TABLE IF NOT EXISTS enemy (id VARCHAR(255) PRIMARY KEY)")
    mycursor.execute("CREATE TABLE IF NOT EXISTS lockedusers (id INTEGER PRIMARY KEY, username TEXT, chat_id INTEGER, locked INTEGER DEFAULT 0)")
    mycursor.execute("CREATE TABLE IF NOT EXISTS messages (messageid VARCHAR(255) ,id VARCHAR(255), text TEXT)")
    mycursor.execute("CREATE TABLE IF NOT EXISTS foshlist (text VARCHAR(255) PRIMARY KEY)")
    mycursor.execute("CREATE TABLE IF NOT EXISTS makhals (name TEXT , userid INTEGER , chatid INTEGER , tedad INTEGER)")
    mycursor.execute("CREATE TABLE IF NOT EXISTS setting (setting TEXT , st TEXT)")
    mycursor.execute("CREATE TABLE IF NOT EXISTS comtlist (id VARCHAR(255) , text TEXT)")
    mycursor.execute("CREATE TABLE IF NOT EXISTS profiles (id INTEGER PRIMARY KEY, name TEXT, bio TEXT, photo TEXT)")
    mycursor.execute("INSERT INTO setting VALUES (?,?)", ('comment','off'))
    mycursor.execute("INSERT INTO setting VALUES (?,?)", ('autoblock','off'))
    mycursor.execute("INSERT INTO setting VALUES (?,?)", ('autosend','off'))    
    mycursor.execute("INSERT INTO setting VALUES (?,?)", ('cardnum','0')) 
    mycursor.execute("INSERT INTO setting VALUES (?,?)", ('wallet','None')) 
    db.commit()
    db.close()

# ========================== userids ==========================
def addenemy(userid):
    db = sqlite3.connect("self.db")
    mycursor = db.cursor()
    mycursor.execute("INSERT INTO enemy VALUES (?)", (userid,))
    db.commit()
    db.close()
def addusl(user_id,usern,chatid):
    db = sqlite3.connect("self.db")
    mycursor = db.cursor()
    mycursor.execute("INSERT INTO lockedusers (id, username, chat_id) VALUES (?, ?, ?)", (user_id, usern,chatid))
    db.commit()
    db.close()


def addfosh(userid):
    db = sqlite3.connect("self.db")
    mycursor = db.cursor()
    mycursor.execute("INSERT INTO foshlist VALUES (?)", (userid,))
    db.commit()
    db.close()


def addcom(userid):
    db = sqlite3.connect("self.db")
    mycursor = db.cursor()
    mycursor.execute("INSERT INTO comtlist (id,text) VALUES (?,?)", (userid,"First!."))
    db.commit()
    db.close()


def delenemy(userid):
    db = sqlite3.connect("self.db")
    mycursor = db.cursor()
    mycursor.execute("DELETE FROM enemy WHERE id = ?", (userid,))
    db.commit()
    db.close()


def enemylist():
    db = sqlite3.connect("self.db")
    mycursor = db.cursor()
    mycursor.execute("SELECT id FROM enemy")
    curse = [i[0] for i in mycursor.fetchall()]
    db.close()
    return curse

def userls(id):
    db = sqlite3.connect("self.db")
    mycursor = db.cursor()
    mycursor.execute("SELECT * FROM lockedusers WHERE id=? AND locked=0", (id,))
    curse = mycursor.fetchall()
    db.close()
    return curse

def foshlist():
    db = sqlite3.connect("self.db")
    mycursor = db.cursor()
    mycursor.execute("SELECT text FROM foshlist")
    curse = [i[0] for i in mycursor.fetchall()]
    db.close()
    return curse
def textcom(chati):
    db = sqlite3.connect("self.db")
    mycursor = db.cursor()
    mycursor.execute("SELECT text FROM comtlist WHERE id = '%i'"% chati)
    curse = [i[0] for i in mycursor.fetchall()]
    return curse
def comlist():
    db = sqlite3.connect("self.db")
    mycursor = db.cursor()
    mycursor.execute("SELECT id FROM comtlist")
    curse = [i[0] for i in mycursor.fetchall()]
    db.close()
    return curse
def textmessages(chati):
    db = sqlite3.connect("self.db")
    mycursor = db.cursor()
    mycursor.execute("SELECT text FROM messages WHERE id = '%i'"% chati)
    curse = [i[0] for i in mycursor.fetchall()]
    return curse
def stcom():
    db = sqlite3.connect("self.db")
    mycursor = db.cursor()
    mycursor.execute("SELECT st FROM setting WHERE setting = 'comment'")
    curse = [i[0] for i in mycursor.fetchall()]
    return curse
def autoblockst():
    db = sqlite3.connect("self.db")
    mycursor = db.cursor()
    mycursor.execute("SELECT st FROM setting WHERE setting = 'autoblock'")
    curse = [i[0] for i in mycursor.fetchall()]
    return curse
def delfosh(ids):
    db = sqlite3.connect("self.db")
    mycursor = db.cursor()
    mycursor.execute("DELETE FROM foshlist WHERE text = ?", (ids,))
    db.commit()
    db.close()


def delcom(ids):
    db = sqlite3.connect("self.db")
    mycursor = db.cursor()
    mycursor.execute("DELETE FROM comtlist WHERE id ='%i'" % ids )
    db.commit()
    db.close()

# ========================== chatids ==========================
def insertChatid(chatid):
    try:
        db = sqlite3.connect("self.db")
        mycursor = db.cursor()
        mycursor.execute("INSERT INTO chatids VALUES (?)", (chatid,))
        db.commit()
        db.close()
    except sqlite3.IntegrityError:
        pass
def insertmessage(messageid,id,text):
    try:
        db = sqlite3.connect("self.db")
        mycursor = db.cursor()
        mycursor.execute("INSERT INTO messages VALUES (?,?,?)", (messageid,id,text))
        db.commit()
        db.close()
    except sqlite3.IntegrityError:
        pass


def removeUUserid(chatid):
    db = sqlite3.connect("self.db")
    mycursor = db.cursor()
    mycursor.execute("DELETE FROM chatids WHERE chatid = ?", (chatid,))
    db.commit()
    db.close()


def loadChatid():
    db = sqlite3.connect("self.db")
    mycursor = db.cursor()
    mycursor.execute("SELECT chatid FROM chatids")
    curse = [i[0] for i in mycursor.fetchall()]
    db.close()
    return curse


def delallfosh():
    db = sqlite3.connect("self.db")
    mycursor = db.cursor()
    mycursor.execute("DELETE FROM foshlist")
    db.commit()
    db.close()


def delallenemy():
    db = sqlite3.connect("self.db")
    mycursor = db.cursor()
    mycursor.execute("DELETE FROM enemy")
    db.commit()
    db.close()


# ========================== makhals ==========================
def firstNml(name, userid, chatid, tedad):
    db = sqlite3.connect("self.db")
    mycursor = db.cursor()
    mycursor.execute("INSERT INTO makhals VALUES (?,?,?,?)", (name, userid, chatid, tedad))
    db.commit()
    db.close()


def oncom():
    db = sqlite3.connect("self.db")
    mycursor = db.cursor()
    mycursor.execute("UPDATE setting SET st = ? WHERE setting = ?", ("on", "comment"))
    db.commit()
    db.close()
def edittext(ids,tex):
    db = sqlite3.connect("self.db")
    mycursor = db.cursor()
    mycursor.execute("UPDATE comtlist SET text = '%s' WHERE id = '%s'"% (tex,ids))
    db.commit()
    db.close()

def cardnumset(tex):
    db = sqlite3.connect("self.db")
    mycursor = db.cursor()
    mycursor.execute("UPDATE setting SET st = '%s' WHERE setting = 'cardnum'"% tex)
    db.commit()
    db.close()
def walletset(tex):
    db = sqlite3.connect("self.db")
    mycursor = db.cursor()
    mycursor.execute("UPDATE setting SET st = '%s' WHERE setting = 'wallet'"% tex)
    db.commit()
    db.close()
def offcom():
    db = sqlite3.connect("self.db")
    mycursor = db.cursor()
    mycursor.execute("UPDATE setting SET st = ? WHERE setting = ?", ("off", "comment"))
    db.commit()
    db.close()

def onblock():
    db = sqlite3.connect("self.db")
    mycursor = db.cursor()
    mycursor.execute("UPDATE setting SET st = ? WHERE setting = ?", ("on", "autoblock"))
    db.commit()
    db.close()

def offblock():
    db = sqlite3.connect("self.db")
    mycursor = db.cursor()
    mycursor.execute("UPDATE setting SET st = ? WHERE setting = ?", ("off", "autoblock"))
    db.commit()
    db.close()

def onautosend():
    db = sqlite3.connect("self.db")
    mycursor = db.cursor()
    mycursor.execute("UPDATE setting SET st = ? WHERE setting = ?", ("on", "autosend"))
    db.commit()
    db.close()

def offautosend():
    db = sqlite3.connect("self.db")
    mycursor = db.cursor()
    mycursor.execute("UPDATE setting SET st = ? WHERE setting = ?", ("off", "autosend"))
    db.commit()
    db.close()

def updateMakhal(userid, chatid, tedad):
    db = sqlite3.connect("self.db")
    mycursor = db.cursor()
    mycursor.execute("UPDATE makhals SET tedad = ? WHERE userid = ? AND chatid = ?", (tedad, userid, chatid))
    db.commit()
    db.close()


def getMakhal(userid):
    db = sqlite3.connect("self.db")
    mycursor = db.cursor()
    mycursor.execute("SELECT * FROM makhals WHERE userid = ? ", (userid,))
    curse = mycursor.fetchall()
    db.close()
    return curse

def getsetting(userid):
    db = sqlite3.connect("self.db")
    mycursor = db.cursor()
    mycursor.execute("SELECT st FROM setting WHERE setting = '%s' " % userid )
    curse = [i[0] for i in mycursor.fetchall()]
    db.close()
    return curse


# ========================== setting BETA ==========================
def loadSetting():
    db = sqlite3.connect("self.db")
    mycursor = db.cursor()
    mycursor.execute("SELECT * FROM setting")
    curse = mycursor.fetchall()
    db.close()
    return curse

def loadMessages():
    db = sqlite3.connect("self.db")
    mycursor = db.cursor()
    mycursor.execute("SELECT messageid FROM messages")
    curse = mycursor.fetchall()
    db.close()
    return curse

def save_profile_data(user,bio):
    db = sqlite3.connect("self.db")
    mycursor = db.cursor()
    mycursor.execute("INSERT INTO profiles (id, name, bio, photo) VALUES (?, ?, ?, ?)", (user.id, user.first_name, bio, user.photo.big_file_id))
    db.commit()
    db.close()


# Retrieve user profile data from database
def retrieve_profile_data(user_id):
    db = sqlite3.connect("self.db")
    mycursor = db.cursor()
    mycursor.execute("SELECT * FROM profiles WHERE id=?", (user_id,))
    profile_data = mycursor.fetchone()
    db.close()
    if profile_data:
        return {"id": profile_data[0], "name": profile_data[1], "bio": profile_data[2], "photo": profile_data[3]}
    else:
        return None
    
def sefet(user_id):
    db = sqlite3.connect("self.db")
    mycursor = db.cursor()
    mycursor.execute("SELECT * FROM lockedusers WHERE id=?", (user_id,))
    profile_data = mycursor.fetchone()
    db.close()
    return profile_data
# Delete user profile data from database
def delete_profile_data(user_id):
    db = sqlite3.connect("self.db")
    mycursor = db.cursor()
    mycursor.execute("DELETE FROM profiles WHERE id=?", (user_id,))
    db.commit()
    db.close()
def deluslo(user_id):
    db = sqlite3.connect("self.db")
    mycursor = db.cursor()
    mycursor.execute("DELETE FROM lockedusers WHERE id=?", (user_id,))
    db.commit()
    db.close()
# create tables if not exists
connects()
# connect2()
# connect3()
# connect4()
# connect5()
# connect6()
# connect7()
