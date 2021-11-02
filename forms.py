from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

# Create form for users to edit their movie rating and review.
class EditMovie(FlaskForm):
    rating = StringField('Your rating out of 10, eg. 7.5', validators=[DataRequired()])
    review = StringField('Your Review', validators=[DataRequired()])
    submit = SubmitField('Done')

# Create form for users to add a new movie to the list.
class AddMovie(FlaskForm):
    title = StringField('Movie Title')
    submit = SubmitField('Add Movie', validators=[DataRequired()])
