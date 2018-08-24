from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, SelectField
from wtforms.validators import DataRequired, Email

class MetadataGeneratorForm(FlaskForm):
    name = StringField("Classifier Name", validators=[DataRequired()])
    description = TextAreaField("Classifier Description",
                                validators=[DataRequired()])
    ngrams = SelectField("N-grams")
    author_names = StringField("Author Name(s)", validators=[DataRequired()])
    email = StringField("Correspondence Email", validators=[DataRequired(), Email()])
    submit = SubmitField("Submit")
