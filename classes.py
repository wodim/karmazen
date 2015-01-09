# -*- coding: utf-8 -*-

import re
import urllib

from bs4 import BeautifulSoup

from utils import *


class LinksPage(object):

    def __init__(self, session, url):
        self.session = session
        self.url = url

        r = session.get(url)
        soup = BeautifulSoup(r.text)

        assert r.status_code == 200 and soup.find("li", {"class": "usertext"})

        self.links = [Link.from_soup(link, session=self.session, referrer=self.url)
                      for link in soup.find_all(attrs={"class": "news-summary"})]

    def sort_by_karma(self):
        return [link for link in sorted(self.links,
                                        key=lambda x: x.karma,
                                        reverse=True)]


class Link(object):

    def __init__(self, session, referrer=None, **kw):
        self.session = session
        self.referrer = referrer

    def __eq__(self, other):
        return self._id == other._id

    def __ne__(self, other):
        return not self.__eq__(other)

    def __repr__(self):
        return '<Link id=%d karma=%d url=%s>' % (self._id, self.karma, self.url)

    @classmethod
    def from_soup(cls, soup, **kw):
        obj = cls(kw["session"], kw["referrer"])

        obj._id = int(soup.find("div", attrs={"class": "votes"})
                      .find("a")["id"].replace("a-votes-", ""))
        obj.title = soup.find("h2").find("a").text
        obj.url = soup.find("div", {"class": "share_icons"})["data-url"]

        obj.votes_users = int(soup.find("span", id=re.compile("^a-usu-")).text)
        obj.votes_anonymous = int(
            soup.find("span", id=re.compile("^a-ano-")).text)
        obj.votes_negatives = int(
            soup.find("span", id=re.compile("^a-neg-")).text)
        obj.votes = obj.votes_users + obj.votes_anonymous
        try:
            obj.comments = int(soup.find("span",
                                         attrs={"class": "comments-counter"})
                               .find("span",
                                     attrs={"class": "counter"}).text)
        except AttributeError:
            obj.comments = 0
        obj.karma = int(soup.find("span", id=re.compile("^a-karma")).text)

        obj.warning = soup.find("div", attrs={"class": "warn"}) is None
        obj.voted = soup.find("a", id=re.compile("^a-shake-")) is None

        return obj

    def upvote(self):
        if not self.voted:
            payload = {"id": self._id, "user": self.session.user_id,
                       "key": self.session.control_key, "l": 0,
                       "u": urllib.quote_plus(self.referrer),
                       "_": random.randint(1000000000000, 9999999999999)}
            r = self.session.get(UPVOTE_URL, params=payload)
            try:
                return r.json()
            except ValueError:
                return False # caído, baneado, etc

    """
    Tipos de voto negativo que se pasan a downvote_code:
      -1 = irrelevante
      -2 = antigua
      -3 = cansina
      -4 = sensacionalista
      -5 = spam
      -6 = duplicada
      -7 = microblogging
      -8 = errónea
      -9 = copia/plagio
    No hay valor por defecto si no se pasa ningún código.
    """
    def downvote(self, downvote_code):
        if not self.voted and downvote_code:
            payload = {"id": self._id, "user": self.session.user_id,
                       "value": downvote_code, "key": self.session.control_key, 
                       "l": 0, "u": urllib.quote_plus(self.referrer),
                       "_": random.randint(1000000000000, 9999999999999)}
            r = self.session.get(DOWNVOTE_URL, params=payload)
            try:
                return r.json()
            except ValueError:
                return False
        else:
            return False
