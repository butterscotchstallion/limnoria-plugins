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
import requests
from random import choice
from bs4 import BeautifulSoup

try:
    from supybot.i18n import PluginInternationalization
    _ = PluginInternationalization('Ericpedia')
except ImportError:
    # Placeholder that allows to run the plugin on a bot
    # without the i18n module
    _ = lambda x: x

class Ericpedia(callbacks.Plugin):
    """Fetches random Wikipedia articles and replaces a word with Eric"""
    threaded = True

    def e(self, irc, msg, args):
        """
        Fetches random wikipedia article and replaces a random word
        """
        channel = msg.args[0]
        origin_nick = msg.nick
        url = self.registryValue("wikipediaRandomPageURL", channel=channel)
        
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.60 Safari/537.36"
        }

        request = requests.get(url, timeout=10, headers=headers)
        
        if request.status_code == requests.codes.ok:
            html = request.content
            title = self.get_title_from_html(html)

            if title:
                words = title.split(" ")
                random_word = choice(words)
                replaceWithThisString = self.registryValue("replaceString", channel=channel)

                if replaceWithThisString == "$nick":
                    replaceWithThisString = origin_nick.title()

                replaced_title = title.replace(random_word, replaceWithThisString)

                self.log.debug("Ericpedia: %s => %s" % (title, replaced_title))

                irc.sendMsg(ircmsgs.privmsg(channel, replaced_title))
            else:
                self.log.error("Ericpedia: problem getting title from HTML")

        else:
            self.log.error("Ericpedia: status code %s for %s" % (request.status_code, url))

    e = wrap(e)

    def get_title_from_html(self, html):
        """
        Retrieves value of <title> tag from HTML
        """
        soup = BeautifulSoup(html, "lxml")
        
        if soup is not None:
            heading = soup.find("h1", id="firstHeading")
            
            if heading is not None:
                self.log.debug("Ericpedia: found h1#firstHeading: %s" % heading.get_text())

                return heading.get_text()

Class = Ericpedia


# vim:set shiftwidth=4 softtabstop=4 expandtab textwidth=79:
