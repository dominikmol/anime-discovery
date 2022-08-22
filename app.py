#   importing required packages
from flask import Flask, render_template, request
from jikanpy import Jikan

#   function replacing values where score is set to None with 0
def replace_none(dict):
    for key, value in dict.items():
        if key == 'score':
            if value is None:
                dict[key] = 0

#   function for filtering animes with score below our requirements
def score_filter(dict, score):
    for key, value in dict.items():
        if key == 'score':
            if value >= score:
                return True
            else:
                return False

app = Flask(__name__)

app.config["TEMPLATES_AUTO_RELOAD"] = True

#   creating list of tags/genres
genres_list = []
with open('./genres_list.txt', 'r') as f:
    for line in f:
        genres_list.append(line.strip())

@app.route('/', methods=["GET", "POST"])
def index():
    #   checking if request method is equal to POST
    if request.method == "POST":
        #   declaring valablles and getting data from form
        year = int(request.form['year'])
        season = request.form['season']
        anime_score = float(request.form['minScore'])
        black_list = request.form.getlist('blacklist[]')
        tags = request.form.getlist('tags[]')
        fields_key_list = ['url', 'title', 'image_url', 'synopsis', 'episodes', 'genres', 'themes', 'demographics', 'score', 'source', 'airing_start']
        genre_key_list = ['genres', 'themes', 'demographics']
        jikan = Jikan()
        anime_list = []
        blacklisted = []
        hight_score = 0
        current_score = 0
        best_anime = []

        #   collecting database of anime based on our requiremtns
        anime_database = jikan.season(year=year, season=season)['anime']
        
        #   fixing database, filtering data
        for anime in anime_database:
            replace_none(anime)
            # creating fields for anime list
            anime = {key: anime[key] for key in fields_key_list}

            #   adding tags/genres for correct fields
            for key in genre_key_list:
                if key in anime.keys():
                    genre_names = []
                for anime_info in anime[key]:
                    genre_names.append(anime_info['name'])
                anime[key] = genre_names
            if score_filter(anime, anime_score):
                #   adding anime to list
                anime_list.append(anime)

        #   sorting anime by score from highest to lowest, without anime below unwanted score 
        anime_list.sort(key=lambda x: x['score'], reverse=True)

        #   creating list of blacklisted anime
        for anime in anime_list:
            for key in genre_key_list:
                for blacklist_key in black_list:
                    if blacklist_key in anime[key]:
                        if anime not in blacklisted:
                            blacklisted.append(anime)
        
        #   delelting anime from list that has tags/genres from a blacklist
        for anime in blacklisted:
            anime_list.remove(anime)

        #   adding points and searching for the most fitted anime
        for anime in anime_list:
            for key in genre_key_list:
                for tag in tags:
                    if tag in anime[key]:
                        current_score += 1
                        if current_score > hight_score:
                            hight_score = current_score
                            best_anime = anime
            current_score = 0
        
        #   correcting time format
        anime['airing_start'] = anime['airing_start'][0:10]
        
        return render_template('anime.html', anime=best_anime)
    else:
        return render_template('index.html', blacklist=genres_list, tags=genres_list)

if __name__ == "__main__":
    app.run(debug=True)