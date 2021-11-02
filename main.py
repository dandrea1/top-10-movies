from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from forms import EditMovie, AddMovie
from movie_selector import MovieSelector, MOVIE_DB_IMAGE_URL

# Initiate App, Bootstrap, Database
app = Flask(__name__)
app.config['SECRET_KEY'] = 'YOUR SECRET'
Bootstrap(app)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///top-ten-movies.db"
# Optional: But it will silence the deprecation warning in the console.
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)

# initiate custom MovieSelector class
movie_selector = MovieSelector()

# Create Movies Table
class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String(250), nullable=False)
    rating = db.Column(db.Float, nullable=True )
    ranking = db.Column(db.Integer, nullable=True )
    review = db.Column(db.String(250), nullable=True )
    img_url = db.Column(db.String(250), nullable=False)


# Create database models
db.create_all()


# Website Path Definitions

@app.route("/")
def home():
    movies = Movie.query.order_by(Movie.rating.desc()).all()
    i = 1
    for movie in movies:
        movie.ranking = i
        i += 1
    db.session.commit()
    movies = Movie.query.order_by(Movie.rating).all()
    return render_template("index.html", movies=movies)


@app.route("/edit", methods=["POST", "GET"])
def edit():
    # Create Form from custom form class
    edit_movie_form = EditMovie()
    # Find movie user wishes to edit
    movie_id = request.args.get('id')
    movie_selected = Movie.query.get(movie_id)
    # Update database if user submits form with updated data
    if edit_movie_form.validate_on_submit():
        movie_selected.rating = float(edit_movie_form.rating.data)
        movie_selected.review = edit_movie_form.review.data
        db.session.commit()
        return redirect(url_for('home'))
    return render_template("edit.html", form=edit_movie_form, movie=movie_selected)


@app.route("/delete", methods=["POST", "GET"])
def delete():
    movie_id = request.args.get('id')
    Movie.query.filter(Movie.id == movie_id).delete()
    db.session.commit()
    return redirect(url_for('home'))


@app.route("/add", methods=["POST", "GET"])
def add():
    # Create Form from custom form class
    add_movie_form = AddMovie()
    if add_movie_form.validate_on_submit():
        movie_title = add_movie_form.title.data
        # use Movie api to search for titles that match with user's input
        movie_choices = movie_selector.search_movie(movie_title)
        # pass movie choices to select template so user can select the right movie.
        return render_template('select.html', movies=movie_choices)

    return render_template('add.html', form=add_movie_form)


@app.route("/find")
def find():
    movie_api_id = request.args.get("id")
    movie_data = movie_selector.get_movie_data(movie_id=movie_api_id)
    new_movie = Movie(
        title=movie_data['original_title'],
        year=movie_data['release_date'].split("-")[0],
        description=movie_data["overview"],
        img_url=f"{MOVIE_DB_IMAGE_URL}{movie_data['poster_path']}"
    )
    db.session.add(new_movie)
    db.session.commit()
    return redirect(url_for("edit", id=new_movie.id))


if __name__ == '__main__':
    app.run(debug=True)
