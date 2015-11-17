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
    _ = PluginInternationalization('Inhibiter')
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
    conf.registerPlugin('Inhibiter', True)


Inhibiter = conf.registerPlugin('Inhibiter')

conf.registerChannelValue(Inhibiter, 'voiceChance',
                        registry.Integer(15, _("""0-100 chance to voice instead of kick""")))

conf.registerChannelValue(Inhibiter, 'collateralChance',
                        registry.Integer(0, _("""0-100 chance to inflict collateral damage""")))

conf.registerChannelValue(Inhibiter, 'opChance',
                        registry.Integer(30, _("""0-100 chance to op""")))

conf.registerChannelValue(Inhibiter, 'welcomeMessageCooldownInMinutes',
                        registry.Integer(60, _("""Wait X minutes before welcoming the same person""")))

conf.registerChannelValue(Inhibiter, 'actOfGodVoiceChance',
                        registry.Integer(20, _("""0-100 chance to randomly voice someone instead""")))

conf.registerChannelValue(Inhibiter, 'collateralTargets',
                         registry.CommaSeparatedListOfStrings([""], _("""Other nicks that will be kicked at random""")))

# vim:set shiftwidth=4 tabstop=4 expandtab textwidth=79:
