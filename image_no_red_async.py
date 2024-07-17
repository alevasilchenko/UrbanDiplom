import os
from PIL import Image, UnidentifiedImageError

import cv2
from timeit import default_timer as timer

import asyncio

from paths_filenames import path_report, need_files, directory_source, directory_dest


async def processing_image(file_task):

    print(f'\nStart processing of {file_task}...', end='')
    filename, extension = os.path.splitext(file_task)
    image = cv2.imread(f'{directory_source}\\{file_task}')
    shape = image.shape
    n = 0
    for i in range(shape[0]):
        for j in range(shape[1]):
            n += 1
            image[i, j, 2] = 0
            if n % 1000000 == 1:

                await asyncio.sleep(0)

    cv2.imwrite(f'{directory_dest}\\{filename}_no_red{extension}', image)
    print(f'\nFinishing processing of {file_task}...', end='')


async def main():

    tasks = [loop.create_task(processing_image(f))for f in files]

    await asyncio.wait(tasks)


if __name__ == '__main__':

    start = timer()

    files = os.listdir(directory_source)

    for file in files:
        try:
            image_file = Image.open(f'{directory_source}\\{file}')
        except UnidentifiedImageError:
            files.remove(file)

    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())

    duration = timer() - start

    filename = f'{path_report}\\{need_files[7]}'
    with open(filename, mode='w') as data_file:
        data_file.write(str(round(duration, 2)))

    print(f'Total time: {duration:.2f} seconds.')
