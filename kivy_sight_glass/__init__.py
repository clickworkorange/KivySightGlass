#!/usr/bin/env python3

"""
SightGlass
==========
Defines the Kivy :class:`SightGlass` class, an animated bar graph
type widget that emulates the appearance of liquid inside a sight
glass.
"""

import os
import random
import operator
from functools import partial
from kivy.properties import ColorProperty, BoundedNumericProperty, ObjectProperty
from kivy.uix.widget import Widget
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.stencilview import StencilView
from kivy.uix.image import Image
from kivy.animation import Animation
from kivy.graphics import Rectangle, Line, Color
from kivy_gradient import Gradient


class SightGlass(AnchorLayout, StencilView):
    glass_color = ColorProperty()
    glass_shade = ColorProperty()
    liquid_color = ColorProperty()
    scale_major = ObjectProperty(None)
    scale_minor = ObjectProperty(None)
    scale_ratio = BoundedNumericProperty(0.5, min=0.0, max=1.0)
    scale_color = ColorProperty()
    level = BoundedNumericProperty(0, min=-10, max=110)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size_hint = (1, 1)
        self.liquid = Liquid()
        self.add_widget(self.liquid)
        self.gradlines = Gradlines()
        self.add_widget(self.gradlines)
        self.gradients = []
        # initial level should be set instantly
        self.initial = True

    def on_level(self, widget, level):
        self.liquid.set_level(self.level, self.initial)

    def get_min_level(self):
        return self.property("level").get_min(self)

    def get_max_level(self):
        return self.property("level").get_max(self)

    def on_glass_color(self, widget, color):
        gradient = Gradient.horizontal((1, 1, 1, 1), (0, 0, 0, 1))
        with self.canvas.before:
            # beneath liquid
            Color(rgba=self.glass_color)
            self.gradients.append(
                Rectangle(pos=self.pos, size=self.size, texture=gradient)
            )
        with self.canvas.after:
            # above liquid
            Color(rgba=self.glass_color)
            self.gradients.append(
                Rectangle(pos=self.pos, size=self.size, texture=gradient)
            )

    def on_glass_shade(self, widget, color):
        gradient = Gradient.vertical((1, 1, 1, 1), (0, 0, 0, 1))
        with self.canvas.after:
            # shading
            Color(rgba=self.glass_shade)
            self.gradients.append(
                Rectangle(pos=self.pos, size=self.size, texture=gradient)
            )

    def on_liquid_color(self, widget, color):
        self.liquid.color = self.liquid_color

    def on_size(self, widget, size):
        self.initial = False
        for gradient in self.gradients:
            gradient.pos = self.pos
            gradient.size = self.size
        # self.gradlines.draw(self.scale_major)
        self.liquid.set_level(self.level, True)


class Gradlines(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def on_parent(self, widget, parent):
        self.parent.bind(scale_major=self.draw)
        self.parent.bind(scale_minor=self.draw)

    def draw(self, parent, scale):
        # TODO: best way to propagate properties parent > child?
        scale_major = self.parent.scale_major
        scale_minor = self.parent.scale_minor
        self.canvas.clear()
        # [x, y] offset, to place scale outside glass
        offset = {"x": 0, "y": 0}
        w = 2
        z = 5
        a = 270
        b = 90
        if isinstance(scale_major, int):
            self.canvas.add(Color(rgba=self.parent.scale_color))
            major = self.height / scale_major
            for i in range(1, scale_major + 1):
                # scale_major+1 so that a final set of minor lines
                # is drawn above the last major line
                x = self.x + offset["x"]
                y = self.y + (major * i) - w + offset["y"]
                if i < scale_major:
                    self.canvas.add(
                        Line(joint="bevel", width=w, ellipse=(x, y, self.width, z, a, b))
                    )
                if scale_minor:
                    minor = major / scale_minor
                    a = a + (b - a) * self.parent.scale_ratio
                    w = 1
                    for j in range(1, scale_minor):
                        y = self.y + (major * i) + (minor * j) - w + offset["y"] - major
                        self.canvas.add(
                            Line(joint="bevel", width=w, ellipse=(x, y, self.width, z, a, b))
                        )
        elif isinstance(scale_major, list):
            self.canvas.add(Color(rgba=self.parent.scale_color))
            major = self.height / 100
            for i in scale_major:
                x = self.x + offset["x"]
                y = self.y + (major * i) - w + offset["y"]
                if i < 100:
                    self.canvas.add(
                        Line(joint="bevel", width=w, ellipse=(x, y, self.width, z, a, b))
                    )


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
        for i in range(0, 3):
            phase = "-" if i % 2 else "+"
            wave = Wave(
                color=self.color,
                distance=random.randrange(100, 200),
                offset=random.randrange(-200, 200),
                phase=phase,
                speed=(random.randrange(80, 120) / 100)
            )
            self.waves.append(wave)
            self.add_widget(wave)

    def oscillate(self, overshoot, dt=0):
        if abs(overshoot) > 1:
            # TODO: use "pressure" (speed)
            duration = max(abs(overshoot) / 100, 1)
            anim = Animation(y=self.y + overshoot, d=duration, t="in_out_sine")
            # TODO: use "viscosity" (damping)
            overshoot = -(overshoot / 1.5)
            anim.on_complete = partial(self.oscillate, overshoot)
            anim.start(self)

    def set_level(self, level, instant=False, dt=0):
        Animation.cancel_all(self)
        # ufo=window.height-self.height, but how?
        ufo = 528
        height = ((self.parent.height / 100) * level) - ufo
        if instant:
            # TODO: set the y pos directly if instant (no animation)
            anim = Animation(y=height, d=0)
        else:
            for wave in self.waves:
                # stir things up
                wave.distance = wave.max_distance
            delta = self.y - height
            # TODO: use "viscosity" (damping)
            overshoot = delta / 5
            # TODO: use "pressure" (speed)
            duration = max(abs(delta) / 100, 1)
            anim = Animation(y=height - (overshoot / 2), d=duration, t="in_out_sine")
            anim.on_complete = partial(self.oscillate, overshoot)
        anim.start(self)

    def on_level(self, widget, level):
        self.set_level(level)

    def on_color(self, widget, color):
        for i, wave in enumerate(self.waves):
            f = random.randrange(-100, 100) / 200.0
            r = min(self.color[0] + f, 1)
            g = min(self.color[1] + f, 1)
            b = min(self.color[2] + f, 1)
            wave.color = [r, g, b] + [min((0.1 + i / 10), 0.5)]


class Wave(Image):
    def __init__(self, offset=0, phase="+", distance=200, speed=1, damping=20, **kwargs):
        super().__init__(**kwargs)
        self.source = os.path.join(os.path.dirname(__file__), "images/wave.png")
        self.size = self.texture.size
        # TODO: offset_x?
        self.offset = -(self.width / 2) + offset
        self.phase = operator.neg if phase == "-" else operator.pos
        self.distance = distance
        self.max_distance = distance
        self.min_distance = 10
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
        anim = Animation(x=self.offset + self.phase(self.distance), d=1 / self.speed, t="in_out_sine")
        anim += Animation(x=self.offset, d=1 / self.speed, t="in_out_sine")
        anim.on_complete = self.animate
        anim.start(self)
        self.distance = max(self.distance - (self.damping / self.distance) * 100, self.min_distance)
