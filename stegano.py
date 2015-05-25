import sys
import re

def to_bits(s):
    result = []
    for c in s:
        bits = bin(ord(c))[2:]
        bits = '00000000'[len(bits):] + bits
        result.extend([int(b) for b in bits])
    return result

def from_bits(bits):
    chars = []
    for b in range(len(bits) / 8):
        byte = bits[b*8:(b+1)*8]
        chars.append(chr(int(''.join([str(bit) for bit in byte]), 2)))
    return ''.join(chars)

if len(sys.argv) < 2:
    print 'Too few parameters'
    exit()

mess_file = open("mess.txt", "r")
cover_file = open("cover.html", "r")
help_file = open("help.html", "w")
detect_file = open("detect.txt", "w")

lines = 0
spaces = 0
for line in cover_file:
    line = re.sub(' +', ' ', line)
    if line.count(' ') > 0:
        spaces += 1
    lines += 1
    help_file.write(line)
help_file.close()
cover_file.close()
cover_file = open("cover.html", "r")

if sys.argv[1] == "-e":
    line_number = 0;
    watermark_file = open("watermark.html", "w")
    bit_message = to_bits(mess_file.readline())
    if sys.argv[2] == "-1":
        if len(bit_message) > lines:
            print "cover file is too short"
            exit()
        for i in range(0, len(bit_message)):
            if bit_message[i] == 1:
                line = cover_file.readline()
                watermark_file.write(line[:-1] + ' \n')
            else:
                watermark_file.write(cover_file.readline())
        for i in range(len(bit_message), lines):
            watermark_file.write(cover_file.readline())
    elif sys.argv[2] == "-2":
        help_file = open("help.html", "r")
        print bit_message
        if len(bit_message) > spaces:
            print "cover file is too short"
            exit()
        for i in range(lines):
            line = help_file.readline()
            if line.count(' ') > 0 and line_number < len(bit_message) - 1:
                if bit_message[line_number] == 1:
                    line = re.sub(" ", "  ", line, 1)
                    watermark_file.write(line)
                else:
                    watermark_file.write(line)
                line_number += 1
            else:
                watermark_file.write(line)
        for i in range(line_number, lines):
            watermark_file.write(help_file.readline())
    elif sys.argv[2] == "-3":
        print "-e -3"

    elif sys.argv[2] == "-4":
        print "-e -4"

    else:
        print "Unknown second parameter"
        exit()
elif sys.argv[1] == "-d":
    watermark_file = open("watermark.html", "r")
    if sys.argv[2] == "-1":
        bit_message = []
        for i in range(lines-1):
            line = watermark_file.readline()
            if len(line) > 1:
                if line[-2] == ' ':
                    bit_message.append(1)
                else:
                    bit_message.append(0)
        print from_bits(bit_message)
    elif sys.argv[2] == "-2":
        bit_message = []
        for i in range(lines-1):
            line = watermark_file.readline()
            if len(line) > 0 and line.count('  ') > 0 or line.count(' ') > 0:
                if line.count('  ') > 0:
                    bit_message.append(1)
                else:
                    bit_message.append(0)
        print from_bits(bit_message)

    elif sys.argv[2] == "-3":
        print "-e -3"

    elif sys.argv[2] == "-4":
        print "-e -4"

    else:
        print "Unknown second parameter"
        exit()
else:
    print "Unknown first parameter"
    exit()
