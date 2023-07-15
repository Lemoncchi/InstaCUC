from flask_wtf import FlaskForm, file
from flask_uploads import UploadSet, configure_uploads, IMAGES, patch_request_class
from wtforms import StringField, SubmitField, TextAreaField, FileField
from wtforms.validators import DataRequired, Length, ValidationError

from instacuc import app

photos = UploadSet('photos', IMAGES)
configure_uploads(app, photos)
patch_request_class(app)  # set maximum file size, default is 16MB

def ascii_only(form, field):
    if not field.data.isascii():
        raise ValidationError('由于目前使用的水印算法会有部分误码，中文编码嵌入后解码效果惨不忍睹，所以目前只能输入英文 (⋟﹏⋞)')

class HelloForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(1, 20)])
    body = TextAreaField('Message（若无消息可留空）', validators=[DataRequired(), Length(1, 200)])
    hidden_message = TextAreaField('Hidden Message', validators=[Length(0, 200), ascii_only])
    photo = FileField(u'图片', validators=[
        file.FileAllowed(photos, u'只能上传图片！'), 
        file.FileRequired(u'文件未选择！')
    ],)
    submit = SubmitField()
