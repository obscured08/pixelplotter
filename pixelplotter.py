import cv2
import numpy as np
import matplotlib.pyplot as plt
import os
import argparse
import random
from matplotlib.colors import is_color_like, ListedColormap, LogNorm, PowerNorm

# Full list of Matplotlib colormaps
VALID_CMAPS = [
    'Accent', 'Accent_r', 'Blues', 'Blues_r', 'BrBG', 'BrBG_r', 'BuGn', 'BuGn_r', 'BuPu', 'BuPu_r', 
    'CMRmap', 'CMRmap_r', 'Dark2', 'Dark2_r', 'GnBu', 'GnBu_r', 'Grays', 'Grays_r', 'Greens', 'Greens_r', 
    'Greys', 'Greys_r', 'OrRd', 'OrRd_r', 'Oranges', 'Oranges_r', 'PRGn', 'PRGn_r', 'Paired', 'Paired_r', 
    'Pastel1', 'Pastel1_r', 'Pastel2', 'Pastel2_r', 'PiYG', 'PiYG_r', 'PuBu', 'PuBuGn', 'PuBuGn_r', 
    'PuBu_r', 'PuOr', 'PuOr_r', 'PuRd', 'PuRd_r', 'Purples', 'Purples_r', 'RdBu', 'RdBu_r', 'RdGy', 
    'RdGy_r', 'RdPu', 'RdPu_r', 'RdYlBu', 'RdYlBu_r', 'RdYlGn', 'RdYlGn_r', 'Reds', 'Reds_r', 'Set1', 
    'Set1_r', 'Set2', 'Set2_r', 'Set3', 'Set3_r', 'Spectral', 'Spectral_r', 'Wistia', 'Wistia_r', 'YlGn', 
    'YlGnBu', 'YlGnBu_r', 'YlGn_r', 'YlOrBr', 'YlOrBr_r', 'YlOrRd', 'YlOrRd_r', 'afmhot', 'afmhot_r', 
    'autumn', 'autumn_r', 'berlin', 'berlin_r', 'binary', 'binary_r', 'bone', 'bone_r', 'brg', 'brg_r', 
    'bwr', 'bwr_r', 'cividis', 'cividis_r', 'cool', 'cool_r', 'coolwarm', 'coolwarm_r', 'copper', 
    'copper_r', 'cubehelix', 'cubehelix_r', 'flag', 'flag_r', 'gist_earth', 'gist_earth_r', 'gist_gray', 
    'gist_gray_r', 'gist_grey', 'gist_grey_r', 'gist_heat', 'gist_heat_r', 'gist_ncar', 'gist_ncar_r', 
    'gist_rainbow', 'gist_rainbow_r', 'gist_stern', 'gist_stern_r', 'gist_yarg', 'gist_yarg_r', 
    'gist_yerg', 'gist_yerg_r', 'gnuplot', 'gnuplot2', 'gnuplot2_r', 'gnuplot_r', 'gray', 'gray_r', 
    'grey', 'grey_r', 'hot', 'hot_r', 'hsv', 'hsv_r', 'inferno', 'inferno_r', 'jet', 'jet_r', 'magma', 
    'magma_r', 'managua', 'managua_r', 'nipy_spectral', 'nipy_spectral_r', 'ocean', 'ocean_r', 'pink', 
    'pink_r', 'plasma', 'plasma_r', 'prism', 'prism_r', 'rainbow', 'rainbow_r', 'seismic', 'seismic_r', 
    'spring', 'spring_r', 'summer', 'summer_r', 'tab10', 'tab10_r', 'tab20', 'tab20_r', 'tab20b', 
    'tab20b_r', 'tab20c', 'tab20c_r', 'terrain', 'terrain_r', 'turbo', 'turbo_r', 'twilight', 
    'twilight_r', 'twilight_shifted', 'twilight_shifted_r', 'vanimo', 'vanimo_r', 'viridis', 
    'viridis_r', 'winter', 'winter_r'
]

