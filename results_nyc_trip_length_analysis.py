import pickle
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.pyplot import cm
import matplotlib.gridspec as gridspec

trip_length_bins = np.array(list(range(0,40,1))) +0.5
trip_v_bins_kmh = np.array(list(range(0,100,5))) +2.5
trip_start_hour_bins = np.array(list(range(0,24,1)))+0.5
trip_dur_seconds_bins = np.array(list(range(0,60*60*2,60*10)))+0.5*(60*10) #i.e every ten mins bins...

trip_dur_minutes_bins = trip_dur_seconds_bins/60


path_to_results_file = '/home/toshiba/Dropbox/RandomDataResults/'
results_filename = 'nyc_2017_taxi_trip_data_analysis_results.pickle'


with open((path_to_results_file+'nyc_2017_taxi_trip_data_analysis_results.pickle'), 'rb') as handle:
    trip_data_results_dict = pickle.load(handle)


num_months = 12

graph_colour=iter(cm.rainbow(np.linspace(0,1,num_months)))
#for i in range(n):
#   c=next(graph_colour)
#https://stackoverflow.com/questions/4971269/how-to-pick-a-new-color-for-each-plotted-line-within-a-figure-in-matplotlib

grid_spec = gridspec.GridSpec(4,1)
fig = plt.figure()

ax1 = fig.add_subplot(grid_spec[0])
ax2 = fig.add_subplot(grid_spec[1])
ax3 = fig.add_subplot(grid_spec[2])
ax4 = fig.add_subplot(grid_spec[3])

for key, values in trip_data_results_dict.items():

    line_plot_colour = next(graph_colour)     

    ax1.plot(trip_length_bins[0:-1], values['len_freq'], c=line_plot_colour)
    ax1.set_xlabel('Trip Length/[km]')
    ax1.set_ylabel('Frequency Count')
    ax1.set_title('2017 NYC Taxi Trip Overview')
    
    ax2.plot(trip_v_bins_kmh[0:-1], values['mean_v'], c=line_plot_colour)
    ax2.set_xlabel('Trip Mean Velocity/[km/h]')
    ax2.set_ylabel('Frequency Count')

    ax3.plot(trip_start_hour_bins[0:-1], values['start_hrs_freq'],c=line_plot_colour)
    ax3.set_xlabel('Trip Start Time/[Hrs]')
    ax3.set_ylabel('Frequency Count')

#    ax4.plot(trip_dur_seconds_bins[0:-1], values['dur_s'], c=line_plot_colour)
#    ax4.set_xlabel('Trip Duration/[s]')
#    ax4.set_ylabel('Frequency Count')
    trip_dur_mins = values['dur_s']/60
    ax4.plot(trip_dur_minutes_bins[0:-1], trip_dur_mins, c=line_plot_colour)
    ax4.set_xlabel('Trip Duration/[Minutes]')
    ax4.set_ylabel('Frequency Count')

plt.subplots_adjust(hspace=0.4)
plt.show()
