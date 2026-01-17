#!/usr/bin/env python3
"""
Celestial Uproar - 大闹天宫
A visual art piece capturing the explosive energy of rebellion
Final masterpiece version with refined craftsmanship
"""

from PIL import Image, ImageDraw, ImageFont, ImageFilter
import math
import random
import os

# Canvas settings
WIDTH = 2000
HEIGHT = 2800

# Refined color palette - carefully calibrated
BG_COLOR = (10, 10, 18)
CRIMSON = (168, 22, 38)
VOLCANIC = (210, 52, 12)
IMPERIAL_GOLD = (252, 178, 38)
CELESTIAL_AZURE = (32, 72, 128)
CLOUD_WHITE = (250, 250, 254)
ENERGY_ORANGE = (252, 108, 28)
DEEP_BLUE = (18, 28, 58)
GOLD_LIGHT = (255, 212, 98)

def interpolate_color(c1, c2, t):
    """Smooth color interpolation"""
    return tuple(int(c1[i] + (c2[i] - c1[i]) * t) for i in range(3))

def create_refined_cloud(draw, center_x, center_y, radius, base_color, rotation=0, layers=5):
    """Create multi-layered organic cloud forms with precision"""
    for layer in range(layers):
        scale = 1.0 - (layer * 0.1)
        r = radius * scale
        points = []
        num_points = 18

        for i in range(num_points):
            angle = (2 * math.pi * i / num_points) + rotation + (layer * 0.08)
            # More refined organic variation
            variation = 0.82 + 0.36 * math.sin(angle * 3.5) * math.cos(angle * 2)
            actual_r = r * variation
            px = center_x + actual_r * math.cos(angle)
            py = center_y + actual_r * math.sin(angle)
            points.append((px, py))

        # Color gradient by layer - more subtle transition
        color_factor = layer / layers
        layer_color = interpolate_color(base_color, BG_COLOR, color_factor * 0.5)
        draw.polygon(points, fill=layer_color)

