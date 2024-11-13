from wtforms import RadioField, StringField
from flask_wtf import FlaskForm, RecaptchaField
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms.validators import Length, InputRequired, ValidationError


def file_size_limit(max_size):
    def _file_size_limit(_, field):
        if field.data and len(field.data.read()) > max_size:
            raise ValidationError(
                f"File size must be less than {max_size / (1024 * 1024)} MB."
            )

        field.data.seek(0)

    return _file_size_limit


class UsernameForm(FlaskForm):
    username = StringField(
        "Username",
        validators=[InputRequired(), Length(min=5, max=10)],
    )
    recaptcha = RecaptchaField()


class KYCForm(FlaskForm):
    name = StringField(
        "Name",
        validators=[InputRequired(), Length(min=5, max=100)],
    )
    age = StringField(
        "Age",
        validators=[InputRequired(), Length(min=1, max=3)],
    )
    location = StringField(
        "Location",
        validators=[InputRequired(), Length(min=5, max=100)],
    )
    id_number = StringField(
        "ID Number",
        validators=[InputRequired(), Length(min=5, max=20)],
    )
    id_front = FileField(
        "ID Card Front",
        validators=[
            FileRequired(),
            FileAllowed(["jpg", "png"], "Images only!"),
            file_size_limit(1 * 1024 * 1024),
        ],
    )
    id_back = FileField(
        "ID Card Back",
        validators=[
            FileRequired(),
            FileAllowed(["jpg", "png"], "Images only!"),
            file_size_limit(1 * 1024 * 1024),
        ],
    )
    recaptcha = RecaptchaField()


class AllowedAttributesForm(FlaskForm):
    name = RadioField(
        "Name",
        choices=[(1, "Enabled"), (0, "Disabled")],
        validators=[InputRequired()],
        default=0,
    )
    age = RadioField(
        "Age",
        choices=[(1, "Enabled"), (0, "Disabled")],
        validators=[InputRequired()],
        default=0,
    )
    location = RadioField(
        "Location",
        choices=[(1, "Enabled"), (0, "Disabled")],
        validators=[InputRequired()],
        default=0,
    )
    id_number = RadioField(
        "ID Number",
        choices=[(1, "Enabled"), (0, "Disabled")],
        validators=[InputRequired()],
        default=0,
    )
    recaptcha = RecaptchaField()
