# -*- encoding: utf-8 -*-
import requests
import sys
from urlparse import urlparse

from BeautifulSoup import BeautifulStoneSoup


URL_ELEMENT_NAME = 'loc'


def compare(url1, url2):
    """
    Recursively compares two sitemaps.

    Two sitemaps are equal if they contain the same URLs and all
    the contents of those URLs are equal.

    We also "filter" lists of HTMLs to avoid crawling those since
    we just want to compare the sitemaps and its contents, not the
    HTMLs pointed by the leaves.
    """
    sitemap_base = BeautifulStoneSoup(requests.get(url1).content)
    other_sitemap_base = BeautifulStoneSoup(requests.get(url2).content)

    soup1_urls = [u.text for u in sitemap_base(URL_ELEMENT_NAME)]
    soup2_urls = [u.text for u in other_sitemap_base(URL_ELEMENT_NAME)]

    soup1_urls.sort()
    soup2_urls.sort()

    if not contains_xmls(soup1_urls) and equal_paths(soup1_urls, soup2_urls):
        return True

    return equal_paths(soup1_urls, soup2_urls) and\
            all(compare(u1,u2) for u1,u2 in zip(soup1_urls, soup2_urls))


def contains_xmls(urls_list):
    """
    Inspects the first element to see if the contents are sitemaps to continue
    crawling or are just list of URLs.

    WARNING: This assumes the lists are homogeneous. It improves performance
    a lot cause it helps to avoid requesting HTMLs.
    """
    return urls_list[0].endswith('.xml')


def equal_paths(url_list1, url_list2):
    """
    Compares two lists of URLs, only by their paths (discarding netloc).
    """
    return [urlparse(url).path for url in url_list1] == [urlparse(url).path for url in url_list2]


def main(*args):
    args = args[0]
    print "The sitemaps are equal: {cmp}.".format(cmp=compare(args[0], args[1]))


if __name__ == '__main__':
    main(sys.argv[1:])
