#!/usr/bin/env python
# encoding: utf-8

### Outputs 3 csv files:
###   dataset_yelp: Our dataset that we will split into training and validation
###   dataset_unknown: Our test dataset (includes review_text that were AFTER last review period, so we have no label!
###   dataset_rejects: Yelp restaurants that for some reason or other did not have health scores on site. We do not include in our main dataset.

import string
import urllib2
from bs4 import BeautifulSoup
import re
import re
import csv
import time
import datetime
#from nltk.corpus import stopwords
import nltk
import time


def check_url_exists(ur):
    try:
        urllib2.urlopen(ur)
        return True
    except urllib2.HTTPError:
        return False
    except urllib2.URLError:
        return False

# returns a list of lists, each sublist being a page of reviews of a restaurant
def get_urls(csv_rejects):
    # below 5 pages of reviews, standard
    #urls=['http://www.yelp.com/biz/chicos-pizza-san-francisco']
    # below is a quick test, only 40 reviews
    #urls=['http://www.yelp.com/biz/lucky-ocean-cafe-san-francisco']
    # below url has no yelp inspections on site
    #urls=['http://www.yelp.com/biz/ocean-pearl-restaurant-san-francisco']
    #urls=['http://www.yelp.com/biz/quickly-san-francisco-12']
    #below url has 100 score
    #urls=['http://www.yelp.com/biz/state-bird-provisions-san-francisco']

    #below is mix of 100 and lesser scores
    #urls=['http://www.yelp.com/biz/lite-bite-san-francisco']

    #below is restaurant with no reviews
    #urls=['http://www.yelp.com/biz/greenlid-studiomix-san-francisco']

    #below is restaurant with no inspec socre
    #urls=['http://www.yelp.com/biz/blue-c-sushi-san-francisco']

    # one inspection only (no table)
    #urls=['http://www.yelp.com/biz/causwells-san-francisco-5']

    #urls=['http://www.yelp.com/biz/chicos-pizza-san-francisco', 'http://www.yelp.com/biz/state-bird-provisions-san-francisco',
    #        'http://www.yelp.com/biz/blue-c-sushi-san-francisco', 'http://www.yelp.com/biz/greenlid-studiomix-san-francisco',
    #        'http://www.yelp.com/biz/rickybobby-san-francisco', 'http://www.yelp.com/biz/kitchen-story-san-francisco',
    #        'http://www.yelp.com/biz/v-105-san-francisco', 'http://www.yelp.com/biz/dinosaurs-san-francisco',
    #        'http://www.yelp.com/biz/mau-san-francisco', 'http://www.yelp.com/biz/bar-tartine-san-francisco',
    #        'http://www.yelp.com/biz/zero-zero-san-francisco','http://www.yelp.com/biz/lolinda-san-francisco',
    #        'http://www.yelp.com/biz/straw-san-francisco','http://www.yelp.com/biz/causwells-san-francisco-5']

    #urls=['http://www.yelp.com/biz/zero-zero-san-francisco','http://www.yelp.com/biz/l-ardoise-bistro-san-francisco',
    #        'http://www.yelp.com/biz/grubbin-san-francisco','http://www.yelp.com/biz/wooly-pig-cafe-san-francisco',
    #        'http://www.yelp.com/biz/plow-san-francisco','http://www.yelp.com/biz/marcellas-lasagneria-san-francisco',
    #        'http://www.yelp.com/biz/deli-board-san-francisco','http://www.yelp.com/biz/ty-sandwich-san-francisco',
    #        'http://www.yelp.com/biz/v-105-san-francisco']

    """
    fileurls = open('/home/jasonmach/project/yelp_predictor/jason_url.txt', 'r')
    urls = []
    for line in fileurls.readlines():
        urls.append(line.strip(' \n'))
        urls = urls[0:5]
    """
    # up to page 54 of yelp search for only $ filter, only seleted restaurants with between 10-200 reviews
    """
    urls=['http://www.yelp.com/biz/pastel-do-brazil-san-francisco-2','http://www.yelp.com/biz/choice-yakiniku-san-francisco','http://www.yelp.com/biz/tacos-club-san-francisco',
            'http://www.yelp.com/biz/two-sons-sandwiches-san-francisco','http://www.yelp.com/biz/diamond-cafe-san-francisco',
            'http://www.yelp.com/biz/dragoneats-san-francisco','http://www.yelp.com/biz/front-cafe-san-francisco',
            'http://www.yelp.com/biz/paulies-pickling-san-francisco','http://www.yelp.com/biz/la-espiga-de-oro-san-francisco',
            'http://www.yelp.com/biz/pop-up-cafe-san-francisco-4','http://www.yelp.com/biz/cholo-soy-san-francisco',
            'http://www.yelp.com/biz/jbs-place-san-francisco','http://www.yelp.com/biz/jonas-on-hyde-san-francisco',
            'http://www.yelp.com/biz/little-heaven-deli-san-francisco','http://www.yelp.com/biz/eleven-o-one-san-francisco',
            'http://www.yelp.com/biz/the-morning-fix-san-francisco','http://www.yelp.com/biz/cindys-market-san-francisco',
            'http://www.yelp.com/biz/back-yard-kitchen-san-francisco','http://www.yelp.com/biz/red-chilli-san-francisco',
            'http://www.yelp.com/biz/taqueria-cazadores-san-francisco-2','http://www.yelp.com/biz/red-sea-market-san-francisco',
            'http://www.yelp.com/biz/mexico-tipico-san-francisco-2','http://www.yelp.com/biz/pauls-deli-san-francisco',
            'http://www.yelp.com/biz/pops-sandwich-shop-san-francisco','http://www.yelp.com/biz/fresh-bay-cafe-san-francisco',
            'http://www.yelp.com/biz/lunch-geek-san-francisco','http://www.yelp.com/biz/clanceys-market-and-deli-san-francisco',
            'http://www.yelp.com/biz/cole-valley-cafe-san-francisco','http://www.yelp.com/biz/mint-cafe-san-francisco',
            'http://www.yelp.com/biz/taqueria-castillo-mason-san-francisco','http://www.yelp.com/biz/heung-yuen-restaurant-san-francisco',
            'http://www.yelp.com/biz/sun-kwong-restaurant-san-francisco','http://www.yelp.com/biz/el-taco-loco-the-original-san-francisco',
            'http://www.yelp.com/biz/alamo-square-cafe-san-francisco','http://www.yelp.com/biz/sutter-cafe-san-francisco',
            'http://www.yelp.com/biz/j-and-a-restaurant-san-francisco','http://www.yelp.com/biz/el-paraiso-cafe-san-francisco',
            'http://www.yelp.com/biz/el-castillito-taqueria-san-francisco','http://www.yelp.com/biz/henrys-cafe-and-deli-san-francisco-2',
            'http://www.yelp.com/biz/garage-cafe-san-francisco','http://www.yelp.com/biz/el-rancho-grande-san-francisco',
            'http://www.yelp.com/biz/slider-shack-san-francisco','http://www.yelp.com/biz/fog-lifter-cafe-san-francisco',
            'http://www.yelp.com/biz/whats-up-dog-san-francisco-12','http://www.yelp.com/biz/le-petitts-kitchen-san-francisco-2',
            'http://www.yelp.com/biz/grove-street-market-san-francisco','http://www.yelp.com/biz/boudin-sourdough-bakery-and-cafe-san-francisco-16',
            'http://www.yelp.com/biz/la-paz-restaurant-pupuseria-san-francisco','http://www.yelp.com/biz/la-laguna-taqueria-san-francisco',
            'http://www.yelp.com/biz/sweet-joannas-cafe-san-francisco-2','http://www.yelp.com/biz/la-quinta-restaurant-san-francisco',
            'http://www.yelp.com/biz/mura-san-francisco','http://www.yelp.com/biz/the-little-spot-cafe-san-francisco',
            'http://www.yelp.com/biz/deli-and-san-francisco-5','http://www.yelp.com/biz/el-tepa-taqueria-san-francisco',
            'http://www.yelp.com/biz/kui-shin-bo-san-francisco-2','http://www.yelp.com/biz/reaction-restaurant-san-francisco-2',
            'http://www.yelp.com/biz/elsys-restaurant-san-francisco','http://www.yelp.com/biz/bread-and-butter-cafe-san-francisco-2',
            'http://www.yelp.com/biz/gourmet-kitchen-san-francisco','http://www.yelp.com/biz/hongry-kong-truck-san-francisco'
            'http://www.yelp.com/biz/peter-ds-san-francisco','http://www.yelp.com/biz/the-hollow-cow-market-san-francisco',
            'http://www.yelp.com/biz/new-college-hill-market-san-francisco','http://www.yelp.com/biz/jins-cafe-san-francisco',
            'http://www.yelp.com/biz/sungari-dumpling-house-san-francisco-2']
    """
    urls = ['http://www.yelp.com/biz/missions-kitchen-san-francisco',
	'http://www.yelp.com/biz/the-store-on-the-corner-san-francisco',
	'http://www.yelp.com/biz/cafe-francisco-san-francisco-2',
	'http://www.yelp.com/biz/milan-pizza-san-francisco',
	'http://www.yelp.com/biz/the-mayflower-restaurant-san-francisco',
	'http://www.yelp.com/biz/altena-restaurant-san-francisco',
	'http://www.yelp.com/biz/great-saigon-restaurant-san-francisco',
	'http://www.yelp.com/biz/taqueria-mana-san-francisco',
	'http://www.yelp.com/biz/jt-restaurant-and-catering-san-francisco',
	'http://www.yelp.com/biz/los-guanacos-san-francisco',
	'http://www.yelp.com/biz/palacio-latino-san-francisco']


    all_urls = []
    for item in urls:
        print item
        if check_url_exists(item + '?sort_by=date_desc') == False:
            print 'WHAT? Restuarant URL doesnt exist apparently'
            continue
        counter = 40
        iter = 1
        temp = []
        temp.append(item + '?sort_by=date_desc')
        html = urllib2.urlopen(item + '?sort_by=date_desc').read()
        soup = BeautifulSoup(html)
        page = soup.find('div', {"class":"page-of-pages"})

        # restaurant has no reviews, skip and add to rejects
        if page == None:
            title = soup.find('h1',itemprop="name")
            name = title.text.encode("utf-8").strip(' \t\n\r').replace('|',' ')
            csv_rejects.writerow(name)
            continue

        while iter < int(page.text.split()[-1]):
            new_url = item + '?start=' + str(counter) + '&sort_by=date_desc'
            if check_url_exists(new_url):
                temp.append(new_url)
            counter += 40
            iter += 1
        all_urls.append(temp)
        time.sleep(20)
    print 'Master list ready...'
    return all_urls

