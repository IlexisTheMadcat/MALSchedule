import requests
from dataclasses import dataclass

from bs4 import BeautifulSoup, Tag

from utils import convert_list_iterator as convert


class FetchError(Exception):
    pass


@dataclass
class Anime:
    name: str
    producer: str
    tags: list
    image_url: str
    score: float
    synopsis: str
    metadata: dict
    estimated_rating: str


class MALSchedule:
    def __init__(self):
        self.previous_fetch = None

    def request_schedule(self):
        response = requests.get("https://myanimelist.net/anime/season/schedule")
        if response.status_code != 200:
            raise FetchError("MAL did not return a status code of 200.")

        html = response.content
        soup = BeautifulSoup(html, "html.parser")

        entries = dict()

        week_data: Tag = soup.find("div", class_="js-categories-seasonal")

        passed_article = False
        for ind, day_data in enumerate(convert(week_data.children)):
            if passed_article:
                ind = ind-1
            if day_data.name == "article": 
                passed_article = True
                continue

            anime = dict()
            for anime_entry in convert(day_data.children):
                try: anime_entry["style"]
                except KeyError: pass
                else: 
                    if "display: none" in anime_entry["style"]: continue

                if "anime-header" in anime_entry["class"]:
                    weekday = anime_entry.text
                    if weekday not in entries:
                        entries[weekday] = list()

                if all([i in anime_entry.attrs["class"] for i in ["seasonal-anime", "js-seasonal-anime"]]):
                    anime["name"] = anime_entry.find("div", class_=""
                                              ).find("div", class_="title"
                                              ).find("div", class_="title-text"
                                              ).find("h2", class_="h2_anime_title"
                                              ).a.text

                    producer_info = anime_entry.find("div", class_=""
                              ).find("div", class_="prodsrc"
                              ).find("span", class_="producer")
                    if not producer_info.find("a"):
                        anime["producer"] = "Not provided"
                    else:
                        anime["producer"] = producer_info.a.text

                    anime["tags"] = []
                    for tag_element in convert(
                        anime_entry.find("div", class_=""
                                  ).find("div", class_="genres js-genre"
                                  ).find("div", "genres-inner js-genre-inner"
                                  ).children):
                        if tag_element == "-": continue
                        anime["tags"].append(tag_element.find("a")["title"])
                           
                    img = anime_entry.find("div", class_="image").a.img
                    if "src" in img.attrs:
                        anime["image_url"] = anime_entry.find("div", class_="image").a.img.attrs['src']
                    elif "data-src" in img.attrs: anime["image_url"] = anime_entry.find("div", class_="image").a.img.attrs['data-src']
                    else: anime["image_url"] = "about:blank"

                    try: anime["score"] = float(
                        anime_entry.find("div", class_="information"
                                  ).find("div", class_="scormem"
                                  ).find("span", title="Score"
                                  ).i.text)
                    except ValueError: anime["score"] = 0

                    anime["synopsis"] = anime_entry.find("div", class_="synopsis js-synopsis").span.text.replace("\r", "")
                        
                    anime["metadata"] = dict()
                    for i in anime_entry.find("div", class_="synopsis js-synopsis").find_all("p", class_="mb4 mt8"):
                        anime["metadata"][i.span.text.strip(":")] = i.a.text.strip()
                   
                    # !!! Ratings are not from the MPAA. These are just suggestions based on given data.
                    if "Demographic" in anime["metadata"] and anime["metadata"]["Demographic"] == "Kids":
                        anime["estimated_rating"] = "G"
                    if "Ecchi" in anime["tags"]:
                        anime["estimated_rating"] = "R"
                    if "Hentai" in anime["tags"] or "Erotics" in anime["tags"]:
                        anime["estimated_rating"] = "NC-17"
                    if "estimated_rating" not in anime:
                        anime["estimated_rating"] = "PG"

                    entries[weekday].append(Anime(**anime))

        return entries