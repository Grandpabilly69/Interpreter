import sys

#read arguments
program_filepath = sys.argv[1]

##################
#Tokenise program
##################

#read lines in file

program_lines = []
with open(program_filepath,"r") as program_file:
    program_lines =[line.strip() for line in program_file.readlines()]

program = []
token_count = 0
label_track = {}
for line in program_lines:
    parts = line.split(" ")
    opcode = parts[0]
    #check if empty line
    if opcode == "":
        continue
    #checks if it is a label
    if opcode.endswith(":"):
        label_track[opcode[:-1]] = token_count
        continue
    #store opcode token
    program.append(opcode)
    token_count+=1

    #handel each opcode
    if opcode == "PUSH":
        number = int(parts[1])
        program.append(number)
        token_count+=1
    elif opcode == "PRINT":
        #parse string literal
        string_literal = " ".join(parts[1:])[1:-1]
        program.append(string_literal)
        token_count+=1
    elif opcode == "JUMP.EQ.0":
        # read label
        label = parts[1]
        program.append(label)
        token_count += 1
    elif opcode == "JUMP.GT.0":
        #read label
        label = parts[1]
        program.append(label)
        token_count+=1

#####################
#Interperate the program
#####################

class Stack:
    def __init__(self,size):
        self.buf = [0 for i in range(size)]
        self.sp = -1

    def push(self,number):
        self.sp += 1
        self.buf[self.sp] = number

    def pop(self):
        number = self.buf[self.sp]
        self.sp -= 1
        return number

    def top(self):
        return self.buf[self.sp]

pc = 0
stack = Stack(256)

while program[pc] != "HALT":
    opcode = program[pc]
    pc += 1

    if opcode == "PUSH":
        number = program[pc]
        pc += 1
        stack.push(number)
    elif opcode == "POP":
        stack.pop()
    elif opcode == "ADD":
        a = stack.pop()
        b = stack.pop()
        stack.push(a+b)
    elif opcode == "SUB":
        a = stack.pop()
        b = stack.pop()
        stack.push(b-a)
    elif opcode == "PRINT":
        string_literal = program[pc]
        pc += 1
        print(string_literal)
    elif opcode == "READ":
        number = int(input())
        stack.push(number)
    elif opcode == "JUMP.EQ.0":
        number = stack.top()
        if number == 0:
            pc = label_track[program[pc]]
        else:
            pc += 1
    elif opcode == "JUMP.GT.0":
        number = stack.top()
        if number > 0:
            pc = label_track[program[pc]]
        else:
            pc += 1
