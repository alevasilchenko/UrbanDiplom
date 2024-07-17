from timeit import default_timer as timer

from request_sequential import request_sequential
from request_threading import request_threading
from request_processing import request_processing
from request_async import request_async

from paths_filenames import path_report, need_files

urls = ['https://get.wallhere.com/photo/mountains-lake-reflection-trees-1180204.jpg',
        'https://img.freepik.com/free-photo/beautiful-plants-in-natural-environment_23-2151357915.jpg?w=1380&t=st='
        '1720764892~exp=1720765492~hmac=4f0ea4a8c97012edcdda918fd89973c9089d0d6b85ee3d3fe76268eb9a31f9b6',
        'https://media.istockphoto.com/id/607280514/ru/%D1%84%D0%BE%D1%82%D0%BE/lupins-%D0%BE%D0%B7%D0%B5%D1%80%D0%BE-'
        '%D1%82%D0%B5%D0%BA%D0%B0%D0%BF%D0%BE.jpg?s=612x612&w=0&k=20&c=z_nkbYlZo5yVREnUW8xtn7HSlK-XdN2nLeGdLKBoqns=',
        'https://static-cse.canva.com/blob/846900/photo1502082553048f009c37129b9e1583341920812.jpeg',
        'https://i.pinimg.com/originals/c9/e7/73/c9e773a3d34d8a0018deecae0f2c6e7b.jpg',
        'https://cs8.pikabu.ru/post_img/2017/02/18/4/og_og_1487396404277683272.jpg',
        'https://wallpaper.forfun.com/fetch/25/254a3ec8ad1fdf5b13f4a19abc3db471.jpeg',
        'https://attaches.1001tur.ru/country_gallery/82/J4F31Xomsb1eCo94TrBN10z19CS3eCdN.jpg',
        'https://wallbox.ru/wallpapers/main/201628/7b78dd8f2d5ef02.jpg',
        'https://sun9-60.userapi.com/impg/bUzvMnM2bUtTcyf2lAXhZqGXDAg2Lsm0G8_1hA/pXvN5DmHYLs.jpg?size='
        '807x538&quality=95&sign=182ab0d2c6b8afcbab66fa79f23a6002&c_uniq_tag='
        'IDV0D3alygjFN-XBiG7So2uJop_12uGLFzUMhqUgg7E&type=album']

NUMBER_OF_REPEATS = 2
THREADS_LIMIT = 10
MAX_THREADS = min(len(urls), THREADS_LIMIT)

start_time = timer()

if __name__ == '__main__':

    start_sequential_time = timer()

# sequential execution

    result_time, request_time = request_sequential(NUMBER_OF_REPEATS, urls)
    if result_time is not None:
        print(f'Result_time = {result_time: .2f}, Target_time = {request_time: .2f}')
        filename = f'{path_report}\\{need_files[0]}'
        with open(filename, mode='w') as data_file:
            data_file.write(str(round(result_time, 2)))

    print(f'\nTOTAL SEQUENTIAL TIME = {timer() - start_sequential_time: .1f} seconds.')

if __name__ == '__main__':

    start_threading_time = timer()

# threading execution

    times_threading = request_threading(NUMBER_OF_REPEATS, MAX_THREADS, urls)
    if times_threading is not None:
        line1, line2 = '', ''
        for index, time in enumerate(times_threading):
            print(index + 1, round(time, 2))
            line1 += str(index + 1) + ' '
            line2 += str(round(time, 2)) + ' '
        content = line1 + '\n' + line2
        filename = f'{path_report}\\{need_files[1]}'
        with open(filename, mode='w') as data_file:
            data_file.write(content)

    print(f'\nTOTAL THREADING TIME = {timer() - start_threading_time: .1f} seconds.')

if __name__ == '__main__':

    start_multiprocessing_time = timer()

# multiprocessing execution

    times_processing = request_processing(NUMBER_OF_REPEATS, urls)
    if times_processing is not None:
        line1, line2 = '', ''
        for index, time in enumerate(times_processing):
            print(index + 1, round(time, 2))
            line1 += str(index + 1) + ' '
            line2 += str(round(time, 2)) + ' '
        content = line1 + '\n' + line2
        filename = f'{path_report}\\{need_files[2]}'
        with open(filename, mode='w') as data_file:
            data_file.write(content)

    print(f'\nTOTAL MULTIPROCESSING TIME = {timer() - start_multiprocessing_time: .1f} seconds.')

if __name__ == '__main__':

    start_async_time = timer()

# async execution

    result_time = request_async(NUMBER_OF_REPEATS, urls)
    if result_time is not None:
        print(f'Result_time = {result_time: .2f}')
        filename = f'{path_report}\\{need_files[3]}'
        with open(filename, mode='w') as data_file:
            data_file.write(str(round(result_time, 2)))

    print(f'\nTOTAL ASYNC TIME = {timer() - start_async_time: .1f} seconds.')

    print(f'\nSUMMARY TIME = {timer() - start_time: .0f} seconds.')
