###
# Copyright (c) 2015, PrgmrBill
# All rights reserved.
#
#
###

import supybot.conf as conf
import supybot.registry as registry
try:
    from supybot.i18n import PluginInternationalization
    _ = PluginInternationalization('GoogleCSE')
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
    conf.registerPlugin('GoogleCSE', True)

GoogleCSE = conf.registerPlugin('GoogleCSE')

# Google API key. Required.
conf.registerGlobalValue(GoogleCSE, 'apiKey',
     registry.String("", _("""Google API key""")))

# Google search engine ID. Required.
conf.registerGlobalValue(GoogleCSE, 'searchEngineID',
     registry.String("", _("""Google search engine ID""")))

# Safe search filter.
conf.registerGlobalValue(GoogleCSE, 'searchFilter',
     registry.String("medium", _("""Safe search filter""")))

# This is the baseURL used, verbatim. No protocols are prepended.
# I set it up this way so that if the URL needs to change in the future
# for some reason, it would be easy to do that.
conf.registerGlobalValue(GoogleCSE, 'baseURL',
     registry.String("https://www.googleapis.com/customsearch/v1", _("""Base search URL including protocol.""")))

conf.registerGlobalValue(GoogleCSE, 'useBold',
     registry.Boolean(False, _("""Use bold in replies""")))

conf.registerGlobalValue(GoogleCSE, 'noResultsMessage',
     registry.String("No results for that query.", _("""Message to send when there are no results""")))
     
     
     
     
     
     
     
     
     
     
     
# vim:set shiftwidth=4 tabstop=4 expandtab textwidth=79:
