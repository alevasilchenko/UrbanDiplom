import os
from PIL import Image, UnidentifiedImageError

import cv2
from timeit import default_timer as timer

from paths_filenames import path_report, need_files, directory_source, directory_dest

start = timer()

files = os.listdir(directory_source)

for file in files:
    try:
        image_file = Image.open(f'{directory_source}\\{file}')
    except UnidentifiedImageError:
        files.remove(file)

number_of_images = len(files)

for file in files:
    print(f'Start processing of {file}...')
    filename, extension = os.path.splitext(file)
    image = cv2.imread(f'{directory_source}\\{file}')
    image = 255 - image
    cv2.imwrite(f'{directory_dest}\\{filename}_inv_by_matrix{extension}', image)
    print(f'Finishing processing of {file}...')

duration = timer() - start

filename = f'{path_report}\\{need_files[9]}'
with open(filename, mode='w') as data_file:
    data_file.write(str(round(duration, 2)))

print(f'Total time: {duration:.2f} seconds.')