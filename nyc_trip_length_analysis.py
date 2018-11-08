"""
NYC trip data trip length/times distribution anaylsis...

"""


import numpy as np
import pickle
import datetime, time
import matplotlib.pyplot as plt



path_to_file = "/home/user/Downloads/nyc_taxi_trip_data/"
file_name = "yellow_tripdata_2017-10.csv"
#file_name = "mini_sample_nyc_taxi_trip_data.csv"


#VendorID,tpep_pickup_datetime,tpep_dropoff_datetime,passenger_count,trip_distance,RatecodeID,store_and_fwd_flag,PULocationID,DOLocationID,payment_type,fare_amount,extra,mta_tax,tip_amount,tolls_amount,improvement_surcharge,total_amount

trip_distance_miles = np.loadtxt(path_to_file+file_name, delimiter=',',usecols=(4), skiprows=1)
trip_distance_metres = trip_distance_miles*1609.344


trip_start_times_str_array = np.loadtxt(path_to_file+file_name, delimiter=',',usecols=(1),dtype=str, skiprows=1)
trip_end_times_str_array = np.loadtxt(path_to_file+file_name, delimiter=',', usecols=(2), dtype=str, skiprows=1)


#(datetime.datetime(*time.strptime(s, "%Y-%m-%d %H:%M:%S")[:6]))



trip_start_times_datetime_list = []

def StringToDatetimeConv(date_string_array):
    """ note format as follows: "%Y-%m-%d %H:%M:%S" 
        output will be datetime object... 
        lists throughout... """
    datetime_list = [] #np.zeros_like(date_string_array)
    for i in range(len(date_string_array)):
        datetime_list.append((datetime.datetime(*time.strptime(date_string_array[i], "%Y-%m-%d %H:%M:%S")[:6])))

    return datetime_list



trip_start_times_datetime_list =  StringToDatetimeConv(trip_start_times_str_array)

trip_end_times_datetime_list = StringToDatetimeConv(trip_end_times_str_array)


def TripDurationSeconds(trip_start_times, trip_end_times):
    """ inputs are lits, with datetime objects... 
        outputs seconds (i.e. duration of trip...)
        """

    trip_duration_seconds = []
    if len(trip_start_times) == len(trip_end_times):

        for i in range(len(trip_start_times)):
            trip_duration_seconds.append(int(datetime.timedelta.total_seconds(trip_end_times[i] - trip_start_times[i])))

    return trip_duration_seconds

trip_duration_seconds_list = TripDurationSeconds(trip_start_times_datetime_list, trip_end_times_datetime_list)

def TripDayTimeStartHour(trip_start_times):
    trip_start_hour = []
    for i in range(len(trip_start_times)):
        trip_start_hour.append(trip_start_times[i].hour)

    return trip_start_hour 




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











