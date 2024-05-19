import os
import re
import pandas as pd
import google.generativeai as genai
import json
from datetime import datetime, timedelta
from dotenv import load_dotenv
from loguru import logger
from tqdm.auto import tqdm

from utils import save_json, load_json, generate_html, save_html, save_generation_error
from settings import REVIEW_PROMPT, CONSOLIDATE_PROMPT, FEEDS, DAYS_BACK, BATCH_SIZE

load_dotenv()


def configure_genai(api_key: str) -> None:
    """
    Configures the Google Generative AI with the provided API key.

    Parameters:
    api_key (str): The API key for Google Generative AI.
    """
    genai.configure(api_key=api_key)


def get_and_filter_feeds(
    feeds: list[str], reviewed_urls: list[str], days: int = 1
) -> pd.DataFrame:
    """
    Retrieves and filters feed data, excluding already reviewed URLs and limiting results to the specified number of days.

    Parameters:
    feeds (list[str]): List of feed URLs.
    reviewed_urls (list[str]): List of already reviewed URLs.
    days (int): Number of days to filter data (default is 1).

    Returns:
    pd.DataFrame: Filtered DataFrame containing the feed data.
    """
    logger.info("Reading and filtering feeds...")
    dfs = [pd.read_csv(feed) for feed in feeds]
    df = pd.concat(dfs)

    df["Date"] = pd.to_datetime(df["Date"]).dt.tz_localize(None)

    now = datetime.now()
    before = now - timedelta(days=days)
    df = df[(df["Date"] >= before) & (df["Date"] <= now)]

    df = df.sort_values(by="Date", ascending=False).drop_duplicates()
    df["Date"] = df["Date"].dt.strftime("%Y-%m-%d")

    df["Plain Description"] = df["Plain Description"].fillna("")
    df["Description"] = df["Description"].fillna(df["Plain Description"])

    # Limit description to reasonable length
    df["Description"] = df["Description"].str[:1000]
    df = df.drop(columns=["Plain Description"])

    df = df[~df["Link"].isin(reviewed_urls)]
    df = df.drop_duplicates(subset=["Title", "Link"])
    df = df[
        df["Description"].str.strip().astype(bool)
        | df["Link"].str.contains("twitter.com|x.com")
    ]

    logger.info(f"Filtered {len(df)} articles from feeds.")
    return df


def format_df(df: pd.DataFrame) -> str:
    """
    Formats the DataFrame into a string with specific columns.

    Parameters:
    df (pd.DataFrame): DataFrame to be formatted.

    Returns:
    str: Formatted string representation of the DataFrame.
    """
    output = [
        f"{row.Title}\n{row.Date}\n{row.Description}\nSource: {row.Link}"
        for row in df.itertuples()
    ]
    return "\n--------------------\n".join(output)


def generate_content(prompt: str) -> dict | None:
    """
    Generates content based on the provided prompt using Google Generative AI.

    Parameters:
    prompt (str): The prompt to generate content from.

    Returns:
    dict | None: Generated content in JSON format, or None if an error occurs.
    """
    generation_config = {"temperature": 0.1, "max_output_tokens": 8192}
    model = genai.GenerativeModel(
        "gemini-1.5-pro-latest", generation_config=generation_config
    )
    response = model.generate_content(prompt)

    try:
        data = json.loads(re.sub(r"```(?:json)?\n|```", "", response.text))

        if not isinstance(data, list):
            logger.error(f"Invalid response from API")
            # Send prompt to error log
            save_generation_error("PROMPT: \n" + prompt)
            # Send response to error log    
            save_generation_error("RESPONSE: \n" + response.text)
            return None

        return data


    except json.JSONDecodeError as e:

        logger.error(f"JSON decode error: {e}")
        # Send prompt to error log
        save_generation_error("PROMPT: \n" + prompt)
        # Send response to error log    
        save_generation_error("RESPONSE: \n" + response.text)

    except ValueError as e:
        logger.error(f"API Value error: {e}")

    return None


def main() -> None:
    """
    Main function to configure the AI, load and process feed data, generate new content, and save the output as HTML and JSON files.
    """
    logger.info("Starting the process...")

    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        logger.error(
            "Google API key not set. Please set the GOOGLE_API_KEY environment variable."
        )
        raise ValueError(
            "Google API key not set. Please set the GOOGLE_API_KEY environment variable."
        )

    configure_genai(api_key)

    date = datetime.now()
    json_filename = f"data/data_{date.strftime('%Y_%m_%d')}.json"

    if os.path.exists(json_filename):
        cache = load_json(json_filename)
        valid_articles = cache.get("valid_articles", [])
        reviewed_urls = cache.get("reviewed_urls", [])
    else:
        valid_articles = []
        reviewed_urls = []

    reviewed_titles = {item["Title"] for item in valid_articles}

    df = get_and_filter_feeds(FEEDS, reviewed_urls, days=DAYS_BACK)

    if df.empty:
        logger.info("No new articles found. Exiting.")
        return

    reviewed_urls.extend(df["Link"].tolist())

    total_rows = len(df)
    batches = [df[i : i + BATCH_SIZE] for i in range(0, total_rows, BATCH_SIZE)]

    for batch in tqdm(batches, desc="Processing batches", total=len(batches)):
        feed_text = format_df(batch)
        review_prompt = REVIEW_PROMPT.format(content=feed_text)
        reviewed_articles = generate_content(review_prompt)

        if reviewed_articles:
            for item in reviewed_articles:
                if item["Title"] not in reviewed_titles:
                    valid_articles.append(item)

    # Check if any articles were found
    if not valid_articles:
        logger.info("No valid articles found. Exiting.")
        return

    consolidate_prompt = CONSOLIDATE_PROMPT.format(
        content=json.dumps(valid_articles, indent=2)
    )
    consolidated_data = generate_content(consolidate_prompt)

    if not consolidated_data:
        logger.error("Failed to generate consolidated data.")
        return

    cache = {"valid_articles": valid_articles, "reviewed_urls": reviewed_urls}
    save_json(cache, json_filename)

    html_output = generate_html(consolidated_data, date)
    save_html(html_output)

    logger.info("Process completed successfully.")


if __name__ == "__main__":
    main()