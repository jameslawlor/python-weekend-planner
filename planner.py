from fpdf import FPDF

class WeekendPlannerPDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 14)
        self.set_text_color(40, 40, 40)
        self.cell(0, 10, 'Weekend Planner', 0, 1, 'C')
        # self.ln(5)

    def section_title(self, title):
        self.set_font('Arial', 'B', 12)
        self.set_text_color(70, 130, 180)
        self.cell(0, 10, title, 0, 1, 'L')
        # self.ln(2) 

    def numbered_list(self, num_items, width):
        self.set_font('Arial', '', 10)
        self.set_text_color(0, 0, 0)
        for i in range(1, num_items + 1):
            self.cell(10, 10, f"{i}.", 0, 0, 'R')
            self.cell(width - 10, 10, '', 1, 1, 'R')
        # self.ln(5)

    def add_section_with_list(self, title, num_items, width):
        self.section_title(title)
        self.numbered_list(num_items, width)

    def draw_double_schedule(self, title1, title2, days):
        self.set_font('Arial', 'B', 12)
        self.set_text_color(70, 130, 180)
        # self.cell(0, 10, f"{title1} and {title2} Schedule", 0, 1, 'C')
        self.ln(2)

        self.set_font('Arial', '', 10)
        total_columns = len(days) * 2
        col_width_adjustment = -20
        column_width = (self.w + col_width_adjustment) / (total_columns + 0.5)
        row_height = 11
        hours = [f"{h}:00" for h in range(7, 22)]

        # Print the headers: each day has two sub-headers (one for each person)
        self.cell(column_width / 2, row_height, '', 1, 0, 'C')  # Empty top-left corner
        for day in days:
            self.cell(column_width * 2, row_height, day, 1, 0, 'C')
        self.ln()

    
        # Print sub-headers
        self.cell(column_width / 2, row_height, '', 1, 0, 'C')  # Empty top-left corner
        for _ in days:
            self.cell(column_width, row_height, title1, 1, 0, 'C')
            self.cell(column_width, row_height, title2, 1, 0, 'C')
        self.ln()

        # Print the hourly slots for both schedules
        for hour in hours:
            self.cell(column_width / 2, row_height, hour, 1, 0, 'C')  # Print the hour
            self.set_draw_color(200, 200, 200)  # Light gray color
            for _ in days:
                self.cell(column_width, row_height, '', 1, 0)
                self.cell(column_width, row_height, '', 1, 0)
            self.set_draw_color(0)  # Reset to default (black)
            self.ln()
        # self.ln(5)

    def draw_empty_box(self, title, row_size, width, ):

        self.set_font('Arial', '', 10)

        x_position = self.get_x()        
        # Move to the starting x position of the box
        # self.set_x()
        y_position = self.get_y()        
        self.set_xy(x_position+100, y_position-50)
        self.section_title(title)
        self.set_xy(x_position+100, y_position-40)
        
        box_height = row_size * 10  # Height based on row size (each row is 10 units tall)
        
        # Draw the empty box with a border at the correct position
        self.cell(width, box_height, '', border=1, ln=1, align='R')
        self.ln(5)


if __name__ == "__main__":
    pdf = WeekendPlannerPDF()

    pdf.add_page()

    # Set the width for each section to be half of the page
    half_width = (pdf.w) / 2
    
    # Add Goals list on the left side
    pdf.add_section_with_list("Goals", 4, half_width - 10)
    # print(half_width)
    # Add TODO box on the right side
    pdf.draw_empty_box("TODO", 4, half_width-10, )

    days = ["Friday", "Saturday", "Sunday"]
    pdf.draw_double_schedule("Marski", "Me", days)
    
    output_path = "planner.pdf"
    print(f"Writing to {output_path}")
    pdf.output("planner.pdf")