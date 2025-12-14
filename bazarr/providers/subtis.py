# -*- coding: utf-8 -*-

import logging
import os
from urllib.parse import quote

from requests import Session
from subliminal.video import Movie
from subliminal_patch.providers import Provider
from subliminal_patch.subtitle import Subtitle
from subzero.language import Language

__version__ = "0.8.7"

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
    provider_name = "subtis"
    version = __version__

    def __init__(self):
        self.session = None

    def initialize(self):
        self.session = Session()
        self.session.headers.update(
            {"User-Agent": f"Bazarr/Subtis/{__version__}", "Accept": "application/json"}
        )

    def terminate(self):
        if self.session:
            self.session.close()

    def query(self, language, video):
        """Query subtitles for a given video."""
        if not video.name or not video.size:
            root_logger.info("Subtis: Missing video name or size")
            return []

        filename = os.path.basename(video.name)
        encoded_name = quote(filename)
        url = f"https://api.subt.is/v1/subtitle/file/name/{video.size}/{encoded_name}"

        try:
            response = self.session.get(url, timeout=10)
            response.raise_for_status()

            data = response.json()

            if not isinstance(data, dict):
                root_logger.info("Subtis: Invalid response format")
                return []

            subtitle_data = data.get("subtitle", {})
            subtitle_link = subtitle_data.get("subtitle_link")

            if not subtitle_link:
                root_logger.info("Subtis: No subtitle found for %s", filename)
                return []

            title_name = data.get("title", {}).get("title_name", "Unknown")

            subtitle = SubtisSubtitle(
                language=language,
                video=video,
                page_link=url,
                title=title_name,
                download_url=subtitle_link,
            )

            return [subtitle]

        except Exception as e:
            root_logger.info("Subtis: Error searching for %s: %s", filename, e)
            return []

    def list_subtitles(self, video, languages):
        subtitles = []
        for language in languages:
            subtitles.extend(self.query(language, video))
        return subtitles

    def download_subtitle(self, subtitle):
        """Download subtitle content."""
        if not subtitle.download_url:
            root_logger.info("Subtis: No download URL available")
            return

        try:
            response = self.session.get(subtitle.download_url, timeout=30)
            response.raise_for_status()

            if not response.content:
                root_logger.info("Subtis: Empty subtitle content")
                return

            subtitle.content = response.content

        except Exception as e:
            root_logger.info(
                "Subtis: Exception during download from %s: %s",
                subtitle.download_url,
                str(e),
            )
