# pip install -r requirements.txt (Do at First)
# python application.py

# For Api Call----> "import requests" and "pip install requests" 

from flask import Flask,render_template,request,redirect
from flask_cors import CORS,cross_origin
import pickle
import requests
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
    image=[]
    index=movies_new[movies_new['title']==movie_name].index[0]
    enumerated_array = list(enumerate(similarity_model[index]))
    
    # Sort the array based on the values in descending order
    sorted_distance = sorted(enumerated_array, key=lambda x: x[1], reverse=True)
    
    # Get the top five distances with their indices
    top_five_elements = sorted_distance[:8]

    for index,value in top_five_elements:
        if f!=0: # In order to eliminate Same Movie.
            result.append(movies_new['title'].iloc[index])
            image.append(fetch_poster(index))
        f=1
    return result,image

"""def fetch_poster(index):
    
    # Finding Movie Id, given movie Index, beacuse for API we need movie ID, As per the Movie "Id" it will fetch Poster not "Index"
    movie_id=movies_new[movies_new.index==index]['id']
    movie_id=np.array(movie_id)[0]
    # API URL from where we will get All Movie Details
    url = "https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(movie_id)
    # Request or Fetch data from this URL 
    data = requests.get(url)
    # converts the response from the API, which is typically in JSON format, into a Python dictionary.
    data = data.json()

    # Extract the poster path from the JSON data
    poster_path = data['poster_path']

    if poster_path:
    # Create the full URL for the movie poster using the base URL
         full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
         return full_path
    else:
        return "https://www.google.com/url?sa=i&url=https%3A%2F%2Fwingandaprayer.live%2F2018%2F07%2F16%2Fits-a-no-photo-day%2F&psig=AOvVaw10q6yemfjbCuUR37MPUEzs&ust=1704570954653000&source=images&cd=vfe&opi=89978449&ved=0CBMQjRxqFwoTCOj5tPuDx4MDFQAAAAAdAAAAABAD"
"""

def fetch_poster(index):
    # Finding Movie Id, given movie Index, because for API we need movie ID,
    # As per the Movie "Id" it will fetch Poster, not "Index"
    movie_id = movies_new[movies_new.index == index]['id']
    movie_id = np.array(movie_id)[0]

    # API URL from where we will get All Movie Details
    url = "https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(movie_id)

    # Request or Fetch data from this URL 
    data = requests.get(url)

    # Check if the request was successful (status code 200)
    if data.status_code == 200:
        # Convert the response from the API, which is typically in JSON format, into a Python dictionary.
        data = data.json()

        # Extract the poster path from the JSON data if available
        poster_path = data.get('poster_path')

        if poster_path:
            # Create the full URL for the movie poster using the base URL
            full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
            return full_path
        else:
            # Handle the case where poster_path is not available
            # Provide a default poster URL or handle it as needed
            return "https://wingandaprayerdotlive.files.wordpress.com/2018/07/no-image-available.jpg?w=167&h=167" 
    else:
        # Handle the error (e.g., print an error message)
        print(f"Error: {data.status_code} - {data.text}")
        # Provide a default poster URL or handle it as needed
        return "https://wingandaprayerdotlive.files.wordpress.com/2018/07/no-image-available.jpg?w=167&h=167"  # Return None or handle the error as needed


@app.route('/',methods=['GET','POST'])
def index():
    # Only For Categorical Column
    all_movie_name=sorted(movies_new['title'].unique())
    

    return render_template('index_poster.html',movie_list=all_movie_name)


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
    result , image=recommend(movie_name)
    
    
    # Solution Find
    return render_template('index_poster.html',movie_list=all_movie_name, movie_name_result=result, movie_poster_url=image, Actual_movie_search=movie_name)


if __name__=='__main__':
    app.run(debug=True)


# https://api.themoviedb.org/3/movie/{movie_id}?api_key=YOUR_API_KEY&language=en-US
# https://api.themoviedb.org/3/movie/65?api_key=6eac47901ec0def9d0012399c9c2bcf8&language=en-US
# copy paste this "api" in google we will get some "json string".
# go to "json viewer" to view the json string properly.
# tmdb image path, go to stack overflow to get full_path details (http://image.tmdb.org/t/p/w500/your_poster_path)