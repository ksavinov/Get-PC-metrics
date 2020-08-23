#!/usr/bin/python3
# -*- coding: utf-8 -*-
""" Module that builds graphics of using RAM, CPU """
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime


def build_grahipcs():
    df = pd.read_csv('metrics.csv', sep=';')
    
    # convert timestamp
    df["timestamp"] = pd.to_datetime(df["timestamp"], format='%H:%M')


    # plot percents used by CPU, RAM
    ax1 = plt.subplot()
    ax1.plot_date(df['timestamp'], df['Used CPU %'], '-', label='Used CPU %')
    ax1.plot_date(df['timestamp'], df['Used RAM %'], '-', label='Used RAM %')
    ax1.legend()
    # plot volume
    ax2 = plt.subplot()

    # issue: https://github.com/matplotlib/matplotlib/issues/9610
    df.set_index("timestamp", inplace=True)
    df.index.to_pydatetime()

    # current YYYY MM DD in saved screenshot file
    now = datetime.now()
    dt_string = now.strftime("%Y%m%d")
    # save report
    plt.savefig('cpu_mem_%s.png' % dt_string)


if __name__ == "__main__":
    build_grahipcs()
