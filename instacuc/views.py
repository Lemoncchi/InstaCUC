from flask import flash, redirect, render_template, url_for

from instacuc import app, db
from instacuc.forms import HelloForm, photos
from instacuc.models import Message

from covert_communication.image import extract_watermark, embed_watermark

@app.route('/', methods=['GET', 'POST'])
def index():
    form = HelloForm()
    if form.validate_on_submit():
        name = form.name.data
        body = form.body.data
        hidden_message = form.hidden_message.data
        img_file_name = photos.save(form.photo.data)
        img_file_path = photos.path(img_file_name)
        embed_watermark(img_file_path, hidden_message, img_file_path)
        file_url = photos.url(img_file_name)
        message = Message(body=body, name=name, img_file_name=img_file_name, hidden_message=hidden_message)
        db.session.add(message)
        db.session.commit()
        flash('Your message have been sent to the world!')
        return redirect(url_for('index'))

    messages = Message.query.order_by(Message.timestamp.desc()).all()
    return render_template('index.html', form=form, messages=messages, photos=photos)