def create_energy_wave(draw, center_x, center_y, max_radius, direction_angle, colors):
    """Create sweeping energy waves with better curvature"""
    num_waves = 8
    for i in range(num_waves):
        angle = direction_angle + (i - num_waves//2) * 0.14
        length = max_radius * (0.55 + 0.45 * (i / num_waves))

        # More refined curved wave form
        points = [center_x, center_y]
        for t in range(25):
            progress = t / 25
            r = length * progress
            curve = math.sin(progress * math.pi * 1.2) * 45 * (1 - progress * 0.7)
            px = center_x + r * math.cos(angle) + curve * math.cos(angle + math.pi/2)
            py = center_y + r * math.sin(angle) + curve * math.sin(angle + math.pi/2)
            points.extend([px, py])

        color = colors[i % len(colors)]
        # Better tapered polygon
        progress = 1.0
        width = ((1 - progress) * 28 + 4)
        perp_angle = angle + math.pi / 2
        p1x = points[-2] + width * math.cos(perp_angle)
        p1y = points[-1] + width * math.sin(perp_angle)
        p2x = points[-2] - width * math.cos(perp_angle)
        p2y = points[-1] - width * math.sin(perp_angle)
        points.extend([p1x, p1y, p2x, p2y])

        if len(points) >= 8:
            draw.polygon(points, fill=color)

def create_structural_frame(draw, x, y, width, height, color, thickness=7):
    """Create precise architectural frames with detail"""
    # Outer frame with precise corners
    draw.rectangle([x, y, x + width, y + height], outline=color, width=thickness)

    # Inner detail lines with consistent spacing
    offset = 18
    draw.rectangle([x + offset, y + offset, x + width - offset, y + height - offset],
                  outline=tuple(max(0, c - 35) for c in color), width=2)

    # Corner accents
    corner_size = 25
    # Top-left
    draw.rectangle([x, y, x + corner_size, y + thickness], fill=color)
    draw.rectangle([x, y, x + thickness, y + corner_size], fill=color)
    # Bottom-right
    draw.rectangle([x + width - corner_size, y + height - thickness, x + width, y + height], fill=color)
    draw.rectangle([x + width - thickness, y + height - corner_size, x + width, y + height], fill=color)

def create_particle_field(draw, density=280):
    """Create subtle atmospheric particle field with clustering"""
    # Create cluster centers
    clusters = []
    for _ in range(12):
        clusters.append((random.randint(200, WIDTH - 200), random.randint(200, HEIGHT - 200)))

    for _ in range(density):
        # Choose cluster or random position
        if random.random() > 0.65:
            cx, cy = random.choice(clusters)
            x = cx + random.randint(-80, 80)
            y = cy + random.randint(-80, 80)
        else:
            x = random.randint(50, WIDTH - 50)
            y = random.randint(50, HEIGHT - 50)

        x = max(20, min(WIDTH - 20, x))
        y = max(20, min(HEIGHT - 20, y))
        size = random.uniform(0.8, 2.2)

        # Color distribution
        color_rand = random.random()
        if color_rand > 0.65:
            color = CLOUD_WHITE
        elif color_rand > 0.35:
            color = GOLD_LIGHT
        else:
            color = IMPERIAL_GOLD

        draw.ellipse([x, y, x + size, y + size], fill=color)

def create_vertical_flow(draw, start_x, start_y, end_y, width_base, color_start, color_end):
    """Create upward flowing energy columns with smoother transitions"""
    steps = 45
    for i in range(steps):
        t = i / steps
        y = start_y + (end_y - start_y) * t
        width = width_base * (1 - t * 0.65)

        # Taper and fade with better curve
        color = interpolate_color(color_start, color_end, t * 0.8)
        sway = math.sin(t * 12) * 18 * (1 - t * 0.5) + math.cos(t * 8) * 8
        x = start_x + sway

        draw.ellipse([x - width/2, y - width/3.5, x + width/2, y + width/3.5], fill=color)

def create_energy_glow(draw, center_x, center_y, radius, color, layers=4):
    """Create soft glowing energy points"""
    for i in range(layers):
        r = radius * (1 - i * 0.2)
        alpha_factor = 1 - (i * 0.25)
        glow_color = interpolate_color(color, BG_COLOR, i * 0.15)
        draw.ellipse([center_x - r, center_y - r, center_x + r, center_y + r], fill=glow_color)

def main():
    random.seed(42)

    # Create main image
    img = Image.new('RGB', (WIDTH, HEIGHT), BG_COLOR)
    draw = ImageDraw.Draw(img)

    # ========== BACKGROUND LAYERS ==========

    # Layer 1: Deep atmospheric gradient - more subtle
    for y in range(0, HEIGHT, 35):
        brightness = int(255 * (1 - y / HEIGHT) * 0.08)
        color = tuple(max(0, c + brightness) for c in BG_COLOR)
        draw.rectangle([0, y, WIDTH, y + 35], fill=color)

    # Layer 2: Celestial structures - rigid order (refined positions)
    structures = [
        (165, 145, 290, 570),
        (1555, 245, 250, 490),
        (75, 1145, 190, 395),
        (1730, 945, 205, 435),
        (290, 1795, 230, 365),
        (1465, 1745, 250, 405)
    ]

    for sx, sy, sw, sh in structures:
        create_structural_frame(draw, sx, sy, sw, sh,
                               tuple(max(0, c - 48) for c in CELESTIAL_AZURE), thickness=7)

    # Layer 3: Background cloud formations - adjusted positions
    bg_clouds = [
        (420, 590, 145, 0.45),
        (1580, 790, 165, 1.85),
        (290, 1410, 125, 2.35),
        (1680, 1610, 155, 0.75),
        (920, 290, 185, 1.55)
    ]

    for cx, cy, cr, rot in bg_clouds:
        create_refined_cloud(draw, cx, cy, cr,
                            tuple(min(255, c + 18) for c in BG_COLOR), rot, layers=4)

    # ========== MIDDLE LAYERS ==========

    # Layer 4: Vertical energy streams (upward momentum - refined)
    streams = [
        (520, 2720, 580, 105, ENERGY_ORANGE, VOLCANIC),
        (850, 2770, 480, 95, IMPERIAL_GOLD, ENERGY_ORANGE),
        (1180, 2740, 530, 90, VOLCANIC, CRIMSON),
        (1510, 2700, 105, 100, ENERGY_ORANGE, IMPERIAL_GOLD)
    ]

    for sx, sy, ey, sw, cs, ce in streams:
        create_vertical_flow(draw, sx, sy, ey, sw, cs, ce)

    # Layer 5: Central energy burst (the core uprising)
    center_x, center_y = WIDTH // 2, HEIGHT // 2 - 30

    # Multiple radiating waves with refined angles
    wave_colors = [CRIMSON, VOLCANIC, IMPERIAL_GOLD, ENERGY_ORANGE, GOLD_LIGHT]
    for angle_base in [0.05, 0.45, 0.85, 1.25, 1.65, 2.05, 2.45, 2.85]:
        create_energy_wave(draw, center_x, center_y, 560, angle_base, wave_colors)

    # Layer 6: Foreground cloud forms (chaos and energy - refined)
    fg_clouds = [
        (center_x + 20, center_y - 370, 225, 0.18, CRIMSON),
        (center_x - 290, center_y + 30, 175, 1.05, VOLCANIC),
        (center_x + 310, center_y - 70, 195, 2.05, IMPERIAL_GOLD),
        (center_x - 190, center_y - 470, 145, 2.85, ENERGY_ORANGE),
        (center_x + 230, center_y + 290, 165, 0.58, CRIMSON)
    ]

    for cx, cy, cr, rot, color in fg_clouds:
        create_refined_cloud(draw, cx, cy, cr, color, rot, layers=6)

    # Layer 7: Energy concentration points with glow
    focal_points = [
        (center_x - 195, center_y - 145, 42, GOLD_LIGHT),
        (center_x + 185, center_y - 95, 38, IMPERIAL_GOLD),
        (center_x + 10, center_y + 195, 47, ENERGY_ORANGE),
        (center_x - 145, center_y + 255, 32, VOLCANIC),
        (center_x + 225, center_y + 175, 40, CRIMSON)
    ]

    for fx, fy, fr, fc in focal_points:
        create_energy_glow(draw, fx, fy, fr, fc, layers=4)

    # ========== DETAIL LAYERS ==========

    # Layer 8: Subtle particle field
    create_particle_field(draw, density=320)

    # Layer 9: Geometric accent lines (subtle structure)
    for i in range(5):
        y = 440 + i * 440
        draw.line([140, y, WIDTH - 140, y], fill=IMPERIAL_GOLD, width=1)

    # ========== TYPOGRAPHY ==========

    font_path = 'skills/canvas-design/canvas-fonts/EricaOne-Regular.ttf'
    if os.path.exists(font_path):
        try:
            # Main character - monumental
            font_large = ImageFont.truetype(font_path, 260)
            text = "闹"
            bbox = draw.textbbox((0, 0), text, font=font_large)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]
            text_x = (WIDTH - text_width) // 2
            text_y = HEIGHT - 650

            # Multi-layer shadow for depth
            for offset in [10, 6, 3, 1]:
                shadow_factor = offset * 28
                shadow_color = tuple(max(0, BG_COLOR[i] - shadow_factor + 40) for i in range(3))
                draw.text((text_x + offset, text_y + offset), text,
                         font=font_large, fill=shadow_color)

            # Main text with subtle gradient effect
            draw.text((text_x - 1, text_y - 1), text, font=font_large, fill=(215, 145, 22))
            draw.text((text_x, text_y), text, font=font_large, fill=IMPERIAL_GOLD)
            draw.text((text_x + 1, text_y), text, font=font_large, fill=(255, 192, 60))

            # Top subtitle - anchoring
            font_medium = ImageFont.truetype(font_path, 90)
            subtitle = "大闹"
            bbox_sub = draw.textbbox((0, 0), subtitle, font=font_medium)
            sub_width = bbox_sub[2] - bbox_sub[0]
            sub_x = (WIDTH - sub_width) // 2
            sub_y = text_y - 200

            # Subtitle shadow
            draw.text((sub_x + 3, sub_y + 3), subtitle, font=font_medium, fill=(0, 0, 0))
            # Subtitle main
            draw.text((sub_x, sub_y), subtitle, font=font_medium, fill=CLOUD_WHITE)

            # Small accent text
            font_small = ImageFont.truetype(font_path, 50)
            accent = "天宫"
            bbox_acc = draw.textbbox((0, 0), accent, font=font_small)
            acc_width = bbox_acc[2] - bbox_acc[0]
            acc_x = (WIDTH - acc_width) // 2
            acc_y = text_y + 220

            draw.text((acc_x, acc_y), accent, font=font_small, fill=GOLD_LIGHT)

        except Exception as e:
            print(f"Font rendering: {e}")

    # Apply very subtle gaussian blur for cohesion
    img = img.filter(ImageFilter.GaussianBlur(radius=0.25))

    # Save final masterpiece
    output_path = 'celestial_uproar.png'
    img.save(output_path, 'PNG', optimize=True, quality=100)
    print(f"Masterpiece saved to: {output_path}")

if __name__ == '__main__':
    main()
