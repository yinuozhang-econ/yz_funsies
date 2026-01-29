from pathlib import Path

class joltageDeterminator:
    def __init__(self, input_path):
        self.joltage_sum = 0
        self.joltage = []
        self.local_dir = Path(__file__).resolve().parent
        self.input_path = self.local_dir / input_path
    def load_input(self, processor=None):
        with open(self.input_path, 'r', encoding="utf-8") as f:
            for raw_line in f:
                line = raw_line.strip()
                if processor: 
                    processor(line)
    def part1_solution(self,line):
        '''Part1: sum the largest two "batteries" for each bank
            1) Set the largest and the second largest to be 0. 
            2) Go through each digit, excluding the last one.
                2a) if current_digit is the last digit, replace the second_largest with current_digit if current_digit>second_largest, otherwise do nothing
            3) if current_digit is larger than the largest, set the largest to current_digit, and the second largest to next digit
            4) if the current digit is smaller than or equal to the largest, replace the second_largest with current_digit if current_digit>second_largest, otherwise do nothing
            '''
        self.joltage_sum = 0
        self.joltage = []
        largest = 0
        second_largest = 0
        for index, digit_char in enumerate(str(line)):
            current_digit = int(digit_char)
            if index < len(str(line))-1:  
                next_digit = int(str(line)[index+1])              
                if current_digit > largest:
                    largest = current_digit
                    second_largest = next_digit
                else: 
                    if current_digit > second_largest:
                        second_largest = current_digit
            else:
                if current_digit > second_largest:
                    second_largest = current_digit
                else:
                    pass
        joltage = int(str(largest) + str(second_largest))
        self.joltage.append(joltage)
        self.joltage_sum = self.joltage_sum+joltage
        print(f"The joltage for bank {line} is {joltage}. The total joltage so far is {self.joltage_sum}.")

    def find_big(self,num_str):
        return max(int(num) for num in num_str)

    def part2_solution_new(self,line,top_num = 12):
        self.joltage_list = []
        self.joltage = 0
        """Part 2: instead of two, need to do top_num=12.
           Gonna do it recursively this time
           1) for each ranking, truncate the line to the "feasible string" 
           2) find the largest number in the feasible string
           3) truncate line from the index of the found largest number, repeat.
            """
        num_str = str(line)
        print(f"For battery {line}:", end = '')
        for rank in range(1,top_num+1):
            if top_num - rank == 0:
                line_to_search = num_str
            else:
                line_to_search = num_str[:-(top_num - rank)]
            biggest = self.find_big(line_to_search)
            self.joltage_list.append(biggest)
            index = num_str.index(str(biggest))
            num_str = num_str[index+1:]
            self.joltage += self.joltage_list[rank-1]*10**(top_num-rank)
        self.joltage_sum += self.joltage
        print(f"the joltage list is {self.joltage_list} and joltage is {self.joltage}.")
        print(f"the total sum is {self.joltage_sum} so far.")

   
# ===== MAIN CODE =====
filename = "D3_input.txt"
# filename = "D3_input_test.txt"
determinant = joltageDeterminator(filename)
# determinant.load_input(processor=determinant.part2_solution_new)
# string = "234234234234278"
string = "2112212224221323212122212232121422221211292212942125222122223422322222422223522212222211332222222272"
determinant.part2_solution_new(string, top_num=12)
