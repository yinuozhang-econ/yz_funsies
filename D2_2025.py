import math

class IDValidator:
    
    def __init__(self, ranges):
        self.ranges = ranges
        self.sum = 0
    def get_factors(self, n):
        factors = set()
        for i in range(1, int(math.sqrt(n)) + 1):
            if n % i == 0:
                factors.add(i)
                factors.add(n // i) # Add the "partner" factor
        return sorted(list(factors))    
    def part2_solution(self):
        '''
        Part 2: some sequence appears at least twice: e.g. 5555555 in 5488908-5597446; 14101091-14196519 
        Break each range to 'unit ranges' based on the digit length. e.g. 99-2000 will be: 99, 100-999, 1000-2000.
        For each 'unit range':
            - consider the factor of the digits length, then truncate them.
        1) consider all the common factors of start_digits and end_digits, including 1
            2) for each factor k: consider the first k digits of the start number, repeat it start_digits/k times and see if it falls in the range.
                2a) if it falls below the start, increment the first k digits by 1 and try again: 
                    - once plus one causes the first k digits to have an additional digit, we need to check if that new number is in the common factors list 
                    - However, if the factor is 1
        '''
        self.sum = 0
        for start, end in self.ranges:
            self.invalid_ids = [] # just to keep track of invalid ids for each range. Then I will sum it 
            initial = start
            print(f"\nRange {start}-{end}: ", end="")
            list_log10 = list(range(int(math.log10(start)), int(math.log10(end))+1))
            for r_log10 in list_log10:
                if 10**(r_log10+1) < end:
                    current_range = range(initial, 10**(r_log10+1))
                    digits = len(str(initial))
                else:  
                    current_range = range(initial, end+1)
                    digits = len(str(end))
                print(f"\n Interval {list(current_range)[0]}-{list(current_range)[-1]}: ", end="")
                initial = 10**(r_log10+1)
                if int(math.log10(list(current_range)[-1])) == 0: #5-20: 5-9, 10-20.
                    print(f"no invalid ids by definition.")
                    continue
                factors_list = self.get_factors(digits)   
                for factor in factors_list:
                    seq = int(str(current_range[0])[:factor])
                    num = int(str(seq)*(digits//factor)) 
                    while num < current_range[0] and digits//factor >1:
                        print(f"\n The first one {num} of factor {factor} falls below {current_range[0]}: ", end="")
                        seq += 1
                        num = int(str(seq)*(digits//factor))
                        print(f"try {num}")
                    while num <= end and digits//factor > 1:
                        self.invalid_ids.append(num) if num not in self.invalid_ids else None
                        print(f"Found invalid ID {num} of factor {factor}, ", end="")
                        # self.sum += num
                        seq += 1
                        num = int(str(seq)*(digits//factor)) 
                print(f"\n Invalid IDs in this interval: {self.invalid_ids}")
            print(f"\n Invalid IDs in this range: {self.invalid_ids}")    
            self.sum += sum(self.invalid_ids)
        print(f"\nThe sum of all invalid IDs is {self.sum}")
        return self.sum        

    def part1_solution(self):
        '''
        Part 1: exact two parts
        1) if start has odd digits
            1a) if end also has the same number of odd digits, then this range is ineligible
            1b) if not, suppose the start digits are 2k+1. 
                check if the doubled of 1000(k-1 many 0's) falls in the range
            check if seq "double" (in integer sense) falls in the range. If it does, sum +=1
            !!! NEED TO AMEND: 96763-229430, think I only need to worry about it if the digit difference is one
        2) if the start has even digits
            take the first k digits, check if that "double" (in integer sense) falls in the range. 
            2a) if the "doubled" one falls below the start, need to add one and try again, until we reach 2b) or 2c).
            2b) if the "doubled" one exceeds the end, move to the next range
            2c) if the "doubled" one falls into the range, sum +=1, repeat until it reaches 2b)
        '''
        for start, end in self.ranges: 
            start_digits = len(str(start))
            end_digits = len(str(end))
            if start_digits % 2 !=0 and start_digits == end_digits:
                print(f"\nThere is no invalid ID between {start}-{end} because the start and end have the same amount of odd digits.\n")
                continue
            else:
                if start_digits % 2 !=0:
                    seq = int(str(1)+str(0)*((start_digits-1)//2))
                    num = int(str(seq)*2)
                    slice_digit = start_digits//2 + 1
                else: 
                    slice_digit = int(start_digits/2)
                    num = start
                seq = int(str(num)[:slice_digit])
                num = int(str(seq)*2)
                print(f"\nRange {start}-{end}: ", end="")
                if num > end:
                    print(f"The first one {num} exceeds {end}. Go to next range. \n")
                elif num < start: 
                    print(f"The first one {num} falls below {start}: ", end="")
                    while num < start:
                        seq +=1
                        num = int(str(seq)*2)
                        print(f"try {num}")
                while num <= end:
                    print(f"{num}, ", end="")
                    self.sum += num
                    seq += 1
                    num = int(str(seq)*2)
        print(f"\nThe sum of all invalid IDs is {self.sum}")
        return self.sum

# ===== MAIN CODE =====
print("please put in the id sequence")
line = input().strip()
ranges = []
for range_str in line.split(','):
    start, end = map(int, range_str.split('-'))
    ranges.append((start, end))

# Create validator instance
validator = IDValidator(ranges)

# ===== CONTROL WHICH PART TO RUN =====
# Uncomment the line(s) you want to run:

# validator.part1_solution()  # Run Part 1
validator.part2_solution()  # Run Part 2 (when implemented)