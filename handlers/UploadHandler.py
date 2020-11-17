from handlers.BaseHandler import *
import os
import string
import random
import json

class UploadHandler(BaseHandler):
    @tornado.web.authenticated
    async def get(self):
        self.render("upload.html")

    @tornado.web.authenticated
    async def post(self):
        img_file = self.request.files['img_file'][0]
        original_fname = img_file['filename']
        description = self.get_argument('title')
        extension = os.path.splitext(original_fname)[1]
        fname = ''.join(random.choice(string.ascii_lowercase + string.digits) for x in range(6))
        final_filename= fname+extension
        output_file = open("static/uploads/" + final_filename, 'wb')
        output_file.write(img_file['body'])

        # Add file details to database
        await self.execute(
                "INSERT INTO gallery (author_id,file_name,description,published)"
                "VALUES (%s,%s,%s,CURRENT_TIMESTAMP)",
                self.current_user.id,
                final_filename,
                description
            )

        self.write("file: " + final_filename + " is uploaded <br />")
        self.finish("Return to <a href='/gallery'>gallery</a>")