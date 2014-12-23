# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
from ConfigParser import ConfigParser
from datetime import datetime
import math
import random
import requests
import time
import urllib
import sys

from utils import *
from classes import LinksPage, Link

config = ConfigParser()
config.readfp(open("config.ini"))
username = config.get("karmazen", "username")
username = config.get("karmazen", "password")

r_s = requests.Session()
r_s.headers = {"User-Agent": USER_AGENT}
# login.
r_s.get(LOGIN_URL_GET)
time.sleep(exp_delay(SHORT_INTERACTION_DELAY))
payload = {"username": username,
           "password": password,
           "processlogin": "1",
           "return": "/"}
r = r_s.post(LOGIN_URL_POST, data=payload)
soup = BeautifulSoup(r.text)
assert r.url == FRONT_PAGE_URL and soup.find("li", {"class": "usertext"})

print u"Sesión iniciada."

r_s.user_id = int(urllib.unquote(r_s.cookies["u"]).split(":", 1)[0])
r_s.control_key = r_s.cookies["k"]

# bucle principal
while True:
    # compruebo si NO es el momento de ponerse en marcha y me echo a dormir.
    if not should_i(activity[datetime.now().hour] * 2):
        print "No es momento de despertarse. Me echo a dormir."
        time.sleep(normal_delay(LONG_SLEEP_DELAY))
        continue

    # noche de acción
    # hay una ligera probabilidad de no leer la portada siquiera e ir
    # directamente a pendientes.
    if should_i(0.7):
        front_page = LinksPage(r_s, FRONT_PAGE_URL)

        # votar o no votar.
        for link in front_page.links:
            if should_i(0.4) and not link.voted:
                print ("He considerado votar %s (%d de karma)"
                      " (PORTADA)") % (link.url, link.karma)
                time.sleep(exp_delay(MID_INTERACTION_DELAY))
                link.upvote()

    # ahora las pendientes.
    queue_page = LinksPage(r_s, QUEUE_URL)
    queue_page_sorted = queue_page.sort_by_karma()

    for link in queue_page.links:
        # una octava parte de las noticias es votada con una probabilidad
        # superior y sin tener en cuenta negativos o advertencias
        if (should_i(0.8) and
                link in queue_page_sorted[:len(queue_page_sorted) / 8]):
            print "Voy a votar %s (%d de karma)" % (link.url, link.karma)
            time.sleep(exp_delay(MID_INTERACTION_DELAY))
            link.upvote()
            continue

        # hay una probabilidad de que ni siquiera considere votar si no es de
        # las primeras. si lo considera, ha de estar en la mitad de la página
        # y no debe de tener demasiados negativos con respecto a usuarios que
        # han votado
        if (should_i(0.6) and
                link in queue_page_sorted[:len(queue_page_sorted) / 2] and
                link.votes_negatives <= math.ceil(link.votes_users * 0.3) and
                not link.voted):
            print "He considerado votar %s (%d de karma)" % (link.url,
                                                             link.karma)
            time.sleep(exp_delay(MID_INTERACTION_DELAY))
            link.upvote()

    print "Me echo a dormir."
    time.sleep(normal_delay(LONG_SLEEP_DELAY))