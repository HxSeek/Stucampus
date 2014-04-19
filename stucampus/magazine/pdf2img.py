import os

from django_rq import job
from redis import Redis
from wand.image import Image

from stucampus.settings import path, MEDIA_ROOT


@job('pdf2img', connection=Redis(), timeout=600)
def pdf2img(magazine):
    pdf_path = os.path.join(MEDIA_ROOT, magazine.pdf_file.name)
    filename = os.path.basename(magazine.pdf_file.name)
    save_path = os.path.join(MEDIA_ROOT, 'magazine', magazine.name,
                            'img_' + filename)
    if os.path.exists(save_path):
        return
    with Image(filename=pdf_path, resolution=300) as image:
        image.compression_quality = 99
        image.save(filename=os.path.join(save_path))

