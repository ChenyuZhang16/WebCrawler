from selenium import webdriver , common
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
import time
import os
import requests
delay = 0.2
delayManual = 3.0;

# INPUT section ==========
webUrl = "https://www.lanzoux.com/b015d257e";
password = "2027";
targetFolder = "."
# ========================

targetFolder = './' + targetFolder + '/'
if not os.path.exists(targetFolder):
	os.makedirs(targetFolder)

options = webdriver.FirefoxOptions()
# # options.add_argument('--no-sandbox')
driver = webdriver.Firefox(options=options)
driver.get(webUrl)
# time.sleep(delayManual)

if password:
	while True:
		try:
			pwd = driver.find_element_by_name("pwd")
		except common.exceptions.NoSuchElementException:
			time.sleep(delay)
		else:
			break

	pwd.send_keys(password)
	pwd.send_keys(Keys.RETURN)
else:
	print('No pwd')


#
# # /html/body/div[6]/div[4]/div[1]/div/div[5]/div/a
# # /html/body/div[6]/div[4]/div[1]/div/div[2]/div/a
# # /html/body/div[6]/div[4]/div[1]/div/div[74]/div/a
#

timeDelayed = 0
isButton = True
while True:
	try:
		gengduo = driver.find_element_by_id('filemore')
	except common.exceptions.NoSuchElementException:
		# print('except1')
		time.sleep(delay)
		timeDelayed = timeDelayed + delay;
		# print(timeDelayed)
		if timeDelayed > 2:
			isButton = False
			break
	else:
		break
timeDelayed = 0
while True:
	try:
		gengduo.click()
	except common.exceptions.ElementNotInteractableException:
		# print('except2')
		time.sleep(delay)
		timeDelayed = timeDelayed + delay;
		# print(timeDelayed)
		if timeDelayed > 2:
			isButton = False
			break
	else:
		break
if not isButton:
	print('No FileMore btn')

# try:
# 	gengduo = driver.find_element_by_id('filemore')
# except common.exceptions.NoSuchElementException:
# 	pass
# else:
# 	gengduo.click()

time.sleep(delayManual)
while True:
	downloadable = driver.find_elements_by_xpath("//*[@class='mlink minPx-top']")
	if not downloadable:
		time.sleep(delay)
	else:
		break

print('No of files: ' + str(len(downloadable)))

links = []
for downlinks in downloadable:
	links.append(downlinks.get_attribute('href'))

# print(links)
# link = links[0]
currentNumOfFile = 0;
for link in links :
	currentNumOfFile = currentNumOfFile + 1;
	driver.get(link)

	# options = webdriver.FirefoxOptions()
	# profile = webdriver.FirefoxProfile()
	# profile.set_preference("browser.download.folderList", 2)
	# profile.set_preference("browser.download.manager.showWhenStarting", False)
	# profile.set_preference('browser.helperApps.neverAsk.saveToDisk', 'application/pdf')
	# profile.set_preference("browser.download.dir", '~/Documents/webdriver/down/')
	# options.add_argument('--no-sandbox')
	# driver = webdriver.Firefox(options=options,firefox_profile=profile)
	# link = 'https://www.lanzoux.com/iwpjeh2rtsd'
	# driver.get("https://www.lanzoux.com/iwpjeh2rtsd")

	# BDY link

	while True:
		try:
			loadlink = driver.find_element_by_xpath("//*[@class='n_downlink']")
		except common.exceptions.NoSuchElementException:
			time.sleep(delay)
		else:
			break


	filename = driver.title
	filename = filename[:-6]
	print(str(currentNumOfFile) + '/' + str(len(downloadable)) + ': ' + filename)

	lk = loadlink.get_attribute('src')
	driver.get(lk)
	time.sleep(delayManual)
	bdylink = driver.find_element_by_xpath('//*[@href]')
	bdylink = bdylink.get_attribute('href')
	driver.get(bdylink)

	# Network error
	while True:
		try:
			# print(driver.page_source)
			authbtn = driver.find_element_by_xpath('//*[@class="submit"]')
		except common.exceptions.NoSuchElementException:
			time.sleep(delay)
		else:
			break

	time.sleep(delayManual)
	# print(driver.page_source)
	# authbtn.click()

	action = webdriver.common.action_chains.ActionChains(driver)
	action.move_to_element_with_offset(authbtn, 10, 10).click().perform()

	# Final download link
	time.sleep(delayManual)
	pdfbtn = driver.find_elements_by_xpath('//*[@href]')

	# time.sleep(2)
	# print(driver.page_source)
	# print(pdfbtn)
	# print(pdfbtn[0].get_attribute('href'))

	pdflink = pdfbtn[0].get_attribute('href')

	# driver.get(pdflink)
	r = requests.get(pdflink,allow_redirects=True)
	open(targetFolder+filename,'wb').write(r.content)
