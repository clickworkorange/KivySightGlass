#!/usr/bin/env python3

"""
SightGlass
==========
Defines the Kivy :class:`SightGlass` class, an animated bar graph 
type widget that emulates the appearance of liquid inside a sight 
glass. 
"""

import os, random, operator
#from math import sqrt, cos, sin, pi
#from math import cos, sin, pi
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
  scale_color = ColorProperty()
  level = BoundedNumericProperty(0, min=0, max=100)
  scale = BoundedNumericProperty(0, min=0, max=100) # TODO: rename this

  def __init__(self, **kwargs):
    super().__init__(**kwargs)
    self.size_hint = (1, 1)
    self.liquid = Liquid()
    self.add_widget(self.liquid)
    self.gradients = []
    self.graduation = InstructionGroup()
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

  def draw_scale(self, scale):
    # TODO: [x,y] offset, to place scale outside glass
    self.graduation.clear()
    if scale:
      self.graduation.add(Color(rgba=self.scale_color))
      step = int(self.height/scale)
      for i in range(step, int(self.height), step):
        a = 200
        b = 220
        w = 1.2
        x = self.x
        y = self.y + i
        z = 5
        self.graduation.add(Line(joint="bevel", width=w, ellipse=(x, y, self.width, z, a, b)))
      self.canvas.add(self.graduation)

  def on_size(self, widget, size):
    self.initial = False
    for gradient in self.gradients:
      gradient.pos = self.pos
      gradient.size = self.size
    self.draw_scale(self.scale)
    self.liquid.set_level(self.level, True)

class Liquid(RelativeLayout): 
  level = BoundedNumericProperty(0, min=0, max=100)
  color = ColorProperty((1,1,1,1))
  # TODO: swing up/down around new level (animation transition?)
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
    for i in range(0,4):
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
    for wave in self.waves:
      # stir things up
      wave.distance = wave.max_distance
    if abs(overshoot) > 0:
      duration = 1 # TODO: use "pressure" (speed)
      anim = Animation(y=self.y-overshoot, d=duration, t="in_out_sine") 
      overshoot = -(overshoot/1.5) # TODO: use "viscosity" (damping)
      anim.on_complete = partial(self.oscillate, overshoot)
      anim.start(self)

  def set_level(self, level, instant=False, dt=0):
    Animation.cancel_all(self)
    ufo = 280 # TODO: where does this value come from? 
    height = ((self.parent.height / 100) * level) - ufo
    if instant:
      # TODO: set the y pos directly if instant (no animation)
      anim = Animation(y=height, d=0) 
    else:
      delta = self.y - height
      overshoot = -(delta/10) 
      duration = max(abs(delta) / 100, 1) # TODO: use "pressure" (speed)
      anim = Animation(y=height+overshoot, d=duration, t="in_out_sine") 
      anim.on_complete = partial(self.oscillate, overshoot)
    anim.start(self)

  def on_level(self, widget, level):
    self.set_level(level)

  def on_color(self, widget, color):
    for i,wave in enumerate(self.waves):
      wave.color = self.color #[0:3] + [min((0.1 + i/10),1)]

class Wave(Image): 
  def __init__(self, offset=0, phase="+", distance=200, speed=1, damping=20, **kwargs):
    super().__init__(**kwargs)
    self.source = os.path.join(os.path.dirname(__file__),"wave.png")
    self.size = self.texture.size
    self.offset = -(self.width / 2) + offset # TODO: offset_x?
    self.phase = operator.neg if phase == "-" else operator.pos
    self.distance = distance
    self.max_distance = distance
    self.min_distance = 3
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