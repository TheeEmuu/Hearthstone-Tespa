import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from multiprocessing.dummy import Pool as ThreadPool
from Spreadsheet import Datasheet


def main():
    sheet = Datasheet()

    # Initilize driver
    driver = webdriver.Chrome('D:\Programming\Chromedriver\chromedriver.exe')
    driver.set_window_position(1000, 0)
    driver.set_window_size(2560, 1080)
    driver.get("http://www.hsreplay.net")
    # go to meta tab
    elem = driver.find_elements_by_xpath("//*[contains(text(), 'Meta')]")
    elem[0].click()
    time.sleep(1)
    # go to 'By Class'
    elem = driver.find_element_by_id("tab-archetypes")
    elem.click()

    time.sleep(1)
    # get all classes
    elem = driver.find_element_by_class_name("class-box-container")
    elem = elem.find_elements_by_class_name("class-box")

    matchups_dict = []
    todo = []

    # loops over each class
    for x in elem:
        # loops over each archetype
        for y in x.find_elements_by_class_name("ReactVirtualized__Grid__innerScrollContainer"):
            # gets each archetype
            for z in y.find_elements_by_class_name("table-row-header"):
                # gets name of archetype
                link = z.find_element_by_class_name("player-class")
                archetype = link.text
                # as long as the archetype isn't 'other', add it to be checked
                if archetype != "Other":
                    todo.append(link.get_attribute('href'))

    pool = ThreadPool(8)
    results = pool.map(get_matchups, todo)

    driver.close()

    data = []
    for x in results:
        for y in x:
            data.append(y.player)
            data.append(y.opp)
            data.append(y.winrate)

    sheet.insert(data)


def get_matchups(link):
    matchups = []
    archdriver = webdriver.Chrome('D:\Programming\Chromedriver\chromedriver.exe')
    archdriver.get(link)
    time.sleep(5)
    archetype = archdriver.find_element_by_id("archetype-container").get_attribute("data-archetype-name")
    # go to matchups for the given class
    mat = archdriver.find_element_by_id("tab-matchups")
    mat.click()
    time.sleep(5)
    # loop over each class
    try:
        e = archdriver.find_element_by_class_name("class-box-container")
        e = e.find_elements_by_class_name("class-box")
        # loops over each class
        opp = []
        winrates = []
        for a in e:
            # loops over each archetype
            q = a.find_elements_by_class_name("grid-container-left")[1]
            for b in q.find_elements_by_class_name("ReactVirtualized__Grid__innerScrollContainer"):
                # gets each archetype
                for c in b.find_elements_by_class_name("table-row-header"):
                    k = c.find_element_by_class_name("player-class")
                    opp.append(k.text)
            q = a.find_elements_by_class_name("grid-container")[3]
            count = 2
            for b in q.find_elements_by_class_name("table-cell"):
                if count == 2:
                    count = 0
                    winrates.append(b.text)
                else:
                    count += 1
        for i in range(0, len(opp)):
            matchups.append(Matchup(archetype, opp[i], winrates[i]))
    except:
        print("no " + archetype + " data")

    archdriver.close()
    return matchups


class Matchup:
    def __init__(self, player, opp, winrate):
        self.player = player
        self.opp = opp
        self.winrate = winrate

main()