def generate_streamplot(image_path, detail, colormap_or_color, show_arrows, bg_color, intensity, smooth, sample_colors, density, gx_k, gy_k, integration, max_len, min_len, output_path, limit, taper, unbroken, spread, norm_type, random_starts, padding, pad_mode, angle):
    if not os.path.isfile(image_path):
        print(f"Error: File '{image_path}' not found.")
        return

    img_bgr = cv2.imread(image_path)
    if img_bgr is None:
        print("Error: Could not load image.")
        return
    
    # Apply Padding (Border)
    if padding > 0:
        h, w = img_bgr.shape[:2]
        pad_h = int(h * (padding / 100.0))
        pad_w = int(w * (padding / 100.0))
        
        if pad_mode == 'replicate':
            img_bgr = cv2.copyMakeBorder(img_bgr, pad_h, pad_h, pad_w, pad_w, cv2.BORDER_REPLICATE)
        else:
            # Background color for OpenCV is BGR
            bg_bgr = (bg_color[2], bg_color[1], bg_color[0])
            img_bgr = cv2.copyMakeBorder(img_bgr, pad_h, pad_h, pad_w, pad_w, cv2.BORDER_CONSTANT, value=bg_bgr)
            
        print(f"[*] Applied {padding}% padding ({pad_w}px x {pad_h}px border, mode: {pad_mode})")
    
    # limit resize stuff
    if limit > 0:
        h, w = img_bgr.shape[:2]
        max_dim = max(h, w)
        if max_dim > limit:
            scale = limit / max_dim
            img_bgr = cv2.resize(img_bgr, (int(w * scale), int(h * scale)), interpolation=cv2.INTER_AREA)
            print(f"[*] Image downscaled to max dimension {limit}px (Scale factor: {scale:.2f})")

    img_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)
    img_gray = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)

    if smooth > 0:
        k = smooth if smooth % 2 != 0 else smooth + 1
        processed_img = cv2.GaussianBlur(img_gray, (k, k), 0)
    else:
        processed_img = img_gray

    img_inv = cv2.bitwise_not(processed_img)
    norm = img_inv.astype(np.float32) / 255.0

    # ensures ksizes are odd and in range (max 31 for OpenCV Sobel)
    gx_k = max(1, min(31, gx_k if gx_k % 2 != 0 else gx_k + 1))
    gy_k = max(1, min(31, gy_k if gy_k % 2 != 0 else gy_k + 1))

    gx = cv2.Sobel(norm, cv2.CV_32F, 1, 0, ksize=gx_k)
    gy = cv2.Sobel(norm, cv2.CV_32F, 0, 1, ksize=gy_k)
    u, v = -gy, gx

    h, w = img_gray.shape
    y, x = np.mgrid[0:h, 0:w]
    skip = detail
    X_s, Y_s = x[::skip, ::skip], y[::skip, ::skip]
    U_s, V_s = u[::skip, ::skip], v[::skip, ::skip]
    
    # Apply vector rotation if angle is not 0
    if angle != 0.0:
        theta = np.radians(angle)
        cos_t = np.cos(theta)
        sin_t = np.sin(theta)
        U_rot = (U_s * cos_t) - (V_s * sin_t)
        V_rot = (U_s * sin_t) + (V_s * cos_t)
        U_s, V_s = U_rot, V_rot

    speed = np.sqrt(U_s**2 + V_s**2)
    brightness_sample = norm[::skip, ::skip]
    
    # Taper logic
    if taper != 0.0:
        speed_norm = (speed - speed.min()) / (speed.max() - speed.min() + 1e-6)
        
        # Safeguard for negative exponents to avoid dividing by absolute zero
        if taper < 0:
            speed_norm = np.clip(speed_norm, 1e-4, 1.0)
            
        lw_array = (np.power(speed_norm, taper) * intensity) + 0.05
    else:
        lw_array = (brightness_sample * intensity) + 0.2

    # the colors
    active_cmap = None
    line_color_data = None

    if sample_colors:
        sampled_rgb = img_rgb[::skip, ::skip] / 255.0
        flat_colors = sampled_rgb.reshape(-1, 3)
        active_cmap = ListedColormap(flat_colors)
        line_color_data = np.arange(len(flat_colors)).reshape(X_s.shape)
    elif "," in colormap_or_color:
        palette = [c.strip() for c in colormap_or_color.split(",")]
        if all(is_color_like(c) for c in palette):
            active_cmap = ListedColormap(palette)
            line_color_data = speed
            print(f"[*] Custom palette detected: {palette}")
        else:
            print("[!] Warning: One or more colors in your palette were invalid. Falling back to viridis.")
            active_cmap = 'viridis'
            line_color_data = speed
    elif colormap_or_color in VALID_CMAPS:
        line_color_data = speed
        active_cmap = colormap_or_color
    elif is_color_like(colormap_or_color):
        line_color_data = colormap_or_color
        active_cmap = None
    else:
        line_color_data = speed
        active_cmap = 'viridis'

    # Handle Normalization logic (only applies if mapped to speed)
    active_norm = None
    if norm_type != 'linear' and active_cmap and not sample_colors:
        if norm_type == 'log':
            active_norm = LogNorm(vmin=max(speed.min(), 1e-6), vmax=speed.max())
        elif norm_type == 'power':
            active_norm = PowerNorm(gamma=0.5, vmin=speed.min(), vmax=speed.max())

    # Handle Random Start Points
    starts = None
    if random_starts > 0:
        starts = np.column_stack([
            np.random.uniform(X_s.min(), X_s.max(), random_starts),
            np.random.uniform(Y_s.min(), Y_s.max(), random_starts)
        ])

    final_bg = tuple(c/255.0 for c in bg_color)
    fig, ax = plt.subplots(figsize=(12, 10))
    fig.patch.set_facecolor(final_bg)
    ax.set_facecolor(final_bg)
    
    astyle = 'fancy' if show_arrows else '-'
    
    # Determine the density logic (tuple override)
    plot_density = tuple(spread) if spread else density

    # Base Keyword Arguments for Streamplot
    stream_kwargs = {
        'color': line_color_data, 
        'cmap': active_cmap, 
        'linewidth': lw_array,
        'density': plot_density,
        'arrowstyle': astyle, 
        'arrowsize': 1.2 * (intensity / 1.0),
        'integration_direction': integration,
        'maxlength': max_len,
        'minlength': min_len
    }

    # Conditionally add advanced kwargs to prevent Matplotlib conflicts
    if starts is not None:
        stream_kwargs['start_points'] = starts
    if active_norm is not None:
        stream_kwargs['norm'] = active_norm
    if unbroken:
        stream_kwargs['broken_streamlines'] = False

    ax.streamplot(X_s, Y_s, U_s, V_s, **stream_kwargs)

    ax.set_aspect('equal')
    ax.invert_yaxis()
    ax.axis('off')

    # Output / Display Logic
    if output_path:
        plt.savefig(output_path, dpi=300, facecolor=fig.get_facecolor(), bbox_inches='tight')
        print(f"Success! Output silently saved to: {output_path}")
    else:
        print("Opening display window... (Use the floppy disk icon in the toolbar to save manually)")
        plt.show()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Transform an image into a high-resemblance streamplot art piece.",
        formatter_class=argparse.RawTextHelpFormatter,
        epilog="Examples:\n"
               "  python3 script.py photo.jpg -c tab:blue -bg 0 0 0\n"
               "  python3 script.py photo.jpg -d 4 -lw 0.5 -s 1 --sample\n"
               "  python3 script.py photo.jpg -o final_render.png -int forward -max 8.0 -limit 1500"
    )
    
    parser.add_argument("image", nargs="?", help="Path to the input image file.")

    parser.add_argument("-o", "--output", type=str, default=None,
        help="Optional: Path to explicitly save the output image (e.g., 'result.png').\n"
             "If provided, the script will save the file and skip opening the display window.")

    parser.add_argument("-d", "--detail", type=int, default=8, 
        help="Grid spacing (Range: 2 to 100).\n"
             "  2-5: Extremely high detail (Slowest).\n"
             "  6-15: Standard artistic detail.\n"
             "  16-100: Abstract/Minimalist look.\n"
             "Default: 8")
    
    parser.add_argument("-c", "--cmap", type=str, default="viridis",
        help="Color or Colormap choice. Accepts one of following six formats at a time:\n\n"
             "  1. MATPLOTLIB COLORMAPS: 'magma', 'inferno', 'Blues', etc. (See --list-cmaps)\n"
             "  2. BASE COLORS: 'b', 'g', 'r', 'c', 'm', 'y', 'k', 'w'\n"
             "  3. TABLEAU & CSS NAMES: 'tab:blue', 'dodgerblue', 'limegreen', etc.\n"
             "  4. HEXADECIMAL STRINGS: '#FF5733', '#2C3E50', etc.\n"
             "  5. GRAYSCALE VALUES: '0.0' (black) to '1.0' (white).\n"
             "  6. CUSTOM PALETTE: '#000000, #FFFFFF, red, blue' (Comma separated)\n"
             "  * Use 'random' to pick a verified colormap at random.\n"
             "Default: viridis")
    
    parser.add_argument("-bg", "--background", type=int, nargs=3, default=[255, 255, 255],
        metavar=('R', 'G', 'B'), 
        help="Background color as RGB integers (0-255).\n"
             "Default: 255 255 255")

    parser.add_argument("-lw", "--linewidth", type=float, default=1.5,
        help="Base multiplier for line thickness (Range: 0.1 to 10.0).\n"
             "Default: 1.5")
    
    parser.add_argument("-den", "--density", type=float, default=3.0,
        help="Controls the closeness of streamlines (Range: 0.1 to 10.0).\n"
             "  Higher values = more packed lines (less white space).\n"
             "Default: 3.0")
             
    parser.add_argument("-sp", "--spread", type=float, nargs=2, default=None,
        metavar=('X', 'Y'),
        help="Directional density as a tuple (e.g., 1.0 5.0). Overrides -den.\n"
             "Allows stretching the grid to favor horizontal or vertical flow.")
    
    parser.add_argument("-s", "--smooth", type=int, default=3,
        help="Pre-processing gaussian Blur strength (Range: 0 to 99).\n"
             "  0: Raw/Jagged lines (Gritty resemblance).\n"
             "  1-9: Flowing liquid lines (Natural resemblance).\n"
             "Default: 3")

    parser.add_argument("-limit", "--limit", type=int, default=0,
        help="Optional: Maximum image dimension in pixels (e.g., 1500).\n"
             "If the image is larger, it will be downscaled before processing.\n"
             "0 = No limit (Process at original resolution).\n"
             "Default: 0")

    parser.add_argument("-gx", "--gx_ksize", type=int, default=3,
        help="Sobel operator kernel size for the X-axis gradient (Range: 1 to 31).\n"
             "Must be an odd number (even inputs are auto-adjusted).\n"
             "  Higher = ignores small details for broader flow calculations.\n"
             "Default: 3")

    parser.add_argument("-gy", "--gy_ksize", type=int, default=3,
        help="Sobel operator kernel size for the Y-axis gradient (Range: 1 to 31).\n"
             "Must be an odd number (even inputs are auto-adjusted).\n"
             "Default: 3")

    parser.add_argument("-int", "--integration", type=str, choices=['both', 'forward', 'backward'], default='both',
        help="Direction to integrate the streamline from the starting point.\n"
             "  'both': Long, continuous flowing lines.\n"
             "  'forward'/'backward': Shorter, directional burst lines.\n"
             "Default: both")

    parser.add_argument("-max", "--maxlength", type=float, default=4.0,
        help="Maximum line length in axes coordinates (Range: 0.1 to 50.0).\n"
             "  0.1-1.0: Short, dashed brush strokes.\n"
             "  4.0: Standard flowing lines.\n"
             "  15.0+: Infinite spirograph loops (can be slow).\n"
             "Default: 4.0")

    parser.add_argument("-min", "--minlength", type=float, default=0.1,
        help="Minimum line length in axes coordinates (Range: 0.01 to 2.0).\n"
             "  Lines shorter than this are deleted.\n"
             "  0.01: Keeps all dots and noise.\n"
             "  1.0+: Strict filter, keeps only massive sweeping curves.\n"
             "Default: 0.1")

    parser.add_argument("-t", "--taper", type=float, default=0.0,
        help="Apply an ink-stroke taper effect using an exponent.\n"
             "  0.0: Off (Fixed width based on image brightness).\n"
             "  1.0: Standard taper (Ink brush effect based on speed).\n"
             "  2.0, 3.0+: Power Taper (Sharp calligraphy effect).\n"
             "  0.5: Bulging effect (Thick lines, tiny tapers).\n"
             " -1.0: Inverted taper (Thick in slow areas, thin in fast).\n"
             "Default: 0.0")
             
    parser.add_argument("-p", "--padding", type=int, default=0,
        help="Percentage of background-colored padding to add to edges (0-100).\n"
             "Allows lines to taper out naturally before hitting the file boundary.\n"
             "Default: 0")

    parser.add_argument("-pm", "--pad-mode", type=str, choices=['constant', 'replicate'], default='constant',
        help="Padding mode if -p is used.\n"
             "  'constant': Uses solid background color (Creates a frame/boundary).\n"
             "  'replicate': Stretches edge pixels (Allows organic bleed).\n"
             "Default: constant")

    parser.add_argument("-a", "--angle", type=float, default=0.0, 
        help="Rotate the final vector field by a specific degree angle (e.g., 45.0).\n"
             "Excellent for creating diagonal striping when paired with mismatched Sobel kernels.\n"
             "Default: 0.0")

    parser.add_argument("--norm", type=str, choices=['linear', 'log', 'power'], default='linear',
        help="Color normalization curve for mapping speeds to colors.\n"
             "  linear: Standard mapping.\n"
             "  log: Emphasizes lower speeds.\n"
             "  power: Accentuates highest speeds.\n"
             "Default: linear")
             
    parser.add_argument("-rs", "--random-starts", type=int, default=0,
        help="Number of random seed points for streamlines (e.g., 5000).\n"
             "Overrides density grid seeding. Great for organic/chaotic looks.\n"
             "Default: 0 (Off)")

    parser.add_argument("--unbroken", action="store_true",
        help="Allow lines to weave and overlap without being terminated by collision.\n"
             "(Requires Matplotlib 3.6+).")

    parser.add_argument("--no-arrows", action="store_false", dest="arrows",
        help="Disable 'fancy' directional arrowheads.")

    parser.add_argument("--sample", action="store_true", 
        help="Sample actual RGB colors from the original image pixels.\n"
             "Note: This overrides the --cmap selection.")

    parser.add_argument("--list-cmaps", action="store_true", 
        help="Show all 160+ verified Matplotlib colormap names and exit.")
    
    parser.set_defaults(arrows=True)

    args = parser.parse_args()

    if args.list_cmaps:
        print("\n AVAILABLE COLORMAPS ")
        for i in range(0, len(VALID_CMAPS), 5):
            print("{:<18} {:<18} {:<18} {:<18} {:<18}".format(*VALID_CMAPS[i:i+5] + [''] * (5 - len(VALID_CMAPS[i:i+5]))))
        os.sys.exit(0)

    if not args.image:
        parser.print_help()
        os.sys.exit(1)

    if args.cmap.lower() == 'random' and not args.sample:
        args.cmap = random.choice(VALID_CMAPS)
        print(f"Randomly selected colormap: {args.cmap}")

    generate_streamplot(args.image, args.detail, args.cmap, args.arrows, args.background, 
                        args.linewidth, args.smooth, args.sample, args.density, 
                        args.gx_ksize, args.gy_ksize, args.integration, args.maxlength, 
                        args.minlength, args.output, args.limit, args.taper, 
                        args.unbroken, args.spread, args.norm, args.random_starts, args.padding, args.pad_mode, args.angle)