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
    
    def yt(self, irc, msg, args, query):
        """Queries Youtube API"""
        baseURL = self.registryValue('baseURL')
        noResultsMessage = self.registryValue('noResultsMessage')
        useBold = self.registryValue('useBold')
        safeSearch = self.registryValue('safeSearch')
        
        opts = {'q': query, 
                'alt': 'json', 
                'v': 2, 
                'max-results': 1,
                'safeSearch': safeSearch}
        
        searchURL = '%s?%s' % (baseURL, urllib.urlencode(opts))
        
        self.log.info("TubeSleuth URL: %s" % (searchURL))
        
        result = False
        
        try:
            response = utils.web.getUrl(searchURL).decode('utf8')
            
            data = json.loads(response)
            
            # Check if we have any results
            try:
                # Maximum of one result, so the first one is the video
                entries = data['feed']['entry']
                
                if entries:
                    video = entries[0]
                    id = video["media$group"]['yt$videoid']['$t']
                    title = video['title']['$t']
                    
                    if useBold and title:
                        title = ircutils.bold(title)
                    
                    result = "https://youtu.be/%s :: %s" % (id, title)
                    
                    # Attempt to get views. Not all videos provide this information
                    try:
                        views = video['yt$statistics']['viewCount']
                        
                        # If views are available, format with commas
                        if views:
                            formattedViews = '{:,}'.format(int(views))
                            
                            if useBold and formattedViews:
                                formattedViews = ircutils.bold(formattedViews)
                            
                            result = "%s :: Views: %s" % (result, formattedViews)
                            
                    except KeyError, e:
                        self.log.info("TubeSleuth: failed to get views for %s" % (title))
                    
                    # Attempt to get rating
                    try:
                        stringRating = video["gd$rating"]["average"]                        
                        rating = round(int(stringRating), 2)
                        
                        if useBold and rating:
                            rating = ircutils.bold(rating)
                        
                        result = "%s :: Rating: %s" % (result, rating)
                    
                    except KeyError, e:
                        self.log.info("TubeSleuth: failed to get rating for %s" % (title))
                    
            except KeyError, e:
                self.log.info(e)
            
        except Exception, err:
            self.log.error(str(err))
        
        if result:
            irc.reply(result)
        else:
            irc.reply(noResultsMessage)
        
    yt = wrap(yt, ['text'])

Class = TubeSleuth


# vim:set shiftwidth=4 softtabstop=4 expandtab textwidth=79:
