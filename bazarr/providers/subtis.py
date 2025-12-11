# -*- coding: utf-8 -*-
from __future__ import absolute_import

import logging
import os
try:
    from urllib.parse import quote
except ImportError:
    from urllib import quote

from requests import Session
from subliminal.video import Movie
from subliminal_patch.providers import Provider
from subliminal_patch.subtitle import Subtitle
from subzero.language import Language

root_logger = logging.getLogger()


class SubtisSubtitle(Subtitle):
    provider_name = "subtis"
    hash_verifiable = False

    def __init__(self, language, video, page_link, title, download_url):
        super(SubtisSubtitle, self).__init__(
            language, hearing_impaired=False, page_link=page_link
        )
        self.video = video
        self.download_url = download_url
        self._title = str(title).strip()
        self.release_info = self._title

    @property
    def id(self):
        return self.page_link

    def get_matches(self, video):
        matches = set()
        
        if isinstance(video, Movie):
            matches.update(["title", "year"])
        
        return matches


class SubtisProvider(Provider):
    languages = {Language.fromalpha2("es")}
    video_types = (Movie,)

    def __init__(self):
        self.session = None

    def initialize(self):
        self.session = Session()
        self.session.headers["User-Agent"] = "Bazarr"

    def terminate(self):
        if self.session:
            self.session.close()

    def query(self, language, video):
        subtitles = []

        filename = os.path.basename(video.name)
        encoded_name = quote(filename)
        url = f"https://api.subt.is/v1/subtitle/file/name/{video.size}/{encoded_name}"

        root_logger.info("Subtis: Searching with URL: %s", url)

        try:
            response = self.session.get(url, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                subtitle_link = data.get("subtitle", {}).get("subtitle_link")
                title_name = data.get("title", {}).get("title_name", "Unknown")
                
                if subtitle_link:
                    root_logger.info("Subtis: Found subtitle: %s", title_name)
                    subtitle = SubtisSubtitle(
                        language=language,
                        video=video,
                        page_link=url,
                        title=title_name,
                        download_url=subtitle_link
                    )
                    subtitles.append(subtitle)
                
        except Exception as e:
            root_logger.error("Subtis: Error searching: %s", e)

        return subtitles

    def list_subtitles(self, video, languages):
        subtitles = []
        for language in languages:
            subtitles.extend(self.query(language, video))
        return subtitles

    def download_subtitle(self, subtitle):
        root_logger.info("Subtis: Downloading from: %s", subtitle.download_url)
        
        try:
            response = self.session.get(subtitle.download_url, timeout=30)
            
            if response.status_code == 200:
                subtitle.content = response.content
                root_logger.info("Subtis: Downloaded %d bytes", len(response.content))
                
        except Exception as e:
            root_logger.error("Subtis: Exception during download: %s", str(e))
