"""
Label printing via Brother QL-810W P-touch Editor Lite
"""

from PIL import Image, ImageDraw, ImageFont
import qrcode
from brother_ql.raster import BrotherQLRaster
from brother_ql.conversion import convert

# Fix Pillow compatibility
if not hasattr(Image, 'ANTIALIAS'):
    Image.ANTIALIAS = Image.Resampling.LANCZOS

# Constants
PTLITE_PRN_PATH = r"D:\PTLITE.PRN"
TOTAL_FILE_SIZE = 112640
HEADER_PADDING = 200
LABEL_WIDTH = 696  # 62mm at 300dpi


def print_label(url: str, issue_number: str, title: str, description: str = "") -> str:
    """
    Generate and print a label with QR code and text.
    
    Args:
        url: URL to encode in QR code
        issue_number: Issue/PR number (e.g., '#1234')
        title: Issue/PR title
        description: Optional brief description
    
    Returns:
        Success message or error
    """
    # Generate QR code
    qr = qrcode.QRCode(version=1, box_size=8, border=1)
    qr.add_data(url)
    qr.make(fit=True)
    qr_img = qr.make_image(fill_color='black', back_color='white').convert('RGB')
    qr_size = qr_img.size[0]
    
    # Create label image
    label_height = max(qr_size + 10, 150)
    label = Image.new('RGB', (LABEL_WIDTH, label_height), 'white')
    draw = ImageDraw.Draw(label)
    
    # Paste QR on left
    label.paste(qr_img, (5, 5))
    
    # Load fonts
    try:
        font_big = ImageFont.truetype('arial.ttf', 28)
        font_small = ImageFont.truetype('arial.ttf', 20)
    except OSError:
        font_big = ImageFont.load_default()
        font_small = font_big
    
    # Add text on right
    text_x = qr_size + 20
    draw.text((text_x, 10), issue_number, fill='black', font=font_big)
    draw.text((text_x, 45), title[:30], fill='black', font=font_small)  # Truncate long titles
    if description:
        draw.text((text_x, 72), description[:35], fill='black', font=font_small)
    
    # Save temp image
    temp_path = "temp_label.png"
    label.save(temp_path)
    
    # Convert to Brother QL raster format
    qlr = BrotherQLRaster('QL-810W')
    raster = convert(
        qlr=qlr,
        images=[temp_path],
        label='62',
        rotate='0',
        threshold=70,
        cut=True
    )
    
    # Create padded output (112640 bytes with 200-byte header)
    output = bytearray(TOTAL_FILE_SIZE)
    output[HEADER_PADDING:HEADER_PADDING + len(raster)] = raster
    
    # Write to PTLITE.PRN
    with open(PTLITE_PRN_PATH, 'wb') as f:
        f.write(output)
    
    return f"Label printed: {issue_number} - {title}"

