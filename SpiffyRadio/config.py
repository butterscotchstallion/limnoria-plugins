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
    _ = PluginInternationalization('SpiffyRadio')
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
    conf.registerPlugin('SpiffyRadio', True)


SpiffyRadio = conf.registerPlugin('SpiffyRadio')

conf.registerGlobalValue(SpiffyRadio, 'icecastAPIURL', 
    registry.String("", _("""Icecast API URL""")))

conf.registerGlobalValue(SpiffyRadio, 'nowPlayingTemplate', 
    registry.String("Now playing $artist - $title ($listeners listeners) :: Tune in: $listenurl", _("""Template used for np command""")))

conf.registerGlobalValue(SpiffyRadio, 'autoAnnounceChannels', 
    registry.CommaSeparatedListOfStrings([], _("""Auto announce new tracks to these channels""")))

conf.registerGlobalValue(SpiffyRadio, 'autoAnnounceNewTracks', 
    registry.Boolean(False, _("""Whether to announce new tracks when detected. Use in conjunction with pollingIntervalInSeconds.""")))

conf.registerGlobalValue(SpiffyRadio, 'pollingIntervalInSeconds', 
    registry.PositiveInteger (30, _("""Interval in seconds to poll the API for track changes""")))

conf.registerGlobalValue(SpiffyRadio, 'errorMessage', 
    registry.String("Error retrieving current track.", _("""This message is used if there is a problem reaching the API""")))

# vim:set shiftwidth=4 tabstop=4 expandtab textwidth=79:
