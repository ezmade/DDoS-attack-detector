from flask_wtf import FlaskForm
from wtforms import SelectField, SubmitField, Label, FileField
from wtforms.validators import DataRequired

class ClassificationForm(FlaskForm):
    
    input_file = FileField(
        label="Выберите файл",
        validators=[DataRequired('Выберите файл')]
    )

    classification_model = SelectField(
        label='Выберите модель'
    )

    result = Label(field_id=1, text="Результат: ")

