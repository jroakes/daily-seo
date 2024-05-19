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


PROMPT = """Please review the following new content and combine it into a concise list of unique news events, news stories, or important updates.

Guidelines you must follow:
1. Ignore promotional and non-serious content. Keep only important news and events about respected companies.
2. Only keep items relevant to digital marketing, including SEO, paid marketing, social, and the internet.
3. The link must be a valid URL and come from the source provided in the content. DO NOT attepmt to guess a link URL.
4. Do not include any markdown formatting in your response; it will be interpreted as an error.
5. Keep categories high-level and simple. Do not use multiple areas for the same category (e.g., "Search & AI"). Choose the best category.
6. DO NOT repeat headlines covering the same event or news story. If the story is covered in the existing titles, omit it when reviewing new content.
7. If different titles covering the same news item are found in the new content, pick only one.  NEVER output a new item that is covered in the existing content or prior in the new content.
8. Prioritize newer content over older.  

Existing content:
{existing_data}

New content for review:
{content}

Output should be valid JSON with a list of objects with the following keys:
- Title
- Category
- Description
- Link

Valid JSON:
"""


DAYS_BACK = 3
