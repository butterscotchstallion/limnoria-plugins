###
# Copyright (c) 2015, butterscotchstallion
# All rights reserved.
#
#
###

import supybot.conf as conf
import supybot.registry as registry
try:
    from supybot.i18n import PluginInternationalization
    _ = PluginInternationalization('Leafly')
except:
    # Placeholder that allows to run the plugin on a bot
    # without the i18n module
    _ = lambda x: x


def configure(advanced):
    # This will be called by supybot to configure this module.  advanced is
    # a bool that specifies whether the user identified themself as an advanced
    # user or not.  You should effect your configuration by manipulating the
    # registry as appropriate.
    from supybot.questions import expect, anything, something, yn
    conf.registerPlugin('Leafly', True)


Leafly = conf.registerPlugin('Leafly')

conf.registerGlobalValue(Leafly, 'appID',
     registry.String("", _("""App ID""")))

conf.registerGlobalValue(Leafly, 'appKey',
     registry.String("", _("""App key""")))

conf.registerGlobalValue(Leafly, 'template',
     registry.String("[$category] $name ($rating) :: Flavors: $flavors :: Effects: $tags :: $permalink", _("""Display template""")))

conf.registerGlobalValue(Leafly, 'errorMessage',
     registry.String("Lookup failed. Try !g leafly blue dream", _("""Message to display if something went wrong.""")))

conf.registerGlobalValue(Leafly, 'noResultsMessage',
     registry.String("No results for that query.", _("""Message to display if there were no results.""")))
     
     
     
     
     
     
     
     
     
     
     
     
# vim:set shiftwidth=4 tabstop=4 expandtab textwidth=79:
