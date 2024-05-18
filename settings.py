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


PROMPT = """Please review the following new content and combine it into a concise list of core events, news items, or important updates.

Guidelines:
1. Ignore promotional or non-serious content.
2. Be thorough and include as many new items as possible, but avoid duplication with existing content.
3. Only keep items relevant to digital marketing, including SEO, paid marketing, and the internet.
4. Choose the best example when multiple items cover the same news item or event. Don't cover the same story twice.
5. Provide a link to the source of the content.
6. Do not include any markdown formatting in your response; it will be interpreted as an error.
7. Do not add new items if they are already covered in the existing titles.
8. Keep categories high-level and simple. Do not use multiple areas for the same category (e.g., "Search & AI"). Choose the best category.

Existing titles and categories:
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
