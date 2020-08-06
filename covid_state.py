#!/usr/bin/env python

#************************************************************************************************
#************************************************************************************************

import numpy as np
import datetime as dt
import pandas as pd
import os
import subprocess

#import plotly.figure_factory as ff
#from myPlot import Plot

# matplotlib stuff
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

# My external functions
#from covid_state import seven_day
#from covid_state import LinePlot
#from covid_state import BarPlot
#from covid_state import read_data
#from covid_state import plot_data

#************************************************************************************************
#************************************************************************************************
# Calculate seven-day rolling average for raw case and death data
def seven_day(d_list):
    answer = []
    for i in range(0,len(d_list)-6):
        #print(i, i+7, d_list[i:i+7], int(sum(d_list[i:i+7])/7))
        answer.append(int(sum(d_list[i:i+7])/7))
        
    return answer
    
#************************************************************************************************
#************************************************************************************************
# A generic plotting function
#def Plot(ax, data1, data2, legend_props=leg_prop, plot_props=plot_dict):
def LinePlot(ax, data1, data2, xticks, param_dict, font_size=14):

# Format plot
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%m/%d/%Y'))
    #days = [d for d in data1[0::7]]
    ax.set_xticks(xticks)
    #gcf.autofmt_xdate()

# Set font size for text in axes
    for item in ([ax.title, ax.xaxis.label, ax.yaxis.label]):
        item.set_fontsize(font_size+4)

    ax.tick_params(axis='both',labelsize=font_size)
    ax.grid(True, linestyle='--', color='black')
        
# Set grid parameters
    ax.grid(True, linestyle='--', color='black')

# Create plot    
    out = ax.plot(data1, data2, **param_dict)

# Create legend
    ax.legend(fontsize=font_size+4)
    
    return out
#************************************************************************************************
#************************************************************************************************
# A generic plotting function
#def Plot(ax, data1, data2, legend_props=leg_prop, plot_props=plot_dict):
def BarPlot(ax, data1, data2, xticks, param_dict, font_size=14):

# Format plot
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%m/%d/%Y'))
    #days = [d for d in data1[0::7]]
    ax.set_xticks(xticks)
    #gcf.autofmt_xdate()

# Set font size for text in axes
    for item in ([ax.title, ax.xaxis.label, ax.yaxis.label]):
        item.set_fontsize(font_size+4)

    ax.tick_params(axis='both',labelsize=font_size)
    ax.grid(True, linestyle='--', color='black')
        
# Set grid parameters
    ax.grid(True, linestyle='--', color='black')

# Create plot    
    out = ax.bar(data1, data2, **param_dict)

# Create legend
    ax.legend(fontsize=font_size+4)
    
    return out
#**************************************
def read_data(fname, state):
    
    # read from data file
    data=pd.read_csv(fname)
    
    # remove any records with no fips number
    _data=data.dropna(subset=['fips'])
    
    data_=_data[_data['state']==state]
    #print(len(data), len(_data), len(data_))

    # Read data from data frame <- this is cumulative case and death data
    dates = data_['date'].tolist()
    cases = data_['cases'].tolist()
    deaths = data_['deaths'].tolist()
    answer = dict(dates=dates, cases=cases, deaths=deaths)
    
    #print('\nDates')
    #print(dates)
    
    # Convert dates to floats
    x_dates = [dt.datetime.strptime(d,'%Y-%m-%d').date() for d in dates]
    #x_dates = [dt.datetime.strptime(d,'%m/%d/%Y').date() for d in dates]
    answer['x_dates']=x_dates
    
    # Process raw data
    answer['cases_new'] = [cases[i+1]-cases[i] for i in range(0,len(cases)-1)]
    answer['deaths_new'] = [deaths[i+1]-deaths[i] for i in range(0,len(deaths)-1)]
    answer['cases_total'] = cases[len(cases)-1]
    answer['deaths_total'] = deaths[len(deaths)-1]

    #

    #print('\nCases')
    #print(cases)
    
    return answer
    
#************************************************************************************************
#************************************************************************************************
def plot_data(data_dict, state, output_dir, xticks):
    date = str(data_dict['x_dates'][len(data_dict['x_dates'])-1])
    #xticks = [d for d in data_dict['x_dates'][0::7]]

# Create plotting figure and axes *****************************************
    fig = plt.figure(figsize=(16, 24))

