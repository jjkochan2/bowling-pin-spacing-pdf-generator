from reportlab.graphics.shapes import Drawing, Circle
from reportlab.graphics import renderPDF
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
import math

def draw_pin_mark(canvas, x, y, pin_number):
    canvas.setStrokeColorRGB(0, 0, 0)
    number_of_circles = 3
    for i in range(number_of_circles):
        r = round((i + 1) / 10 * inch, 2)
        canvas.circle(x, y, r)
        if i == number_of_circles - 1:
            text = str(pin_number)
            text_width = canvas.stringWidth(text, canvas._fontname, canvas._fontsize)
            canvas.drawString(x - (text_width / 2), y - 1.5 * r, text)

def generate_bowling_template(spacing_inches):
    d = Drawing()
    d.add(Circle(0 * inch, 0 * inch, 1 * inch))
    d.add(Circle(2 * inch, 2 * inch, 1 * inch))
    x1, y1, x2, y2 = d.getBounds()
    d.width = x2 - x1
    d.height = y2 - y1
    d.renderScale = 1 
    d.transform = (1, 0, 0, 1, -x1, -y1)
    renderPDF.drawToFile(d, "drawing.pdf")
    filename = f"bowling_template_{round(spacing_inches, 3)}in_spacing.pdf"
    pagesize = letter
    c = canvas.Canvas(filename, pagesize=pagesize)
    width, height = pagesize
    
    row_height = spacing_inches * (math.sqrt(3) / 2)

    start_x = width / 2
    total_tri_height = 3 * row_height * inch
    start_y = (height / 2) + (total_tri_height / 2)
    
    c.setFont("Helvetica", 10)
    # c.drawString(0.5 * inch, 10.5 * inch, f"Bowling Pin Template - Spacing: {round(spacing_inches, 3)}\"")
    
    pin_count = 1
    
    # Generate 4 rows (1, 2, 3, 4 pins per row)
    for row in range(4):
        # Current row's vertical position
        current_y = start_y - (row * row_height * inch)
        
        pins_in_row = row + 1
        
        # Calculate the horizontal offset to keep the row centered
        row_width = (pins_in_row - 1) * spacing_inches * inch
        left_edge = start_x - (row_width / 2)
        
        for p in reversed(range(pins_in_row)):
            current_x = left_edge + (p * spacing_inches * inch)
            
            # Draw a mark for the pin (a circle and a crosshair)
            draw_pin_mark(c, current_x, current_y, pin_count)


            # c.line(current_x - 10, current_y, current_x + 10, current_y)
            # c.line(current_x, current_y - 10, current_x, current_y + 10)
            
            # Label the pin number
            pin_count += 1

    c.showPage()
    c.save()
    print(f"Success! '{filename}' has been created.")

FULLSCALE_PIN_SPACING = 12 # [in]
FULLSCALE_PIN_WIDTH = 4.766 # [in]
MINI_PIN_WIDTH = 0.519 # [in]

MINI_SPACING_INCHES = FULLSCALE_PIN_SPACING / FULLSCALE_PIN_WIDTH * MINI_PIN_WIDTH

if __name__ == "__main__":
    generate_bowling_template(MINI_SPACING_INCHES)