import xml.etree.ElementTree as ET

import requests

class Podcast:
    def __init__(self, show):
        self.show: str = show
        self.tree = self._get_tree()
        self.show_name = self.get_show_name()
        self.description = self.get_description()
        self.image = self.get_image()
        self.RSS_link = self.get_RSS_link()
        self.episodes = self.get_episodes()

    def to_client(self):
        return {
            "title": self.show_name,
            "description": self.description,
            "image": self.image,
            "RSSLink": self.RSS_link,
            "episodes": self.episodes
        }

    def _get_tree(self):
        url:str = "https://assets.library.nashville.gov/talkinglibrary/shows/" + self.show + "/feed.xml"
        response = requests.get(url)
        xml:str = response.text
        feed = ET.fromstring(xml)
        channel = feed.find("channel")
        return channel
    
    def get_description(self):
        feed = self.tree
        description = feed.find("description").text
        description = description.strip("\n")
        description = description.strip()
        return description

    def get_show_name(self):
        feed = self.tree
        title = feed.find("title").text
        return title

    def get_image(self):
        feed = self.tree
        image = feed.find("image").find("url").text
        return image
    
    def get_RSS_link(self) -> str:
        namespace:dict = {"atom": "http://www.w3.org/2005/Atom"}
        tree = self.tree
        atom = tree.find("atom:link", namespace)
        href:str = atom.get("href")
        return href
    
    def get_episodes(self):
        feed = self.tree
        namespace = {"itunes": "http://www.itunes.com/dtds/podcast-1.0.dtd"}
        ret_val = []
        episodes = feed.findall("item")
        for episode in episodes:
            individual = {}
            individual.update({"title": episode.find("title").text})
            individual.update({"pubDate": episode.find("pubDate").text})
            individual.update({"enclosure": episode.find("enclosure").get("url")})
            individual.update({"duration": episode.find(".//itunes:duration", namespace).text})
            ret_val.append(individual)
        return ret_val