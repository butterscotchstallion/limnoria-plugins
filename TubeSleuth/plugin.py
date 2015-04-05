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
        base_url = self.registryValue('baseURL')
        no_results_message = self.registryValue('noResultsMessage')
        use_bold = self.registryValue('useBold')
        safe_search = self.registryValue('safeSearch')
        
        opts = {'q': query, 
                'alt': 'json', 
                'v': 2, 
                'max-results': 1,
                'safeSearch': safe_search}
        
        search_url = '%s?%s' % (base_url, urllib.urlencode(opts))
        
        self.log.info("TubeSleuth URL: %s" % (search_url))
        
        result = False
        
        try:
            response = utils.web.getUrl(search_url).decode('utf8')
            
            data = json.loads(response)
            
            # Check if we have any results
            try:
                # Maximum of one result, so the first one is the video
                entries = data['feed']['entry']
                
                if entries:
                    video = entries[0]
                    id = video["media$group"]['yt$videoid']['$t']
                    title = video['title']['$t']
                    
                    if use_bold and title:
                        title = ircutils.bold(title)
                    
                    result = "https://youtu.be/%s :: %s" % (id, title)
                    
                    # Attempt to get views. Not all videos provide this information
                    try:
                        views = video['yt$statistics']['viewCount']
                        
                        # If views are available, format with commas
                        if views:
                            formatted_views = '{:,}'.format(int(views))
                            
                            if use_bold and formatted_views:
                                formatted_views = ircutils.bold(formatted_views)
                            
                            result = "%s :: Views: %s" % (result, formatted_views)
                            
                    except KeyError, e:
                        self.log.info("TubeSleuth: failed to get views for %s" % (title))
                    
                    # Attempt to get rating
                    try:
                        json_rating = video["gd$rating"]["average"]                        
                        rating = round(int(json_rating), 2)
                        
                        if use_bold and rating:
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
            irc.reply(no_results_message)
        
    yt = wrap(yt, ['text'])

Class = TubeSleuth


# vim:set shiftwidth=4 softtabstop=4 expandtab textwidth=79:
