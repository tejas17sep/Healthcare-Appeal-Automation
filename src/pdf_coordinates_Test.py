import fitz


pdf = "templates/BCBS.pdf"

doc = fitz.open(pdf)

page = doc[0]


# Create drawing object
shape = page.new_shape()


# Page size
width = page.rect.width
height = page.rect.height


# Grid size (small boxes)
grid = 10


# Draw vertical lines

for x in range(0, int(width), grid):

    shape.draw_line(
        fitz.Point(x, 0),
        fitz.Point(x, height)
    )


# Draw horizontal lines

for y in range(0, int(height), grid):

    shape.draw_line(
        fitz.Point(0, y),
        fitz.Point(width, y)
    )


# Commit lines

shape.finish(
    color=(1, 0, 0),
    width=0.3
)

shape.commit()


# Add coordinates every 50 points

for x in range(0, int(width), 50):

    page.insert_text(
        fitz.Point(x + 2, 15),
        str(x),
        fontsize=8
    )


for y in range(0, int(height), 50):

    page.insert_text(
        fitz.Point(5, y + 12),
        str(y),
        fontsize=8
    )


# Save final PDF

doc.save(
    "BCBS_grid.pdf"
)


# Create preview image

pix = page.get_pixmap(
    dpi=150
)

pix.save(
    "BCBS_grid.png"
)


print("Grid created successfully")