Radio information for Icecast 2 streams

## Commands

`!np` - Shows the currently playing track

## Available options

`supybot.plugins.SpiffyRadio.icecastAPIURL` - This URL is queried to get track information.

`supybot.plugins.SpiffyRadio.nowPlayingTemplate` - This template is used to display track information

Default value: `Now playing $artist - $title ($listeners listeners) :: Tune in: $listenurl`

`supybot.plugins.SpiffyRadio.pollingIntervalInSeconds` - Poll API every X seconds

`supybot.plugins.SpiffyRadio.autoAnnounceNewTracks` - Whether to announce new tracks (Boolean)

`supybot.plugins.SpiffyRadio.autoAnnounceChannels` - Comma separated list of channels to which to announce. No spaces.

Example: `!config supybot.plugins.SpiffyRadio.autoAnnounceChannels #foo,#bar`

`supybot.plugins.SpiffyRadio.errorMessage` - This message is displayed when there is a problem reaching the API.