import threading
import requests
import queue
import time
from random import randint


def request_threading(number_of_repeats, max_threads, urls):

    class RequestThread(threading.Thread):

        def __init__(self, number, que):
            super().__init__()
            self.number = number
            self.que = que
            # self.daemon = True

        def run(self):
            nonlocal success
            print(f'Starting thread {self.number}...')
            while True:
                try:
                    que_obj = self.que.get(block=False)
                except queue.Empty:
                    print(f'Exiting thread {self.number}...')
                    return
                else:
                    index_url = que_obj[0]
                    try:
                        data_url = requests.get(que_obj[1])
                    except requests.RequestException as exc:
                        print(index_url, exc)
                        print('ERROR RESULT!')
                        print(f'Exiting thread {self.number}...')
                        success = False
                        return
                    else:
                        print(index_url, data_url)
                        if not images[index_url]:
                            images[index_url] = data_url.content

    images = [None] * len(urls)

    urls_queue = queue.Queue()

    times_on_every_number_of_threads = []

    for number_of_threads in range(1, max_threads + 1):

        print(f'\nDoing with Number of Threads = {number_of_threads} ({number_of_threads}/{max_threads})')

        print(f'\nStart {number_of_repeats} times of threading execution of requests...')

        total_times = []

        for i in range(number_of_repeats):
            print(f'    Starting # {i + 1}...')
            success = True
            threads = []

            urls_queue.queue.clear()
            urls_index_list = [i for i in range(len(urls))]
            while len(urls_index_list):
                number = randint(0, len(urls_index_list) - 1)
                index = urls_index_list[number]
                url = urls[index]
                urls_index_list.pop(number)
                urls_queue.put((index, url))

            for thread_number in range(1, number_of_threads + 1):
                threads.append(RequestThread(thread_number, urls_queue))

            start_time = time.time()

            for thread in threads:
                thread.start()

            for thread in threads:
                thread.join()

            if success:
                end_time = time.time()
                duration = end_time - start_time
                print(f'Total time # {i + 1}: {duration: .2f} seconds')
                total_times.append(duration)

            if (i < number_of_repeats - 1) or (number_of_threads < max_threads):
                print('Pause for 1 seconds...')
                time.sleep(1)

        if len(total_times):
            min_total_time = min(total_times)
            times_on_every_number_of_threads.append(min_total_time)
            print(f'\nMinimum total time: {min_total_time: .2f} seconds')
        else:
            print('\nEXECUTING WITH NOT SUCCESS!')
            return None

    for index, image in enumerate(images):
        filename = f'images_source\\image_{index}.jpg'
        with open(filename, 'wb') as file:
            file.write(image)

    print('Done threading execution of requests.')

    return times_on_every_number_of_threads
