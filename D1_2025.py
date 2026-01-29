import re

print("please put in the sequence (you can skip the space between R/L and the number)")
line = input().strip()
# Insert space before R/L except for the first one
line = re.sub(r'(?<!^)([RL])', r' \1', line)
items = line.split()

old_value = 50
count_passzero = 0
'''
1) start anywhere not zero, right.
    1a) stop at zero (e.g. initial + R150)
        covered by check2 != check
    1b) stop at nonzero     
        covered by check2 != check
2) start at zero, right
    covered by check2 != check
3) start anywhere not zero, left.
    3a) stop at zero, and turn less than 100 (e.g. initial + L50)
        need to +1 outside of check2 != check, 
    3b) stop at nonzero; or stop at zero, and turn more than 100, including 100.
        covered by check2 != check
4) start at zero, left (e.g. at zero + L1)
    4a) stop at nonzero
        On top of check2 != check, need to -1
    4b) stop at zero
        covered by check2 != check    
'''
for item in items:
    check = old_value//100
    if item[0] == 'L':
        new_value = old_value - int(item[1:])
    elif item[0] == 'R':
        new_value = old_value + int(item[1:])
    check2 = new_value//100
    diff = abs(check2 - check)
    if check2 != check:
        count_passzero += diff
        if item[0] == 'L':  # case 4a
            if new_value%100 != 0 and old_value % 100 == 0: 
                count_passzero -= 1
    if item[0] == 'L':  # case 3a
        if old_value%100 != 0 and new_value % 100 == 0: # and int(item[1:])//100 == 0: 
            count_passzero += 1
    old_value = new_value % 100

print(f"The pw is {count_passzero} under method 0x434C49434B, landed at {old_value}")

