# Fontx2-converter
FONTX2 conversion utilities.

## fontx2-cli.py

Import:
- FONTX2 binary file
- FONTX2 JSON format

Utils:
- crop borders (sx, dx, top, bottom)

Export:
- FONTX2 binary file
- FONTX2 JSON format
- JPEG image

```
usage: fontx2-cli.py [-h] [--from_binary FROM_BINARY] [--from_json FROM_JSON] [--new NEW] [--start_char START_CHAR] [--stop_char STOP_CHAR]
                     [--width WIDTH] [--height HEIGHT] [--crop_sx CROP_SX] [--crop_dx CROP_DX] [--crop_top CROP_TOP]
                     [--crop_bottom CROP_BOTTOM] [--to_binary TO_BINARY] [--to_json TO_JSON] [--to_jpg TO_JPG]

Convert FontX2

optional arguments:
  -h, --help            show this help message and exit
  --from_binary FROM_BINARY
                        FontX2 filename (binary version).

  --from_json FROM_JSON
                        FontX2 filename (json version).
  --new NEW             FontX2 new json filename.
  --start_char START_CHAR
                        ONLY USED FOR NEW FONT. Starting char. (default: 32)
  --stop_char STOP_CHAR
                        ONLY USED FOR NEW FONT. Stopping char. (default: 127)
  --width WIDTH         ONLY USED FOR NEW FONT. Font width. (default: 16)
  --height HEIGHT       ONLY USED FOR NEW FONT. Font height. (default: 16)
  --crop_sx CROP_SX     Crop sx
  --crop_dx CROP_DX     Crop dx
  --crop_top CROP_TOP   Crop top
  --crop_bottom CROP_BOTTOM
                        Crop bottom
  --to_binary TO_BINARY
                        FontX2 filename (binary version).
  --to_json TO_JSON     FontX2 filename (json version).
  --to_jpg TO_JPG       Dump font in jpeg format.
```

# demo fonts
Example fonts from https://github.com/tuupola/embedded-fonts.
