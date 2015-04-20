# TubeSleuth #

Searches Youtube using [Youtube Data API (v3)](https://developers.google.com/youtube/v3/)

## Using TubeSleuth ##

- [Get a developer key](https://code.google.com/apis/youtube/dashboard/gwt/index.html#settings)
- Load TubeSleuth: `!load TubeSleuth`
- Set the key

    `!config set config supybot.plugins.TubeSleuth.developerKey someDeveloperKeyHere`

- Try it

    `!yt snoop dogg pump pump`

### Example output ###

    https://youtu.be/q_6wNxMb6xU :: Snoop Dogg - Pump Pump feat. Lil Malik

## Available Options ##

`template` - This is the template used when displaying search output.

Default value: `$link :: $title`

`sortOrder` - The order parameter specifies the method that will be used to order resources in the API response. Default value: `relevance`

`useBold` - Whether to bold the output. Default value: `False`

`noResultsMessage` - Reply when there are no results for a search. Default value: `No results for that query`

`safeSearch` - Whether to filter search results. Default value: `medium` Possible values: `none`, `moderate`, `strict`

`respondToPrivateMessages` - Whether to respond to private messages. Default value: `False`

### Note ###

- As of April 20th 2015 [the v2 API was deprecated](https://developers.google.com/youtube/2.0/developers_guide_protocol_deprecated)

### Upgrading from version 2 API ###

- Set your API key as noted at the top
- Update your template: `!config supybot.plugins.TubeSleuth.template $link :: $title`











