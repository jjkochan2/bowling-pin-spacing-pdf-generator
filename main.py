from reportlab.graphics.shapes import Drawing, String, Circle, Rect
from reportlab.graphics import renderPDF
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
import math

def save_drawing(drawing):
    x1, y1, x2, y2 = drawing.getBounds()
    print(f'bounds: {drawing.getBounds()}')
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

def draw_pin_mark(drawing, x, y, pin_number, scale):
    number_of_circles = 3
    r = FULLSCALE_PIN_BOTTOM_WIDTH / 2 * scale
    r_max = FULLSCALE_PIN_MAX_WIDTH / 2 * scale
    for i in range(number_of_circles):
        print(f"r: {r}")
        drawing.add(Circle(x, y, r, strokeWidth=1, fillColor=None))
        if i == number_of_circles - 1:
            text = str(pin_number)
            drawing.add(String(x, y - 1.5 * r, text, textAnchor='middle'))
        r += (r_max - r) / (number_of_circles - 1) * (i + 1)

def draw_pin_layout(drawing, x, y, scale):
    x *= scale
    y *= scale
    spacing_inches = FULLSCALE_PIN_SPACING * scale
    row_height = spacing_inches * (math.sqrt(3) / 2)
    pin_count = 1
    for row in range(4):
        # Current row's vertical position
        current_y = y + row * row_height
        
        pins_in_row = row + 1
        
        # Calculate the horizontal offset to keep the row centered
        row_width = (pins_in_row - 1) * spacing_inches
        left_edge = -(row_width / 2)
        
        for p in range(pins_in_row):
            current_x = x + left_edge + (p * spacing_inches)
            
            # Draw a mark for the pin
            draw_pin_mark(drawing, current_x, current_y, pin_count, scale)

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

def draw_lane_outline(drawing, x, y, scale):
    drawing.add(Rect(x, y, FULLSCALE_LANE_WIDTH * scale, FULLSCALE_LANE_HEIGHT * scale, strokeWidth=1, fillColor=None))

def generate_bowling_template(scale):
    d = Drawing()

    draw_pin_layout(d, FULLSCALE_LANE_WIDTH / 2, FULLSCALE_LANE_HEIGHT, scale)

    draw_lane_outline(d, 0, 0, scale)
    
    save_drawing(d)


FULLSCALE_PIN_SPACING = 12 * inch
FULLSCALE_PIN_MAX_WIDTH = 4.766 * inch
FULLSCALE_PIN_BOTTOM_WIDTH = 2.031 * inch
FULLSCALE_LANE_WIDTH = 41.5 * inch
FULLSCALE_LANE_HEIGHT = 60 * 12 * inch
MINI_PIN_MAX_WIDTH = 0.519 * inch
SCALE = MINI_PIN_MAX_WIDTH / FULLSCALE_PIN_MAX_WIDTH

if __name__ == "__main__":
    generate_bowling_template(SCALE)