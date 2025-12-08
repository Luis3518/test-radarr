# -*- coding: utf-8 -*-
from __future__ import absolute_import

import logging
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
        return matches


class SubtisProvider(Provider):
    languages = {Language("spa", "MX")}
    video_types = Movie

    def __init__(self):
        self.session = None

    def initialize(self):
        self.session = Session()
        self.session.headers["User-Agent"] = "Bazarr"

    def terminate(self):
        if self.session:
            self.session.close()

    def query(self, language, video):
        return []

    def list_subtitles(self, video, languages):
        root_logger.info("BAZARR Subtis: Video = %s", video)
        root_logger.info("BAZARR Subtis: Idiomas solicitados = %s", languages)
        root_logger.info("BAZARR Subtis: Tamaño del archivo = %s", video.size)

        subtitles = []
        for language in languages:
            subtitles.extend(self.query(language, video))

        return subtitles

    def download_subtitle(self, subtitle):
        """Descarga el contenido del subtítulo"""
        pass
