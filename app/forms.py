from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, SelectField
from wtforms.validators import DataRequired, Email, NumberRange

class MetadataGeneratorForm(FlaskForm):
    name = StringField("Classifier Name", validators=[DataRequired()])
    description = TextAreaField("Classifier Description",
                                validators=[DataRequired()])
    ngrams = SelectField("N-grams", choices=["None", 1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
    author_names = StringField("Author Name(s)", validators=[DataRequired()])
    institution = StringField("Institution")
    email = StringField("Correspondence Email", validators=[DataRequired(), Email()])
    max_length = StringField("Max Length", validators=[DataRequired(), NumberRange(min=1, max=2500)])
    submit = SubmitField("Submit")
