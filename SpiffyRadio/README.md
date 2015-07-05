Radio information for Icecast 2 streams

## Install and load SpiffyRadio
- `git clone https://github.com/prgmrbill/limnoria-plugins.git`
- `cd limnoria-plugins`
- `cp -r SpiffyRadio ~/your_bot_directory/plugins`
- `cd ~/your_bot_directory/plugins/SpiffyRadio`
- `pip install -r requirements.txt --user --upgrade`
- `!load SpiffyRadio`

## Configure SpiffyRadio

There is only one option that you are required to set, which is the stream API URL.

`!config supybot.plugins.SpiffyRadio.icecastAPIURL http://example.com:8000/status-json.xsl`

If you would like the bot to announce new tracks automatically, set the announce channels:

`!config supybot.plugins.SpiffyRadio.autoAnnounceChannels #foo`

You can also change how often the API is polled for new tracks. The default is 30 seconds, which 
should be sufficient.

`!config supybot.plugins.SpiffyRadio.pollingIntervalInSeconds 30`

## Commands

`!np` - Shows the currently playing track.

## Available options

`supybot.plugins.SpiffyRadio.icecastAPIURL` - This URL is queried to get track information.

`supybot.plugins.SpiffyRadio.nowPlayingTemplate` - This template is used to display track information

Default value: `Now playing $artist - $title ($listeners listeners) :: Tune in: $listenurl`

`supybot.plugins.SpiffyRadio.pollingIntervalInSeconds` - Poll API every X seconds

`supybot.plugins.SpiffyRadio.autoAnnounceNewTracks` - Whether to announce new tracks (Boolean)

`supybot.plugins.SpiffyRadio.autoAnnounceChannels` - Comma separated list of channels to which to announce. No spaces.

Example: `!config supybot.plugins.SpiffyRadio.autoAnnounceChannels #foo,#bar`

`supybot.plugins.SpiffyRadio.errorMessage` - This message is displayed when there is a problem reaching the API.