from flask_wtf import FlaskForm
from wtforms import SelectField, FileField, SubmitField
from wtforms.validators import DataRequired

class ClassificationForm(FlaskForm):

    classification_model = SelectField(
        label='Выберите модель для классификации'
    )

    input_file = FileField(
        label='Выберите файл для классификации', 
        validators=[DataRequired('Необходимо выбрать файл')]
    )

    submit_button = SubmitField(
        label='Загрузить'
    )

