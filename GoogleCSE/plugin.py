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
import supybot.plugins as plugins
import supybot.ircutils as ircutils
import supybot.callbacks as callbacks
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
    #regexps = ['googleSnarfer']
    
    @internationalizeDocstring
    def g(self, irc, msg, args, query):
        """Uses Google Custom Search Engine to perform queries against Google's API"""    
        headers = dict(utils.web.defaultHeaders)
        key = self.registryValue('apiKey')
        cx = self.registryValue('searchEngineID')
        baseURL = self.registryValue('baseURL')
        searchFilter = self.registryValue('searchFilter')

        # API key required
        if not key:
            raise callbacks.Error('GoogleCSE: invalid API key')
        
        # Search engine ID required
        if not cx:
            raise callbacks.Error('GoogleCSE: invalid search engine ID')
        
        # Available options: https://developers.google.com/custom-search/json-api/v1/reference/cse/list
        opts = {'q': query, 'key': key, \
                'cx': cx, 'num': 1, \
                'safe': searchFilter, 'alt': 'json'}
        
        searchURL = '%s?%s' % (baseURL, urllib.urlencode(opts))
        
        # Log URL we're using for debugging
        self.log.info("GoogleCSE URL: %s" % (searchURL))
        
        # Initialize result
        result = False
        
        try:
            response = utils.web.getUrl(searchURL, headers=headers).decode('utf8')
            
            data = json.loads(response)
            
            # Check if there was an error
            try:
                if data['error']:
                    message = data['error']['message']
                    self.log.info("GoogleCSE error: %s" % (message))
                    raise callbacks.Error(message)
            except KeyError:
                pass
            
            # Search results
            items = data['items']
            
            # Return the first link
            if items:
                result = items[0]['link']
        
        except utils.web.Error as e:
            self.log.error("GoogleCSE HTTPError: %s" % (str(e)))
        
        if result:
            irc.reply(result)
        else:
            irc.reply(_('No results'))
    
    g = wrap(g, ['text'])

Class = GoogleCSE


# vim:set shiftwidth=4 softtabstop=4 expandtab textwidth=79:
