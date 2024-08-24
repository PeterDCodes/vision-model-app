
#own sorting scrip here. that will recieve a list of files names in format '000.jpg'. I will need to sort by ignoring .jpg and convert to ints

#images = ['000.jpg','100.jpg','010.jpg','020.jpg', '001.jpg', '002.jpg']

import string

def image_dir_sort(files):

    file_count = 0
    for file in files:
        #take the first filename and get the number
        file_number = str(file[:-4])
        files[file_count] = int(file_number)
        file_count += 1

    files = sorted(files)

    for i in range(len(files)):
        files[i] = str(files[i]) + '.jpg'

    return files