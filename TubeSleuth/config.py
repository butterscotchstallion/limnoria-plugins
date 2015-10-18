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
    _ = PluginInternationalization('TubeSleuth')
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
    conf.registerPlugin('TubeSleuth', True)

TubeSleuth = conf.registerPlugin('TubeSleuth')

conf.registerGlobalValue(TubeSleuth, 'developerKey',
     registry.String("", _("""Google API key. Required.""")))

conf.registerGlobalValue(TubeSleuth, 'sortOrder',
     registry.String("relevance", _("""The order parameter specifies the method that will be used to order resources in the API response.""")))
     
conf.registerGlobalValue(TubeSleuth, 'template',
     registry.String("$yt_logo $link :: $title", _("""Template used for search result replies""")))

conf.registerGlobalValue(TubeSleuth, 'useBold',
     registry.Boolean(False, _("""Use bold in replies""")))

conf.registerGlobalValue(TubeSleuth, 'noResultsMessage',
     registry.String("No results for that query", _("""Message reply when there are no results""")))

conf.registerGlobalValue(TubeSleuth, 'safeSearch',
     registry.String("moderate", _("""Safe search filtering: none, moderate, strict""")))

conf.registerGlobalValue(TubeSleuth, 'respondToPrivateMessages',
     registry.Boolean(False, _("""Whether the bot should respond to this command in private messages""")))

# vim:set shiftwidth=4 tabstop=4 expandtab textwidth=79:
