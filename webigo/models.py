# -*- coding: utf-8 -*-
# webigo.models
import logging
from StringIO import StringIO
from google.appengine.ext import db
from django.utils import simplejson
from goban import Goban

class Game(db.Model):
    size = db.IntegerProperty(required=True)
    black = db.StringProperty()
    white = db.StringProperty()
    black_caught = db.IntegerProperty(default=0)
    white_caught = db.IntegerProperty(default=0)
    turn_count = db.IntegerProperty(default=1)
    pass_count = db.IntegerProperty(default=0)
    data = db.TextProperty()
    prev_data = db.TextProperty()
    created_at = db.DateTimeProperty(auto_now_add=True)
    updated_at = db.DateTimeProperty(auto_now=True)

    @property
    def turn(self):
        logging.info(self.turn_count)
        return Goban.black if self.turn_count % 2 else Goban.white

    @property
    def turn_label(self):
        return u'黒' if self.turn is Goban.black else u'白'

    def touch(self, x, y):
        self._ensure_goban_object()
        caught = self.goban_object.touch(x, y, self.turn)
        if self.is_kou():
            raise Goban.Untouchable()
        if self.turn is Goban.black:
            self.white_caught += caught
        else:
            self.black_caught += caught
        self.prev_data = self.data
        self.data = simplejson.dumps(self.goban_object.data)
        self.turn_count += 1
        self.pass_count = 0

    def pass_touch(self):
        self.prev_data = self.data
        self.turn_count += 1
        self.pass_count += 1

    def render(self):
        self._ensure_goban_object()
        buffer = StringIO()
        self.goban_object.render(buffer, html=True)
        return buffer.getvalue()
        
    def _ensure_goban_object(self):
        if not hasattr(self, 'goban_object'):
            self.goban_object = Goban(self.size)
            if self.data is not None:
                self.goban_object.data = simplejson.loads(self.data)

    def is_kou(self):
        if self.prev_data is None: return False
        prev_goban_object = Goban(self.size)
        prev_goban_object.data = simplejson.loads(self.prev_data)
        return self.goban_object.is_kou(prev_goban_object)

