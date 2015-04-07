# -*- coding: utf-8 -*-
###
# 
# GoogleCSE plugin - Uses Google Custom Search Engine to perform queries
# against the Google API.
#
# Copyright (c) 2015, PrgmrBill
# All rights reserved.
#
#
###

import supybot.utils as utils
from supybot.commands import *
import supybot.ircmsgs as ircmsgs
import supybot.plugins as plugins
import supybot.ircutils as ircutils
import supybot.callbacks as callbacks
import urllib
import json

try:
    from supybot.i18n import PluginInternationalization
    _ = PluginInternationalization('GoogleCSE')
except ImportError:
    # Placeholder that allows to run the plugin on a bot
    # without the i18n module
    _ = lambda x: x

class GoogleCSE(callbacks.Plugin):
    threaded = True
    callBefore = ['Web']

    def g(self, irc, msg, args, query):
        """Uses Google Custom Search Engine to perform queries against Google's API"""
        channel = msg.args[0]
        origin_nick = msg.nick
        is_channel = irc.isChannel(channel)
        
        # Settings
        key = self.registryValue('apiKey')
        cx = self.registryValue('searchEngineID')
        base_url = self.registryValue('baseURL')
        search_filter = self.registryValue('searchFilter')
        use_bold = self.registryValue('useBold')
        no_results_message = self.registryValue('noResultsMessage')
        no_api_key_message = self.registryValue('noAPIKeyMessage')
        no_search_engine_id_message = self.registryValue('noSearchEngineIDMessage')
        respond_to_pm = self.registryValue('respondToPrivateMessages')
        is_private_message = not is_channel
        
        if is_channel:
            message_destination = channel
        else:
            message_destination = origin_nick
        
        # Make note of PMs that were sent to bot
        if is_private_message and not respond_to_pm:
            self.log.info("GoogleCSE: not responding to PM from %s" % (origin_nick))
            return
        
        # Make sure we have a search query first. Seems it just shows the help text 
        # in this case.
        if not query:
            return
        
        # API key required
        if not key:
            irc.error(no_api_key_message)
            self.log.error('GoogleCSE: %s' % (no_api_key_message))
            return
        
        # Search engine ID required
        if not cx:
            irc.error(no_search_engine_id_message)
            self.log.error('GoogleCSE: %s' % (no_search_engine_id_message))
            return
        
        # Available options: https://developers.google.com/custom-search/json-api/v1/reference/cse/list
        opts = {'q': query, 'key': key, \
                'cx': cx, 'num': 1, \
                'safe': search_filter, 'alt': 'json'}
        
        search_url = '%s?%s' % (base_url, urllib.urlencode(opts))
        
        # Show URL in debug mode. Note: this includes the API key, which could be
        # considered sensitive information.
        self.log.debug("GoogleCSE URL: %s" % (search_url))
        
        # Initialize result
        result = False
        
        try:
            response = utils.web.getUrl(search_url).decode('utf8')
            
            data = json.loads(response)
            
            # Check if there was an error
            try:
                if data['error']:
                    message = data['error']['message']
                    self.log.error("GoogleCSE API error: %s" % (message))
            except KeyError:
                pass
            
            # If there are no results, there will not be a data['items']
            # In that case, there are no results
            try:
                # Search results
                items = data['items']
                
                # Return the first link
                if items:
                    item = items[0]
                    title = item['title']                   
                    
                    if use_bold and title:
                        title = ircutils.bold(title)
                    
                    result = "%s :: %s" % (item['link'], title)
            except:
                pass
        
        except utils.web.Error as e:
            self.log.error("GoogleCSE HTTPError: %s" % (str(e)))
        
        if result:        
            irc.sendMsg(ircmsgs.privmsg(message_destination, result))
        else:
            irc.error(no_results_message)
    
    g = wrap(g, ['text'])

Class = GoogleCSE


# vim:set shiftwidth=4 softtabstop=4 expandtab textwidth=79:
