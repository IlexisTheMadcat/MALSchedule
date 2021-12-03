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

class MALSchedule:
    def __init__(self):
        self.previous_fetch = None

    def request_schedule(self):
        response = requests.get("https://myanimelist.net/anime/season/schedule")
        if response.status_code != 200:
            raise FetchError("MAL did not return a status code of 200.")

        html = response.content
        soup = BeautifulSoup(html, "html.parser")

        entries = {
            0: list(),
            1: list(),
            2: list(),
            3: list(),
            4: list(),
            5: list(),
            6: list(),
            7: list(), 
            8: list()
        }

        week_data: Tag = soup.find("div", class_="js-categories-seasonal")
        print(len(convert(week_data.children)))

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
                    if "display: none" in anime_entry["style"]:
                        continue

                if all([i in anime_entry.attrs["class"] for i in ["seasonal-anime", "js-seasonal-anime"]]):
                    
                    anime["name"] = anime_entry.find("div", class_=""
                                              ).find("div", class_="title"
                                              ).find("div", class_="title-text"
                                              ).find("h2", class_="h2_anime_title"
                                              ).a.text

                    anime["producer"] = anime_entry.find("div", class_=""
                                                  ).find("div", class_="prodsrc"
                                                  ).a.text

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
                    except ValueError: anime["score"] = "N/A"

                    anime["synopsis"] = anime_entry.find("div", class_="synopsis js-synopsis").span.text.replace("\r", "")
                        
                    anime["metadata"] = dict()
                    for i in anime_entry.find("div", class_="synopsis js-synopsis").find_all("p", class_="mb4 mt8"):
                        anime["metadata"][i.span.text.lower().strip(":")] = i.a.text

                    entries[ind].append(Anime(**anime))

        return entries