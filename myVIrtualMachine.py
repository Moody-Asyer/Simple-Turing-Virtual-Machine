import time
import argparse


def execute(instructions, memory, simulation):
    print('Ins: ', instructions)
    while not instructions.strip().lstrip('-').isnumeric():
        for i in range(len(instructions)):
            if instructions[i] == '(':
                kurung_awal = i
            elif instructions[i] == ')':
                kurung_akhir = i
                break
        instruction = instructions[kurung_awal:kurung_akhir + 1]
        tape = convert_and_store(instruction, memory)
        result = turing_machine(tape, simulation)
        instructions = instructions.replace(instruction, ' '+str(result)+' ')
        print('Ins: ', instructions)
    return int(instructions)

def convert_and_store(instruction, memo):
    instruction = instruction[1:-1]
    if instruction == 'start':
        return 0
    elif instruction == 'end':
        return -1
    elif instruction[:4] == 'goto':
        return int(instruction[5:]) # this will be the number of goto destination
    elif instruction.isnumeric():
        return instruction
    try:
        operator, operand1, operand2 = instruction.split()
        operand1, operand2 = int(operand1), int(operand2)
    except:
        print('Invalid syntax')
        exit()
    tape = []
    if operator == '=':
        memo[operand1] = operand2
        return 0 # go to next line
    elif operator == '>':
        tape.append('G')
        for i in range(memo[operand1]):
            tape.append(0)
        tape.append('#')
        for i in range(memo[operand2]):
            tape.append(0)
    elif operator == '<':
        tape.append('L')
        for i in range(memo[operand1]):
            tape.append(0)
        tape.append('#')
        for i in range(memo[operand2]):
            tape.append(0)
    elif operator == "+":
        tape.append('A')
        for i in range(operand1):
            tape.append(0)
        tape.append('#')
        for i in range(operand2):
            tape.append(0)
    elif operator == "-":
        tape.append('S')
        for i in range(operand1):
            tape.append(0)
        tape.append('#')
        for i in range(operand2):
            tape.append(0)
    elif operator == "*":
        tape.append('M')
        for i in range(operand1):
            tape.append(0)
        tape.append('#')
        for j in range(operand2):
            tape.append(0)
        tape.append('#')
    elif operator == "/":
        tape.append('D')
        for i in range(operand1):
            tape.append(0)
        tape.append('#')
        for j in range(operand2):
            tape.append(0)
        tape.append("#")
    elif operator == "IF":
        if operand1 == 0: # False
            return 0
        else: # True
            return operand2
    tape.append('B')
    return tape


def turing_machine(tape, simulation):
    state = 'q0'
    pointer = 0
    if type(tape) != list:
        return tape
    while state != 'q4':
        if simulation:
            time.sleep(1)
            print('state: ', state)
            print(' '.join(list(map(str, tape))))
            print('  '*(pointer)+'^')
        # untuk penjumlahan
        if state == 'q0' and tape[pointer] == 'A':
            state = 'q1'
            pointer += 1
        elif state == 'q1' and tape[pointer] == 0:
            pointer += 1
        elif state == 'q1' and tape[pointer] == '#':
            state = 'q2'
            pointer += 1
        elif state == 'q2' and tape[pointer] == 0:
            tape[pointer] = '#'
            state = 'q3'
            pointer -= 1
        elif state == 'q3' and tape[pointer] == '#':
            tape[pointer] = 0
            state = 'q1'
            pointer += 1
        elif state == 'q2' and tape[pointer] == 'B':
            state = 'q4'
        # untuk pengurangan
        elif state == 'q0' and tape[pointer] == 'S':
            state = 'q5'
            pointer += 1
        elif state == 'q5' and tape[pointer] == 0:
            state = 'q6'
            tape[pointer] = 'X'
            pointer += 1
        elif state == 'q6' and tape[pointer] == 0:
            state = 'q6'
            pointer += 1
        elif state == 'q6' and tape[pointer] == '#':
            state = 'q7'
            pointer += 1
        elif state == 'q7' and tape[pointer] == 0:
            tape[pointer] = 'Y'
            state = 'q8'
            pointer -= 1
        elif state == 'q8' and tape[pointer] == '#':
            pointer -= 1
        elif state == 'q8' and tape[pointer] == 'Y':
            pointer -= 1
        elif state == 'q8' and tape[pointer] == 0:
            pointer -= 1
        elif state == 'q8' and tape[pointer] == 'X':
            tape[pointer] = 'Y'
            state = 'q5'
            pointer += 1
        elif state == 'q7' and tape[pointer] == 'Y':
            pointer += 1
        elif state == 'q7' and tape[pointer] == '#':
            pointer += 1
        elif state == 'q7' and tape[pointer] == 'B':
            state = 'q9'
            pointer -= 1
        elif state == 'q9' and tape[pointer] == 'Y':
            state = 'q9'
            pointer -= 1
        elif state == 'q9' and tape[pointer] == '#':
            state = 'q9'
            pointer -= 1
        elif state == 'q9' and tape[pointer] == 0:
            state = 'q9'
            pointer -= 1
        elif state == 'q9' and tape[pointer] == 'X':
            state = 'q4'
            tape[pointer] = 0

        #contoh perkalian 3x2
        #step1
        elif state == 'q0' and tape[pointer] == 'M':
            state = 'q10'
            pointer += 1
        elif state == 'q10' and tape[pointer] == 0:
            tape[pointer] = 'X'
            state = 'q11'
            pointer += 1
        elif state == 'q11' and tape[pointer] == 0:
            pointer += 1
        elif state == 'q11' and tape[pointer] == '#':
            state = 'q12'
            pointer += 1
        elif state == 'q12' and tape[pointer] == 0:
            tape[pointer] = 'Y'
            state = 'q13'
            pointer += 1
        elif state == 'q13' and tape[pointer] == 0:
            pointer += 1
        elif state == 'q13' and tape[pointer] == '#':
            state = 'q14'
            pointer += 1
        elif state == 'q14' and tape[pointer] == 'B':
            tape[pointer] = 0
            tape.append('B')
            state = 'q15'
            pointer -= 1
        elif state == 'q14' and tape[pointer] == 0:
            pointer += 1
        elif state == 'q15' and tape[pointer] == '#':
            state = 'q16'
            pointer -= 1
        elif state == 'q15' and tape[pointer] == 0:
            pointer -= 1
        elif state == 'q16' and tape[pointer] == 0:
            pointer -= 1
        elif state == 'q16' and tape[pointer] == 'Y':
            state = 'q12'
            pointer += 1
        elif state == 'q12' and tape[pointer] == '#':
            state = 'q17'
            pointer -= 1
        elif state == 'q17' and tape[pointer] == 'Y':
            tape[pointer] = 0
            pointer -= 1
        elif state == 'q17' and tape[pointer] == '#':
            pointer -= 1
            state = 'q18'
        elif state == 'q18' and tape[pointer] == 0:
            pointer -= 1
        elif state == 'q18' and tape[pointer] == 'X':
            pointer += 1
            state = 'q10'
        elif state == 'q10' and tape[pointer] == '#':
            state = 'q19'
            pointer += 1
        elif state == 'q19' and tape[pointer] == 0:
            tape[pointer] = 'Y'
            pointer += 1
        elif state == 'q19' and tape[pointer] == '#':
            state = 'q4'

        # Pembagian
        elif state == 'q0' and tape[pointer] == 'D':
            state = 'q20'
            pointer += 1
        elif state == 'q20' and tape[pointer] == 0:
            pointer += 1
        elif state == 'q20' and tape[pointer] == '#':
            state = 'q21'
            pointer += 1
        elif state == 'q21' and tape[pointer] == 0:
            tape[pointer] = 'Y'
            state = 'q22'
            pointer -= 1
        elif state == 'q22' and tape[pointer] == '#':
            pointer -= 1
        elif state == 'q22' and tape[pointer] == 0:
            tape[pointer] = 'X'
            state = 'q20'
            pointer += 1
        elif state == 'q20' and tape[pointer] == 'X':
            pointer += 1
        elif state == 'q21' and tape[pointer] == 'Y':
            pointer += 1
        elif state == 'q22' and tape[pointer] == 'Y':
            pointer -= 1
        elif state == 'q22' and tape[pointer] == 'X':
            pointer -= 1
        elif state == 'q21' and tape[pointer] == '#':
            state = 'q26'
            pointer += 1
        elif state == 'q26' and tape[pointer] == 0:
            pointer += 1
        elif state == 'q26' and tape[pointer] == "B":
            tape[pointer] = 0
            pointer -= 1
            tape.append('B')
            state = 'q27'
        elif state == 'q27' and tape[pointer] == 0:
            pointer -= 1
        elif state == 'q27' and tape[pointer] == '#':
            state = 'q23'
            pointer -= 1
        elif state == 'q23' and tape[pointer] == 'Y':
            tape[pointer] = 0
            pointer -= 1
        elif state == 'q23' and tape[pointer] == '#':
            state = 'q21'
            pointer += 1
        elif state == 'q22' and tape[pointer] == 'D':
            state = 'q24'
            pointer += 1
        elif state == 'q24' and tape[pointer] == 'X':
            pointer += 1
        elif state == 'q24' and tape[pointer] == '#':
            pointer += 1
            state = 'q25'
        elif state == 'q25' and tape[pointer] == 'Y':
            pointer += 1
        elif state == 'q25' and tape[pointer] == 0:
            tape[pointer] = 'Y'
            pointer += 1
        elif state == 'q25' and tape[pointer] == '#':
            state = 'q4'
        # operator lebih besar
        elif state == 'q0' and tape[pointer] == 'G':
            state = 'q28'
            pointer += 1
        elif state == 'q28' and tape[pointer] == 0:
            tape[pointer] = 'X'
            state = 'q29'
            pointer += 1
        elif state == 'q29' and tape[pointer] == 0:
            pointer += 1
        elif state == 'q29' and tape[pointer] == '#':
            state = 'q30'
            pointer += 1
        elif state == 'q30' and tape[pointer] == 0:
            tape[pointer] = 'X'
            state = 'q31'
            pointer -= 1
        elif state == 'q30' and tape[pointer] == 'X':
            pointer += 1
        elif state == 'q30' and tape[pointer] == 'B': # True
            state = 'q34'
            tape[pointer] = 0
            tape.append('B')
            pointer -= 1
        elif state == 'q34' and tape[pointer] == 'X':
            pointer -= 1
        elif state == 'q34' and tape[pointer] == '#':
            state = 'q35'
            pointer -= 1
        elif state == 'q35' and tape[pointer] == 0:
            tape[pointer] = 'X'
            pointer -= 1
        elif state == 'q35' and tape[pointer] == 'X':
            state = 'q4'
        elif state == 'q31' and tape[pointer] == '#':
            state = 'q33'
            pointer -= 1
        elif state == 'q31' and tape[pointer] == 0:
            pointer -= 1
        elif state == 'q31' and tape[pointer] == 'X':
            pointer -= 1
        elif state == 'q33' and tape[pointer] == 0:
            pointer -= 1
        elif state == 'q33' and tape[pointer] == 'X':
            state = 'q28'
            pointer += 1
        elif state == 'q28' and tape[pointer] == '#': # False
            state = 'q32'
            pointer += 1
        elif state == 'q32' and tape[pointer] == 'X':
            pointer += 1
        elif state == 'q32' and tape[pointer] == 0:
            tape[pointer] = 'X'
            pointer += 1
        elif state == 'q32' and tape[pointer] == 'B':
            state = 'q4'
        # operator lebih kecil
        elif state == 'q0' and tape[pointer] == 'L':
            state = 'q36'
            pointer += 1
        elif state == 'q36' and tape[pointer] == 0:
            tape[pointer] = 'X'
            state = 'q37'
            pointer += 1
        elif state == 'q37' and tape[pointer] == 0:
            pointer += 1
        elif state == 'q37' and tape[pointer] == '#':
            state = 'q38'
            pointer += 1
        elif state == 'q38' and tape[pointer] == 0:
            tape[pointer] = 'X'
            state = 'q39'
            pointer -= 1
        elif state == 'q38' and tape[pointer] == 'X':
            pointer += 1
        elif state == 'q38' and tape[pointer] == 'B': # False
            state = 'q42'
            pointer -= 1
        elif state == 'q42' and tape[pointer] == 'X':
            pointer -= 1
        elif state == 'q42' and tape[pointer] == '#':
            state = 'q43'
            pointer -= 1
        elif state == 'q43' and tape[pointer] == 0:
            tape[pointer] = 'X'
            pointer -= 1
        elif state == 'q43' and tape[pointer] == 'X':
            state = 'q4'
        elif state == 'q39' and tape[pointer] == '#':
            state = 'q41'
            pointer -= 1
        elif state == 'q39' and tape[pointer] == 0:
            pointer -= 1
        elif state == 'q39' and tape[pointer] == 'X':
            pointer -= 1
        elif state == 'q41' and tape[pointer] == 0:
            pointer -= 1
        elif state == 'q41' and tape[pointer] == 'X':
            state = 'q36'
            pointer += 1
        elif state == 'q36' and tape[pointer] == '#': # True
            state = 'q40'
            pointer += 1
        elif state == 'q40' and tape[pointer] == 'X':
            pointer += 1
        elif state == 'q40' and tape[pointer] == 0:
            tape[pointer] = 'X'
            pointer += 1
        elif state == 'q40' and tape[pointer] == 'B':
            tape[pointer] = 0
            tape.append('B')
            state = 'q4'
        else:
            print('Invalid syntax')
            break
    if simulation:
        time.sleep(1)
        print('state: ', state)
        print(' '.join(list(map(str, tape))))
        print('  '*(pointer)+'^')
        interupt = input('Continue? ')
    if state == 'q4':
        return tape.count(0)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("program")
    args = parser.parse_args()
    instruction_file = open(args.program, 'r')

    lines = []
    for instruction in instruction_file:
        lines.append(instruction.strip())

    memory = [None, None, None]

    line_num = 0
    while line_num != -1:
        result = execute(lines[line_num], memory, simulation=True)
        if result == 0:
            line_num += 1
        else:
            line_num = result
        print(memory)