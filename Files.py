import os
def exe_finder():
    tbit = []
    sbit = []
    for root, dirs, files in os.walk("C:\Program Files (x86)", topdown=False):
        for name in files:
            if name.endswith(".exe"):
                tbit.append(name)
                
    for root, dirs, files in os.walk("C:\Program Files", topdown=False):
        for name in files:
            if name.endswith(".exe"):
                sbit.append(name)

    return sbit, tbit