# takes a url and scrapes attributes we want from the html, writes to csv
def scrape(urls, filer, filer_real,iattrib):

    # if site has no inspection
    no_inspec = False
    if iattrib == None:
        no_inspec = True

    # each item in param_map is a list, where each item is  [INSPEC#, NEW_DATE, OLD_DATE, [6_PARAMS]]
    param_map = []

    # item here is (DATE, [6 PARAMS] )
    # list is ordered, so first item in the list is the newest DATE - inspection
    p = 0
    if not no_inspec:
      while p < len(iattrib):
	  if p == len(iattrib) - 1:
	      param_map.append( [p, iattrib[p][0] , str(datetime.date(1900,1,1)), iattrib[p][1] ] )
	  else:
	      param_map.append( [p, iattrib[p][0] , iattrib[p+1][0], iattrib[p][1] ] )
	  p += 1

      # full_map is the final, each key in full_map is the numbered inspection, value is [ [6 PARAMS], REVIEW_CORPUS, RATING_AVG, review_count ]
      full_map = {}

      unknown_map = {}
      unknown_map[-1] = [ param_map[0][3], '', 0, 0]

      # initiliaze dict
      for item in param_map:
	  full_map[item[0]] = [item[3], '', 0 , 0]

    review_count = 0
    x = 0
    for ur in urls:
	x += 1
	print ("HIT " + str(x))
	print ur
        html = urllib2.urlopen(ur).read()
	soup = BeautifulSoup(html)
	title = soup.find('h1',itemprop="name")
	reviews = soup.findAll('p',itemprop='description')
        ratings = soup.findAll('meta', {"itemprop":"ratingValue"})
        dates = soup.findAll('meta', {"itemprop":"datePublished"})
        
        category = soup.find('meta',{"property":"og:description"})['content'].encode("utf-8").strip(' \t\n\r')

	price_category = soup.find('dd',{"class":"nowrap price-description"}).text.encode('utf-8').strip(' \t\n\r')

	name = title.text.encode("utf-8").strip(' \t\n\r').replace('|',' ')
	total_rating = float( ratings[0]['content'] )

        if reviews == None:
            print "This should not have happened, restaurant has no reviews even though it passed first check"

        # for case of no yelp inspection
        review_agg = ''

	i = 0
	while (i < len(reviews)):
	    rating = float( ratings[i+1]['content'] )
	    date = dates[i]['content'] 
	    review_text = reviews[i].text.encode("utf-8").replace('|',' ').replace('\n',' ').replace('-', ' ').replace('.','. ').replace('  ',' ').strip(' \t\n\r')
            
            # feature select from review_text
            review_text = select_features(review_text)

            if not no_inspec:
              flag = True
	      for item in param_map:
                  # this is the unknown data, no labels cuz no inspection!
                  if flag and date > item[1]:
		      unknown_map[-1][3] += 1
		      unknown_map[-1][1] = unknown_map[-1][1] + ' ' + review_text
		      unknown_map[-1][2] += rating
                      flag = False
		  if date < item[1] and date >= item[2]:
		      full_map[item[0]][3] += 1
		      full_map[item[0]][1] = full_map[item[0]][1] + ' ' + review_text
		      full_map[item[0]][2] += rating 
            else:
                review_agg = review_agg + ' ' + review_text
	    i += 1
            review_count += 1

    if not no_inspec:
      for key,val in full_map.iteritems():
          # if it equals 0, that means there were no reviews for that time period... we lost a sample :(
          if val[3] != 0:
              filer.writerow( [name + ' ' + str(key),total_rating,category,price_category,review_count,key,val[2] / float(val[3]),val[1]] + val[0] ) 

      if unknown_map[-1][3] != 0:
          filer_real.writerow( [name,total_rating,category,price_category,review_count,-1,unknown_map[-1][2] / float(unknown_map[-1][3]),unknown_map[-1][1]] ) 
    else:
          filer_real.writerow( [name,total_rating,category,price_category,review_count,-1,total_rating,review_agg] ) 

