## daily-seo

## About

Uses Gemini Model to auto-curate content from 20+ individual user and website feeds.  Feeds are setup using the rss.app tool because it supports pulling Twitter posts for provided users.  Script runs with a github action every four hours.


# To Use
If you want to create your own feed, here are the general untested directions.

1. Setup your own feeds in rss.app.  [rss.app](https://rss.app) converts the feeds to CSV which makes them really easy to import.  RSS App costs about $20 per month.
2. Clone this repository.
3. Update the settings.py file with your own feeds, and optionally tweak the PROMPT text.
4. Update the styles and HTML in script.py to your liking.
5. You will need to add your Google GenerativeAI API key to this Action secret in settings (GOOGLE_API_KEY).
6. You will need to modify action permissions to allow them to read AND write to your repo.
7. Set Github Pages to read out of the /docs folder.
8. The script should run automatically every 4 hours if you set up correctly.

Optionally, you can set up a custom domain to point to your site, or you can use the default sub-domain option.

