from flask_wtf import Form
from wtforms import StringField
from wtforms.validators import InputRequired, Length, URL, Regexp

class QueForm(Form):
    url = StringField('URL', validators=[
        InputRequired(),
        Length(min=34, max=60),
        URL(),
        #Regexp(r'https?:\/\/boards.4chan.org\/[a-z]+\/thread\/[0-9]+\/?', 0, 'Invalid 4chan URL.'),
    ])

