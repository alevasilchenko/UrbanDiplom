import os
from PIL import Image, UnidentifiedImageError

import cv2
from timeit import default_timer as timer

from threading import Thread
from queue import Queue

from paths_filenames import path_report, need_files, directory_source, directory_dest

start = timer()

files = os.listdir(directory_source)

for file in files:
    try:
        image_file = Image.open(f'{directory_source}\\{file}')
    except UnidentifiedImageError:
        files.remove(file)

THREADS_LIMIT = 10
MAX_THREADS = min(len(files), THREADS_LIMIT)


def processing_image():
    while not image_queue.empty():
        file_task = image_queue.get()
        print(f'\nStart processing of {file_task}...', end='')
        filename, extension = os.path.splitext(file_task)
        image = cv2.imread(f'{directory_source}\\{file_task}')
        shape = image.shape
        for i in range(shape[0]):
            for j in range(shape[1]):
                image[i, j, 2] = 0
        cv2.imwrite(f'{directory_dest}\\{filename}_no_red{extension}', image)
        print(f'\nFinishing processing of {file_task}...', end='')


image_queue = Queue()
times = []

for number_of_threads in range(1, MAX_THREADS + 1):
    print(f'\nNumber of threads = {number_of_threads} ({number_of_threads}/{MAX_THREADS})')
    image_queue.queue.clear()

    for file in files:
        image_queue.put(file)

    threads = []

    for thread_number in range(number_of_threads):
        thread = Thread(target=processing_image)
        threads.append(thread)

    starting_threads = timer()

    for index, thread in enumerate(threads):
        print(f'\nActivation of thread {index + 1}...', end='')
        thread.start()

    for thread in threads:
        thread.join()

    finishing_threads = timer()
    duration = finishing_threads - starting_threads
    times.append(duration)

    print(f'\nTime for iteration: {duration: .2f} seconds.')

line1, line2 = '', ''
for index, time in enumerate(times):
    print(index + 1, round(time, 2))
    line1 += str(index + 1) + ' '
    line2 += str(round(time, 2)) + ' '
    content = line1 + '\n' + line2
    filename = f'{path_report}\\{need_files[5]}'
    with open(filename, mode='w') as data_file:
        data_file.write(content)

duration = timer() - start

print(f'Total time: {duration:.2f} seconds.')
