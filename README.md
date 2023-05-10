
### Description

This Kivy bar graph widget seeks to emulate the appearance of liquid inside a sight glass. It is currently at an experimental stage - consider it early alpha at best. 

> A sight glass or water gauge is a type of level sensor, a transparent tube through which the operator of a tank or boiler can observe the level of liquid contained within. 

https://en.wikipedia.org/wiki/Sight_glass

<img width="256" height="256" src="https://github.com/clickworkorange/KivySightGlass/assets/196348/ed7e3588-d459-4c0e-b272-cd42b7b79896" />

### Early preview video of a SightGlass in action

https://github.com/clickworkorange/KivySightGlass/assets/196348/2d69461b-6e3f-4ba8-ab48-24d1cc258f69

### Design 
This could probably have been better realised using a shader/mesh approach, but as I suffer from a major OpenGL-fu deficit* I decided to try a more basic approach: instead of a mesh the "liquid" consists of layered bitmap textures with a wavy top edge, which animate from side to side on a sine easing function. The extent of the animation is dampened over time, calming the surface, though this increases again whenever the level is changed, perturbing the liquid. Some slight randomisation of alpha, colour, position, speed and movement range between the layeres helps improve the illusion, and means no two sight glasses will look the same. 

\*) Let's be honest; . 

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

### Wetware at work
Resistance may indeed be futile, and I for one welcome our new software based overlords - who I'm sure are paying close attention. But only humans can enjoy writing code, and that joy itself can be seen as an act of <a href="https://en.wikipedia.org/wiki/Joy_as_an_Act_of_Resistance">resistance</a>. 

<img src="/human_coder.png" alt="Wetware at work" width="128" height="128" />
