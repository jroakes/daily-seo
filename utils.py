import os
import json
from datetime import datetime
from loguru import logger
from settings import HTML_STYLE


def generate_html(data: list[dict], date: datetime) -> str:
    """
    Generates an HTML string based on the provided data and date.

    Parameters:
    data (list[dict]): List of data dictionaries to be included in the HTML.
    date (datetime): The date for the HTML content.

    Returns:
    str: Generated HTML content.
    """
    if not data:
        logger.warning("No valid data to display.")
        return "<html><body><h1>No valid data to display</h1></html></body>"

    pretty_date = date.strftime("%B %d, %Y")
    html = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <link rel="icon" href="/daily-seo-logo.png">
        <title>DailySEO Updates - {pretty_date}</title>
        <link href="https://cdnjs.cloudflare.com/ajax/libs/materialize/1.0.0/css/materialize.min.css" rel="stylesheet">
        {HTML_STYLE}
    </head>
    <body>
        <nav>
        <div class="nav-wrapper">
            <a href="#" class="brand-logo center">DailySEO</a>
        </div>
        </nav>
        <div class="container">
        <h1>Latest Updates</h1>
        <div class="date">{pretty_date}</div>
    """

    categories = set(item["Category"] for item in data)
    for category in categories:
        html += f"<h2>{category}</h2>"
        html += '<div class="row">'
        for item in data:
            if item["Category"] == category:
                sources = "".join(
                    f'<li><a href="{link}" target="_blank">↗ Read on {link.split("/")[2]}</a></li>'
                    for link in item["Links"]
                )
                html += f"""
        <div class="col s12">
            <div class="card blue-grey lighten-4">
            <div class="card-content">
                <span class="card-title">{item['Title']}</span>
                <p>{item['Description']}</p>
                <h5>Sources:</h5>
                <ul class="sources">
                    {sources}
                </ul>
            </div>
            </div>
        </div>
        """
        html += "</div>"

    html += """
        </div>
        <footer>
        <p>Content generated by AI using Google Gemini. Updated from various sources every four hours.</p>
        <p>For suggestions of new sources, please email <a href="mailto:jroakes@gmail.com">jroakes@gmail.com</a>.</p>
        <p>Feel free to build your own version by cloning <a href="https://github.com/jroakes/daily-seo" target="_blank">this repository</a>.</p>
        </footer>
        <script src="https://cdnjs.cloudflare.com/ajax/libs/materialize/1.0.0/js/materialize.min.js"></script>
    </body>
    </html>
    """
    logger.info("HTML content generated successfully.")
    return html


def save_html(html_content: str, filename: str = "docs/index.html") -> None:
    """
    Saves the provided HTML content to a specified file.

    Parameters:
    html_content (str): The HTML content to be saved.
    filename (str): The file name where the content will be saved (default is "docs/index.html").
    """
    try:
        with open(filename, "w") as file:
            file.write(html_content)
        logger.info(f"HTML content saved to {filename}.")
    except Exception as e:
        logger.error(f"Failed to save HTML content: {e}")


def save_json(data: dict, filename: str) -> None:
    """
    Saves the provided data to a specified JSON file.

    Parameters:
    data (dict): The data to be saved.
    filename (str): The file name where the data will be saved.
    """
    try:
        with open(filename, "w") as file:
            json.dump(data, file, indent=4)
        logger.info(f"Data saved to JSON file {filename}.")
    except Exception as e:
        logger.error(f"Failed to save JSON data: {e}")


def load_json(filename: str) -> dict:
    """
    Loads data from a specified JSON file.

    Parameters:
    filename (str): The file name from which to load the data.

    Returns:
    dict: Loaded data from the JSON file.
    """
    if os.path.exists(filename):
        try:
            with open(filename, "r") as file:
                data = json.load(file)
            logger.info(f"Data loaded from JSON file {filename}.")
            return data
        except Exception as e:
            logger.error(f"Failed to load JSON data: {e}")
            return {}
    else:
        logger.warning(f"JSON file {filename} does not exist.")
        return {}
