import os
from flask.ext.script import Command
from application.lib.models import Media
from common.session import manager

import shutil
class RemoveImages(Command):

    def run(self):
        session = manager.get('standalone')

        medias = session.query(Media).all()

        for media in medias:
            print 'Removing image {image}'.format(image=media.get_path())
            if os.path.exists(media.get_directory()):
                shutil.rmtree(media.get_directory())
                session.delete(media)

        session.commit()







