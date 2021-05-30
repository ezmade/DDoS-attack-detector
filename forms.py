from flask_wtf import FlaskForm
from wtforms import SelectField, FileField, DecimalField, StringField
from wtforms.fields.simple import SubmitField
from wtforms.validators import DataRequired, StopValidation, ValidationError, number_range

class ClassificationForm(FlaskForm):
    
    input_file = FileField(
        label='Выберите файл',
        validators=[DataRequired('Выберите файл')]
    )

    classification_model = SelectField(
        label='Выберите модель'
    )

    submit = SubmitField(label=('Загрузить'))

    def validate_input_file(self, input_file):
        if not (str(input_file.data.filename).endswith('.csv')):
            raise StopValidation(
                'Format is not supported. Choose .csv file.'
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
        validators=[DataRequired('Введите значение'), 
        number_range(min=1, max=100)]
    )

    sizes = DecimalField(
        label='Введите размер скрытого слоя',
        validators=[DataRequired('Введите значение'), 
        number_range(min=1, max=1000)]
    )

    label_name = StringField(
        label='Введите название ключевого признака',
        validators=[DataRequired('Введите значение')]
    )
    
    input_file = FileField(
        label='Выберите набор данных',
        validators=[DataRequired('Выберите файл')]
    )

    submit = SubmitField(label=('Обучить'))

    def validate_input_file(self, input_file):
        if not (str(input_file.data.filename).endswith('.csv')):
            raise StopValidation(
                'Format is not supported. Choose .csv file.'
            )

    


