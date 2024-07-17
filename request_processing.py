import multiprocessing
import requests
import time
import os
from random import randint


class MainProcess(multiprocessing.Process):

    def __init__(self, task_queue, images, number):
        super().__init__()
        self.task_queue = task_queue
        self.images = images
        self.number = number

    def run(self):
        process_name = self.name
        while not self.task_queue.empty():
            current_task = self.task_queue.get()
            print(f'Processing {self.number} with {current_task}...')
            index, data_url = current_task.process()
            self.task_queue.task_done()
            if index is not None:
                self.images = data_url
                filename = f'images_source\\image_{index}.jpg'
                if not os.path.isfile(filename):
                    with open(filename, 'wb') as file:
                        file.write(data_url)
            else:
                print('Correcting pausing for 5 seconds...')
                time.sleep(5)


class Task:

    def __init__(self, index, url):
        self.index = index
        self.url = url

    def process(self):
        try:
            data_url = requests.get(self.url)
        except requests.RequestException as exc:
            print(self.index, exc)
            print('ERROR RESULT!')
            return None, None
        else:
            print(self.index, data_url)

        return self.index, data_url.content

    def __str__(self):
        return f'request from url {self.index}'


def request_processing(number_of_repeats, urls):

    images = [None] * len(urls)

    tasks = multiprocessing.JoinableQueue()

    max_processes = multiprocessing.cpu_count()

    times_on_every_number_of_processes = []

    for number_of_processes in range(1, max_processes + 1):

        print(f'\nDoing with Number of Processes = {number_of_processes} ({number_of_processes}/{max_processes})')

        print(f'\nStart {number_of_repeats} times of multiprocessing execution of requests...')

        total_times = []

        for i in range(number_of_repeats):
            print(f'    Starting # {i + 1}...')
            processes = []

            while not tasks.empty():
                tasks.get()

            urls_index_list = [i for i in range(len(urls))]
            while len(urls_index_list):
                number = randint(0, len(urls_index_list) - 1)
                index = urls_index_list[number]
                url = urls[index]
                urls_index_list.pop(number)
                tasks.put(Task(index, url))

            for process_number in range(1, number_of_processes + 1):
                processes.append(MainProcess(tasks, images, process_number))

            start_time = time.time()

            for process in processes:
                process.start()

            tasks.join()

            if True:
                end_time = time.time()
                duration = end_time - start_time
                print(f'Total time # {i + 1}: {duration: .2f} seconds')
                total_times.append(duration)

            if (i < number_of_repeats - 1) or (number_of_processes < max_processes):
                print('Pause for 1 seconds...')
                time.sleep(1)

        if len(total_times):
            min_total_time = min(total_times)
            times_on_every_number_of_processes.append(min_total_time)
            print(f'\nMinimum total time: {min_total_time: .2f} seconds')
        else:
            print('\nEXECUTING WITH NOT SUCCESS!')
            return None

    print('Done multiprocessing execution of requests.')

    return times_on_every_number_of_processes
