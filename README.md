# PixelPlotter

**PixelPlotter** is a command-line tool that ingests images and then uses streamplots from Matplotlib to generate newly manipulated images. 

By calculating image gradients using OpenCV Sobel operators and plotting the perpendicular vector fields with Matplotlib, this script generates "streamline" portraits and abstract images.


## Features
* **Granular Detail Control:** Adjust grid spacing and line density to range from minimalist abstract shapes to highly detailed photorealistic sketches.
* **Massive Color Library:** Supports 160+ Matplotlib colormaps, Tableau/CSS named colors, hex codes, or direct pixel color sampling from the original image.
* **Mathematical Flow Control:** Fine-tune the underlying vector math (Sobel kernel sizes, streamline integration lengths) to change the "texture" of the lines.
* **Smart Downscaling:** Optional built-in limiters to process massive images quickly without crashing.
* **Silent Rendering:** Easily render straight to disk for batch processing.

## Requirements

This tool requires **Python 3** and the following libraries:
* `opencv-python`
* `numpy`
* `matplotlib`

You can install the dependencies via pip:

```bash
pip install opencv-python numpy matplotlib
```

## Quick Start

Run the script by pointing it to an image. By default, it will open a preview window where you can manually save the result.

```bash
python3 pixelplotter.py your_photo.jpg
```

### More Examples

**1. Blueprint Look** (Solid blue lines on a dark background)
```bash
python3 pixelplotter.py photo.jpg -c tab:blue -bg 10 10 15 -lw 1.0 -s 1
```

**2. High-Detail Liquid Flow** (Dense, smooth lines with native colors)
```bash
python3 pixelplotter.py photo.jpg -d 4 -den 5.0 -s 8 --sample
```

**3. Silent Batch Render** (Limits file size for speed and saves directly to disk)
```bash
python3 pixelplotter.py photo.jpg -o output_art.png -limit 1500 -c random
```

---

## Command Line Arguments

### Basic Options
| Flag | Name | Default | Description |
| :--- | :--- | :--- | :--- |
| `image` | Input Image | `None` | Path to the source image file. |
| `-o` | `--output` | `None` | Path to save the file (e.g., `render.png`). Skips the preview window if used. |
| `-limit` | `--limit` | `0` (Off) | Max image dimension. If this switch is used and the limit is exceeded, the image is downscaled before math begins. Great for speed. |

### Aesthetic & Style Levers
| Flag | Name | Default | Description |
| :--- | :--- | :--- | :--- |
| `-d` | `--detail` | `8` | Grid spacing (2-100). Lower numbers = tighter grids / more detail. |
| `-den` | `--density` | `3.0` | Closeness of lines (0.1-10.0). Higher = less white space. Affects processing time |
| `-lw` | `--linewidth` | `1.5` | Base multiplier for stroke thickness. |
| `-bg` | `--background` | `255 255 255` | Background color as RGB integers (0-255). |
| `--no-arrows`| Disable Arrows| `False` | Removes the "fancy" directional arrowheads from the lines. |

### Color Options (`-c` / `--cmap`)
You can pass multiple formats into the `-c` flag. (Default is `viridis`).
* **Matplotlib Colormaps:** `magma`, `Blues`, `autumn`, etc. (Use `--list-cmaps` to see all 160+ options).
* **Base/Named Colors:** `b`, `k`, `tab:blue`, `dodgerblue`, `limegreen`.
* **Hex Codes:** `#FF5733`, `#2C3E50`.
* **Random:** Type `random` to let the script pick a verified colormap for you.
* **Override Flag:** Use `--sample` to ignore the `-c` flag entirely and color the lines using the actual RGB pixels from the original photo.

### Advanced Mathematical Control
Some of these flags can severely affect processing time. Beware.
| Flag | Name | Default | Description |
| :--- | :--- | :--- | :--- |
| `-s` | `--smooth` | `3` | Pre-processing Gaussian blur (0-99). Higher = ignores texture for graceful, liquid curves. |
| `-gx` / `-gy` | Kernel Size | `3` | Sobel operator lookahead size (1-31, odd numbers). Higher = broader flow detection. |
| `-int` | `--integration` | `both` | Streamline growth direction: `both`, `forward`, or `backward`. |
| `-max` | `--maxlength` | `4.0` | How far a line can travel across the axes before being forced to stop. |
| `-min` | `--minlength` | `0.1` | Filter for short lines. Set to `0.01` to keep dots/noise, or `1.0`+ to keep only massive sweeps. |

---

## Some tips
* **Too much white space?** Increase `--density` to `5.0` or `8.0`.
* **Lines look too jagged?** Increase `--smooth` to `7` or `11` to force the vector field to ignore tiny pixel noise.
* **Taking too long?** If you are processing a 4K image, add `-limit 1500` to your command, or increase the detail spacing to `-d 12`.

---

## Disclaimer

**PixelPlotter** is provided "as is" for artistic and educational purposes. 

* **No Liability:** The author is not responsible for any damages, data loss, or system issues resulting from the use of this software. 
* **Content Responsibility:** Users are solely responsible for the images they process. Ensure you have the legal right to use and modify any source imagery you input into this tool.
* **Artistic Ownership:** The author claims no ownership over the works generated by users through this software. The copyright of the output remains with the user, subject to the license of the original source material.



## License

This project is licensed under the **MIT License**. See the `LICENSE` file for full legal text.