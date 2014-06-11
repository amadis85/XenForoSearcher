import urllib2	
import cookielib
from BeautifulSoup import BeautifulSoup
import re

NICKNAME = 'StuffStore'

headers = { 'User-Agent' : 'Mozilla/5.0 (iPhone)' } 
cookiejar= cookielib.CookieJar() 
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookiejar)) 
urllib2.install_opener(opener) 
try:
	request = urllib2.Request('https://legalrc.biz/', None, headers)
	response = urllib2.urlopen(request)
	payload = response.read()
	soup = BeautifulSoup(payload)
except HTTPError as e:
    print 'The server couldn\'t fulfill the request.'
    print 'Error code: ', e.code
except URLError as e:
    print 'We failed to reach a server.'
    print 'Reason: ', e.reason
else:
	pass
    # everything is fine


#	Find all links of magazines from main page 
cell = soup.findAll('li', attrs={'class' : re.compile("node forum level_2")})
countMagazine = len(cell)
i = 0
print "All magazines load.\nQuantity of magazines: %i\n" % countMagazine 
#	Go to the magazine
for i in range(countMagazine):
	magazine = cell[i].find('a')
	magazine_link = magazine.attrs[0][1]
	magazine_description = magazine.text
	print("Searching in %i : %s" % (i, magazine_description)).encode('cp1251', errors='replace') #.encode('cp1252', errors='replace')
	request = urllib2.Request('https://legalrc.biz/' + magazine_link, None, headers)
	response = urllib2.urlopen(request)
	payload = response.read()
	soup = BeautifulSoup(payload)
	#	Find all links of themes from magazine page
	theme = soup.findAll('a', attrs={'href' : re.compile("threads/"), 'title' : '', 'class' : 'PreviewTooltip'})
	
	countTheme = len(theme)
	print "Finded %i themes" % countTheme
	j = 0
	#	Go to the theme
	for j in range(countTheme):
		print("\t%i : %i" % (i, j))
		theme_link = theme[j].attrs[0][1]
		theme_description = theme[j].text
		print("\tSearching in %i : %s" % (j, theme_description)).encode('cp1251', errors='replace') #.encode('cp1252', errors='replace')
		m = soup.findAll('a', attrs={'href' : re.compile(theme_link+"page-")})
#		print m
		if m:
			countPages = int(m[-1].text)
		else:
			countPages = 1
#		countPages = int(soup.findAll('a', attrs={'href' : re.compile(theme_link+"page-")})[-1].text)
		print "\tQuantity page in theme %i" % (countPages,)
		for page in range(1, countPages+1):
			if page == 1:
				final_link = 'https://legalrc.biz/' + theme_link
			else:
				final_link = 'https://legalrc.biz/' + theme_link + 'page-' + str(page)
			print "\t URL: " + final_link + "\n"
			request = urllib2.Request(final_link, None, headers)
			response = urllib2.urlopen(request)
			payload = response.read()
			soup_page = BeautifulSoup(payload)
			res_re = soup_page.body.findAll(text = re.compile('%s' % NICKNAME))
			if res_re:
				print "%i : %s" % (len(res_re), final_link)
			
		
# file('some.file', 'w').write(foo.encode('koi8-r'))