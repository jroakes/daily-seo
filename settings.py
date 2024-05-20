FEEDS = [
    "https://rss.app/feeds/AABZSamcHV77NMiB.csv",
    "https://rss.app/feeds/sAy6ZaKW7CpN7IjW.csv",
    "https://rss.app/feeds/L9TaZ7ef3KY1OVSp.csv",
    "https://rss.app/feeds/zXT0futnCJaljpuB.csv",
    "https://rss.app/feeds/4fqrhqQwdYetXIiu.csv",
    "https://rss.app/feeds/WM0ES6W8raiIV5KN.csv",
    "https://rss.app/feeds/oFcjPHjOF13DeGeb.csv",
    "https://rss.app/feeds/lqj3El87pV7U2x1x.csv",
    "https://rss.app/feeds/FAjw4Wfyj8afW97N.csv",
    "https://rss.app/feeds/Y9nhDTA9fNMlpu69.csv",
    "https://rss.app/feeds/1HNaz8LPmdTmbMBA.csv",
    "https://rss.app/feeds/Vju8BCZrred11RCR.csv",
    "https://rss.app/feeds/ceLARR5M4ZQbm0Qs.csv",
    "https://rss.app/feeds/x92LuoEdMz23kaxF.csv",
    "https://rss.app/feeds/MxtGb5DgBO0Sdq76.csv",
    "https://rss.app/feeds/jSFu20bgbRearGVA.csv",
    "https://rss.app/feeds/wu0i0iKh6ZPRGn3t.csv",
    "https://rss.app/feeds/Ejq27y98poTCOoAF.csv",
    "https://rss.app/feeds/klsS5hw8EqNpv6xh.csv",
    "https://rss.app/feeds/3Ke56kL7J38dQPUj.csv",
    "https://rss.app/feeds/qni1oWlODGZ8sqV5.csv",
]


DAYS_BACK = 3
BATCH_SIZE = 30
MODEL_NAME = "gemini-1.5-pro-latest"



CONSOLIDATE_PROMPT = """Please review the following JSON list of new web articles/posts and consolidate the items into a list of unique news stories organized by category.  Please pick a concise high-level category for each story and supply a title and description from the supplied articles.  Carefully select up to 3 source links from the articles/posts that are highly relevant to each story.  Each story MUST have at least one source link. DO NOT attempt to guess a source link URL.  Only use the provided links and do not attempt to infer them from the titles or descriptions. 

Articles to Review:
{content}

Output should be valid JSON with a list of story objects with the following keys:
- Title (string): Title of the story. Escape any quotes in title value.
- Category (string): Category of the story
- Description (string): Description of the story. Escape any quotes in description value.
- Links (array of strings): List of links to pages that discuss the same story

DO NOT use markdown formatting in your response; it will be interpreted as an error.  Ensure that you escape any quotes found within JSON values.

Valid JSON:
"""


REVIEW_PROMPT = """Please review the following articles and posts and curate a full list of interesting news events, news stories, or important updates relevant to digital marketing (SEO, paid marketing, social media, the internet).

Filter out:
* Promotional content (press releases, product announcements, company-specific achievements)
* Non-serious content
* Content not relevant to digital marketing
* Articles or Posts with missing or incomplete information

Examples of Promotional Content to Exclude:
* "Acme Corp launches new AI-powered ad targeting platform."
* "WidgetCo achieves record Q3 revenue growth."

Examples of News Content to Keep:
* "Google updates its search ranking algorithm with a focus on Core Web Vitals."
* "Facebook announces changes to its advertising policies regarding political content."

IMPORTANT: DO NOT attempt to guess link URLs. Only use the provided links and do not attempt to infer them from the titles or descriptions.

Content for review:
{content}

Output should be valid JSON. All items should be unique and contain full information. DO NOT use 'none', 'nan', 'null', or '' as a valid JSON value. The JSON should be an array of objects with the following keys:
- Title (string): Title of the article. Escape any quotes in title value.
- Description (string): Description of the article. Escape any quotes in description value.
- Link (string): Link to the content. Only use provided links; do not guess or infer URLs.

DO NOT use markdown formatting in your response; it will be interpreted as an error. Ensure that you escape any quotes found within JSON values.

Valid JSON:
"""


HTML_STYLE = """<style>
        body {
            background-color: #f5f5f5;
            color: #333;
        }
        nav {
            background-color: #333 !important;
        }
        .brand-logo {
            font-size: 2rem;
            font-weight: bold;
            animation: throb 3s infinite;
            background: linear-gradient(90deg, #ffeb3b, #fdd835);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        @keyframes throb {
            0%, 100% {
                opacity: 1;
            }
            50% {
                opacity: 0.5;
            }
        }
        .card {
            margin: 15px 0;
            padding: 10px;
        }
        .card-title {
            font-weight: bold;
        }
        .card-content {
            color: #000;
            padding: 10px;
        }
        .sources {
            list-style-type: none;
            padding: 0;
        }
        .sources li {
            margin-bottom: 5px;
        }
        .sources a {
            color: #0277bd;
            text-decoration: none;
            position: relative;
            padding-left: 20px;
        }
        .sources a::before {
            content: '→';
            color: #fdd835;
            margin-right: 10px;
            font-weight: bold;
            text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.5);
        }
        .container {
            max-width: 100%;
        }
        h1 {
            color: #333;
            margin-top: 40px;
            text-align: center;
            text-decoration: underline;
            text-decoration-color: #fdd835;
            margin-bottom: 10px;
            text-underline-offset: 10px;
        }
        .date {
            color: rgba(0, 0, 0, 0.6);
            font-size: 2rem;
            text-align: center;
            margin-bottom: 60px;
        }
        h2 {
            color: #0288d1;
            margin-top: 40px;
            font-size: 3rem;
            text-decoration: underline;
            text-decoration-style: dashed;
            text-decoration-color: #fdd835;
            text-underline-offset: 10px;
        }
        h5 {
            margin-top: 20px;
            color: #333;
        }
        footer {
            margin-top: 40px;
            padding: 20px;
            background-color: #e0e0e0;
            text-align: center;
        }
        </style>"""
