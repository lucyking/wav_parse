import sys
import time
import pylab as pl
from scipy.io import wavfile
import matplotlib.pyplot as plt
import numpy as np

# plt.text(i, j + 0.5, '({}, {})'.format(i, j))
# https://stackoverflow.com/questions/14321627/scipy-io-wavfile-gives-wavfilewarning-chunk-not-understood-error
## The easiest solution to this problem is to convert the wav file into other wav file using SoX.
##    $ sox wavfile.wav wavfile2.wav
if(len(sys.argv) < 2):
    print("No input wav file. Abort!")
    exit(-1)
input_file = sys.argv[1]
samplerate, data = wavfile.read(input_file)
#samplerate, data = wavfile.read('./a2.wav')

print(samplerate)
print(type(data))
print(f"number of channels = {data.shape[1]}")
length = data.shape[0] / samplerate
print(f"length = {length}s")

start_cut = False
start_frame = 0
end_frame = 0

content = ""

'''
print(data[707909][0])
print(data[707909][1])
print(data[707909, 0])
print(data[707909, 1])
#exit(0)
'''

for i in range(0, 48000 * 3):
    content += ('%d %f (s)  l %d  r %d' % (i, i / samplerate, data[i, 0], data[i, 1])) + '\n'
    if abs(data[i, 0] - data[i, 1]) > 1000:
        if start_cut is False:
            start_frame = i
            start_cut = True
        continue
    else:
        start_cut = False
        end_frame = i

with open('wav_in_txt.log', 'w+') as f:
    f.write(content)
# exit(6)

#X = 3.00
#Y = 3.40
#X = 2.80
#Y = 3.40

#X = 31.55
#Y = 31.60

X = 0
Y = length

#X = 42.11
#Y= 44

#X = 3.10
#Y= 3.20

SIMPLE_RATE=100

wav_time = np.linspace(X, Y, int((Y - X) * 48000))

L_channel = data[int(X * 48000):int(Y * 48000), 0]
R_channel = data[int(X * 48000):int(Y * 48000), 1]

# L_channel_24in1 = []
# R_channel_24in1 = []


def simple24in1(input_channel):
    input_channel_24in1 = []
    for i in range(0, int(len(input_channel) / SIMPLE_RATE)):
        cur_max = -1000000
        for j in range(0, SIMPLE_RATE):
            index = i * SIMPLE_RATE + j
            #print(f"i:{i} j:{j} index:{index}")
            if input_channel[index] > cur_max:
                cur_max = input_channel[index]
        input_channel_24in1.append(cur_max)
    return input_channel_24in1

L_channel_24in1 = simple24in1(L_channel)
R_channel_24in1 = simple24in1(R_channel)

R_24in1_length = len(R_channel_24in1)


L_THREAD = 200
R_THREAD = 200

def boolean_simple(L_channel_24in1, simple_target_alue):
    SLINCE_TIME_THREAD = 1.0
    L_24in1_length = len(L_channel_24in1)
    L_channel_24in1_flag = []
    L_flag_count = 0
    for i in range(0, L_24in1_length, 1):
        if L_channel_24in1[i] < L_THREAD:
            L_flag_count += 1
            L_channel_24in1_flag.append(L_flag_count)
        else:
            L_flag_count = 0
            L_channel_24in1_flag.append(0)

    for i in range(L_24in1_length-1, 0, -1):
        if (L_channel_24in1_flag[i-1] > 0) and (L_channel_24in1_flag[i] > 0):
            if L_channel_24in1_flag[i-1] < L_channel_24in1_flag[i]:
                L_channel_24in1_flag[i-1] = L_channel_24in1_flag[i]

    SIMPLE_COUNT_SUM_THREAD = samplerate/SIMPLE_RATE * SLINCE_TIME_THREAD

    L_bool_flag=[]
    L_MUTE_FLAG_VALUE = simple_target_alue
    for i in range(0, L_24in1_length, 1):
        if L_channel_24in1_flag[i] > SIMPLE_COUNT_SUM_THREAD:
            L_bool_flag.append(L_MUTE_FLAG_VALUE)
        else:
            L_bool_flag.append(0)

    return L_bool_flag


