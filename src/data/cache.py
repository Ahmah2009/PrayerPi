import pickle
import os
import csv 

CACHE_FILE = './data/time_tuples.pkl'
SOURCE_FILE = './data/times.csv'

def load_time_tuples():
    if os.path.exists(CACHE_FILE):
        with open(CACHE_FILE, 'rb') as f:
            time_tuples = pickle.load(f)
        return time_tuples
    
    time_tuples = set()
    with open(SOURCE_FILE) as file:
        for row in csv.reader(file):
            if row[0] == "Month" or len(row) < 3:
                continue
            month = int(row[0])
            day = int(row[1])
            for time_str in row[2:]:
                hour, minute = map(int, time_str.split(":"))
                time_tuples.add((month, day, hour, minute))
    
    with open(CACHE_FILE, 'wb') as f:
        pickle.dump(time_tuples, f)
    return time_tuples
