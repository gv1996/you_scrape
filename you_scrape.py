#! /usr/bin/env python3

import sys
import requests
from bs4 import BeautifulSoup


if (len(sys.argv)) < 2:
    print('Usage: ./{} [search query]'.format(__file__))
    sys.exit()


# read the args to get the url
query = '+'.join(sys.argv[1:])
url = "https://www.youtube.com/results?search_query={}".format(query)

# get the page from the Internet
html = requests.get(url).text

# prepare the parser
soup = BeautifulSoup(html, 'html.parser')

# get the video list (parent container)
videos = soup.find_all('div', { 'class': 'yt-lockup' })

with open('results-{}.csv'.format(query), 'w') as f:

    # CSV headers
    f.write('title,link,duration\n')

    # iterate over the videos
    for video in videos:

        duration_div = video.find('span', { 'class': 'video-time' })

        # skipping playlists
        if duration_div == None:
            continue

        duration = duration_div.text
        duration_breakup = duration.split(':')

        # skip if the video duration is greater than an hour
        if len(duration_breakup) > 2:
            continue

        # skip if the video duration is not in between 3 and 5 minutes
        if int(duration_breakup[0]) > 5 or int(duration_breakup[0]) < 3:
            continue

        # get and write the title and href
        title_div = video.find('h3', { 'class': 'yt-lockup-title' }).find('a')
        f.write('\"{}\",'.format(title_div.text))
        f.write('\"https://www.youtube.com{}\",'.format(title_div['href']))

        # write the duration
        f.write('\"{}\"\n'.format(duration_div.text))
