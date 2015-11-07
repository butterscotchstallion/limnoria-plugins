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
    _ = PluginInternationalization('Ericpedia')
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
    conf.registerPlugin('Ericpedia', True)


Ericpedia = conf.registerPlugin('Ericpedia')
# This is where your configuration variables (if any) should go.  For example:
conf.registerChannelValue(Ericpedia, 'replaceString',
    registry.String("Eric", _("""Replaces random part of the title with this string or $nick for the nick of the person issuing the command.""")))

conf.registerChannelValue(Ericpedia, 'wikipediaRandomPageURL',
    registry.String("https://en.wikipedia.org/wiki/Special:Random", _("""URL used to find a random Wikipedia page""")))

# vim:set shiftwidth=4 tabstop=4 expandtab textwidth=79:
