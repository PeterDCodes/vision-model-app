#make a master file

#add a video folder which is where the training vid will be stored

#add scripts folder where main.py yaml and model test files will be

#make the following folder structure

# dataset/
# ├── images/
# │   ├── train/         # Training images
# │   │   ├── image1.jpg
# │   │   ├── image2.jpg
# │   │   └── ...
# │   └── val/           # Validation images
# │       ├── image1.jpg
# │       ├── image2.jpg
# │       └── ...
# └── labels/
#     ├── train/         # Labels corresponding to training images
#     │   ├── image1.txt
#     │   ├── image2.txt
#     │   └── ...
#     └── val/           # Labels corresponding to validation images
#         ├── image1.txt
#         ├── image2.txt
#         └── ...

import os
from video_parse import video_parse

def config_files(project_name, object_name):

    #can make improvement here using a 'subfolder' function to clean up the following code with a loop function from a list of these required directories??

    main_folder = "./" + project_name
    os.mkdir(main_folder)

    #make video folder
    video = "./" + main_folder + '/video'
    os.mkdir(video)

    #make scripts folder
    scripts = "./" + main_folder + '/scripts'
    os.mkdir(scripts)

    #make a autodata folder used to store future auto data
    autodata = "./" + main_folder + '/autodata'
    os.mkdir(autodata)    

    #make dataset folder
    dataset = "./" + main_folder + '/dataset'
    os.mkdir(dataset)

    #make images folder
    images = "./" + dataset + '/images'
    os.mkdir(images)

    #image/train folder
    train = "./" + images + '/train'
    os.mkdir(train)

    #image/val folder
    val = "./" + images + '/val'
    os.mkdir(val)

    #make labels folder
    labels = "./" + dataset + '/labels'
    os.mkdir(labels)

    #image/train folder
    train = "./" + labels + '/train'
    os.mkdir(train)

    #image/val folder
    val = "./" + labels + '/val'
    os.mkdir(val)

    #now need to make the YAML config
    #and add the main.py into this folder