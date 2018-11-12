"""
NYC trip data trip length/times distribution anaylsis...

"""


import numpy as np
import pickle
import datetime, time
#import matplotlib.pyplot as plt


#c207
#path_to_file = "/home/user/Downloads/nyc_taxi_trip_data/"


#C255
path_to_file = "/home/toshiba/Downloads/NYC_taxi_trip_datasets_2017/"

"""
file_name = "yellow_tripdata_2017-03.csv"
#file_name = "mini_sample_nyc_taxi_trip_data.csv"


#VendorID,tpep_pickup_datetime,tpep_dropoff_datetime,passenger_count,trip_distance,RatecodeID,store_and_fwd_flag,PULocationID,DOLocationID,payment_type,fare_amount,extra,mta_tax,tip_amount,tolls_amount,improvement_surcharge,total_amount

trip_distance_miles = np.loadtxt(path_to_file+file_name, delimiter=',',usecols=(4), skiprows=1)
trip_distance_metres = trip_distance_miles*1609.344


trip_start_times_str_array = np.loadtxt(path_to_file+file_name, delimiter=',',usecols=(1),dtype=str, skiprows=1)
trip_end_times_str_array = np.loadtxt(path_to_file+file_name, delimiter=',', usecols=(2), dtype=str, skiprows=1)

"""

def LoadTaxiTripData(file_path):

    trip_distance_miles = np.loadtxt(file_path, delimiter=',',usecols=(4), skiprows=1)
    trip_distance_km = trip_distance_miles*1.609344

    trip_start_times_str_array = np.loadtxt(file_path, delimiter=',',usecols=(1),dtype=str, skiprows=1)
    trip_end_times_str_array = np.loadtxt(file_path, delimiter=',', usecols=(2), dtype=str, skiprows=1)

    taxi_trip_data_dict = {'start_t':trip_start_times_str_array,'end_t':trip_end_times_str_array ,'dist_km':trip_distance_km}

    return taxi_trip_data_dict


#(datetime.datetime(*time.strptime(s, "%Y-%m-%d %H:%M:%S")[:6]))



#trip_start_times_datetime_list = []

def StringToDatetimeConv(date_string_array):
    """ note format as follows: "%Y-%m-%d %H:%M:%S" 
        output will be datetime object... 
        lists throughout... """
    datetime_list = [] #np.zeros_like(date_string_array)
    for i in range(len(date_string_array)):
        datetime_list.append((datetime.datetime(*time.strptime(date_string_array[i], "%Y-%m-%d %H:%M:%S")[:6])))

    return datetime_list



#trip_start_times_datetime_list =  StringToDatetimeConv(trip_start_times_str_array)

#trip_end_times_datetime_list = StringToDatetimeConv(trip_end_times_str_array)


def TripDurationSeconds(trip_start_times, trip_end_times):
    """ inputs are lits, with datetime objects... 
        outputs seconds (i.e. duration of trip...)
        """

    trip_duration_seconds = []
    if len(trip_start_times) == len(trip_end_times):

        for i in range(len(trip_start_times)):
            trip_duration_seconds.append(int(datetime.timedelta.total_seconds(trip_end_times[i] - trip_start_times[i])))

    return trip_duration_seconds

#trip_duration_seconds_list = TripDurationSeconds(trip_start_times_datetime_list, trip_end_times_datetime_list)

def TripDayTimeStartHour(trip_start_times):
    trip_start_hour = []
    for i in range(len(trip_start_times)):
        trip_start_hour.append(trip_start_times[i].hour)

    return trip_start_hour 


"""

trip_length_bins = list(range(0,40000,500))



hist, bin_edges = np.histogram(trip_distance_metres, trip_length_bins)


# trip distance histogram
plt.hist(trip_distance_metres, bins = trip_length_bins)
plt.title('NYC, Oct2017, Yellow Taxi Trip Length histogram')
plt.xlabel('Distance/[m]')
plt.show()

# Trip starting hour histogram...
trip_start_time_hour = TripDayTimeStartHour(trip_start_times_datetime_list)
trip_start_hour_bins = list(range(0,24,1))
plt.hist(trip_start_time_hour, bins = trip_start_hour_bins)
plt.title('NYC, Oct2017, Yellow Taxi Trip Start Hour Histogram')
plt.xlabel('Start Hour/[hrs]')
plt.show()

# Trip mean velocity histogram
trip_mean_v_ms = trip_distance_metres/np.array(trip_duration_seconds_list)
trip_mean_v_kmh = trip_mean_v_ms*(3600/1000)
trip_v_bins_kmh = list(range(0,100,5))
plt.hist(trip_mean_v_kmh, bins = trip_v_bins_kmh)
plt.title('NYC, Oct2017, Yellow Taxi Trip Mean Velocity Histogram')
plt.xlabel('Mean Velocity/[km/h]')
plt.show()

"""


# for processing an entire year of this phucking trip data...
import glob

taxi_trip_datasets_list = glob.glob(path_to_file+'*.csv')

year_results = dict()

trip_length_bins = list(range(0,40,1))
trip_v_bins_kmh = list(range(0,100,5))
trip_start_hour_bins = list(range(0,24,1))
trip_dur_seconds_bins = list(range(0,60*60*2,60*10)) #i.e every ten mins bins...

for taxi_dataset in taxi_trip_datasets_list:

    month_key = taxi_dataset[-6:-4]
    print('current working month: %s' % month_key)

    taxi_month_dataset_dict = LoadTaxiTripData(taxi_dataset)

    trip_start_times_datetime_list =  StringToDatetimeConv(taxi_month_dataset_dict['start_t'])

    trip_end_times_datetime_list = StringToDatetimeConv(taxi_month_dataset_dict['end_t'])

    trip_start_hours = TripDayTimeStartHour(trip_start_times_datetime_list)

    trip_dur_seconds = TripDurationSeconds(trip_start_times_datetime_list,trip_end_times_datetime_list)

    trip_dur_hours_array = np.array(trip_dur_seconds)/(60*60)

# may need to consider removing zeros and any repeated lines here... 
    trip_mean_v_kmh = taxi_month_dataset_dict['dist_km']/trip_dur_hours_array

    trip_dur_s_hist, bin_edges = np.histogram(trip_dur_seconds, trip_dur_seconds_bins)

    trip_len_hist, bin_edges = np.histogram(taxi_month_dataset_dict['dist_km'], trip_length_bins)

    trip_mean_v_hist, bin_edges = np.histogram(trip_mean_v_kmh, trip_v_bins_kmh)

    trip_start_hrs_hist, bin_edges = np.histogram(trip_start_hours, trip_start_hour_bins)


    year_results[month_key] = {'len_freq':trip_len_hist,'mean_v':trip_mean_v_hist,'start_hrs_freq':trip_start_hrs_hist,'dur_s':trip_dur_s_hist}


    del taxi_month_dataset_dict


#pickle save results-analysis...
path_to_results_file = '/home/toshiba/Dropbox/RandomDataResults/'

with open((path_to_results_file+'nyc_2017_taxi_trip_data_analysis_results.pickle'), 'wb') as handle:
    pickle.dump(year_results, handle, protocol=pickle.HIGHEST_PROTOCOL)





