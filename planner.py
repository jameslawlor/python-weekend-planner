from fpdf import FPDF

class WeekPlannerPDF(FPDF):
    def header(self):
        # self.set_font('Arial', 'B', 10)
        # self.set_text_color(40, 40, 40)
        # self.cell(0, 0, 'Week Planner', 0, 1, 'C')
        # self.ln(5)
        pass

    def section_title(self, title):
        self.set_font('Arial', 'B', 9)
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

    def draw_schedule(self, days, hours):
        self.set_font('Arial', 'B', 10)
        self.set_text_color(70, 130, 180)
        # self.cell(0, 10, f"{title1} and {title2} Schedule", 0, 1, 'C')
        self.ln(1)

        self.set_font('Arial', '', 10)
        total_columns = len(hours)
        col_width_adjustment = -7
        column_width = (self.w + col_width_adjustment) / (total_columns + 0.5)
        row_height = 19

        index_col_width_multiplier = 0.3
        column_title_col_width_multiplier = 0.3

        # Empty top-left corner
        self.cell(column_width*index_col_width_multiplier, row_height*column_title_col_width_multiplier, '', 0, 0, 'C')  

        for hour in hours:
            self.cell(column_width, row_height*column_title_col_width_multiplier, hour, 1, 0, 'C')
        self.ln()

        # Print the hourly slots for both schedules
        for day in days:
            self.set_draw_color(0)  # Reset to default (black)
            self.cell(column_width*index_col_width_multiplier, row_height, day, 1, 0, 'C')  # Print the day
            
            for _ in hours:
                self.set_draw_color(200, 200, 200)  # Light gray color
                self.cell(column_width, row_height, '', border='LR', align='C')  # Draw only left and right borders

                
            self.set_draw_color(0)  # Reset to default (black)    

            # Move to the beginning and draw the bottom border
            self.cell(
                -column_width * len(hours), 
                row_height, 
                '', 
                border='B', 
                align='C')  

            self.ln()

    def draw_empty_box(self, title, row_size, width, ):

        self.set_font('Arial', '', 10)

        x_position = self.get_x()        
        # Move to the starting x position of the box
        # self.set_x()
        y_position = self.get_y()        
        x_adj = 145
        y_adj = -30
        self.set_xy(x_position+x_adj, y_position+y_adj)
        self.section_title(title)
        self.set_xy(x_position+x_adj, y_position+y_adj)
        
        box_height = row_size * 10  # Height based on row size (each row is 10 units tall)
        
        # Draw the empty box with a border at the correct position
        self.cell(width, box_height, '', border=1, ln=1, align='R')
        # self.ln(5)


if __name__ == "__main__":
    pdf = WeekPlannerPDF()

    pdf.set_margins(left=5, top=8, right=5,)
    pdf.add_page(orientation='L')

    # Set the width for each section to be half of the page
    half_width = (pdf.w) / 2
    
    # Add Goals list on the left side
    pdf.add_section_with_list("Goals", 3, half_width - 20)
    # print(half_width)
    # Add TODO box on the right side
    pdf.draw_empty_box("TODO", 3, half_width-20, )

    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    days = ["M", "Tu", "W", "Th", "F", "Sa", "Su"]
    hours = [f"{h}:00" for h in range(8, 21)]

    pdf.draw_schedule(days, hours)
    
    output_path = "planner.pdf"
    print(f"Writing to {output_path}")
    pdf.output("planner.pdf")