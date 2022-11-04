# Kivy-hotrestarter

Hotrestarts kivy application whenever project files changes.

No need to type `python main.py` each time, making a small change in the code 😄.

### Installation

Requires Python >= 3.7

watchfiles==0.18.0


### Demo

https://user-images.githubusercontent.com/63696279/199995369-1a57bdb4-77b6-4cf0-8f0b-07e0ede3100e.mp4


### Usage

```
usage: Kivy hotrestarter [-h] [--width WIDTH] [--height HEIGHT] [--top TOP]
                         [--left LEFT]
                         target_dir

Hotrestarts kivy application when project (target_dir) files changes.

positional arguments:
  target_dir       Directory of the entry-point (main.py) of the kivy
                   application

optional arguments:
  -h, --help       show this help message and exit
  --width WIDTH    Width of the window.
  --height HEIGHT  Height of the window.
  --top TOP        Top position of the window.
  --left LEFT      Left position of the window.
```

(Works on windows, linux and osx)