L_bool_flag = boolean_simple(L_channel_24in1, 750)
R_bool_flag = boolean_simple(R_channel_24in1, 750)

L_Flag = True
R_Flag = True
EQ_FLAG = True
ZR_FLAG = True
if Y==length:
    for index in range(0, int(length*samplerate/SIMPLE_RATE), 1):
        sec = index*SIMPLE_RATE/samplerate
        if L_bool_flag[index]==750 and R_bool_flag[index]==0 and L_Flag:
            print(f"# L ahead: {sec} s")
            L_Flag = False
            R_Flag = True
            EQ_FLAG = True
            ZR_FLAG = True
        elif L_bool_flag[index]==750 and R_bool_flag[index]==750 and EQ_FLAG:
            print(f"# EQ: {sec} s")
            L_Flag = True
            R_Flag = True
            EQ_FLAG = False
            ZR_FLAG = True
        elif L_bool_flag[index]==0 and R_bool_flag[index]==750 and R_Flag:
            print(f"# R ahead: {sec} s")
            L_Flag = True
            R_Flag = False
            EQ_FLAG = True
            ZR_FLAG = True
        elif L_bool_flag[index]==0  and R_bool_flag[index]==0 and ZR_FLAG:
            print(f"# both ==0: {sec} s")
            L_Flag = True
            R_Flag = True
            EQ_FLAG = True
            ZR_FLAG = False
        else:
            pass
        #print("ERR!")
        #print(f"{L_bool_flag[index], R_bool_flag[index]}")
#exit(6)




"""
bResult = []
PRINT_FLAG = True
for i in range(0, int(length*samplerate/SIMPLE_RATE)-1, 1):
    if abs(bResult[i])-abs(bResult[i+1]) > 1:
        if (bResult[i]!=0):
            print(f"# {(bResult[i]/samplerate)*SIMPLE_RATE, bResult[i], bResult[i+1]}")
        else:
            pass
            #print("")

"""

time_24in1 = np.linspace(X, Y, int((Y - X) * 48000/SIMPLE_RATE))

# print(f"size of L_channel={len(L_channel)}")
# exit(7)

def print_change_corner_in_plt(val_list, input_plt, shift_value):
    length = len(val_list)
    if length < 1:
        return
    pre_vaul = val_list[0]
    for i in range(1, length):
        if pre_vaul == val_list[i]:
            pass
        else:
            #print(f'{i, pre_vaul}')
            x = i*SIMPLE_RATE/samplerate
            input_plt.plot(x, pre_vaul, 'r*')
            input_plt.text(x, pre_vaul+shift_value, '({:.2f} s, {})'.format(x, pre_vaul+shift_value))
        pre_vaul = val_list[i]


pl.rcParams['figure.figsize']=(192.0, 12.00)
plt.plot(time_24in1, L_channel_24in1, label="Left channel", marker='|', alpha=0.2)
plt.plot(time_24in1, R_channel_24in1, label="Right channel", marker='_', alpha=0.2)
plt.plot(time_24in1, L_bool_flag, label="Left channel no-mute", marker='x', alpha=0.3)
plt.plot(time_24in1, R_bool_flag, label="Right channel no-mute", marker='x', alpha=0.3)
print_change_corner_in_plt(L_bool_flag, plt, 25)
print_change_corner_in_plt(R_bool_flag, plt, -25)
plt.legend()
plt.xlabel("Time [s]")
plt.ylabel("Amplitude")

# plt.show()
fileName_prefix = int(time.time())
plt.savefig(str(fileName_prefix) + '_plot.png')



# for i in range(0, 100000):
#    print(data[i])


# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