# use 10 feature selection principles from http://cs.brown.edu/courses/csci1951-a/assignments/assignment3/
# ahead of time so that classifier has to deal with less clutter
def select_features(text):
    # 1. lower-case all characters
    #text = text.lower()

    # 2. Strip punctuations
    #text = text.translate(string.maketrans("",""), string.punctuation)

    # 3. Use the stop words list to filter out low value words such as 'the', 'is' and 'on'.
    # modify stop words, as nlkt includes negatives like 'no' in list, which we want to use with n-gram feature extraction
    #stop = stopwords.words('english')
    #stop.remove('no')
    #stop.remove('not')
    #text = " ".join([i for i in text.split(" ") if i not in stop])

    # 4. Replace two or more occurrences of the same character with two occurrences. i.e. 'exciteddddd' to 'excitedd'
    text = re.sub(r'(.)\1{2,}', r'\1', text)

    # 5. remove all numeric characters from string
    text = re.sub("\d+", "", text)

    # 6. Apply stemming using Porter Stemmer
    #myPorterStemmer = nltk.stem.porter.PorterStemmer()
    #text =  " ".join([myPorterStemmer.stem(word) for word in text.strip(" ")])

    return text


# scrapes the yelp inspection page for each restaurant, returns a list of attributes for scrape() to write to csv
# the reason this isn't performed in scrape() is so a GET request isn't sent for every suburl, only once per restaurant
def scrape_inspection(ur):
    temp = []
    html = urllib2.urlopen(ur).read()
    soup = BeautifulSoup(html)
    recent_inspec_score = soup.find('span',{"class":"score"})
    checker = soup.findAll('td', {"class":"violations text-center"})
    header = soup.find('p', {"class":"catcher"})
    
    recent_inspec = header.text.split('—'.decode('utf-8'))[0].strip(' \t\n\r')
    recent_inspec_type = header.text.split('—'.decode('utf-8'))[1].strip(' \t\n\r')
    number_inspections = 0
   
    if checker != None:
        number_inspections = len(checker) + 1
    else:
        if header != None:
            number_inspections = 1

    factors = time.strptime(recent_inspec.replace(",",""), "%B %d %Y")
    recent_inspec_rd = str(datetime.datetime(factors[0], factors[1], factors[2])).split()[0]

    first_inspec_vio_count = 0
    vio = soup.find("div",{"class":"column column-alpha "}).find('ul', {"class":"bullet-list-square violations-list"})

    recent_inspec_vio = ''
    if soup.findAll("p")[1].text.encode('utf-8').strip(' \t\n\r') == "This inspection has no violations.":
        recent_inspec_vio = 'This inspection has no violations.'
    else:
        lister = vio.findAll('li')
        for violation in lister:
            first_inspec_vio_count += 1
            recent_inspec_vio = recent_inspec_vio + ' ' + violation.text.encode("utf-8").strip(' \t\n\r')

    # for the most recent inspection(different format than the rest)
    temp.append((recent_inspec_rd,
                [number_inspections, 
                 int(recent_inspec_score.text), 
                 first_inspec_vio_count, 
                 recent_inspec_type, 
                 recent_inspec_vio])
                )

    # for all other inspections
    k = 0
    table = soup.find("table", {"id":"inspections-table"})
    # there was only one inspection
    if table:
        date_wrapper = table.findAll("td",{"class":"violations text-center"})
        score_wrapper = table.findAll("td",{"class":"text-center"})
        bodies = table.findAll("tr")
        while k < number_inspections - 1:
            score = int( bodies[k+1].findAll("td")[4].text.encode("utf-8").strip(' \t\n\r') )

            inspec_type = bodies[k+1].findAll("td")[1].text.encode("utf-8").strip(' \t\n\r')

            #datea = date_wrapper[k].find("b").text.encode('utf-8').strip(' \t\n\r')
            datea = bodies[k+1].findAll("td")[0].text.encode("utf-8").strip(' \t\n\r')
            dateb = time.strptime(datea.replace(",",""), "%B %d %Y")
            datec = str(datetime.datetime(dateb[0], dateb[1], dateb[2])).split()[0]

            vio_count = 0
            rata = date_wrapper[k].find("span",{"class":"violations-count"})
            if rata != None:
                vio_count = int( date_wrapper[k].find("span",{"class":"violations-count"}).text )

            viol = ''
            if  vio_count == 0:
                viol = 'This inspection has no violations.'
            else:
                lister = bodies[k+1].find("ul",{"class":"bullet-list-square violations-list"})
                for violation in lister.findAll("li"):
                    viol = viol + ' ' + violation.text.encode("utf-8").strip(' \t\n\r').replace('|',' ')
       
            temp.append((datec, 
                        [number_inspections, 
                            score,
                            vio_count,
                            inspec_type,
                            viol])
                        )
            k += 1

    # temp is a list of tuples, where each object is (date, [6 PARAMS] )
    return temp

