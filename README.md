This Kivy bar graph widget seeks to emulate the stylized appearance of liquid inside a sight glass. It is currently at an experimental stage - consider it early alpha at best. 

> A sight glass or water gauge is a type of level sensor, a transparent tube through which the operator of a tank or boiler can observe the level of liquid contained within. 

https://en.wikipedia.org/wiki/Sight_glass

<img width="256" height="256" src="https://github.com/clickworkorange/KivySightGlass/assets/196348/ed7e3588-d459-4c0e-b272-cd42b7b79896" />

#### Early preview video of a SightGlass in action

https://github.com/clickworkorange/KivySightGlass/assets/196348/2d69461b-6e3f-4ba8-ab48-24d1cc258f69

#### Example usage
````kv
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

#### Installation
Clone the repository and install with `pip install .`

#### This code was written by a human
Resistance may be futile, but only humans can enjoy writing code. 

<img src="/human_coder.png" alt="Bad Bot" width="128" height="128" />
