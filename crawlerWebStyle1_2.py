from selenium import webdriver , common
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
import time
import os
import requests
delay = 1.0
delayManual = 3.0;

# INPUT section ==========
webUrl = "https://www.lanzoux.com/b015fte9e";
password = "arm0";
targetFolder = "."
# ========================

# Making folder
targetFolder = './' + targetFolder + '/'
if not os.path.exists(targetFolder):
	os.makedirs(targetFolder)

# Open website
options = webdriver.FirefoxOptions()
# # options.add_argument('--no-sandbox')
driver = webdriver.Firefox(options=options)
driver.get(webUrl)

# Password input
if password:
	while True:
		try:
			pwd = driver.find_element_by_name("pwd")
		except common.exceptions.NoSuchElementException:
			time.sleep(delay)
		else:
			break
	pwd.send_keys(password)

	while True:
		try:
			btnpwd = driver.find_element_by_xpath("//*[@class='btnpwd']")
		except common.exceptions.NoSuchElementException:
			time.sleep(delay)
		else:
			break
	btnpwd.click()
else:
	print('No pwd')


# list more ----------
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

#  ----------

# Get download links
time.sleep(delayManual)
while True:
	downloadable = driver.find_elements_by_xpath("//*[@target='_blank']")
	if not downloadable:
		time.sleep(delay)
	else:
		break

links = []
for downlinks in downloadable:
	links.append(downlinks.get_attribute('href'))

links = links[1:-1]
print('No of files: ' + str(len(links)))
# print(links)

# Accessing each indivisual links
currentNumOfFile = 0
for link in links:
	currentNumOfFile = currentNumOfFile + 1
	driver.get(link)

	# Getting filename
	while True:
		try:
			filename = driver.title
		except common.exceptions.NoSuchElementException:
			time.sleep(delay)
		else:
			break
	filename = filename[:-6]
	print(str(currentNumOfFile) + '/' + str(len(links)) + ': ' + filename)

	# getting src link
	while True:
		try:
			btn3Links = driver.find_element_by_xpath("//*[@class='ifr2']")
		except common.exceptions.NoSuchElementException:
			time.sleep(delay)
		else:
			break
	src = btn3Links.get_attribute('src')
	driver.get(src)

	# getting vip.d0.baidupan link
	while True:
		try:
			baidupanLinkTemp = driver.find_element_by_xpath("//*[@rel='noreferrer']")
		except common.exceptions.NoSuchElementException:
			time.sleep(delay)
		else:
			break
	baidupanLink = baidupanLinkTemp.get_attribute('href')
	driver.get(baidupanLink)

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
	pdflink = pdfbtn[0].get_attribute('href')

	# download
	r = requests.get(pdflink,allow_redirects=True)
	open(targetFolder+filename,'wb').write(r.content)
