###
# Copyright (c) 2015, lunchdump
# All Rights Reserved
#
###


import supybot.conf as conf
import supybot.registry as registry
try:
    from supybot.i18n import PluginInternationalization
    _ = PluginInternationalization('RelevantGif')
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
    conf.registerPlugin('RelevantGif', True)


Giphy = conf.registerPlugin('RelevantGif')

conf.registerGlobalValue(Giphy, 'template',
     registry.String("$url", _("""Template for the output of a search query.""")))

conf.registerGlobalValue(Giphy, 'noResultsMessage',
     registry.String("No results for that query.", _("""This message is sent when there are no results""")))

# vim:set shiftwidth=4 tabstop=4 expandtab textwidth=79:
