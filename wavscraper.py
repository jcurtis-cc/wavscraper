from lxml import html
import requests
import sys
import os.path

try:
    URLfromArg = sys.argv[1]
    userpathFromArg = sys.argv[2]
except:
    print("usage: wavscraper.py <url.com> <userpath>")
    print("eg: wavscraper.py url.com /User/John/Downloads")
    sys.exit(2)

if not os.path.exists(userpathFromArg):
    try:
        os.makedirs(userpathFromArg)
        print("created: ", userpathFromArg)
    except:
        print("could not make directory check argument")
        sys.exit(2)


page = requests.get(URLfromArg)
webpage = html.fromstring(page.content)


scrapedURLs = webpage.xpath('//a[contains(text(), ".wav")]/@href')
fileName = webpage.xpath('//a[contains(@href, ".wav")]/text()')

if not scrapedURLs:
    print()
    print("zero .wav files found at", URLfromArg, "exiting...")
    sys.exit(2)


for idx, url in enumerate(scrapedURLs) :
    split = str(url.split("/")[-1:]).strip("['""']")
    split = split.strip('\"')
    userpath = userpathFromArg + split
    if os.path.isfile(userpath) :
        print(userpath, " already exists in directory, skipping")
    else:
        print('\n')
        print("downloading ", idx + 1, " of ", len(scrapedURLs), ": ", url)
        with open(userpath, 'wb') as f:
            r = requests.get(url, stream=True)
            total_length = r.headers.get('content-length')
            if total_length is None:
                print("writing: ", userpath, '\n')
                f.write(r.content)
            else:
                dl = 0
                total_length = int(total_length)
                for data in r.iter_content(chunk_size=4096):
                    dl += len(data)
                    f.write(data)
                    done = int(50 * dl / total_length)
                    sys.stdout.write("\r[%s%s]" % ('=' * done, ' ' * (50-done)) )
                    sys.stdout.flush()

