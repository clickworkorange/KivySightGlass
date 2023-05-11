
### Description

This Kivy bar graph widget seeks to emulate the appearance of liquid inside a sight glass. It is currently at an experimental stage - consider it early alpha at best. 

> A sight glass or water gauge is a type of level sensor, a transparent tube through which the operator of a tank or boiler can observe the level of liquid contained within. 

https://en.wikipedia.org/wiki/Sight_glass

<img width="256" height="256" src="https://github.com/clickworkorange/KivySightGlass/assets/196348/ed7e3588-d459-4c0e-b272-cd42b7b79896" />

### Preview

https://github.com/clickworkorange/KivySightGlass/assets/196348/2d69461b-6e3f-4ba8-ab48-24d1cc258f69

### Design 
This could probably have been better realised using a shader/mesh approach, but as I suffer from a major OpenGL-fu deficit I decided to try a more basic approach: instead of a mesh the "liquid" consists of layered bitmap textures with a wavy top edge, which animate from side to side on a sine function. The extent of the animation is dampened over time, calming the surface, though it increases again whenever the level is changed, agitating the liquid. Some slight randomisation of alpha, colour, position, speed and movement range between the layeres helps improve the illusion, and means no two sight glasses will look exactly the same. Additionally, the liquid will "overshoot" a requested level and oscillate around it for a while before settling down (note that at the moment it doesn't always settle precisely at the right level, because *maths*, but I hope to have that fixed soon). 

The "tube" portion consists of horizontal front and rear gradients, with the "liquid" appearing in between. A third vertical shading gradient is added on top to add to the illusion of an actual tube. The whole widget is contained inside a <a href="https://kivy.org/doc/stable/api-kivy.uix.stencilview.html">`StencilView`</a>, which creates the outline of the tube by masking the image layers outside it. The maximum level visible inside the tube is 100, and the minimum 0, though -10 to 110 is allowed (for completely full/empty appearance, without any visible sloshing). 

An optional scale can be added, which is currently drawn on the parent widget's <a href="https://kivy.org/doc/stable/api-kivy.graphics.instructions.html">`Canvas`</a> (to allow ofsetting it beyond the edges of the `StencilView`). This can be divided into a maximum of 100 "major" lines, each further divided by a maximum of 10 "minor" lines. The graduation lines are actually ellipses, or partial ellipses, and can be given a curvature and up to 360&deg; length. 

Much of all this can be configured directly in `kvlang`, though at the moment a lot of things remain hard-coded. 

### Goals

- Derive the `ufo` parameter that is used to represent the window height minus the height of the sight glass from the actual properties. This value is needed to accurately set the `level` and is currently hard-coded, because Kivy is being weird about it. 

- Make every aspect of the sight glass widget dynamic and configurable from `.kv`, ideally without cluttering the class with a ton of attributes. I am looking at <a href="https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.AliasProperty">`AliasProperty`</a> as a possible way to achieve this. 

- Maybe add a cylindrical mesh transformation to the waves, so they appear to follow the walls of the tube rather than move linearly from side to side. Keeping resource usage low is a more important goal though, and a 3D transformation might just prove too costly. 

- The ability to give a rounded appearance to the ends of the tube might be nice, perhaps by using a bitmap as the mask instead of (or in addition to) the `StencilView`. Or it may be possible to use `Canvas` drawing tools (i.e. `Line` and `Ellipse`) to draw a <a href="https://kivy.org/doc/stable/api-kivy.graphics.stencil_instructions.html">`Stencil`</a> that has an adjustable top & bottom curvature. 

- Drawing the portion of the scale that is on the back of the tube (if any) *behind* the liquid (and the rear gradient). 

- Attaching a list of strings to the "major" scale lines, so numbers (or any other characters) can be shown alongside. 

- Adding bubbles which ocassionally rise through the liquid. 

### Example usage
````kv
#:import SightGlass kivy_sight_glass.SightGlass

SightGlass:
    id: myglass
    size_hint: .2,1
    level: 33
    glass_color: rgba(127,191,255,63)
    glass_shade: rgba(0,0,0,63)
    liquid_color: rgba(0,215,255,255)
    scale_major: 10
    scale_minor: 5
    scale_color: rgba(255,255,255,95)

Button:
    on_press: myglass.level=90
````

### Installation
Clone the repository and install with `pip install .`

### Suggested use cases

- On an automation dashboard, showing tank levels. 

- As the health/mana bars (or similiar) in a game. 

- In interactive kiosk applications. 

### Wetware at work
Resistance may indeed be futile, and I for one welcome our new software based overlords - who I'm sure are paying close attention. But this software was written by a *human*, and only humans can enjoy writing code. Perhaps that joy by itself will one day be seen as an act of <a href="https://en.wikipedia.org/wiki/Joy_as_an_Act_of_Resistance">resistance</a>?

<img src="/human_coder.png" alt="Wetware at work" width="128" height="128" />

