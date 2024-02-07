# kvhot

Automatically restarts the Kivy application whenever files within the project directory change.

No need to type `python main.py` each time, making a small change in the code 😄.

### Installation

`pip install kvhot`

### Demo

https://user-images.githubusercontent.com/63696279/200531463-4ca1bbec-11e0-49ef-ad5f-b9fcc23760ba.mp4

### Usage

```
usage: kvhot [-h] [--width WIDTH] [--height HEIGHT] [--top TOP] [--left LEFT] [-b BLACKLIST [BLACKLIST ...]] [-V] target_dir

Automatically restarts the Kivy application whenever files within the project's target directory change.

positional arguments:
  target_dir            directory of the entry-point (main.py) of the kivy application

options:
  -h, --help            show this help message and exit
  --width WIDTH         width of the window.
  --height HEIGHT       height of the window.
  --top TOP             top position of the window.
  --left LEFT           left position of the window.
  -b BLACKLIST [BLACKLIST ...], --blacklist BLACKLIST [BLACKLIST ...]
                        exclude specific files/dirs from being monitored.
  -V, --version         show program's version number and exit
```

*(Works on windows, linux and osx)*
