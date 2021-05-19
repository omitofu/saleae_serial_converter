# As Saleae Serial analyzer exports one byte per line cvs file, the readability is poor.
# This converter combines the bytes to a readiable message.
# Fisrt line is supposed to be a header.

# Usage:
# saleae_serial_converter.py saleae_exported_filename converted_filename
import csv
import sys
import os
import shutil

def bytes2msg(bytefile, msgfile):
    F_IDX_TIMES = 0
    F_IDX_NAME = 1
    F_IDX_DATA = 2
    msgs = []
    msg = []

    OldTimestamps = 0
    timestamps = 0

    with open(bytefile, 'r') as rf:
        reader = csv.reader(rf)
        line_count = 0
        for row in reader:
            line_count = line_count + 1
            if line_count == 1:
                continue

            timestamps = int(float(row[F_IDX_TIMES]) * 100000000)
            if (timestamps - OldTimestamps > 100000) or row[F_IDX_NAME] != msg[F_IDX_NAME]:
                if len(msg) > 0:
                        msgs.append(msg)
                msg = row[F_IDX_TIMES:F_IDX_DATA+1]
            else:
                msg.append(row[F_IDX_DATA])
            OldTimestamps = timestamps
        if len(msg)>0:
            msgs.append(msg)
    
    with open(msgfile, "w", newline = '') as wf:
        writer = csv.writer(wf)
        writer.writerows(msgs)
    
    return len(msgs)

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print(" Usage:")
        print(" saleae_serial_converter.py saleae_exported_filename converted_filename")
        exit(-1)
    bytefile = sys.argv[1]
    msgfile = sys.argv[2]
    bytes2msg(bytefile, msgfile)

