import os
from PIL import Image, UnidentifiedImageError

import cv2
from timeit import default_timer as timer

import asyncio
from concurrent.futures import ThreadPoolExecutor

from paths_filenames import path_report, need_files, directory_source, directory_dest


def processing_image(file_task):

    print(f'\nStart processing of {file_task}...', end='')
    filename, extension = os.path.splitext(file_task)
    image = cv2.imread(f'{directory_source}\\{file_task}')
    shape = image.shape
    n = 0
    for i in range(shape[0]):
        for j in range(shape[1]):
            n += 1
            image[i, j, 2] = 0
    cv2.imwrite(f'{directory_dest}\\{filename}_no_red{extension}', image)
    print(f'\nFinishing processing of {file_task}...', end='')


async def main():

    futures = [loop.run_in_executor(executor, processing_image, f) for f in files]

    await asyncio.gather(*futures)


if __name__ == '__main__':

    start = timer()

    files = os.listdir(directory_source)

    for file in files:
        try:
            image_file = Image.open(f'{directory_source}\\{file}')
        except UnidentifiedImageError:
            files.remove(file)

    THREADS_LIMIT = 10
    MAX_THREADS = min(len(files), THREADS_LIMIT)

    times = []

    for number_of_threads in range(1, MAX_THREADS + 1):
        print(f'\nNumber of threads = {number_of_threads} ({number_of_threads}/{MAX_THREADS})')

        executor = ThreadPoolExecutor(max_workers=number_of_threads)

        starting_threads = timer()

        loop = asyncio.get_event_loop()
        loop.run_until_complete(main())

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
        filename = f'{path_report}\\{need_files[10]}'
        with open(filename, mode='w') as data_file:
            data_file.write(content)

    duration = timer() - start

    print(f'Total time: {duration:.2f} seconds.')
