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
import supybot.ircmsgs as ircmsgs
import requests
import json

try:
    from supybot.i18n import PluginInternationalization
    _ = PluginInternationalization('Leafly')
except ImportError:
    # Placeholder that allows to run the plugin on a bot
    # without the i18n module
    _ = lambda x: x

class Leafly(callbacks.Plugin):
    """Uses Leafly API to retrieve information"""
    threaded = True

    def leafly(self, irc, msg, args, query):
        """
        Searches Leafly API based on user input
        """
        app_key = self.registryValue("appKey")
        app_id = self.registryValue("appID")
        response = None
        channel = msg.args[0]
        
        if not app_key or not app_id:
            irc.error("No Leafly appID/apiKey set!")
            self.log.error("No app id/api key set!")
            return
        
        api_url = "http://data.leafly.com/strains"
        
        headers = {
            "app_id": app_id,
            "app_key": app_key,
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.60 Safari/537.36"
        }
        
        data = json.dumps({
            "Page": 0,
            "Take": 1,
            "Search": query
        })
        
        request = requests.post(api_url, data=data, headers=headers)            
        ok = request.status_code == requests.codes.ok
        
        if ok:
            response = json.loads(request.text)
            
            if response:
                strains = response["Strains"]
                
                if len(strains) > 0:
                    strain_info = strains[0]
                    response = self.registryValue("template")
                    response = response.replace("$category", strain_info["Category"])
                    response = response.replace("$name", strain_info["Name"])
                    response = response.replace("$rating", str(strain_info["Rating"]))
                    response = response.replace("$permalink", strain_info["permalink"])
                    
                    """ Flavors """
                    flavors_list = []
                    strain_flavors = strain_info["Flavors"]
                    
                    for flavor in strain_flavors:
                        flavors_list.append(flavor["DisplayLabel"])
                    
                    response = response.replace("$flavors", ", ".join(flavors_list))
                    
                    """ Effects """
                    tag_list = []
                    strain_tags = strain_info["Tags"]
                    
                    for tag in strain_tags:
                        tag_list.append(tag["DisplayLabel"])
                    
                    response = response.replace("$tags", ", ".join(tag_list))
                else:
                    response = self.registryValue("noResultsMessage")
            else:
                self.log.error("Leafly: error decoding JSON response: %s" % request.text[:255])
        else:
            self.log.error("Leafly: status code %s - %s" % (request.status_code, request.text[:255]))
        
        if response is not None:
            irc.sendMsg(ircmsgs.privmsg(channel, response))
        else:
            irc.sendMsg(ircmsgs.privmsg(channel, self.registryValue("errorMessage")))
    
    leafly = wrap(leafly, ['text'])
    
Class = Leafly


# vim:set shiftwidth=4 softtabstop=4 expandtab textwidth=79:











