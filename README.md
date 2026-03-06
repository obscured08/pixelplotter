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

    pip install opencv-python numpy matplotlib

## Quick Start

Run the script by pointing it to an image. By default, it will open a preview window where you can manually save the result.

    python3 pixelplotter.py your_photo.jpg

### More Examples

**1. Blueprint Look** (Solid blue lines on a dark background)

    python3 pixelplotter.py photo.jpg -c tab:blue -bg 10 10 15 -lw 1.0 -s 1

**2. High-Detail Liquid Flow** (Dense, smooth lines with native colors)

    python3 pixelplotter.py photo.jpg -d 4 -den 5.0 -s 8 --sample

**3. Silent Batch Render** (Limits file size for speed and saves directly to disk)

    python3 pixelplotter.py photo.jpg -o output_art.png -limit 1500 -c random

---

## Command Line Arguments

*Note: Some of the advanced mathematical options can severely affect processing time.*

| Flag | Name | Default | Description |
| :--- | :--- | :--- | :--- |
| `image` | Input Image | `None` | Path to the input image file. |
| `-o`, `--output` | Output Path | `None` | Optional: Path to explicitly save the output image (e.g., 'result.png'). Skips display window. |
| `-d`, `--detail` | Grid Detail | `8` | Grid spacing (Range: 2 to 100). Lower is slower/detailed, higher is abstract. |
| `-c`, `--cmap` | Colormap | `viridis` | Color or Colormap choice. Accepts Matplotlib cmaps, hex, CSS names, or 'random'. |
| `-bg`, `--background` | Background | `255 255 255` | Background color as RGB integers (0-255). |
| `-lw`, `--linewidth` | Linewidth | `1.5` | Base multiplier for line thickness (Range: 0.1 to 10.0). |
| `-den`, `--density` | Density | `3.0` | Controls streamline closeness. Higher = more packed lines. |
| `-sp`, `--spread` | Spread | `None` | Directional density tuple (e.g., 1.0 5.0). Overrides density and stretches the grid. |
| `-s`, `--smooth` | Smooth Blur | `3` | Pre-processing gaussian Blur strength (0-99). Higher = smoother flow. |
| `-limit`, `--limit` | Size Limit | `0` (Off) | Max image dimension in pixels. Downscales larger images before processing. |
| `-gx`, `--gx_ksize` | X-Gradient | `3` | Sobel operator kernel size for the X-axis gradient (Range: 1 to 31, odd). |
| `-gy`, `--gy_ksize` | Y-Gradient | `3` | Sobel operator kernel size for the Y-axis gradient (Range: 1 to 31, odd). |
| `-int`, `--integration` | Integration | `both` | Direction to integrate from the starting point: 'both', 'forward', or 'backward'. |
| `-max`, `--maxlength` | Max Length | `4.0` | Maximum line length in axes coordinates before being forced to stop. |
| `-min`, `--minlength` | Min Length | `0.1` | Minimum line length. Lines shorter than this are deleted. |
| `-t`, `--taper` | Ink Taper | `0.0` (Off) | Ink-stroke taper exponent. 1.0 = Standard, 2.0 = Calligraphy, -1.0 = Inverted. |
| `-p`, `--padding` | Padding | `0` | Percentage of background-colored padding to add to edges. Allows lines to taper out. |
| `-a`, `--angle` | Angle | `0.0` | Rotate the final vector field by a specific degree angle (e.g., 45.0). |
| `--norm` | Color Norm | `linear` | Color normalization curve for mapping speeds: 'linear', 'log', or 'power'. |
| `-rs`, `--random-starts` | Random Starts | `0` (Off) | Number of random seed points. Overrides density grid. Great for organic/chaotic looks. |
| `--unbroken` | Unbroken | `False` | Allow lines to weave and overlap without being terminated by collision (Matplotlib 3.6+). |
| `--no-arrows` | No Arrows | `False` | Disable directional arrowheads. |
| `--sample` | Sample Colors | `False` | Sample actual RGB colors from original pixels. Overrides colormap. |
| `--list-cmaps` | List Cmaps | `False` | Show all 160+ verified Matplotlib colormap names and exit. |

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