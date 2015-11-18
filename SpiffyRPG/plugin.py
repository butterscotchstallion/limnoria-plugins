###
# Copyright (c) 2015, butterscotchstallion
# All rights reserved.
#
#
###
import supybot.utils as utils
from supybot.commands import *
import supybot.plugins as plugins
import supybot.ircutils as ircutils
import supybot.callbacks as callbacks
import supybot.ircmsgs as ircmsgs
import supybot.log as log
import supybot.ircdb as ircdb
import supybot.conf as conf
import supybot.dbi as dbi
import random
import re
import datetime

try:
    from supybot.i18n import PluginInternationalization
    _ = PluginInternationalization('SpiffyRPG')
except ImportError:
    # Placeholder that allows to run the plugin on a bot
    # without the i18n module
    _ = lambda x: x

class SqliteSpiffyRPGDB(dbi.DB):
    def __init__(self, filename):
        self.filename = filename
        self.dbs = ircutils.IrcDict()

    def close(self):
        for db in self.dbs.values():
            db.close()
        self.dbs.clear()

    def _get_db(self, channel):
        import sqlite3

        if channel in self.dbs:
            return self.dbs[channel]

        filename = plugins.makeChannelFilename(self.filename, channel)
        db = sqlite3.connect(filename, check_same_thread=False)
        self.dbs[channel] = db
        
        self.initial_setup(db, channel)

        return db

    def register_new_player(self, channel, user_id, char_name, char_class):
        db = self._get_db(channel)
        cursor = db.cursor()
        created_at = time.time()
        params = (user_id, char_name, char_class, created_at)
        cursor.execute("""INSERT INTO spiffyrpg_players(user_id,
                          character_name, 
                          character_class,
                          created_at)
                          VALUES (?, ?, ?, ?)""", params)
        db.commit()

    def get_player_by_user_id(self, channel, user_id):
        db = self._get_db(channel)
        cursor = db.cursor()

        params = (user_id,)
        cursor.execute("""SELECT character_class,
                          character_name,
                          created_at
                          FROM spiffyrpg_players
                          WHERE user_id = ?""", params)
        players = cursor.fetchall()

        if len(players) > 0:
            return players[0]

    def initial_setup(self, db, channel):
        db = self._get_db(channel)
        cursor = db.cursor()

        self.create_battles_table(cursor, db)
        self.create_players_table(cursor, db)

    def create_battles_table(self, cursor, db):
        cursor.execute("""CREATE TABLE IF NOT EXISTS spiffyrpg_battles(
                          user_id INT PRIMARY KEY,
                          attacker_nick TEXT,
                          target_nick TEXT,
                          experienced_gained INT,
                          battled_at TIMESTAMP)""")
        db.commit()

    def create_players_table(self, cursor, db):
        cursor.execute("""CREATE TABLE IF NOT EXISTS spiffyrpg_players(
                          user_id INT PRIMARY KEY,
                          character_class TEXT,
                          character_name TEXT,
                          created_at TIMESTAMP)""")
        db.commit()

SpiffyRPGDB = plugins.DB("SpiffyRPG", {"sqlite3": SqliteSpiffyRPGDB})

class SpiffyRPG(callbacks.Plugin):
    """A gluten-free IRC RPG"""
    threaded = True

    def __init__(self, irc):
        self.__parent= super(SpiffyRPG, self)
        self.__parent.__init__(irc)

        self.db = SpiffyRPGDB()

    def _get_user_id(self, irc, prefix):
        try:
            return ircdb.users.getUserId(prefix)
        except KeyError:
            irc.errorNotRegistered(Raise=True)

    def _announce_new_player(self, irc, char_name, char_class, channel):
        announcement_msg = "%s the %s joined the game!" % (char_name, char_class)

        irc.sendMsg(ircmsgs.notice(channel, announcement_msg))

    def _is_alphanumeric_with_dashes(self, input):
        return re.match('^[\w-]+$', input) is not None

    def _is_valid_char_name(self, char_name):
        return len(char_name) > 1 and len(char_name) <= 16 \
        and self._is_alphanumeric_with_dashes(char_name)

    def _is_valid_char_class(self, char_class):
        return len(char_class) > 1 and len(char_class) <= 30 \
        and self._is_alphanumeric_with_dashes(char_class)

    def sjoin(self, irc, msg, args, user, query):
        """
        Joins the game: !sjoin <character name> <character class>
        """
        channel = msg.args[0]
        user_id = self._get_user_id(irc, msg.prefix)

        if user_id is not None:
            player = self.db.get_player_by_user_id(channel, user_id)

            (char_name, char_class) = query.split(" ")

            log.info("SpiffyRPG: returned player %s with user id %s" % (str(player), user_id))
            log.info("SpiffyRPG: %s to register '%s' the '%s'" % (msg.nick, char_name, char_class))

            if player is not None:
                irc.error("You're already registered!")
            else:
                valid_registration = self._is_valid_char_name(char_name) \
                and self._is_valid_char_class(char_class)

                if valid_registration:
                    self.db.register_new_player(channel, user_id, char_name, char_class)
                    self._announce_new_player(irc, char_name, char_class, channel)
                else:
                    irc.reply("Character names must be between 1-16 characters, alphanumeric")

    sjoin = wrap(sjoin, ["user", "text"])

    def reset(self):
        self.db.close()

    def die(self):
        self.db.close()
        self.__parent.die()

Class = SpiffyRPG


# vim:set shiftwidth=4 softtabstop=4 expandtab textwidth=79:
