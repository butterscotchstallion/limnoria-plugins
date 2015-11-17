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
import time
import supybot.dbi as dbi
import random

try:
    from supybot.i18n import PluginInternationalization
    _ = PluginInternationalization('Inhibiter')
except ImportError:
    # Placeholder that allows to run the plugin on a bot
    # without the i18n module
    _ = lambda x: x

def float_to_gmt(t):
    f = None

    try:
        f = float(t)
    except:
        return None
    return time.strftime("%Y-%m-%d %H:%M:%S GMT", time.gmtime(f))

class SqliteInhibiterDB(dbi.DB):
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
        
        self.initial_setup(db)

        return db

    def initial_setup(self, db):
        cursor = db.cursor()

        cursor.execute("""CREATE TABLE IF NOT EXISTS inhibiter_suckers (
                          key TEXT PRIMARY KEY,
                          nick TEXT,
                          hostmask TEXT,
                          channel TEXT,
                          served_at TIMESTAMP,
                          kick_message TEXT)""")
        db.commit()

    def add(self, nick, channel, hostmask, kick_message):
        log.info("Inhibiter: [%s] NEW SUCKER: %s" % (channel, hostmask))

        db = self._get_db(channel)
        cursor = db.cursor()
        served_at = int(time.time())
        params = (nick, channel, hostmask, served_at, kick_message)

        cursor.execute("""INSERT INTO inhibiter_suckers(
                          nick, channel, hostmask, served_at, kick_message)
                          VALUES(?, ?, ?, ?, ?)""", params)
        db.commit()

    def get_gullible_suckers(self, channel):
        log.info("Inhibiter: fetching suckers for %s" % channel)
        db = self._get_db(channel)
        cursor = db.cursor()
        suckers = 0
        cursor.execute("""SELECT COUNT(*) AS suckers
                          FROM inhibiter_suckers
                          WHERE channel = ?
                          GROUP BY channel
                          ORDER BY served_at ASC
                          LIMIT 1""", (channel,))

        results = cursor.fetchall()

        if len(results) > 0:
            suckers = int(results[0][0])

        return suckers

    def get_gullible_suckers_served_today(self, channel):
        log.info("Inhibiter: fetching today's suckers for %s" % channel)
        db = self._get_db(channel)
        cursor = db.cursor()
        suckers = 0
        cursor.execute("""SELECT COUNT(*) AS suckers
                          FROM inhibiter_suckers
                          WHERE channel = ?
                          AND datetime(served_at, 'unixepoch', 'localtime') BETWEEN DATE('now') AND DATE('now', '-1 day')
                          GROUP BY channel
                          ORDER BY served_at ASC
                          LIMIT 1""", (channel,))

        results = cursor.fetchall()

        if len(results) > 0:
            suckers = int(results[0][0])

        return suckers

    def get_served_since(self, channel):
        """ Find first record ordering by date """
        db = self._get_db(channel)
        cursor = db.cursor()
        served_since = time.time()

        cursor.execute("""SELECT served_at
                          FROM inhibiter_suckers
                          WHERE channel = ?
                          ORDER BY served_at ASC
                          LIMIT 1""", (channel,))

        results = cursor.fetchall()

        log.info("Inhibiter: served_since: %s" % str(results))

        if len(results) > 0:
            served_since = results[0][0]

        served_since = float_to_gmt(served_since)

        return served_since

InhibiterDB = plugins.DB("Inhibiter", {"sqlite3": SqliteInhibiterDB})

class Inhibiter(callbacks.Plugin):
    """Duplicitous power"""
    threaded = True
    gullible_suckers = {}

    def __init__(self, irc):
        self.__parent= super(Inhibiter, self)
        self.__parent.__init__(irc)

        self.db = InhibiterDB()

    def reset(self):
        self.db.close()

    def die(self):
        self.db.close()
        self.__parent.die()
    
    def get_instructions(self, nick):
        verbs = ("to smite your foes", "to gain channel operator status", 
                 "to show others how much you love them", "for your party hat",
                 "for sexy time", "for your complementary coffee")
        verb = random.choice(verbs)
        
        greetings = ("Howdy %s!" % nick, "Hello %s!" % nick, "Aloha, %s!" % nick)
        greeting = random.choice(greetings)

        instructions_message = "%s Type !ops %s" % (greeting, verb)

        return instructions_message

    def doPart(self, irc, msg):
        nick = msg.nick
        channel = msg.args[0]
        quips = ("%s couldn't take the heat" % nick,
                 "I knew %s didn't have what it takes" % nick,
                 "%s lost before they even began" % nick,
                 "%s is unceremoniously defeated" % nick,
                 "And the world turns unnoticing...",
                 "%s was unworthy" % nick,
                 "%s wasn't getting enough attention" % nick)

        quip = random.choice(quips)

        irc.sendMsg(ircmsgs.privmsg(channel, quip))

    def do484(self, irc, msg):
        channel = msg.args[2]
        winner = msg.args[1]
        loser = msg.args[0] 

        message = self.get_winner_message(winner, loser)
        self.kick_gullible_sucker(irc, loser, channel, message)

    def doJoin(self, irc, msg):
        channel = msg.args[0]

        if channel not in self.gullible_suckers:
            self.gullible_suckers[channel] = self.db.get_gullible_suckers(channel)

        log.info("Inhibiter: suckers -> %s" % str(self.gullible_suckers))

        bot_nick = irc.nick
        origin_nick = msg.nick
        is_bot_joining = origin_nick.lower() == bot_nick.lower()

        if is_bot_joining:
            suckers_msg = self.get_kick_message(channel)
            irc.sendMsg(ircmsgs.privmsg(channel, suckers_msg))
        else:
            welcome_message = self.get_instructions(origin_nick)
            irc.sendMsg(ircmsgs.privmsg(channel, welcome_message))

    def doMode(self, irc, msg):
        channel = msg.args[0]

        """
        This approach is flawed because anyone can deop the bot
        or op someone else and get them kicked

        for (mode, nick) in ircutils.separateModes(msg.args[1:]):
            if not nick:
                continue

            # Ignore self modes
            if ircutils.strEqual(nick, irc.nick):
                continue

            if irc.isNick(nick):
                log.info("Inhibiter: mode %s%s on %s" % (mode, nick, channel))

                if mode == "+o":
                    log.info("Inhibiter: %s gained operator status" % nick)

                    is_protected = self.user_has_capability(msg, "protected")

                    if is_protected:
                        log.info("Inhibiter: %s is protected; not kicking." % nick)
                        return

                    hostmask = irc.state.nickToHostmask(nick)
                    self.add_gullible_sucker_and_kick(nick, channel, hostmask)
        """

    def update_gullible_suckers(self, channel):
        if channel not in self.gullible_suckers:
            self.gullible_suckers[channel] = self.db.get_gullible_suckers(channel)

        self.gullible_suckers[channel] += 1

    def add_gullible_sucker(self, nick, channel, hostmask, kick_message):        
        self.db.add(nick, channel, hostmask, kick_message)

    def voice_gullible_sucker(self, irc, nick, channel):
        irc.queueMsg(ircmsgs.voice(channel, nick))

    def op_gullible_sucker(self, irc, nick, channel):
        irc.queueMsg(ircmsgs.op(channel, nick))

    def kick_gullible_sucker(self, irc, nick, channel, kick_message):
        irc.queueMsg(ircmsgs.kick(channel, nick, kick_message))

    def get_kick_message(self, channel):
        served_since = self.db.get_served_since(channel)
        suckers = self.gullible_suckers[channel]
        derisive_nouns = ("gullible sucker", "unwitting participant",
                          "loyal customer")
        derisive_description = random.choice(derisive_nouns)

        if suckers != 1:
            derisive_description += "s"

        message = "%s %s served since %s" % (suckers, derisive_description, served_since)
        
        return message

    def get_act_of_god_voice_message(self, nick):
        messages = ("The gods smile on %s and grant them voice!",
                    "Flying Spaghetti Monster grants %s voice")

        return random.choice(messages)
    
    def trick_or_treat(self, irc, nick, channel):
        """
        Randomly voices or kicks
        """
        self.update_gullible_suckers(channel)
        kick_message = self.get_kick_message(channel)
        hostmask = irc.state.nickToHostmask(nick)
        voice_chance = self.registryValue("voiceChance", channel=channel)
        apply_voice = random.randrange(0, 100) <= voice_chance

        collateral_chance = self.registryValue("collateralChance", channel=channel)
        collateral_targets = self.registryValue("collateralTargets", channel=channel)
        collateral_nick = random.choice(collateral_targets)
        apply_collateral = False

        op_chance = self.registryValue("opChance", channel=channel)
        apply_ops = random.randrange(0, 100) <= op_chance

        act_of_god_voice_change = self.registryValue("actOfGodVoiceChance", channel=channel)
        apply_voice_randomly = random.randrange(0, 100) <= act_of_god_voice_change

        if collateral_nick in irc.state.channels[channel].users:
            apply_collateral = random.randrange(0, 100) <= collateral_chance
        else:
            self.log.info("Inhibiter: collateral target %s is not in %s" % (collateral_nick, channel))

        if apply_collateral:
            self.kick_gullible_sucker(irc, collateral_nick, channel, kick_message)

        if apply_voice_randomly:
            random_user = random.choice(irc.state.channels[channel].users)
            self.voice_gullible_sucker(irc, random_user, channel)
            act_of_god_voice_message = self.get_act_of_god_voice_message(random_user)
            irc.sendMsg(ircmsgs.privmsg(channel, suckers_msg))
        elif apply_ops:
            self.op_gullible_sucker(irc, nick, channel)
        elif apply_voice:
            self.voice_gullible_sucker(irc, nick, channel)
        else:
            self.kick_gullible_sucker(irc, nick, channel, kick_message)

        self.add_gullible_sucker(nick, channel, hostmask, kick_message)

    def get_self_loser_message(self, loser):
        messages = ("And %s was defeated, because they could not stop hitting themselves" % loser,)

        return random.choice(messages)

    def get_winner_message(self, winner, loser):
        messages = ("%s is victorious" % winner, 
                    "%s has triumphed over %s" % (winner, loser),
                    "%s has vaporized %s" % (winner, loser),
                    "%s crushed %s" % (winner, loser),
                    "%s was reduced to ashes by %s" % (loser, winner))

        return random.choice(messages)

    def battle(self, irc, msg, args, opponent):
        """
        battle another user
        """
        channel = msg.args[0]
        nick = msg.nick
        users = irc.state.channels[channel].users
        self.update_gullible_suckers(channel)
        kick_message = self.get_kick_message(channel)
        bot_nick = irc.nick
        opponent_is_bot = opponent.lower() == bot_nick
        opponent_is_services = opponent.lower() == "chanserv"
        opponent_is_self = opponent.lower() == nick.lower()

        if opponent in users:
            if opponent_is_bot or opponent_is_services:
                loser = nick
                winner = opponent
            else:
                chance_to_win = random.randrange(0, 100)

                if chance_to_win >= 50:
                    winner = nick
                    loser = opponent
                else:
                    winner = opponent
                    loser = nick

            if opponent_is_self:
                message = self.get_self_loser_message(loser)
            else:
                message = self.get_winner_message(winner, loser)

            self.kick_gullible_sucker(irc, loser, channel, message)
        else:
            self.kick_gullible_sucker(irc, nick, channel, kick_message)

    battle = wrap(battle, ["text"])
    vaporize = battle

    def served(self, irc, msg, args, when=None):
        """
        Shows number of gullible suckers served
        """
        if when is None:
            when = "ever"

        channel = msg.args[0]

        if channel not in self.gullible_suckers:
            self.gullible_suckers[channel] = self.db.get_gullible_suckers(channel)

        if when == "ever":
            suckers = self.gullible_suckers[channel]
            served_date = "since %s" % self.db.get_served_since(channel)

        if when == "today":
            suckers = self.db.get_gullible_suckers_served_today(channel)
            served_date = "today"

        derisive_nouns = ("gullible sucker", "unwitting participant",
                          "loyal customer")
        derisive_description = random.choice(derisive_nouns)

        if suckers != 1:
            derisive_description += "s"

        suckers_msg = "%s %s served %s" % (suckers, derisive_description, served_date)
        irc.sendMsg(ircmsgs.privmsg(channel, suckers_msg))

    served = wrap(served, ["text"])

    def ops(self, irc, msg, args):
        """
        Command that grants channel operator status...maybe
        """
        channel = msg.args[0]
        nick = msg.nick
        bot_nick = irc.nick
        is_message_from_self = nick.lower() == bot_nick.lower()
        is_protected = self.user_has_capability(msg, "protected")

        # I can't let you do that, David.
        if is_message_from_self:
            return

        #if is_protected:
        #    irc.sendMsg(ircmsgs.privmsg("ChanServ", "OP %s %s" % (channel, nick)))
        #else:
        self.trick_or_treat(irc, nick, channel)

    ops = wrap(ops)

    # aliases for !ops
    ban = ops
    help = ops
    op = ops
    commands = ops
    kick = ops
    kb = ops
    kickban = ops
    list = ops
    whoami = ops
    k = ops
    invite = ops

    def user_has_capability(self, msg, capability_name):
        channel = msg.args[0]
        mask = msg.prefix
        cap = ircdb.makeChannelCapability(channel, capability_name)
        has_cap = ircdb.checkCapability(mask, cap, ignoreDefaultAllow=True)

        if has_cap:
            log.debug("Inhibiter: %s has capability '%s'" % (mask, capability_name))
        else:
            log.debug("Inhibiter: %s does NOT have capability '%s'" % (mask, capability_name))

        return has_cap

Class = Inhibiter


# vim:set shiftwidth=4 softtabstop=4 expandtab textwidth=79:
