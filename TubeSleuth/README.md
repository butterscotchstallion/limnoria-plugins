# TubeSleuth #

Searches Youtube using their public API

## Using TubeSleuth ##

    !yt snoop dogg pump pump
    
### Example output ###

    https://youtu.be/q_6wNxMb6xU :: Snoop Dogg - Pump Pump feat. Lil Malik :: Duration: 00:04:41 :: Views: 188,448 :: Rating: 4.0

## Available Options ##

`template` - This is the template used when displaying search output.

Default value: `$link :: $title :: Duration: $duration :: Views: $view_count :: Rating: $rating`

`useBold` - Whether to bold the output

`noResultsMessage` - Reply when there are no results for a search. Default value: `No results for that query`

`safeSearch` - Whether to filter search results. Default value: `medium` Possible values: `none`, `moderate`, `strict`

`respondToPrivateMessages` - Whether to respond to private messages. Default value: `False`
