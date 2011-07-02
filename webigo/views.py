# -*- coding: utf-8 -*-
"""
webigo.views
"""

import string
import random
import logging

"""
from google.appengine.api import users
from google.appengine.api import memcache
from werkzeug.exceptions import (
  NotFound, MethodNotAllowed, BadRequest
)

from kay.i18n import gettext as _
from kay.auth.decorators import login_required

"""

from werkzeug import (
  unescape, redirect, Response,
)
from kay.utils import (
  render_to_response, get_by_key_name_or_404,
)
from models import Game
from forms import TouchForm

default_goban_size = 19

def index(request):
    games = Game.all().order('-created_at')
    return render_to_response('webigo/index.html', {'games':games})

def new_game(request, size):
    alphabets = string.digits + string.letters
    game_id = ''.join(random.choice(alphabets) for i in xrange(8))
    game = Game(key_name=game_id, size=size)
    game.put()
    return redirect('/game/%s/' % game_id)

def game(request, game_id):
    game = get_by_key_name_or_404(Game, game_id)
    return render_to_response('webigo/game.html', {'game':game})

def touch(request, game_id):
    game = get_by_key_name_or_404(Game, game_id)
    # TODO: validation
    if request.method == 'POST':
        game.touch(int(request.form['x']), int(request.form['y']))
        game.put()
    return redirect('/game/%s/' % game_id)

def pass_touch(request, game_id):
    game = get_by_key_name_or_404(Game, game_id)
    game.pass_touch()
    game.put()
    return redirect('/game/%s/' % game_id)

