import numpy as np
from numpy import random as rd
import sys
import time


# 1.generate float32 data
data_count = 50000
R = rd.randn(data_count).astype(np.float32)
print("float32 data R:\n", R)
print("size of R:", sys.getsizeof(R), "bytes", "\n")

# 2.calculate S and Z
R_max = np.max(R)
R_min = np.min(R)
Q_max = 255
Q_min = 0
S = (R_max - R_min) / (Q_max - Q_min)
Z = Q_max - R_max / S
print("R_max:%.5f, R_min:%.5f, Q_max:%d, Q_min:%d" % (R_max, R_min, Q_max, Q_min))
print("S:%.5f, Z:%.5f" % (S, Z), "\n")

# 3.quantization
Q = np.round(R / S + Z).astype(np.uint8)
print("int8 data Q:\n", Q)
print("size of Q:", sys.getsizeof(Q), "bytes", "\n")


# 4.warm up
warm_up_times = 100
param = np.array(2).astype(np.float32)
for i in range(warm_up_times):
    R / param


param = np.array(2).astype(np.uint8)
for i in range(warm_up_times):
    Q / param


# 5.R calculate speed
times = 100000
print("do %d times R / 2......" % (times,))
start_time = time.time()
param = np.array(2).astype(np.float32)
for i in range(times):
    result_r = R / param
end_time = time.time()
print("time cost of %d times R / 2:%f second" % (times, end_time - start_time,), "\n")


# 6.Q calculate speed
print("do %d times Q // 2......" % (times,))
start_time = time.time()
param = np.array(2).astype(np.uint8)
for i in range(times):
    result_q = Q // param
end_time = time.time()
print("time cost of %d times Q // 2:%f second" % (times, end_time - start_time,), "\n")


# 7.recover Q data to R data
print("R / 2:\n", result_r, "\n")
print("Q // 2-->R / 2:\n", (result_q - Z / param) * S)