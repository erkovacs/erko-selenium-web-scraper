import time
import json
import getopt
import sys
import threading
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
            try:
                button_next = driver.find_element_by_css_selector('input[value="Next"]')
            except:
                break
            else:
                button_next.click()
                page_num += 1

    anchor_len = len(result_anchors)
    print(f'found {anchor_len} anchors looking for {what} on {where}...')

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
        
        # write results
        domain = get_domain(where)
        result['domain'] = domain
        result_json = json.dumps(result)
        write_file(f'./results/{domain}_{what}_{links_seen}.json', result_json)

        links_seen += 1
        time.sleep(5)

def scrape (options, site, search_terms, pages, limit, save_raw):
    driver = webdriver.Chrome(options=options)
    for term in search_terms:
        search(driver, site, term, pages, limit, save_raw)
    driver.quit()

def get_domain (url):
    return urlparse(url).netloc

def main (headless, pages, limit, save_raw):
    
    search_sites = get_cfg('./config/search_sites.cfg')
    search_terms = get_cfg('./config/search_terms.cfg')

    options = Options()
    options.headless = headless
    
    for i in range(0, len(search_sites), 2):
        threads = []
        chunk = search_sites[i:i+2]
        
        for site in chunk:
            thread = threading.Thread(target=scrape, args=(options, site, search_terms, pages, limit, save_raw))
            threads.append(thread)
            thread.start()
            time.sleep(10)

        for thread in threads:
            pass
            thread.join()

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
