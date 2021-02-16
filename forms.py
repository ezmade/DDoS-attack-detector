from flask_wtf import FlaskForm
from wtforms import SelectField, FileField
from wtforms.validators import DataRequired

class ClassificationForm(FlaskForm):
    
    input_file = FileField(
        label="Выберите файл",
        validators=[DataRequired('Выберите файл')]
    )

    classification_model = SelectField(
        label='Выберите модель'
    )


class LearningForm(FlaskForm):

    pass 
