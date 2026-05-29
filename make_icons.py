"""Generate PWA icons for SpeakUp English Tutor app (pure Python, no deps)."""
import struct, zlib, os, math

NAVY  = (13, 27, 42)
GOLD  = (240, 180, 41)
WHITE = (232, 234, 240)

def png_chunk(tag, data):
    c = zlib.crc32(tag + data) & 0xffffffff
    return struct.pack('>I', len(data)) + tag + data + struct.pack('>I', c)

def write_png(path, pixels, size):
    """pixels: list of (r,g,b) tuples, row-major, size x size."""
    raw = b''
    for row in range(size):
        raw += b'\x00'  # filter type None
        for col in range(size):
            r, g, b = pixels[row * size + col]
            raw += bytes([r, g, b])
    compressed = zlib.compress(raw, 9)
    with open(path, 'wb') as f:
        f.write(b'\x89PNG\r\n\x1a\n')
        f.write(png_chunk(b'IHDR', struct.pack('>IIBBBBB', size, size, 8, 2, 0, 0, 0)))
        f.write(png_chunk(b'IDAT', compressed))
        f.write(png_chunk(b'IEND', b''))

def lerp_color(c1, c2, t):
    return tuple(int(c1[i] + (c2[i] - c1[i]) * t) for i in range(3))

def draw_icon(size):
    px = [NAVY] * (size * size)
    cx = size / 2
    cy = size / 2

    # --- Rounded rectangle background (navy-mid) ---
    bg = (26, 46, 68)
    radius = size * 0.18
    margin = size * 0.05
    for y in range(size):
        for x in range(size):
            # rounded rect check
            lx = max(margin + radius - x, x - (size - margin - radius), 0)
            ly = max(margin + radius - y, y - (size - margin - radius), 0)
            if math.sqrt(lx*lx + ly*ly) <= radius + 0.5:
                px[y * size + x] = bg

    # --- Gold circle accent (top-right) ---
    ar = size * 0.09
    ax, ay = size * 0.72, size * 0.27
    for y in range(size):
        for x in range(size):
            if math.sqrt((x-ax)**2 + (y-ay)**2) < ar:
                px[y * size + x] = GOLD

    # --- Draw "E" letter in gold, centered ---
    # We'll draw thick strokes manually
    lw = max(2, size // 22)   # line width
    # Letter bounding box
    lx0 = int(size * 0.28)
    lx1 = int(size * 0.65)
    ly0 = int(size * 0.25)
    ly1 = int(size * 0.75)
    mid_y = (ly0 + ly1) // 2

    def fill_rect(x0, y0, x1, y1, color):
        for y in range(max(0,y0), min(size,y1)):
            for x in range(max(0,x0), min(size,x1)):
                px[y * size + x] = color

    # Vertical stroke of E
    fill_rect(lx0, ly0, lx0 + lw, ly1, GOLD)
    # Top horizontal
    fill_rect(lx0, ly0, lx1, ly0 + lw, GOLD)
    # Middle horizontal (slightly shorter)
    fill_rect(lx0, mid_y - lw//2, lx1 - size//14, mid_y + lw//2 + 1, GOLD)
    # Bottom horizontal
    fill_rect(lx0, ly1 - lw, lx1, ly1, GOLD)

    # --- Small dot accent under "E" ---
    dot_r = max(2, size // 28)
    dot_x = int(size * 0.72)
    dot_y = int(size * 0.70)
    for y in range(size):
        for x in range(size):
            if math.sqrt((x-dot_x)**2 + (y-dot_y)**2) < dot_r:
                px[y * size + x] = GOLD

    return px

os.makedirs('icons', exist_ok=True)

for sz in [192, 512]:
    pixels = draw_icon(sz)
    write_png(f'icons/icon-{sz}.png', pixels, sz)
    print(f'icons/icon-{sz}.png written ({sz}x{sz})')

# Apple touch icon: 180x180
pixels = draw_icon(180)
write_png('icons/apple-touch-icon.png', pixels, 180)
print('icons/apple-touch-icon.png written (180x180)')

# Favicon: 32x32
pixels = draw_icon(32)
write_png('icons/favicon-32.png', pixels, 32)
print('icons/favicon-32.png written (32x32)')

print('Done!')
