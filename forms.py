from flask_wtf import FlaskForm
from wtforms import SelectField, FileField, DecimalField
from wtforms.validators import DataRequired

class ClassificationForm(FlaskForm):
    
    input_file = FileField(
        label='Выберите файл',
        validators=[DataRequired('Выберите файл')]
    )

    classification_model = SelectField(
        label='Выберите модель'
    )


class LearningForm(FlaskForm):

    solvers = SelectField(
        label='Выберите оптимизатор'
    )

    activations = SelectField(
        label='Выберите функцию активации'
    )

    max_iters = DecimalField(
        label='Введите количество итераций',
        validators=[DataRequired('Введите значение')]
    )

    sizes = DecimalField(
        label='Введите размер скрытого слоя',
        validators=[DataRequired('Введите значение')]
    )


