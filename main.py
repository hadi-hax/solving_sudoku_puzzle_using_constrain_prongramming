from kivymd.app import MDApp
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.textfield import MDTextField
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDRectangleFlatButton
# pip install kivymd

from constraint import Problem , AllDifferentConstraint
# pip install python_constraint
class SudokuBoard(MDGridLayout):
    def __init__(self, **kwargs):
        super(SudokuBoard, self).__init__(**kwargs)
        self.cols = 9
        self.rows = 10  # Update rows to accommodate the additional button and label

        self.cells = []
        self.padding = 25
        self.spacing=25

        self.grid = [
            0, 0, 0, 0, 0, 0, 0, 0, 0,
            9, 0, 0, 3, 0, 2, 6, 7, 8,
            0, 0, 0, 0, 9, 0, 0, 0, 5,
            7, 4, 6, 2, 1, 0, 0, 0, 0,
            5, 0, 0, 0, 3, 0, 0, 0, 0,
            0, 0, 3, 6, 0, 0, 0, 9, 0,
            0, 0, 7, 0, 2, 0, 0, 0, 0,
            3, 0, 0, 8, 0, 1, 0, 6, 0,
            0, 6, 5, 0, 0, 0, 8, 0, 9
        ]

        i = 0
        for row in range(9):
            for col in range(9):
                cell = MDTextField(multiline=False,font_size=18,mode="round", input_filter="int",text=f"{self.grid[i]}")
                self.cells.append(cell)
                self.add_widget(cell)
                i += 1

        self.add_widget(MDLabel())  # Adding an empty label for spacing

        solve_button = MDRectangleFlatButton(
            text='Solve',
            size_hint=(1, 0.1),
            on_release=self.solve_sudoku
        )
        self.add_widget(solve_button)
        
    def solve_sudoku(self, instance):
        # Get the values from the input cells
        gred_slution = self.solve(self.grid)

        self.clear_widgets()
        self.cols = 9
        self.rows = 10  # Update rows to accommodate the additional button and label
        self.cells = []
        i = 0
        for row in range(9):
            for col in range(9):
                cell = MDTextField(multiline=False,font_size=18,mode="round", input_filter="int",text=f"{gred_slution[i]}")
                self.cells.append(cell)
                self.add_widget(cell)
                i += 1

        self.add_widget(MDLabel())  # Adding an empty label for spacing

        solve_button = MDRectangleFlatButton(
            text='Solve',
            size_hint=(1, 0.1),
            on_release=self.solve_sudoku
        )
        self.add_widget(solve_button)

    def add_row_constraints(self,problem):
        for row in range(9):
            problem.addConstraint(AllDifferentConstraint(), range(row*9, (row+1)*9))

    def add_column_constraints(self,problem):
        for col in range(9):
            problem.addConstraint(AllDifferentConstraint(), range(col, 81, 9))

    def add_box_constraints(self,problem):
        for row_offset in range(0, 9, 3):
            for col_offset in range(0, 9, 3):
                cells = []
                for row in range(3):
                    for col in range(3):
                        cells.append((row_offset + row) * 9 + col_offset + col)
                problem.addConstraint(AllDifferentConstraint(), cells)

    def solve(self,board):
        problem = Problem()
        
        for i, value in enumerate(board):
            if value == 0:
                problem.addVariable(i, range(1, 10))
            else:
                problem.addVariable(i, [value])
        
        self.add_row_constraints(problem)
        self.add_column_constraints(problem)
        self.add_box_constraints(problem)
        
        solution = problem.getSolution()
        if solution is None:
            return None
        
        solved_grid = [0] * 81
        for cell, value in solution.items():
            solved_grid[cell] = value
        
        return solved_grid


class SudokuApp(MDApp):
    def build(self):
        return SudokuBoard()


if __name__ == '__main__':
    SudokuApp().run()
