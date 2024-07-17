import time
import asyncio
import aiohttp
import aiofiles


def request_async(number_of_repeats, urls):

    chunk_size = 1024

    async def download_an_image(session, url_image, url_index):
        nonlocal success
        print(f'Starting request from url {url_index}...')
        try:
            async with session.get(url_image, ssl=False) as res:
                filename = f'images_source\\image_{url_index}.jpg'
                async with aiofiles.open(filename, 'wb') as fp:
                    # while True:
                    #     chunk = await res.content.read(chunk_size)
                    #     if not chunk:
                    #         break
                    await fp.write(await res.read())
                    print(f'Image file {url_index} is done!')
        except Exception as exc:
            print(url_index, exc)
            success = False
            print('ERROR RESULT!')

    async def main(url_image, url_index):

        async with aiohttp.ClientSession() as session:

            await download_an_image(session, url_image, url_index)

    print(f'\nStart {number_of_repeats} times of async execution of requests...')

    total_times = []

    for i in range(number_of_repeats):
        print(f'    Starting # {i + 1}...')
        success = True

        start_time = time.time()

        loop = asyncio.get_event_loop()

        tasks = []

        for index, url in enumerate(urls):
            tasks.append(main(url, index))

        loop.run_until_complete(asyncio.gather(*tasks))

        if success:
            end_time = time.time()
            duration = end_time - start_time
            print(f'Total time # {i + 1}: {duration: .2f} seconds')
            total_times.append(duration)

        if i < number_of_repeats - 1:
            print('Pause for 1 seconds...')
            time.sleep(1)

    min_total_time = None

    if len(total_times):
        min_total_time = min(total_times)
        print(f'\nMinimum total time: {min_total_time: .2f} seconds')
    else:
        print('\nEXECUTING WITH NOT SUCCESS!')

    print('Done async execution of requests.')

    return min_total_time
