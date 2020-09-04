# File: assembler.py
# Author: Benjamin Ramon
# Date: 04/06/2020
# Section: 509
# E-mail: bramon24@tamu.edu
# Description:
# This Assembler program that translates programs written in the symbolic Hack assembly
# language into binary code that can execute on the Hack hardware platform built in the
# previous projects

import sys

symbol = {"R0": 0, "R1": 1, "R2": 2, "R3": 3, "R4": 4, "R5": 5, "R6": 6, "R7": 7,
          "R8": 8, "R9": 9, "R10": 10, "R11": 11, "R12": 12, "R13": 13, "R14": 14, "R15": 15,
          "SCREEN": 16384, "KBD": 24576, "SP": 0, "LCL": 1, "ARG": 2, "THIS": 3, "THAT": 4}

comp = {"0": "101010", "1": "111111", "-1": "111010", "D": "001100", "A": "110000", "!D": "001111",
        "!A": "110001", "-D": "001111", "-A": "110011", "D+1": "011111", "A+1": "110111", "D-1": "001110",
        "A-1": "110010", "D+A": "000010", "D-A": "010011", "A-D": "000111", "D&A": "000000", "D|A": "010101",
        "M": "110000", "!M": "110001", "-M": "110011", "M+1": "110111", "M-1": "110010", "D+M": "000010",
        "D-M": "010011", "M-D": "000111", "D&M": "000000", "D|M": "010101"}

dest = {"M": "001", "D": "010", "MD": "011", "A": "100", "AM": "101", "AD": "110", "AMD": "111"}

jump = {"JGT": "001", "JEQ": "010", "JGE": "011", "JLT": "100", "JNE": "101", "JLE": "110", "JMP": "111"}

binary_array = []


def label(instruction):
    if instruction[0] == '(':
        return True
    return False


def is_variable(instruction):
    if instruction[0] == '@':
        return True
    return False


def is_int(instruction):
    try:
        int(instruction)
    except Exception:
        return False
    return True


def c_instruction(instruction):
    translated = '111'
    if 'M' in instruction[2:] and 'JM' not in instruction[2:]:
        a = '1'
    else:
        a = '0'
    if ';' in instruction:
        temp_instruc = str(instruction[0])
        temp_instruc2 = str(instruction[2:])
        translated = translated + a + comp[temp_instruc] + '000' + jump[temp_instruc2]
    elif '=' in instruction:
        temp_instruc = str(instruction.split('=')[1])
        temp_instruc2 = str(instruction.split('=')[0])
        translated = translated + a + comp[temp_instruc] + dest[temp_instruc2] + '000'
    else:
        return
    return translated


def main():
    args = sys.argv
    file1 = str(args[1])
    with open(file1, "r") as file:
        line_idx = 0
        for line in file:
            instruc = line.strip()
            if not line.strip() or line[0] == '/':
                continue
            if line.find('//'):
                instruc = line.split('//')
                instruc = str(instruc[0])
                instruc = instruc.strip()
            if label(instruc) and instruc[1:] not in symbol.keys():
                symbol[instruc[1:-1]] = line_idx
            else:
                line_idx += 1

    with open(file1, "r") as file:
        line_idx = 0
        variable_idx = 16
        for line in file:
            instruc = line.strip()
            if not line.strip() or line[0] == '/':
                continue
            if line.find('//'):
                instruc = line.split('//')[0]
                instruc = instruc.strip()
            if label(instruc):
                continue
            elif is_variable(instruc) and instruc[1:] in symbol.keys():
                value = symbol[instruc[1:]]
                value = bin(value)
                value = str(value[2:])
                while len(value) < 16:
                    value = '0' + value
                line_idx += 1
            elif is_variable(instruc) and is_int(str(instruc[1:])) and instruc not in symbol.keys():
                instruc = instruc[1:]
                symbol[instruc] = int(instruc)
                value = symbol[instruc]
                value = bin(value)
                value = str(value[2:])
                while len(value) < 16:
                    value = '0' + value
                line_idx += 1
            elif is_variable(instruc) and instruc not in symbol.keys():
                instruc = instruc[1:]
                symbol[instruc] = variable_idx
                value = symbol[instruc]
                value = bin(value)
                value = str(value[2:])
                while len(value) < 16:
                    value = '0' + value
                variable_idx += 1
                line_idx += 1
            else:  # c instruction
                value = c_instruction(instruc)
                line_idx += 1
            binary_array.append(value)

    output_file = file1.rstrip('asm')
    output_file = output_file + "hack"
    with open(output_file, 'w') as output_file:
        for i in binary_array:
            output_file.write(i + "\n")
    return

main()
