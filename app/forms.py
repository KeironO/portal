from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, SelectField, IntegerField
from wtforms.validators import DataRequired, Email, NumberRange, Length


class MetadataGeneratorForm(FlaskForm):
    uid = StringField("Unique Identifier", validators=[DataRequired(), Length(min=5,
                                                                              max=10)])
    name = StringField("Classifier Name", validators=[DataRequired()])
    description = TextAreaField("Classifier Description",
                                validators=[DataRequired()])
    ngrams = SelectField("N-grams", choices=[["None", "0"], ["1", "1"], ["2", "2"], ["3", "3"],
                                             ["4", "4"], ["5", "5"], ["6", "6"], ["7", "7"], ["8", "8"],
                                             ["9", "9"], ["10", "10"]])
    author_name = StringField("Author Name", validators=[DataRequired()])
    institution = StringField("Institution")
    email = StringField("Correspondence Email", validators=[DataRequired(), Email()])
    max_length = IntegerField("Max Length", validators=[DataRequired(), NumberRange(min=1, max=2500)])
    submit = SubmitField("Submit")
