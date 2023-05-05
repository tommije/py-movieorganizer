#!/usr/bin/env python3

import csv
import requests
from urllib.parse import urlencode

# OMDb API Key
api_key = "YOUR_API_KEY"

# Read listed movies from a .txt file (title, version)
def read_movies_from_file(filename):
    movies = []
    with open(filename, "r", encoding="utf-8") as file:
        for line in file:
            title, version = line.strip().split(", ")
            movies.append((title, version))
    return movies

# Read movie information from a .txt file
movies = read_movies_from_file("movies.txt")

# Get IMDb and Rotten Tomatoes ratings, release year, genre, and director
def get_movie_info(title):
    print(f"Fetching movie info for {title}...")
    params = {
        't': title,
        'apikey': api_key,
    }
    url = f"http://www.omdbapi.com/?{urlencode(params)}"
    response = requests.get(url)
    print(f"Response status code: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"Movie data: {data}")
        imdb_rating = data.get("imdbRating")
        rt_rating = None
        for rating in data.get("Ratings", []):
            if rating["Source"] == "Rotten Tomatoes":
                rt_rating = rating["Value"]
                break
        release_year = data.get("Year")
        genre = data.get("Genre")
        director = data.get("Director")
        return imdb_rating, rt_rating, release_year, genre, director
    return None, None, None, None, None

# Create a list of tuples (movie title, version, IMDb rating, Rotten Tomatoes rating, release year, genre, director)
movies_with_info = []
for movie, version in movies:
    imdb_rating, rt_rating, release_year, genre, director = get_movie_info(movie)
    if imdb_rating or rt_rating:
        movies_with_info.append((movie, version, imdb_rating, rt_rating, release_year, genre, director))

# Sort list alphabetically
sorted_movies_with_info = sorted(movies_with_info, key=lambda x: x[0])

# Write the sorted list to a CSV file
with open("movies_with_info.csv", mode="w", newline="", encoding="utf-8") as csvfile:
    csv_writer = csv.writer(csvfile)
    headers = ["Movie Title", "Version", "IMDb Rating", "Rotten Tomatoes Rating", "Release Year", "Genre", "Director"]
    csv_writer.writerow(headers)
    
    for movie, version, imdb_rating, rt_rating, release_year, genre, director in sorted_movies_with_info:
        csv_writer.writerow([movie, version, imdb_rating, rt_rating, release_year, genre, director])

print("Movies with info have been written to 'movies_with_info.csv'")