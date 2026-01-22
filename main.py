from reportlab.graphics.shapes import Drawing, String, Circle
from reportlab.graphics import renderPDF
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
import math

def save_drawing(drawing):
    x1, y1, x2, y2 = drawing.getBounds()
    drawing.width = x2 - x1
    drawing.height = y2 - y1
    drawing.renderScale = 1 
    drawing.transform = (1, 0, 0, 1, -x1, -y1)
    renderPDF.drawToFile(drawing, "drawing.pdf")

# remove after fully transitioned to Drawing
def draw_pin_mark_canvas(canvas, x, y, pin_number):
    canvas.setStrokeColorRGB(0, 0, 0)
    number_of_circles = 3
    for i in range(number_of_circles):
        r = round((i + 1) / 10 * inch, 2)
        canvas.circle(x, y, r)
        if i == number_of_circles - 1:
            text = str(pin_number)
            text_width = canvas.stringWidth(text, canvas._fontname, canvas._fontsize)
            canvas.drawString(x - (text_width / 2), y - 1.5 * r, text)

def draw_pin_mark(drawing, x, y, pin_number):
    number_of_circles = 3
    for i in range(number_of_circles):
        r = round((i + 1) / 10 * inch, 2)
        drawing.add(Circle(x, y, r, strokeWidth=1, fillColor=None))
        if i == number_of_circles - 1:
            text = str(pin_number)
            drawing.add(String(x, y - 1.5 * r, text, textAnchor='middle'))

def draw_pin_layout(drawing, x, y, spacing_inches):
    row_height = spacing_inches * (math.sqrt(3) / 2)
    pin_count = 1
    for row in range(4):
        # Current row's vertical position
        current_y = y + row * row_height * inch
        
        pins_in_row = row + 1
        
        # Calculate the horizontal offset to keep the row centered
        row_width = (pins_in_row - 1) * spacing_inches * inch
        left_edge = -(row_width / 2)
        
        for p in range(pins_in_row):
            current_x = x + left_edge + (p * spacing_inches * inch)
            
            # Draw a mark for the pin
            draw_pin_mark(drawing, current_x, current_y, pin_count)

            pin_count += 1

# remove after fully transitioned to Drawing
def generate_bowling_template_canvas(spacing_inches):
    filename = f"bowling_template_{round(spacing_inches, 3)}in_spacing.pdf"
    pagesize = letter
    c = canvas.Canvas(filename, pagesize=pagesize)
    c.setFont("Helvetica", 10)
    c.showPage()
    c.save()
    print(f"Success! '{filename}' has been created.")


def generate_bowling_template(spacing_inches):
    d = Drawing()
    
    draw_pin_layout(d, 0, 0, spacing_inches)

    save_drawing(d)


FULLSCALE_PIN_SPACING = 12 # [in]
FULLSCALE_PIN_WIDTH = 4.766 # [in]
MINI_PIN_WIDTH = 0.519 # [in]

MINI_SPACING_INCHES = FULLSCALE_PIN_SPACING / FULLSCALE_PIN_WIDTH * MINI_PIN_WIDTH

if __name__ == "__main__":
    generate_bowling_template(MINI_SPACING_INCHES)