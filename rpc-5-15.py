# This is a sample Python script.
from flask import Flask, render_template
import pandas as pd
import numpy as np
from sklearn.neighbors import NearestNeighbors

# Press ⇧F10 to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.

#Set up the student that need class recommendation
#Our goal is to predict his preference for other courses that he never took
input =  {"COMP_SCI110": 5,
         "ECON201":4,
         "ECON310":3,
         "EARTH101":6
         }

k = 5

def compare_time(course_info, dept1, num1, dept2, num2):
    c1 = course_info[(course_info["dept/pgm"]==dept1) & (course_info["number"]==str(num1))].reset_index()
    c2 = course_info[(course_info["dept/pgm"]==dept2) & (course_info["number"]==str(num2))].reset_index()
    if(c1["date"].equals(c2["date"]) or
            (c1["date"].equals("MoWeFr") and c2["date"].equals("MoWe")) or
    (c2["date"].equals("MoWeFr") and c1["date"].equals("MoWe"))):
        start = [pd.to_datetime(c1["start time"]), pd.to_datetime(c2["start time"])]
        end = [pd.to_datetime(c1["end time"]), pd.to_datetime(c2["end time"])]
        if(np.max(start)  <= np.min(end)):
            return 0
        return 1
#

def compare_schedule(course_info, recommendation, target):
    for sample in recommendation:

        if(compare_time(course_info, sample[:-3], sample[-3:], target[:-3], target[-3:]) == 0):
            return 0
    return 1



def make_recommendation(course_df, k, x):
    model = NearestNeighbors(n_neighbors=k,metric='euclidean')

    #filter the data, leave only the class that the student has rated
    filtered_df = course_df.loc[:,x.index]

    model.fit(filtered_df)
    distance,result = model.kneighbors([x.array])
    return result


app = Flask(__name__)
@app.route('/')
@app.route('/home')
def predict():
    recommendations = []
    distributions = ['II', 'III']
    course_info = pd.read_csv('Northwestern_course_information_new.csv')

    # print(course_info)
    course_info['ClassName'] = course_info['dept/pgm'].astype(str) + course_info['number'].astype(str)

    print(compare_time(course_info, "ANTHRO", 316, "ANTHRO", 317))
    i = 0
    # class_names = course_subset['ClassName']
    # x = pd.Series(input)
    # results = make_recommendation(course_info, k, x)
    # prediction = course_info.iloc[results[0], 1:].sum() / k
    # print(compare_time(course_info, "COMP_SCI", 101, "COMP_SCI", 110))

    course_df = pd.read_csv('ratings_new.csv')
    # Fill in the empty value with 0
    course_df = course_df.fillna(0)
    x = pd.Series(input)
    results = make_recommendation(course_df, k, x)
    main_prediction = course_df.iloc[results[0], 1:].sum() / k
    main_recommendation = main_prediction[~main_prediction.index.isin(x.index)].sort_values(ascending=False)

    # print(prediction.filter(items=class_names))
    len_courses = 4
    distros = [0, 0, 'II', 'I']
    for j in range(len_courses):
        i = 0
        if distros[j] == 0:
            # no filtering
            predictions = main_recommendation
        else:
            # filtering case
            # filter the courses by the distribution  I want
            course_subset = course_info[course_info['area'] == distros[j]]
            # Clsas names of the distro courses
            class_names = course_subset['ClassName']
            # Filtering our recommendations based on the class names in the distro set
            predictions = main_recommendation.filter(items=class_names)
            print(predictions)
            if len(predictions) > 0:

                while(i < len(predictions) & (compare_schedule(course_info, recommendations, predictions.index[i]) == 0 or predictions.index[i] in recommendations)):
                    i += 1
                recommendations.append(predictions.index[i])
    print("Recommendations:", recommendations)
    return render_template('index.html', result=recommendations)
@app.route('/system', methods=['POST', 'GET'])
def home():
    return render_template("index.html")

# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    app.run(debug=True)
    # print(prediction)


