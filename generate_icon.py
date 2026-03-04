#!/usr/bin/env python3
"""Generate a clean, minimalist browser + search bar icon for the Raycast extension."""

from PIL import Image, ImageDraw, ImageFilter
import math

SIZE = 512
PADDING = 0  # Icon padding within canvas


def make_gradient_bg(size):
    """Create a rich indigo-to-purple gradient background with rounded corners."""
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))

    # Create gradient
    gradient = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    for y in range(size):
        for x in range(size):
            # Diagonal gradient: top-left indigo -> bottom-right purple
            t = (x / size * 0.4 + y / size * 0.6)
            r = int(35 + t * 55)       # 35 -> 90
            g = int(25 + t * 5)        # 25 -> 30
            b = int(120 + t * 60)      # 120 -> 180
            gradient.putpixel((x, y), (r, g, b, 255))

    # Rounded rectangle mask
    mask = Image.new("L", (size, size), 0)
    mask_draw = ImageDraw.Draw(mask)
    mask_draw.rounded_rectangle([0, 0, size - 1, size - 1], radius=100, fill=255)

    img = Image.composite(gradient, Image.new("RGBA", (size, size), (0, 0, 0, 0)), mask)
    return img


def draw_icon():
    img = make_gradient_bg(SIZE)
    draw = ImageDraw.Draw(img)

    # === Browser Window ===
    bx1, by1 = 58, 72
    bx2, by2 = SIZE - 58, SIZE - 90
    browser_radius = 28

    # Shadow behind browser (draw on separate layer then composite)
    shadow_layer = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
    shadow_draw = ImageDraw.Draw(shadow_layer)
    shadow_offset = 6
    shadow_draw.rounded_rectangle(
        [bx1 + 3, by1 + shadow_offset, bx2 + 3, by2 + shadow_offset],
        radius=browser_radius,
        fill=(0, 0, 0, 50),
    )
    shadow_layer = shadow_layer.filter(ImageFilter.GaussianBlur(radius=12))
    img = Image.alpha_composite(img, shadow_layer)
    draw = ImageDraw.Draw(img)

    # Browser window - frosted glass look
    # Draw semi-transparent white fill
    browser_layer = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
    bl_draw = ImageDraw.Draw(browser_layer)
    bl_draw.rounded_rectangle(
        [bx1, by1, bx2, by2],
        radius=browser_radius,
        fill=(255, 255, 255, 30),
        outline=(255, 255, 255, 90),
        width=2,
    )
    img = Image.alpha_composite(img, browser_layer)
    draw = ImageDraw.Draw(img)

    # === Title Bar ===
    title_bar_h = 44
    title_bar_bottom = by1 + title_bar_h

    # Divider
    draw.line(
        [(bx1 + 12, title_bar_bottom), (bx2 - 12, title_bar_bottom)],
        fill=(255, 255, 255, 45),
        width=1,
    )

    # Window dots
    dot_r = 5
    dot_y = by1 + title_bar_h // 2
    dot_x_start = bx1 + 24
    dot_gap = 16
    for i, col in enumerate([(255, 95, 86), (255, 189, 46), (39, 201, 63)]):
        cx = dot_x_start + i * dot_gap
        draw.ellipse(
            [cx - dot_r, dot_y - dot_r, cx + dot_r, dot_y + dot_r],
            fill=(*col, 210),
        )

    # === Search Bar (HERO element) ===
    sx1 = bx1 + 18
    sx2 = bx2 - 18
    sy1 = title_bar_bottom + 16
    sy2 = sy1 + 54
    search_radius = 12

    # Bright glowing search bar
    # Glow behind
    glow_layer = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
    glow_draw = ImageDraw.Draw(glow_layer)
    glow_draw.rounded_rectangle(
        [sx1 - 4, sy1 - 4, sx2 + 4, sy2 + 4],
        radius=search_radius + 4,
        fill=(120, 160, 255, 50),
    )
    glow_layer = glow_layer.filter(ImageFilter.GaussianBlur(radius=8))
    img = Image.alpha_composite(img, glow_layer)
    draw = ImageDraw.Draw(img)

    # Search bar fill
    search_layer = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
    sl_draw = ImageDraw.Draw(search_layer)
    sl_draw.rounded_rectangle(
        [sx1, sy1, sx2, sy2],
        radius=search_radius,
        fill=(255, 255, 255, 220),
    )
    img = Image.alpha_composite(img, search_layer)
    draw = ImageDraw.Draw(img)

    # Magnifying glass in search bar
    mag_cx = sx1 + 30
    mag_cy = (sy1 + sy2) // 2
    mag_r = 9
    stroke_w = 3
    glass_color = (70, 70, 110, 230)

    draw.ellipse(
        [mag_cx - mag_r, mag_cy - mag_r, mag_cx + mag_r, mag_cy + mag_r],
        outline=glass_color,
        width=stroke_w,
    )
    # Handle
    hx1 = mag_cx + int(mag_r * 0.7)
    hy1 = mag_cy + int(mag_r * 0.7)
    draw.line(
        [(hx1, hy1), (hx1 + 7, hy1 + 7)],
        fill=glass_color,
        width=stroke_w,
    )

    # "URL" placeholder bar
    url_x1 = mag_cx + mag_r + 18
    url_y = mag_cy
    url_color = (90, 90, 130, 140)
    draw.rounded_rectangle(
        [url_x1, url_y - 5, url_x1 + 130, url_y + 5],
        radius=4,
        fill=url_color,
    )
    # Second shorter segment (like a domain + path)
    draw.rounded_rectangle(
        [url_x1 + 140, url_y - 5, url_x1 + 200, url_y + 5],
        radius=4,
        fill=(90, 90, 130, 90),
    )

    # === Content Area - Globe icons representing browsers ===
    content_area_top = sy2 + 20
    content_area_bottom = by2 - 16
    content_cx = (bx1 + bx2) // 2
    content_area_h = content_area_bottom - content_area_top

    def draw_globe(img, cx, cy, radius, alpha, color_tint=(255, 255, 255)):
        """Draw a minimalist globe icon (circle + meridian + equator)."""
        layer = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
        ld = ImageDraw.Draw(layer)
        r, g, b = color_tint
        stroke = max(2, radius // 10)

        # Outer circle
        ld.ellipse(
            [cx - radius, cy - radius, cx + radius, cy + radius],
            outline=(r, g, b, alpha),
            width=stroke,
        )

        # Horizontal equator line
        ld.arc(
            [cx - radius, cy - radius, cx + radius, cy + radius],
            start=0, end=360,
            fill=(r, g, b, alpha),
            width=stroke,
        )

        # Vertical meridian (full ellipse)
        meridian_w = radius * 0.45
        ld.ellipse(
            [cx - meridian_w, cy - radius, cx + meridian_w, cy + radius],
            outline=(r, g, b, alpha),
            width=stroke,
        )

        # Horizontal line through center
        ld.line(
            [(cx - radius, cy), (cx + radius, cy)],
            fill=(r, g, b, alpha),
            width=stroke,
        )

        # Upper latitude line
        lat_offset = radius * 0.45
        lat_w = radius * 0.85
        ld.arc(
            [cx - lat_w, cy - lat_offset - radius * 0.3,
             cx + lat_w, cy - lat_offset + radius * 0.3],
            start=0, end=360,
            fill=(r, g, b, int(alpha * 0.7)),
            width=max(1, stroke - 1),
        )

        # Lower latitude line
        ld.arc(
            [cx - lat_w, cy + lat_offset - radius * 0.3,
             cx + lat_w, cy + lat_offset + radius * 0.3],
            start=0, end=360,
            fill=(r, g, b, int(alpha * 0.7)),
            width=max(1, stroke - 1),
        )

        return Image.alpha_composite(img, layer)

    # Three globes arranged horizontally in the content area
    globe_r = 32
    globe_cy = content_area_top + content_area_h // 2
    globe_spacing = 105
    globes = [
        (content_cx - globe_spacing, globe_cy, 130, (180, 210, 255)),   # blue-white
        (content_cx, globe_cy, 140, (255, 255, 255)),                    # white
        (content_cx + globe_spacing, globe_cy, 130, (200, 180, 255)),   # purple-white
    ]

    for gx, gy, ga, gc in globes:
        img = draw_globe(img, gx, gy, globe_r, ga, gc)

    draw = ImageDraw.Draw(img)

    return img


# Generate and save
icon = draw_icon()
icon.save("/home/user/open-browser-search/assets/search-icon.png")
icon.save("/home/user/open-browser-search/assets/search-icon@dark.png")

# Also generate a small preview to check readability
small = icon.resize((64, 64), Image.LANCZOS)
small.save("/home/user/open-browser-search/assets/search-icon-64px-preview.png")
tiny = icon.resize((32, 32), Image.LANCZOS)
tiny.save("/home/user/open-browser-search/assets/search-icon-32px-preview.png")

print("Done! Generated:")
print(f"  search-icon.png (512x512)")
print(f"  search-icon@dark.png (512x512)")
print(f"  search-icon-64px-preview.png (64x64)")
print(f"  search-icon-32px-preview.png (32x32)")
