import click

from instacuc import app, db
from instacuc.models import Message

import random


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
@click.option('--count', default=5, help='Quantity of messages, default is 20.')
def forge(count):
    """Generate fake messages."""
    from faker import Faker

    db.drop_all()
    db.create_all()

    def get_example_images():
        """获取测试用图片"""
        import os
        example_img_dir = os.path.join( app.config['UPLOADED_PHOTOS_DEST'], 'example_CUC')
        example_img_list = []
        for filename in os.listdir(example_img_dir):
            example_img_list.append(os.path.join('example_CUC', filename))

        return example_img_list

    example_img_list = get_example_images()

    fake_CN = Faker('zh_CN')
    fake = Faker()
    click.echo('Working...')

    
    for i in range(count):
        has_hidden_message= random.choice([True, False])
        message = Message(
            name=fake.name(),
            body=fake_CN.sentence(),
            timestamp=fake.date_time_this_year(),
            img_file_name= random.choice(example_img_list),
            has_hidden_message=has_hidden_message,
            hidden_message=fake.sentence() if has_hidden_message else None,
            fake=True
        )
        db.session.add(message)

    db.session.commit()
    click.echo('Created %d fake messages.' % count)
