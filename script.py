import pandas as pd
import google.generativeai as genai
import json
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv

from utils import save_json, load_json, generate_html, save_html
from settings import PROMPT, FEEDS

load_dotenv()


def configure_genai(api_key: str) -> None:
    """
    Configures the Google Generative AI with the provided API key.

    Parameters:
    api_key (str): The API key for Google Generative AI.
    """
    genai.configure(api_key=api_key)


def get_and_filter_feeds(
    feeds: list[str], processed_urls: list[str], days: int = 1
) -> pd.DataFrame:
    """
    Retrieves and filters feed data, excluding already processed URLs and limiting results to the specified number of days.

    Parameters:
    feeds (list[str]): List of feed URLs.
    processed_urls (list[str]): List of already processed URLs.
    days (int): Number of days to filter data (default is 1).

    Returns:
    pd.DataFrame: Filtered DataFrame containing the feed data.
    """
    dfs = [pd.read_csv(feed) for feed in feeds]
    df = pd.concat(dfs)
    df["Date"] = pd.to_datetime(df["Date"])

    # Ensure 'Date' column is timezone-naive for comparison
    df["Date"] = df["Date"].dt.tz_localize(None)

    now = datetime.now()
    before = now - timedelta(days=days)

    df = df[(df["Date"] >= before) & (df["Date"] <= now)]
    df = df.sort_values(by="Date", ascending=False).drop_duplicates()
    df["Date"] = df["Date"].dt.strftime("%Y-%m-%d")
    df["Description"] = df["Description"].fillna(df["Plain Description"])
    df = df.drop(columns=["Plain Description"])

    # Filter out already processed URLs
    df = df[~df["Link"].isin(processed_urls)]

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
    generation_config = {"temperature": 0.1, "max_output_tokens": 4000}
    model = genai.GenerativeModel(
        "gemini-1.5-pro-latest", generation_config=generation_config
    )
    response = model.generate_content(prompt)

    try:
        return json.loads(response.text)
    except json.JSONDecodeError as e:
        print("JSON decode error:", e)
        return None


def main() -> None:
    """
    Main function to configure the AI, load and process feed data, generate new content, and save the output as HTML and JSON files.
    """
    # API key should be set as an environment variable for security
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError(
            "Google API key not set. Please set the GOOGLE_API_KEY environment variable."
        )

    configure_genai(api_key)

    # Load existing data and processed URLs for the day
    date = datetime.now()
    json_filename = f"data/data_{date.strftime('%Y_%m_%d')}.json"

    # Check if the JSON file for today exists
    if os.path.exists(json_filename):
        cache = load_json(json_filename)
        existing_data = cache.get("existing_data", [])
        processed_urls = cache.get("processed_urls", [])
    else:
        existing_data = []
        processed_urls = []

    existing_titles = {item["Title"] for item in existing_data}
    existing_data_df = pd.DataFrame(existing_data)

    # Limit existing_data_df to Title and Category
    if not existing_data_df.empty:
        existing_data_df = existing_data_df[["Title", "Category"]]

    df = get_and_filter_feeds(FEEDS, processed_urls)
    feed_text = format_df(df)

    formatted_prompt = PROMPT.format(
        existing_data=existing_data_df.to_markdown(), content=feed_text
    )

    # Log the formatted prompt to a file:
    with open("prompt.txt", "w") as file:
        file.write(formatted_prompt)

    new_data = generate_content(formatted_prompt)

    # Append new items to the existing data
    if new_data:
        for item in new_data:
            if item["Title"] not in existing_titles:
                existing_data.append(item)
                processed_urls.append(item["Link"])

    # Save the updated data and processed URLs to the JSON file for today
    cache = {"existing_data": existing_data, "processed_urls": processed_urls}
    save_json(cache, json_filename)

    html_output = generate_html(existing_data, date)
    save_html(html_output)


if __name__ == "__main__":
    main()