# iteratres through a list of urls, and deeper into suburls, each suburl is a page of reviews
def main():
    f = csv.writer(open("/home/jasonmach/project/yelp_predictor/dataset_yelp.csv", "a"),delimiter='|')
    fbad = csv.writer(open("/home/jasonmach/project/yelp_predictor/dataset_rejects.csv", "a"))
    fbad.writerow(["rejects"])
    freal = csv.writer(open("/home/jasonmach/project/yelp_predictor/dataset_unknown.csv", "a"),delimiter='|')
    f.writerow(["name","total_rating","category","price_category","number_reviews","inspec_period","period_rating","review_text", 
                "number_inspections","health_score","number_violations","inspec_type","inspec_vio","verdict"])
    freal.writerow(["name","total_rating","category","price_category","number_reviews","inspec_period","period_rating","review_text", 
                "number_inspections","health_score","number_violations","inspec_type","inspec_vio","verdict"])
    counter = 1
    temp = get_urls(fbad)
    total_restaurants = len(temp)
    for items in temp:
        time.sleep(20)
        inter = items[0].split('?', 1)[0] 
        inspection_url = inter.replace('biz', 'inspections')
        if check_url_exists(inspection_url) == True:
            inspectors = scrape_inspection(inspection_url)
            scrape(items, f, freal, inspectors)
        else:
            # if there is no health ratings on yelp, add restaurant to test set
            inspectors = None
            scrape(items, f, freal, inspectors)
        print 'Site ' + str(counter) + ' out of ' + str(total_restaurants) + ' done'
        counter += 1
    print 'Operation completed...!'

if __name__ == "__main__":
    main()

