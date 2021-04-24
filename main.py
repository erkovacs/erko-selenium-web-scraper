import time
from selenium import webdriver

DDG_HOME = 'https://html.duckduckgo.com/html/'

def get_cfg (file_name):
    file_handle = open(file_name, 'r')
    contents = file_handle.read()
    lines = contents.split('\n')
    return lines

def search (driver, where, what):
    driver.get(DDG_HOME)
    time.sleep(5) 
    search_box = driver.find_element_by_name('q')
    search_box.send_keys(f'site:{where} {what}')
    search_box.submit()
    time.sleep(5)

def main ():
    search_sites = get_cfg('./config/search_sites.cfg')
    search_terms = get_cfg('./config/search_terms.cfg')

    driver = webdriver.Chrome()
    for site in search_sites:
        for term in search_terms:
            search(driver, site, term)
            
    driver.quit()

main()