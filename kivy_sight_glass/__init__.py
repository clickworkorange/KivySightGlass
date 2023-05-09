#!/usr/bin/env python3

"""
SightGlass
==========
Defines the Kivy :class:`SightGlass` class, an animated bar graph 
type widget that emulates the appearance of liquid inside a sight 
glass. 
"""

import os, random, operator
from functools import partial
from kivy.properties import ColorProperty, BoundedNumericProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.relativelayout import RelativeLayout 
from kivy.uix.stencilview import StencilView
from kivy.uix.image import Image
from kivy.animation import Animation, AnimationTransition
from kivy.graphics import Rectangle, Line, Color, InstructionGroup
from kivy_gradient import Gradient

class SightGlass(BoxLayout, StencilView): 
  glass_color = ColorProperty()
  glass_shade = ColorProperty()
  liquid_color = ColorProperty()
  # TODO: the following three properties could be combined
  # in a single property accepting an int, a list of two,
  # or a list of three numbers (see AliasProperty)
  scale_major = BoundedNumericProperty(0, min=0, max=100)
  scale_minor = BoundedNumericProperty(0, min=0, max=10)
  scale_ratio = BoundedNumericProperty(1.0, min=0.0, max=1.0)
  scale_color = ColorProperty()
  level = BoundedNumericProperty(0, min=0, max=100)

  def __init__(self, **kwargs):
    super().__init__(**kwargs)
    self.size_hint = (1, 1)
    self.liquid = Liquid()
    self.add_widget(self.liquid)
    self.gradients = []
    self.gradlines = InstructionGroup()
    self.initial = True # initial level should be set instantly

  def on_level(self, widget, level):
    self.liquid.set_level(self.level, self.initial)

  def on_glass_color(self, widget, color):
    with self.canvas.before:
      # beneath liquid
      Color(rgba=self.glass_color)
      self.gradients.append(Rectangle(pos=self.pos, size=self.size, texture=Gradient.horizontal((1,1,1,1), (0,0,0,1))))
    with self.canvas.after:
      # above liquid
      Color(rgba=self.glass_color)
      self.gradients.append(Rectangle(pos=self.pos, size=self.size, texture=Gradient.horizontal((1,1,1,1), (0,0,0,1))))

  def on_glass_shade(self, widget, color):
    with self.canvas.after:
      # shading
      Color(rgba=self.glass_shade)
      self.gradients.append(Rectangle(pos=self.pos, size=self.size, texture=Gradient.vertical((1,1,1,1), (0,0,0,1))))

  def on_liquid_color(self, widget, color):
    self.liquid.color = self.liquid_color

  def draw_gradlines(self, scale_major):
    self.gradlines.clear()
    # TODO: [x,y] offset, to place scale outside glass
    offset = {"x": 0, "y": 0}
    if scale_major:
      self.gradlines.add(Color(rgba=self.scale_color))
      major = self.height/scale_major
      for i in range(1, scale_major + 1):
        # scale_major+1 so that a final set of minor lines
        # is drawn above the last major line 
        w = 1.2
        x = self.x + offset["x"]
        y = self.y + (major*i) - w + offset["y"]
        z = 0
        a = 200
        b = 240
        if i < scale_major:
          self.gradlines.add(Line(joint="bevel", width=w, ellipse=(x, y, self.width, z, a, b)))
        if self.scale_minor:
          minor = major/self.scale_minor
          for j in range(1, self.scale_minor):
            y = self.y + (major*i) + (minor*j) - w + offset["y"] - major
            a = 220
            w = 1
            self.gradlines.add(Line(joint="bevel", width=w, ellipse=(x, y, self.width, z, a, b)))
      # Perhaps a bit crude to draw these on the parent canvas,
      # and it means gradients do not apply to gradlines, 
      # but it's the easiest way to allow offset beyond edges
      self.parent.canvas.add(self.gradlines)

  # TODO: this is not neat
  def on_scale_major(self, widget, scale_major):
    self.draw_gradlines(scale_major)
  def on_scale_minor(self, widget, scale_minor):
    self.draw_gradlines(self.scale_major)
  def on_scale_color(self, widget, scale_color):
    self.draw_gradlines(self.scale_major)

  def on_size(self, widget, size):
    self.initial = False
    for gradient in self.gradients:
      gradient.pos = self.pos
      gradient.size = self.size
    self.draw_gradlines(self.scale_major)
    self.liquid.set_level(self.level, True)

class Liquid(RelativeLayout): 
  level = BoundedNumericProperty(0, min=0, max=100)
  color = ColorProperty()
  # TODO: "curvature" (of tube; 0=flat, 1=diameter=width)
  # TODO: read and understand the contents of this blogpost:
  # https://blog.kivy.org/2014/01/kivy-image-manipulations-with-mesh-and-textures/
  # TODO: "amplitude" (wave height)
  # TODO: "opacity" (overall liquid opacity)
  # TODO: "density" ()
  # TODO: "turbidity" (opacity variation)
  # TODO: "viscosity" (damping)
  # TODO: "pressure" (speed)
  # TODO: "uniformity" (colour variation)
  def __init__(self, **kwargs):
    super().__init__(**kwargs)
    self.waves = []
    for i in range(0,8):
      phase = "-" if i % 2 else "+"
      wave = Wave(
        color    = self.color, #TODO: meh (set_color)
        distance = random.randrange(100,200), 
        offset   = random.randrange(-200,200), 
        phase    = phase, 
        speed    = (random.randrange(80,120)/100)
      )
      self.waves.append(wave)
      self.add_widget(wave)

  def oscillate(self, overshoot, dt=0):
    if abs(overshoot) > 1:
      duration = 1 # TODO: use "pressure" (speed)
      anim = Animation(y=self.y+overshoot, d=duration, t="in_out_sine") 
      overshoot = -(overshoot/1.5) # TODO: use "viscosity" (damping)
      anim.on_complete = partial(self.oscillate, overshoot)
      anim.start(self)

  def set_level(self, level, instant=False, dt=0):
    Animation.cancel_all(self)
    ufo = 288 # =window.height-self.height, but how?
    height = ((self.parent.height / 100) * level) - ufo
    if instant:
      # TODO: set the y pos directly if instant (no animation)
      anim = Animation(y=height, d=0) 
    else:
      for wave in self.waves:
        # stir things up
        wave.distance = wave.max_distance
      delta = self.y - height
      overshoot = delta/5 # TODO: use "viscosity" (damping)
      duration = max(abs(delta) / 100, 1) # TODO: use "pressure" (speed)
      anim = Animation(y=height-(overshoot/2), d=duration, t="in_out_sine") 
      anim.on_complete = partial(self.oscillate, overshoot)
    anim.start(self)

  def on_level(self, widget, level):
    self.set_level(level)

  def on_color(self, widget, color):
    for i,wave in enumerate(self.waves):
      wave.color = self.color[0:3] + [min((0.1 + i/10),0.5)]

class Wave(Image): 
  def __init__(self, offset=0, phase="+", distance=200, speed=1, damping=20, **kwargs):
    super().__init__(**kwargs)
    self.source = os.path.join(os.path.dirname(__file__),"wave.png")
    self.size = self.texture.size
    self.offset = -(self.width / 2) + offset # TODO: offset_x?
    self.phase = operator.neg if phase == "-" else operator.pos
    self.distance = distance
    self.max_distance = distance
    self.min_distance = 5
    self.speed = speed
    self.damping = damping
    self.size_hint = (None, None)
    self.pos_hint = {"top": 1}
    self.keep_ratio = False
    self.allow_stretch = True

  def on_parent(self, widget, parent):
    self.x = self.offset
    # TODO: check if already animating
    self.animate()

  def animate(self, dt=0):
    anim = Animation(x=self.offset + self.phase(self.distance), d=1/self.speed, t="in_out_sine") 
    anim += Animation(x=self.offset, d=1/self.speed, t="in_out_sine")
    anim.on_complete = self.animate
    anim.start(self)
    self.distance = max(self.distance - (self.damping / self.distance) * 100, self.min_distance)