import time
import json
import getopt
import sys
from urllib.parse import urlparse
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from helpers import rip_text

DDG_HOME = 'https://html.duckduckgo.com/html/'

def get_cfg (file_name):
    file_handle = open(file_name, 'r')
    contents = file_handle.read()
    lines = contents.split('\n')
    return lines

def write_file (file_name, file_contents):
    file_handle = None
    try:
        file_handle = open(file_name, 'w')
        file_handle.write(file_contents)
    except Exception as e:
        print(f'Error: {e}')
    finally:
        if not (file_handle is None):
            file_handle.close()

def parse (result, html, raw):
    if raw:
        result['rawHtml'] = html

    result['textContent'] = rip_text(html)

def search (driver, where, what, pages, limit, save_raw):
    documents = []
    
    # search for what on site where
    driver.get(DDG_HOME)
    time.sleep(5) 
    search_box = driver.find_element_by_name('q')
    search_box.send_keys(f'site:{where} {what}')
    search_box.submit()

    # cache all links first
    page_num = 1
    result_anchors = []
    while True:
        time.sleep(5)
        anchors = driver.find_elements_by_class_name('result__a')
        for anchor in anchors:
            result_anchors.append(anchor.get_attribute('href'))
        
        # stop if we hit max pages or button is not present
        if (page_num >= pages):
            break
        else:
            button_next = driver.find_element_by_css_selector('input[value="Next"]')
            if button_next is None:
                break
            else:
                button_next.click()
                page_num += 1

    # go through each link
    links_seen = 0
    for anchor in result_anchors:
        if (limit <= links_seen):
            break

        result = {}
        result['href'] = anchor
        
        # navigate there
        driver.get(anchor)
        time.sleep(5)
        
        # get html
        html = driver.page_source
        parse(result, html, save_raw)

        # go back
        driver.back()
        documents.append(result)
        links_seen += 1
        time.sleep(5)

    # return results
    return documents

def get_domain (url):
    return urlparse(url).netloc

def main (headless, pages, limit, save_raw):
    search_sites = get_cfg('./config/search_sites.cfg')
    search_terms = get_cfg('./config/search_terms.cfg')

    options = Options()
    options.headless = headless
    driver = webdriver.Chrome(options=options)
    
    site_results = {}
    for site in search_sites:
        domain = get_domain(site)
        site_results[domain] = []

        for term in search_terms:
            results = search(driver, site, term, pages, limit, save_raw)
            for result in results:
                site_results[domain].append(result)
        
    site_results_json = json.dumps(site_results)
    write_file(f'./results/results.json', site_results_json)
            
    driver.quit()

headless = True
pages = 1
limit = 1999
save_raw = False

opts = getopt.getopt(sys.argv[1:], 'np:l:r')

for k, v in opts[0]:
    if k == '-n': # not headless
        headless = False
    elif k == '-p': # page limit
        pages = int(v)
    elif k == '-l': # result limit
        limit = int(v)
    elif k == '-r': # save raw html too
        save_raw = True
    else:
        print(f'Unknown option {k}. Ignored.')

main(headless,
    pages,
    limit,
    save_raw)