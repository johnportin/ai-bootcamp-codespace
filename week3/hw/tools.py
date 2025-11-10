import requests
from pydantic import BaseModel
from typing import List

HEADERS = {
    "User-Agent": "JohnPortin-AI-Agent/1.0 (https://github.com/johnportin; contact: johnportin@example.com)"
}

class SearchWikipediaTitlesArgs(BaseModel):
    query: str
    limit: int = 5

def search_wikipedia_titles(args: SearchWikipediaTitlesArgs) -> List[str]:
    url = "https://en.wikipedia.org/w/api.php"
    params = {
        "action": "opensearch",
        "search": args.query,
        "limit": args.limit,
        "namespace": 0,
        "format": "json"
    }

    response = requests.get(url, params=params, headers=HEADERS)
    response.raise_for_status()
    data = response.json()
    return data[1]  # list of titles


class GetWikipediaPageArgs(BaseModel):
    title: str

def get_wikipedia_page(args: GetWikipediaPageArgs) -> str:
    url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{args.title}"

    response = requests.get(url, headers=HEADERS)
    if response.status_code != 200:
        return f"Page not found: {args.title}"

    data = response.json()
    return data.get("extract", "No summary available.")
