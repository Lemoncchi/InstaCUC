from flask_wtf import FlaskForm, file
from flask_uploads import UploadSet, configure_uploads, IMAGES, patch_request_class
from wtforms import StringField, SubmitField, TextAreaField, FileField
from wtforms.validators import DataRequired, Length

from instacuc import app

photos = UploadSet('photos', IMAGES)
configure_uploads(app, photos)
patch_request_class(app)  # set maximum file size, default is 16MB

class HelloForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(1, 20)])
    body = TextAreaField('Message', validators=[DataRequired(), Length(1, 200)])
    hidden_message = TextAreaField('Hidden Message', validators=[DataRequired(), Length(1, 200)])
    photo = FileField(u'图片', validators=[
        file.FileAllowed(photos, u'只能上传图片！'), 
        file.FileRequired(u'文件未选择！')
    ],)
    submit = SubmitField()
