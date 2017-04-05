###
# Copyright (c) 2015, lunchdump
# All Rights Reserved
#
###


import supybot.utils as utils
from supybot.commands import *
import supybot.plugins as plugins
import supybot.ircutils as ircutils
import supybot.ircmsgs as ircmsgs
import supybot.callbacks as callbacks
import requests
import sys
from random import randrange
import json

if sys.version_info[0] >= 3:
    from urllib.parse import quote_plus
else:
    from urllib import quote_plus
try:
    from supybot.i18n import PluginInternationalization
    _ = PluginInternationalization('RelevantGif')
except ImportError:
    # Placeholder that allows to run the plugin on a bot
    # without the i18n module
    _ = lambda x: x

class RelevantGif(callbacks.Plugin):
    """This plugin related to a given phrase, and selects a result at
    random to return to the channel"""
    threaded = True

    def __init__(self, irc):
        self.__parent = super(RelevantGif, self)
        self.__parent.__init__(irc)

        # This is a public beta API key
        self.GIPHY_API_KEY = "dc6zaTOxFJmzC"
        # Setting to 0 always returns the first image
        self.CHOOSE_FROM = 0

    def gif(self, irc, msg, args, query):
        """<phrase>

        Returns a gif related to given phrase, Powered By Giphy!
        """
        encoded_query = quote_plus(query)
        giphy_url = "http://api.giphy.com/v1/gifs/search?q=%s&api_key=%s&limit=%d&offset=0" % (encoded_query, self.GIPHY_API_KEY, self.CHOOSE_FROM + 1)
        channel = msg.args[0]
        result = None
        headers = {
            "User-Agent": "limnoria-relevant-gif/v0.0.1",
            "Accept": "application/json"
        }

        self.log.info("RelevantGif: requesting %s" % giphy_url)

        try:
            request = requests.get(giphy_url, timeout=10, headers=headers)

            if request.status_code == requests.codes.ok:
                response = json.loads(request.text)

                total_count = response["pagination"]["total_count"]
                no_result = total_count == 0

                if no_result:
                    self.log.info("RelevantGif: query error for %s" % (giphy_url))
                else:
                    if self.CHOOSE_FROM == 0:
                        the_chosen_one = 0
                    else:
                        the_chosen_one = randrange(0, min(self.CHOOSE_FROM, total_count))

                    chosen_url = response["data"][the_chosen_one]["images"]["original"]["url"]
                    relevantgif_template = self.registryValue("template")
                    relevantgif_template = relevantgif_template.replace("$url", chosen_url)

                    result = relevantgif_template
            else:
                self.log.error("RelevantGif Giphy API %s - %s" % (request.status_code, request.text))

        except requests.exceptions.Timeout as e:
            self.log.error("RelevantGif Timeout: %s" % (str(e)))
        except requests.exceptions.ConnectionError as e:
            self.log.error("RelevantGif ConnectionError: %s" % (str(e)))
        except requests.exceptions.HTTPError as e:
            self.log.error("RelevantGif HTTPError: %s" % (str(e)))
        finally:
            if result is not None:
                irc.sendMsg(ircmsgs.privmsg(channel, result))
            else:
                irc.error(self.registryValue("noResultsMessage"))

    gif = wrap(gif, ['text'])

Class = RelevantGif


# vim:set shiftwidth=4 softtabstop=4 expandtab textwidth=79:
