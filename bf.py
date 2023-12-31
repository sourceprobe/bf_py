#!/usr/bin/env python3
import sys

TAPE_LEN = 30*1000
def build_jumps(prog):
    '''
    build a pair of dicts from
    a program.
    returns (forward, backward)
    forward maps forward->back
    backward maps backward->forward
    '''
    forward = {}
    backward = {}
    stack = []
    i = 0
    while i < len(prog):
        if prog[i] == '[':
            stack.append(i)
        elif prog[i] == ']':
            match = stack.pop()
            backward[i] = match
            forward[match] = i
        i += 1
        pass
    return (forward, backward)

def bf(prog):
    tape = [0]*TAPE_LEN
    (forward, backward) = build_jumps(prog)
    ptr = 0
    pc = 0
    end = len(prog)
    while pc < end:
        c = prog[pc]
        if c == '+':
            tape[ptr] = (tape[ptr]+1) % 255
        elif c == '-':
            tape[ptr] = (tape[ptr]-1) % 255
        elif c == '>':
            ptr += 1
        elif c == '<':
            ptr -= 1
        elif c =='[':
            if tape[ptr] == 0:
                pc = forward[pc]
        elif c == ']':
            if tape[ptr] != 0:
                pc = backward[pc]
        elif c == '.':
            print(chr(tape[ptr]), end='')
        elif c == ',':
            print(", unimplemented")
            sys.exit(1)
        else:
            print("unhandled instn: {}".format(c))
            sys.exit(1)
        pc += 1

def clean(lines):
    data = ""
    for line in lines:
        if line.startswith(';'):
            continue
        else:
            data += line
    data = data.replace('\n', '')
    data = data.replace(' ', '')
    return data
    
if __name__ == "__main__":
    with open(sys.argv[1]) as f:
        lines = f.readlines()
        bf(clean(lines))
