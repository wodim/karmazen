# -*- coding: utf-8 -*-

import math
import random

USER_AGENT = ("Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36"
              " (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36")

# dependiendo de la hora puede que no nos interese iniciar sesión siquiera.
activity = {
    0: 0.7, 1: 0.6, 2: 0.6, 3: 0.2, 4: 0, 5: 0,
    6: 0, 7: 0, 8: 0, 9: 0.1, 10: 0.1, 11: 0.3,
    12: 0.3, 13: 0.3, 14: 0.6, 15: 0.9, 16: 0.2, 17: 0.3,
    18: 0.2, 19: 0.3, 20: 0.3, 21: 0.5, 22: 0.8, 23: 0.9,
}

# retrasos entre acciones. van algo aleatorizados siguiendo un algoritmo.
# asi que esto sería la media.

# interacciones cortas. para cuando el bot va a hacer algo directamente.
# por ejemplo, meneame.net -> iniciar sesión.
SHORT_INTERACTION_DELAY = 5
# leer noticia
MID_INTERACTION_DELAY = 20
# leer comentarios
LONG_INTERACTION_DELAY = 60
# el tiempo durante el cual me echo a dormir cada hora.
# probablemente pise la hora siguiente.
LONG_SLEEP_DELAY = 20 * 60

# urls.
BASE_URL = "https://www.meneame.net"
LOGIN_URL_GET = BASE_URL + "/login?return=%2Flogin"
LOGIN_URL_POST = BASE_URL + "/login"
FRONT_PAGE_URL = BASE_URL + "/"
QUEUE_URL = BASE_URL + "/queue"

UPVOTE_URL = "https://www.meneame.net/backend/menealo"

# fumada
def exp_delay(delay):
    variation = (1 / (1 + math.exp((-delay + 70) / 50))) * 10
    return random.uniform(delay - variation, delay + variation)

normal_delay = lambda delay: random.uniform(delay - delay * 0.2,
                                            delay + delay * 0.2)
should_i = lambda chance: random.uniform(0, 1) <= chance