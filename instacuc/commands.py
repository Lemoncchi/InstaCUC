import os
import random

import click

from covert_communication.image import embed_watermark, extract_watermark
from instacuc import app, db
from instacuc.models import Message


@app.cli.command()
@click.option('--drop', is_flag=True, help='Create after drop.')
def initdb(drop):
    """Initialize the database."""
    if drop:
        click.confirm('This operation will delete the database, do you want to continue?', abort=True)
        db.drop_all()
        click.echo('Drop tables.')
    db.create_all()
    click.echo('Initialized database.')


@app.cli.command()
@click.option('--count', default=5, help='Quantity of messages, default is 5. Must be lest than 6')
def forge(count):
    """Generate fake messages."""
    from faker import Faker

    db.drop_all()
    db.create_all()

    def get_example_images():
        """获取测试用图片"""
        example_img_dir = os.path.join(app.config['UPLOADED_PHOTOS_DEST'], 'example_CUC')
        example_img_list = []
        for filename in os.listdir(example_img_dir):
            example_img_list.append(filename)

        return example_img_list

    example_img_list = get_example_images()

    fake_CN = Faker('zh_CN')
    fake = Faker()
    click.echo('Working...')

    
    for i in range(count):
        has_hidden_message = random.choice([True, False])
        message = Message(
            name=fake.name(),
            body=fake_CN.sentence(),
            timestamp=fake.date_time_this_year(),
            img_file_name=example_img_list[i],
            has_hidden_message=has_hidden_message,
            hidden_message=fake.sentence() if has_hidden_message else None,
            fake=True
        )
        
        img_file_source_path = os.path.join(app.config['UPLOADED_PHOTOS_DEST'], 'example_CUC', message.img_file_name)
        img_file_dest_path = os.path.join(app.config['UPLOADED_PHOTOS_DEST'], message.img_file_name)
        if message.has_hidden_message:
            print(f"{img_file_source_path} ——> {img_file_dest_path}")
            embed_watermark(img_file_source_path, message.hidden_message, img_file_dest_path)
        else:
            import shutil
            shutil.copyfile(img_file_source_path, img_file_dest_path)

        db.session.add(message)

    db.session.commit()
    click.echo('Created %d fake messages.' % count)
