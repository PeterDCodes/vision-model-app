from flask import Flask, request, redirect, render_template
from config_files import config_files
import os
from video_parse import video_parse

#video parse is an imported function. I need to figure out how I can get vid from user and parse into folders.
#order of operations will be to first make all the folders and then save parsed video files into the proper train img folder

# GET Example: If you type a URL in your browser or click on a link, a GET request is made to fetch the content of that page.
# POST Example: When you fill out a form on a website (like a login form) and hit "Submit," a POST request is typically made to send your credentials to the server

app = Flask(__name__)

@app.route("/")
def create_project():
    return render_template("index.html")

@app.route('/submit-project', methods=['POST'])
def submit_project():
    if request.method == 'POST':
        #collect variables needed for file setup and video parsing
        project_name = request.form.get('project_name')
        object_name = request.form.get('object_name') 
        rate = int(request.form.get('rate'))

        #set up files with parsed video
        config_files(project_name, object_name)

        #upload video to folder
        UPLOAD_FOLDER = os.path.join(".", project_name, "video")
        app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
        video_file = request.files['file']
        video_file_name = os.path.join(app.config['UPLOAD_FOLDER'], video_file.filename)
        video_file.save(video_file_name)

        image_path = os.path.join(".", project_name, "dataset", "images", "train")


        #parse that video
        #need to put in the video path
        video_parse(video_file_name, image_path, rate)


        #need to add a FileExistsError so two project of the same name cant be submitted
        return render_template("annotate.html")
    
    else:
        return redirect("/")
    