# Plot ax1 *****************************************
    ax1 = plt.subplot(311, xlabel='Date', 
                  #ylim=(-10, 10),
                  #xlim=(0,1),
                  ylabel='# of cases and deaths',
                  title='COVID-19: Cases and deaths in {} to date - {}'.format(state, date)
                  )

    LinePlot(ax1, data_dict['x_dates'], data_dict['cases'], xticks,
             {'label':'Total cases to date = {}'.format(data_dict['cases_total']), 'marker':'', 'color':'black'})
    LinePlot(ax1, data_dict['x_dates'], data_dict['deaths'], xticks,
             {'label':'Total deaths to date = {}'.format(data_dict['deaths_total']), 'marker':'', 'color':'red'} )
    
    ax1.set_xlim(left=dt.date(2020,1,21))
    ax1.legend(loc='upper left', fontsize=18)

# Plot ax2 *****************************************
    ax2 = plt.subplot(312, xlabel='Date', 
                  #ylim=(-10, 10),
                  #xlim=(,
                  ylabel='# of cases',
                  title='COVID-19: Cases in {} to date - {}'.format(state, date)
                  )

    LinePlot(ax2, data_dict['x_dates'][7:], seven_day(data_dict['cases_new']), 
             xticks, {'label':'Seven day average', 'marker':'', 'color':'red'})

    BarPlot(ax2, data_dict['x_dates'][1:], data_dict['cases_new'], 
            xticks,{'label':'New daily cases', 'color':'blue'})

    ax2.set_xlim(left=dt.date(2020,1,21))
    ax2.legend(loc='upper left', fontsize=18)

# Plot ax3 *****************************************
    ax3 = plt.subplot(313, xlabel='Date', 
                  #ylim=(-10, 10),
                  #xlim=(,
                  ylabel='# of deaths',
                  title='COVID-19 Deaths in {} to date - {}'.format(state, date)
                  )

    LinePlot(ax3, data_dict['x_dates'][7:], seven_day(data_dict['deaths_new']), 
             xticks,{'label':'Seven day average', 'marker':'', 'color':'red'})

    BarPlot(ax3, data_dict['x_dates'][1:], data_dict['deaths_new'], 
            xticks, {'label':'New daily deaths', 'color':'green'})

    ax3.set_xlim(left=dt.date(2020,1,21))
    ax3.legend(loc='upper left', fontsize=18)

    fig.autofmt_xdate()

# Save figure
    plt.savefig(fname=output_dir+'/{}_cases_and_deaths_{}.png'.format(state,date), bbox_inches='tight')
    plt.close(fig)
    #plt.show()
    return
    
#************************************************************************************************
#************************************************************************************************
def get_states_date_directory_xticks(fp, repo_dir):

    # Update git repo
    print('Updating git repo - /usr/bin/git -C '+repo_dir+ ' pull')
    os.system('/usr/bin/git -C '+ repo_dir + ' pull')
    
    # Get list of states
    print('Getting list of states')
    data=pd.read_csv(fp)
    states = set(data['state'].tolist())
    
    # Call read_data with Washington as state
    data_dict = read_data(fp, 'Washington')
    
    # Get date of last data, x_ticks
    print('Getting last data date and calculating x_ticks')
    last_date = str(data_dict['x_dates'][len(data_dict['x_dates'])-1])
    #xticks = [d for d in data_dict['x_dates'][0::7]]
    xticks = [d for d in data_dict['x_dates'][len(data_dict['x_dates'])-1::-7]]
    #xticks = [d for d in x_dates[len(x_dates)-1::-7]]

    # Make directory for plots
    print('Make new folder for plots')
    output_dir = './0Plots_'+last_date
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
            
    return states, last_date, output_dir, xticks
    
#************************************************************************************************
#************************************************************************************************
# Check if this module is called from the command line

if __name__ == '__main__':

# File path of state data cvs file
#data_dir = '/Users/dpcook/Desktop/COVID/Data/'
    repo_dir = '../NYT-covid-19-data/'
    fp = repo_dir + '/us-states.csv'

# Build list of states, date of most recent 
    states, last_date, output_dir, xticks = get_states_date_directory_xticks(fp, repo_dir)

#print(states)
    print('Last date = {}'.format(last_date))
    print('Output folder = {}'.format(output_dir))
    print(xticks)

#state = 'Michigan'
#data_dict = read_data(filename, state)
#plot_data(data_dict, state, output_dir, xticks)

    for state in states:
        print(' {} '.format(state), sep='.', end='', flush=True)
        data_dict = read_data(fp, state)
        plot_data(data_dict, state, output_dir, xticks)
    
    print('Done')