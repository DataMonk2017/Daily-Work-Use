```
####################################################################################
# move the click and use the opened window of browser
# https://stackoverflow.com/questions/11908249/debugging-element-is-not-clickable-at-point-error?page=1&tab=votes#tab-top
# https://stackoverflow.com/questions/27934945/selenium-move-to-element-does-not-always-mouse-hover
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

driver = webdriver.Chrome()

driver.get("http://www.flipkart.com/watches/pr?p%5B%5D=facets.ideal_for%255B%255D%3DMen&p%5B%5D=sort%3Dpopularity&sid=r18&facetOrder%5B%5D=ideal_for&otracker=ch_vn_watches_men_nav_catergorylinks_0_AllBrands")
driver.maximize_window()

# wait for Men menu to appear, then hover it
# use Explicit Waits
men_menu = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//a[@data-tracking-id='men']")))
ActionChains(driver).move_to_element(men_menu).perform()

# wait for Fastrack menu item to appear, then click it
fastrack = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//a[@data-tracking-id='0_Fastrack']")))
fastrack.click()
```
