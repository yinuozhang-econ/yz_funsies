from pathlib import Path
import numpy as np

class optimizer:        
    def prep_input(self,matrix):
        translated_matrix = [self.translator(row) for row in matrix]
        return translated_matrix
    def input_initialization(self,):
        with open(self.input_path, 'r', encoding="utf-8") as f:
            for line in f: 
                row = line.strip()
                self.input_matrix.append(row)
            self.input_numeric_matrix = self.prep_input(self.input_matrix)
        return self.input_numeric_matrix        
    def translator(self, line):
        table = str.maketrans({'.': '0', '@': '1'})  # Create table
        translated_row = line.translate(table) 
        return [int(char) for char in translated_row]
    def put_together(self,matrix,row):
        matrix.append(row)
        return matrix
    def translator_to_graph(self, row, threshold):
        return ''.join({-1: '.'}.get(val, '@' if val >= threshold else 'x') for val in row)
    def translator_output_to_input(self, matrix):
        table = str.maketrans({'x': '.'}) 
        translated_matrix = [row.translate(table) for row in matrix]
        return translated_matrix
    def __init__(self, input_name):
        self.forkable_sum = 0
        self.input_numeric_matrix = []
        self.output_numeric_matrix = []
        self.input_matrix = []
        self.output_matrix = []
        self.local_dir = Path(__file__).resolve().parent
        self.input_path = self.local_dir / input_name
        self.input_initialization()
    def part2_solution(self, num = None, verbose = None):
        self.part2_sum = 0 
        '''continue part 1 until you cannot'''
        self.part1_solution(num, verbose)
        self.part2_sum = self.part2_sum + self.forkable_sum
        round_n = 1
        print(f'Round {round_n} sum: {self.forkable_sum}')
        while self.input_matrix != self.output_matrix:
            new_input = self.translator_output_to_input(self.output_matrix)
            print(f'Output matrix is: {self.output_matrix}')
            print(f"New input matrix is: {new_input}")
            self.input_matrix = new_input
            self.input_numeric_matrix = self.prep_input(self.input_matrix)
            self.part1_solution(num, verbose)
            round_n += 1
            print(f'Round {round_n} sum: {self.forkable_sum}')
            self.part2_sum+= self.forkable_sum
        return self.part2_sum
    def part1_solution(self,num = None, verbose = None):
        # Clear previous results so each call recalculates fresh
        self.output_numeric_matrix = []
        self.output_matrix = []
        self.forkable_sum = 0 
        def adjacent_impact_line(row): 
            row_new = row.copy()
            for i in range(len(row)):
                if row[i] == 0:
                    pass
                else:
                    if i == 0:
                        if row[i+1] == 0:
                            row_new[i] = 0
                        else: 
                            pass
                    elif i == len(row)-1: 
                        if row[i-1] == 0:
                            row_new[i] = 0
                        else: 
                            pass 
                    else: 
                        if row[i+1] == 0 and row[i-1] == 0:
                            row_new[i] = 0
                        elif row[i+1] == 1 and row[i-1] == 1:
                            row_new[i] = 2
                        else:
                            pass
            return row_new
        def above_below_impact_line(row):
            row_new = row.copy()
            for i in range(len(row)):
                if i == 0:
                    row_new[i] = row[i] + row[i+1]
                elif i == len(row)-1:
                    row_new[i] = row[i] + row[i-1]
                else: 
                    row_new[i] = row[i] + row[i-1] + row[i+1]
            return row_new
        def combine(adjacent,above_below):
            for i in range(len(self.input_numeric_matrix)):
                if len(self.input_numeric_matrix) == 1:
                    row = [a if inp > 0 else -1 for a, inp in zip(adjacent[i], self.input_numeric_matrix[i])]
                else: 
                    if i == 0 :
                        row = [(a + b) if inp > 0 else -1 for a, b, inp in zip(adjacent[i], above_below[i+1], self.input_numeric_matrix[i])]
                    elif i == len(self.input_numeric_matrix)-1:
                        row = [(a + b) if inp > 0 else -1 for a, b, inp in zip(adjacent[i], above_below[i-1], self.input_numeric_matrix[i])]
                    else:
                        row = [(a + b + c) if inp > 0 else -1 for a, b, c, inp in zip(adjacent[i], above_below[i-1], above_below[i+1], self.input_numeric_matrix[i])]

                self.output_numeric_matrix.append(row)
        def sum_up(num):
            '''fewer than 'num' will be counted as forkliftable'''
            self.forkable_sum = sum(1 for row in self.output_numeric_matrix for value in row if value < num and value >= 0)
            return self.forkable_sum
        '''forklift 
        for each row, calculate adjacent impact, and impact to above and below rows

        First row should be 0033033430
        0011011110. adjacent: 0011012210 [check left and right]
        0122223321 impact on next row [go thru each digit and sum adjacent]
        Second row:
        2322121222 Impact on previous row
        1110101011. Adjacent: 2220202022
        2322121222 Impact on next row
        Going back to first row: 
        sum up adjacent and impact from next row IF ONLY the entry is 1
            @.@
            ...
            @.@
        '''
        adjacent_impact_matrix = [adjacent_impact_line(row) for row in self.input_numeric_matrix]
        above_below_impact_matrix = [above_below_impact_line(row) for row in self.input_numeric_matrix]  
        combine(adjacent_impact_matrix,above_below_impact_matrix)
        if verbose: 
            print(f"Adjacent impact matrix is {adjacent_impact_matrix}")      
            print(f"Impact to above/below matrix is {above_below_impact_matrix}")
            print(f"Output matrix is {self.output_numeric_matrix}")
        if num is not None:
            sum_up(num)
            self.output_matrix = [self.translator_to_graph(row, num) for row in self.output_numeric_matrix]
            if verbose:
                print("Input Matrix is") 
                for row in self.input_matrix:
                    print({row})
                print("Output matrix is")
                for row in self.output_matrix:
                    print({row})
            return self.forkable_sum
        else: 
            print("No num provided, so only printing out the output numeric matrix.")
            return self.output_numeric_matrix

# ===== MAIN CODE =====
filename = "D4_input.txt"
opt = optimizer(filename)
part_2 = opt.part2_solution(num = 4)
print(f"The result is {part_2}.")
# part_1 = opt.part1_solution(num = 4, verbose = 'on')
# print(f"The result is {part_1}.")