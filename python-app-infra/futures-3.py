import concurrent.futures as t
import urllib.request as r
 
URLS = ['http://www.foxnews.com/',
        'http://www.cnn.com/',
        'http://www.wsj.com/',
        'http://www.bbc.co.uk/',
        'http://some-made-up-domain.com/']
 
# Retrieve a single page and report the url and contents
def load_url(url, timeout):
    with r.urlopen(url, timeout=timeout) as conn:
        print("urlopen succeeded");
        return conn.read()
 
# We can use a with statement to ensure threads are cleaned up promptly
with t.ThreadPoolExecutor(max_workers=5) as e:
    # Start the load operations and mark each future with its URL
    future_to_url = {e.submit(load_url, url, 60): url for url in URLS}
    for future in t.as_completed(future_to_url):
        url = future_to_url[future]
        try:
            data = future.result()
        except Exception as exc:
            print('%r generated an exception: %s' % (url, exc), future)
        else:
            print('%r page is %d bytes' % (url, len(data)), future)

