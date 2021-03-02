"""Run a local proxy server that distributes
   incoming requests to external proxies."""

import asyncio
import aiohttp
from bs4 import BeautifulSoup

from proxybroker import Broker

from script.scrape import get_request_data
websites = []


async def get_pages(urls, proxy_url):
    tasks = [fetch(url, proxy_url) for url in urls]
    for task in asyncio.as_completed(tasks):
        url, content = await task
        print('Done! url: %s; content: %.100s' % (url, content))
        if content is not None:
            soup = BeautifulSoup(content, 'html.parser')
            for a in soup.findAll('p', text="Business website"):
                if a.nextSibling.text is not None:
                    print(a.nextSibling.text)
                    websites.append(a.nextSibling.text)
                    print(len(websites))
                    break
        else:
            websites.append("N/A")
            print(len(websites))


async def fetch(url, proxy_url):
    resp = None
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, proxy=proxy_url) as response:
                resp = await response.read()
    except (aiohttp.errors.ClientOSError, aiohttp.errors.ClientResponseError,
            aiohttp.errors.ServerDisconnectedError) as e:
        print('Error. url: %s; error: %r' % (url, e))
    finally:
        return (url, resp)


def main():
    host, port = '127.0.0.1', 8888  # by default

    loop = asyncio.get_event_loop()

    types = [('HTTP', 'High'), 'HTTPS', 'CONNECT:80']
    codes = [200, 301, 302]

    broker = Broker(max_tries=1, loop=loop)

    # Broker.serve() also supports all arguments that are accepted
    # Broker.find() method: data, countries, post, strict, dnsbl.
    broker.serve(host=host, port=port, types=types, limit=100, max_tries=5,
                 prefer_connect=True, min_req_proxy=5, max_error_rate=0.5,
                 max_resp_time=8, http_allowed_codes=codes, backlog=100)

    urls = get_request_data(index=0)

    proxy_url = 'http://%s:%d' % (host, port)
    loop.run_until_complete(get_pages(urls, proxy_url))

    broker.stop()

    return websites


if __name__ == '__main__':
    main()