This Kivy bar graph widget seeks to emulate the appearance of liquid inside a sight glass. It is currently at an experimental stage, to be considered early apha at best. 

> A sight glass or water gauge is a type of level sensor, a transparent tube through which the operator of a tank or boiler can observe the level of liquid contained within. 

https://en.wikipedia.org/wiki/Sight_glass

<img width="256" height="256" src="https://github.com/clickworkorange/KivySightGlass/assets/196348/ed7e3588-d459-4c0e-b272-cd42b7b79896" />

#### Early preview video of a SightGlass in action
 
https://user-images.githubusercontent.com/196348/236925312-69ec6e30-d9bc-431e-9c68-30a9c2b886dd.mp4

#### Example usage
````kv
    SightGlass:
        id: myglass
        size_hint: .2,1
        glass_color: rgba(127,191,255,63)
        glass_shade: rgba(0,0,0,63)
        liquid_color: rgba(0,215,255,255)
        level:33
        scale:10
        scale_color: rgba(255,255,255,95)

    Button:
        on_press: myglass.level=90
````

#### Installation
Clone the repository and install with `pip install .`

#### This code was written by a human
Resistance may be futile, but only humans can enjoy writing code. 

<img src="/human_coder.png" alt="Bad Bot" width="128" height="128" />
