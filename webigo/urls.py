# -*- coding: utf-8 -*-
# webigo.urls
# 

# Following few lines is an example urlmapping with an older interface.
"""
from werkzeug.routing import EndpointPrefix, Rule

def make_rules():
  return [
    EndpointPrefix('webigo/', [
      Rule('/', endpoint='index'),
    ]),
  ]

all_views = {
  'webigo/index': 'webigo.views.index',
}
"""

from kay.routing import (
  ViewGroup, Rule
)

view_groups = [
  ViewGroup(
    Rule('/', endpoint='index', view='webigo.views.index'),
    Rule('/new/<int:size>', endpoint='new_game', view='webigo.views.new_game'),
    Rule('/game/<game_id>/touch/', endpoint='touch', view='webigo.views.touch'),
    Rule('/game/<game_id>/pass/', endpoint='pass', view='webigo.views.pass_touch'),
    Rule('/game/<game_id>/', endpoint='game', view='webigo.views.game'),
  )
]

