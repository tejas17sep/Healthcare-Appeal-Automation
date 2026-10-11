import fitz

PDF_FILE = "templates/BCBS.pdf"
OUTPUT_IMAGE = "BCBS_grid.png"

# Open PDF
doc = fitz.open(PDF_FILE)
page = doc[0]

width = int(page.rect.width)
height = int(page.rect.height)

# Create shape for grid lines
shape = page.new_shape()

GRID_SIZE = 25

# Vertical grid lines
for x in range(0, width + 1, GRID_SIZE):
    shape.draw_line(
        fitz.Point(x, 0),
        fitz.Point(x, height)
    )

# Horizontal grid lines
for y in range(0, height + 1, GRID_SIZE):
    shape.draw_line(
        fitz.Point(0, y),
        fitz.Point(width, y)
    )

# Commit grid lines
shape.finish(width=0.3)
shape.commit()

# Add X-axis labels
for x in range(0, width + 1, GRID_SIZE):
    page.insert_text(
        (x + 2, 10),
        str(x),
        fontsize=6
    )

# Add Y-axis labels
for y in range(0, height + 1, GRID_SIZE):
    page.insert_text(
        (2, y + 10),
        str(y),
        fontsize=6
    )

# Create high-resolution image
pix = page.get_pixmap(matrix=fitz.Matrix(3, 3), alpha=False)

# Save image
pix.save(OUTPUT_IMAGE)

print(f"Grid created successfully: {OUTPUT_IMAGE}")
print(f"Page Size: Width={width}, Height={height}")