# Leafly

Queries Leafly API to retrieve information. This plugin requires a free app key/app id. You can [sign up for one
here](https://developer.leafly.com/signup)

Once you've signed up, you'll need your `app_key` and `app_id` which will be used to query the Leafly API.

## Install Leafly

- `git clone https://github.com/prgmrbill/limnoria-plugins.git`
- `cd limnoria-plugins`
- `cp -r Leafly ~/your_bot_directory/plugins`
- `cd ~/your_bot_directory/plugins/Leafly`
- `pip install -r requirements.txt --user --upgrade`
- `!load Leafly`
- `!config supybot.plugins.Leafly.appKey your_app_key_here`
- `!config supybot.plugins.Leafly.appID your_app_id_here`

## Using Leafly

### Searching

`!leafly blue dream`

### Other options

`template` - This determines what the output looks like.

Default value: `[$category] $name ($rating) :: Flavors: $flavors :: Effects: $tags :: $permalink`

`errorMessage` - This message is used if something goes wrong. This is typically when your API quota has been exceeded.

Default value: `Lookup failed. Try !g leafly blue dream` 

*Pro Tip* Use this plugin in conjunction with [GoogleCSE](https://github.com/prgmrbill/limnoria-plugins/tree/master/GoogleCSE) to provide a fallback in this scenario.

`noResultsMessage` - This message is used if there were no results.

Default value: `No results for that query.`

