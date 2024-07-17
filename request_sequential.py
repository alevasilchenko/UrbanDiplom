import requests
import time


def request_sequential(number_of_repeats, urls):

    print(f'\nStart {number_of_repeats} times of sequential execution of requests...')

    total_times = []

    min_requests_duration = [0] * len(urls)

    images = [None] * len(urls)

    for i in range(number_of_repeats):
        print(f'    Starting # {i + 1}...')
        success = True

        start_time = time.time()

        for index, url in enumerate(urls):
            request_time = time.time()
            try:
                data = requests.get(url)
            except requests.RequestException as exc:
                print(index, exc)
                success = False
                print('ERROR RESULT!')
                break
            else:
                request_duration = time.time() - request_time
                if not min_requests_duration[index] or (request_duration < min_requests_duration[index]) :
                    min_requests_duration[index] = request_duration
                print(index, data, round(request_duration, 2))
                if not images[index]:
                    images[index] = data.content

        if success:
            end_time = time.time()
            duration = end_time - start_time
            print(f'Total time # {i + 1}: {duration: .2f} seconds')
            total_times.append(duration)

        if i < number_of_repeats - 1:
            print('Pause for 1 seconds...')
            time.sleep(1)

    min_total_time = None
    max_request_duration_within = None

    if len(total_times):
        min_total_time = min(total_times)
        max_request_duration_within = max(min_requests_duration)
        print(f'\nMinimum total time: {min_total_time: .2f} seconds')
        for index, image in enumerate(images):
            filename = f'images_source\\image_{index}.jpg'
            with open(filename, 'wb') as file:
                file.write(image)
    else:
        print('\nEXECUTING WITH NOT SUCCESS!')

    print('Done sequential execution of requests.')

    return min_total_time, max_request_duration_within
