# This is a sample Python script.
import pandas as pd
import numpy as np
from sklearn.neighbors import NearestNeighbors

# Press ⇧F10 to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.

#Set up the student that need class recommendation
#Our goal is to predict his preference for other courses that he never took


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    course_info = pd.read_csv('Northwestern_course_information.csv')
    size = np.array((20,50,100,200))
    time_interval = np.array((("MoWeFr","08:00", "08:50"),
                              ("MoWeFr","09:00","09:50"),
                              ("MoWeFr","10:00","10:50"),
                              ("MoWeFr","11:00","11:50"),
                              ("MoWeFr","12:00","12:50"),
                              ("MoWeFr","13:00","13:50"),
                              ("MoWeFr","14:00","14:50"),
                              ("MoWeFr","15:00","15:50"),
                              ("MoWeFr","16:00","16:50"),
                              ("TuTh", "08:00", "09:20"),
                              ("TuTh", "09:00", "10:20"),
                              ("TuTh", "10:00", "11:20"),
                              ("TuTh", "11:00", "12:20"),
                              ("TuTh", "12:00", "13:20"),
                              ("TuTh", "13:00", "14:20"),
                              ("TuTh", "14:00", "15:20"),
                              ("TuTh", "15:00", "14:20"),
                              ("TuTh", "16:00", "17:20"),
                              ("MoWe", "08:00", "09:20"),
                              ("MoWe", "09:00", "10:20"),
                              ("MoWe", "10:00", "11:20"),
                              ("MoWe", "11:00", "12:20"),
                              ("MoWe", "12:00", "13:20"),
                              ("MoWe", "13:00", "14:20"),
                              ("MoWe", "14:00", "15:20"),
                              ("MoWe", "15:00", "14:20"),
                              ("MoWe", "16:00", "17:20")
                              ))

    course_info["class size"] = np.random.choice(size, size=len(course_info))
    time_matrix = time_interval[np.random.choice(np.arange(0,len(time_interval)), size=len(course_info))].T
    course_info["date"],course_info["start time"],course_info["end time"] = time_matrix
    print(course_info.head())
    course_info.to_csv('Northwestern_course_information_new.csv')




    course_df = pd.read_csv('ratings.csv')
    rate = np.array((np.nan,np.nan,np.nan,np.nan,np.nan,np.nan,np.nan,np.nan,np.nan,np.nan,np.nan,np.nan,np.nan,np.nan,np.nan,np.nan,np.nan,np.nan,np.nan,np.nan,np.nan,np.nan,np.nan,1,2,3,3,3,4,4,4,4,4,5,5,5,5,5,6,6,6,6,6))
    new_row = np.random.choice(rate, (10,len(course_df.columns)-1))
    print(new_row)
    arr = np.arange(34,44).reshape(10,1)
    added=np.concatenate((arr, new_row), axis=1)
    added_df = pd.DataFrame(added,columns=course_df.columns)
    print(added_df)
    course_df = course_df.append(added_df)
    class_list = ["COMP_SCI349","COMP_SCI110","COMP_SCI348","COMP_SCI336","ECON301","ECON201","ECON339","ECON310","COMP_SCI150","ASTRON103","EARTH101","ANTHRO213","COG SCI110", "SOCIOL232", "SOCIOL277", "PSYCH336"]
    for c in class_list:
        course_df[c] = np.random.choice(rate, size=len(course_df))
    print(course_df)
    course_df.to_csv('ratings_new.csv',index=False)
