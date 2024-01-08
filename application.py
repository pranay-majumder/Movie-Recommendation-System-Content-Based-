# pip install -r requirements.txt (Do at First)
# python application.py

# For Api Call----> "import requests" and "pip install requests" 

from flask import Flask,render_template,request,redirect
from flask_cors import CORS,cross_origin
import pickle
import pandas as pd
import numpy as np

application=Flask(__name__)
app=application

# This Line Important for CSS File Loading and Background Image Loading
app.static_folder = 'static'

cors=CORS(app)

similarity_model=pickle.load(open('Model/similarity.pkl','rb'))

# our Actual Data Frame
movies_new=pd.read_csv('Dataset/movies_new.csv')


def recommend(movie_name):
    # Get an Index of the Movie
    f=0
    result=[]
    index=movies_new[movies_new['title']==movie_name].index[0]
    enumerated_array = list(enumerate(similarity_model[index]))
    
    # Sort the array based on the values in descending order
    sorted_distance = sorted(enumerated_array, key=lambda x: x[1], reverse=True)
    
    # Get the top five distances with their indices
    top_five_elements = sorted_distance[:6]

    for index,value in top_five_elements:
        if f!=0: # In order to eliminate Same Movie.
            result.append(movies_new['title'].iloc[index])
        f=1
    return result


@app.route('/',methods=['GET','POST'])
def index():
    # Only For Categorical Column
    all_movie_name=sorted(movies_new['title'].unique())
    

    return render_template('index.html',movie_list=all_movie_name)


@app.route('/predictdata',methods=['GET','POST'])
@cross_origin()
def predict_movie():
    
    all_movie_name=sorted(movies_new['title'].unique())
    
    # request.form.get(' "Name" of The field given in the Form')
    # Name Should be Exactly Match
    movie_name=request.form.get('movie')

    # Check for null or empty values, If any null value is encountered then again we redirect to same page, in order
    # to prevent the submission of the form.
    if None in [movie_name] or "" in [movie_name]:
        # Redirect to an same page if any field is empty
        return redirect('http://127.0.0.1:5000/')
    
    # Call Recommend Function
    result=recommend(movie_name)
    
    
    # Solution Find
    return render_template('index.html',movie_list=all_movie_name, movie_name_result=result)


if __name__=='__main__':
    app.run(debug=True)

