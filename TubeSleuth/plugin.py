###
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
import urllib
import json

try:
    from supybot.i18n import PluginInternationalization
    _ = PluginInternationalization('TubeSleuth')
except ImportError:
    # Placeholder that allows to run the plugin on a bot
    # without the i18n module
    _ = lambda x: x

class TubeSleuth(callbacks.Plugin):
    threaded = True
    callBefore = ['Web']

    def yt(self, irc, msg, args, query):
        """Queries Youtube API"""
        baseURL = self.registryValue('baseURL')
        noResultsMessage = self.registryValue('noResultsMessage')
        headers = dict(utils.web.defaultHeaders)
        
        opts = {'q': query, 'alt': 'json', 'v': 2, 'max-results': 1}
        
        searchURL = '%s?%s' % (baseURL, urllib.urlencode(opts))
        
        self.log.info("TubeSleuth URL: %s" % (searchURL))
        
        result = False
        
        try:
            response = utils.web.getUrl(searchURL, headers=headers).decode('utf8')
            
            data = json.loads(response)
            
            # Check if we have any results
            try:
                # Maximum of one result, so the first one is the video
                entries = data['feed']['entry']
                
                if entries:
                    video = entries[0]
                    id = video["media$group"]['yt$videoid']['$t']
                    title = video['title']['$t']
                    
                    result = "https://youtu.be/%s - %s" % (id, title)
                    
            except KeyError as e:
                self.log.info(str(e))
                
                pass
            
        except:
            self.log.error("TubeSleuth HTTP error")
        
        if result:
            irc.reply(result)
        else:
            irc.reply(_(noResultsMessage))
        
    yt = wrap(yt, ['text'])

Class = TubeSleuth


# vim:set shiftwidth=4 softtabstop=4 expandtab textwidth=79:
