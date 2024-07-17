import os
from PIL import Image, UnidentifiedImageError

import cv2
from timeit import default_timer as timer

import multiprocessing

from paths_filenames import path_report, need_files, directory_source, directory_dest


def processing_image(file_task):
    print(f'\nStart processing of {file_task}...', end='')
    filename, extension = os.path.splitext(file_task)
    image = cv2.imread(f'{directory_source}\\{file_task}')
    shape = image.shape
    for i in range(shape[0]):
        for j in range(shape[1]):
            image[i, j, 2] = 0
    cv2.imwrite(f'{directory_dest}\\{filename}_no_red{extension}', image)
    print(f'\nFinishing processing of {file_task}...', end='')


if __name__ == '__main__':

    MAX_PROCESSES = multiprocessing.cpu_count()

    start = timer()

    files = os.listdir(directory_source)

    for file in files:
        try:
            image_file = Image.open(f'{directory_source}\\{file}')
        except UnidentifiedImageError:
            files.remove(file)

    times = []

    for number_of_processes in range(1, MAX_PROCESSES + 1):
        print(f'\nNumber of processes = {number_of_processes} ({number_of_processes}/{MAX_PROCESSES})')

        starting_processes = timer()

        with multiprocessing.Pool(processes=number_of_processes) as pool:
            pool.map(processing_image, files)

        finishing_processes = timer()
        duration = finishing_processes - starting_processes
        times.append(duration)

        print(f'\nTime for iteration: {duration: .2f} seconds.')

    line1, line2 = '', ''
    for index, time in enumerate(times):
        print(index + 1, round(time, 2))
        line1 += str(index + 1) + ' '
        line2 += str(round(time, 2)) + ' '
        content = line1 + '\n' + line2
        filename = f'{path_report}\\{need_files[6]}'
        with open(filename, mode='w') as data_file:
            data_file.write(content)

    duration = timer() - start

    print(f'Total time: {duration:.2f} seconds.')
