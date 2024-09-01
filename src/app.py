from flask import Flask, request, redirect, render_template, session, send_from_directory
from config_files import config_files
import os
from video_parse import video_parse
from image_dir_sort import image_dir_sort
from model_train import model_train


#video parse is an imported function. I need to figure out how I can get vid from user and parse into folders.
#order of operations will be to first make all the folders and then save parsed video files into the proper train img folder

# GET Example: If you type a URL in your browser or click on a link, a GET request is made to fetch the content of that page.
# POST Example: When you fill out a form on a website (like a login form) and hit "Submit," a POST request is typically made to send your credentials to the server

app = Flask(__name__)
# Set the secret key to some random bytes. Keep this really secret!
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'



@app.route("/")
def create_project():
    return render_template("index.html")


@app.route('/submit-project', methods=['POST'])
def submit_project():
    if request.method == 'POST':
        #collect variables needed for file setup and video parsing
        project_name = request.form.get('project_name')
        session['project_name'] = project_name

        object_name = request.form.get('object_name')
        session['object_name'] = object_name


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
        session['image_path'] = image_path

        #parse that video
        #need to put in the video path
        video_parse(video_file_name, image_path, rate)

        #set 0 image to display as first image in directory
        session['image_number'] = 0
        #set annotations array
        session["annotations"] = {}

        #need to add a FileExistsError so two project of the same name cant be submitted
        return redirect("/annotate")
    
    else:
        return redirect("/")
    

@app.route("/annotate")
def view_images():
        image_path = session['image_path']
        images = image_dir_sort((os.listdir(image_path))) #sorted retrun values of directory in sorted order from helper function.

        current_image = session['image_number']

        image_count = len(images)

        return render_template("temp.html", image=images[current_image], project_name = session['project_name'], image_count = image_count)   #TEMP .HTM being used in place of annotate


@app.route('/<project_name>/dataset/images/train/<filename>')
def serve_image(project_name, filename):
    directory = os.path.join('.', project_name, 'dataset', 'images', 'train')
    return send_from_directory(directory, filename)

@app.route('/next-image')
def next_image():

    #check if user already completed final annotation
     if int(session['image_number']) == len(os.listdir(session['image_path'])) - 1: #if the user has reached final annotation, they will then be sent to final screen
        return redirect("/model-config")

     #moves image to be displayed in annotate up one image in directory
     session['image_number'] += 1

     return redirect("/annotate")

@app.route('/previous-image')
def previous_image():
     #moves image to be displayed in annotate up one image in directory
     session['image_number'] += 1


     return redirect("/annotate")

@app.route('/save-annotations', methods=['POST']) #This gets called every time a box is drawn and data is logged to console
def save_annotations():
    data = request.json
    centerX = format(data['centerX'], ".6f")
    centerY = format(data['centerY'], ".6f")
    normWidth = format(data['normWidth'], ".6f")
    normHeight = format(data['normHeight'], ".6f")

    #turn to string format
    annotation_string = (f'0 {centerX} {centerY} {normWidth} {normHeight}')

    print(annotation_string)
    
    session['annotations']['image_number'] = annotation_string

    #make a .txt file named image_number + .txt and save to labels

    txt_file_name = './' + session['project_name'] + '/dataset/labels/train/' + str(session['image_number']) + ".txt"

    f = open(txt_file_name, "w")
    f.write(annotation_string)
    f.close()

    # Here you can process or save the data as needed
    return {"status": "success"}, 200


@app.route('/model-config')#once the user completes all image annotations, this page will show up.
def model_config():
     #this is where the yaml file will be created
    f= open("config.yaml", "w")

    path = (f'{os.getcwd()}/{session['project_name']}/dataset')

    #path = './' + session['project_name'] + '/dataset'
    train = 'images/train'
    val = 'images/train'

    object_name = session['object_name']

    f.write(f'\npath: {path}\ntrain: {train}\nval: {val}\n\n#classes\nnames:\n 0: {object_name}')
    f.close()
     #will need to collect the epochs from user
     #should also use this to complete some sort of validation tests
    return render_template("model_config.html")

@app.route('/model-create', methods=['POST']) #user creates model from model config page
def model_create():
    epochs = int(request.form.get('epochs'))
    model_train(epochs, project_name = session['project_name'])

    #need to figure out how to put a loading screen while the model is training??????

    return render_template('success.html', project_name = session['project_name'], object_name = session['object_name'])

