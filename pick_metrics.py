#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Pick system data on the PC.
Run it by command: python pick_metrics.py 30
Where arg 30 means minutes, when script picks data about HDD space, CPU, RAM.
Data will be saved in files: metrics.csv, system_data.txt
"""
import psutil
import time
import platform
import shutil
import csv
from datetime import datetime
import sys
import os

# delete metrics.csv in current directory
catalogue_files = os.listdir(os.getcwd())
if "metrics.csv" in catalogue_files:
    os.remove("metrics.csv")

# script time limit
start = time.time()
time_limit = 1

try:
    time_limit = sys.argv[1]
except IndexError:
    print("Please, rerun the script with time limit key (integer), in minutes!")
    quit()

# convert time limit to secs
time_limit = int(time_limit) * 60

print("="*20, " System data ", "="*20)
uname = platform.uname()
cpufreq = psutil.cpu_freq()
total, used, free = shutil.disk_usage("/")
print("System: {}".format(uname.system))
print("Node Name: {}".format(uname.node))
print("Release: {}".format(uname.release))
print("Version: {}".format(uname.version))
print("Machine: {}".format(uname.machine))
print("System type:", platform.architecture()[0])
print("Processor: {}".format(uname.processor), end="\n\n")
print("Total RAM, Gb:", round(psutil.virtual_memory().total / 1024 / 1024 / 1024, 2), end="\n\n")
print("CPU physical cores:", psutil.cpu_count(logical=False))
print("CPU total cores:", psutil.cpu_count(logical=True))
print("CPU max frequency: {:.2f}Mhz".format(cpufreq.max), end="\n\n")
print("Total hard disk space: %d Gb" % (total // (2**30)))
print("Used hard disk space: %d Gb" % (used // (2**30)))
print("Free hard disk space: %d Gb" % (free // (2**30)))
print("="*50, end="\n\n")

# save System data to system_data.txt
with open("system_data.txt", "w") as data_file:
    data_file.write("="*40 + " System data " + "="*40)
    data_file.write("\nSystem: {}".format(uname.system))
    data_file.write("\nNode Name: {}".format(uname.node))
    data_file.write("\nRelease: {}".format(uname.release))
    data_file.write("\nVersion: {}".format(uname.version))
    data_file.write("\nMachine: {}".format(uname.machine))
    data_file.write("\nSystem type: {}".format(platform.architecture()[0]))
    data_file.write("\nProcessor: {}\n".format(uname.processor))
    data_file.write("\nTotal RAM, Gb: {}\n".format(round(psutil.virtual_memory().total / 1024 / 1024 / 1024, 2)))
    data_file.write("\nCPU physical cores: {}".format(psutil.cpu_count(logical=False)))
    data_file.write("\nCPU total cores: {}".format(psutil.cpu_count(logical=True)))
    data_file.write("\nCPU max frequency: {:.2f} Mhz\n".format(cpufreq.max))
    data_file.write("\nTotal hard disk space: %d Gb" % (total // (2 ** 30)))
    data_file.write("\nUsed hard disk space: %d Gb" % (used // (2 ** 30)))
    data_file.write("\nFree hard disk space: %d Gb\n" % (free // (2 ** 30)))
    data_file.write("=" * 95)

# initialize metrics.csv
first_row = ["Used CPU %", "Used RAM Gb", "Used RAM %", "Free HDD Gb", "timestamp"]
with open('metrics.csv', 'w', newline='') as csv_file:
    writer = csv.writer(csv_file, delimiter=";", quoting=csv.QUOTE_MINIMAL)
    writer.writerow(first_row)

while True:
    # save data for: cpu, mem, hdd
    used_cpu = psutil.cpu_percent()

    mem_data = psutil.virtual_memory()
    used_mem_gb = round(mem_data.used / 1024 / 1024 / 1024, 2)
    used_mem_percent = mem_data.percent

    total, used, free = shutil.disk_usage("/")
    free_hdd = free // (2 ** 30)

    # print data for: cpu, mem, hdd
    print("Used CPU, %", used_cpu)
    print("Used RAM, Gb:", used_mem_gb, "({}%)".format(used_mem_percent))
    # print("Free RAM, Gb:", round(psutil.virtual_memory().free / 1024 / 1024 / 1024, 2), "({}%)".format(psutil.virtual_memory().available * 100 // psutil.virtual_memory().total))
    print("Free hard disk space: %d Gb\n\n" % free_hdd)

    # save current time in format: dd/mm/YY H:M
    now = datetime.now()
    dt_string = now.strftime("%H:%M")

    # calculate absolute time
    end = time.time()
    # script_time = int(end - start)
    # script_time = time.strftime('%H:%M', time.gmtime(script_time))

    # save data in metrics.csv
    another_row = [used_cpu, used_mem_gb, used_mem_percent, free_hdd, dt_string]
    with open('metrics.csv', 'a', newline='') as csv_file:
        # csv_file.write("")
        writer = csv.writer(csv_file, delimiter=";", quoting=csv.QUOTE_MINIMAL)
        writer.writerow(another_row)

    # quit after time limit
    if end - start > time_limit:
        quit()

    time.sleep(5)
