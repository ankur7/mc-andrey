import re
import html5lib, lxml, lxml.cssselect
import requests

BASE_URL = 'http://rap.about.com/od/top10songs/ss/Top100RapSongs_'

def extract_song_names(page):
  if page == 1:
    scrape_URL = 'http://rap.about.com/od/top10songs/ss/Top100RapSongs.htm'
  else:
    scrape_URL = BASE_URL + '%s.htm' % page
  r = requests.get(scrape_URL)
  raw_html = r.text
  page = html5lib.parse(raw_html,
                        treebuilder='lxml',
                        namespaceHTMLElements=False)

  css_query = '#articlebody p b'
  selector = lxml.cssselect.CSSSelector(css_query)
  match = selector(page)
  entries = []
  for m in match:
    entries.append(extract_fields(m.text))
  return entries

def extract_fields(str):
  str = re.sub('<a href="http://[a-zA-Z0-9/.]+>', '', str)
  rank_match = '^[0-9]{1,3} |'
  rank = re.findall(rank_match, str)[0].strip()

  if rank == '72':
    return ('', '', '')

  artist_match = ' [a-zA-Z0-9.,&+;\'$\- ]+ -'
  artist = re.findall(artist_match, str)[0][:-1].strip()


  start_index = str.find(artist) + len(artist) + 4
  title = str[start_index:-1]
  if title.endswith('"'):
    title = title[:-1]
  return (rank, artist, title)

def scrape_top_100():
  fo = open("top100raw", "wb")
  page = 1
  master_list = []
  while(page < 11):
    print page
    entries = extract_song_names(page)
    master_list += entries
    page+=1

  for entry in master_list:
    rank, artist, title = entry
    if(len(rank) > 0):
      fo.write(rank + '|' + artist + '|' + title+'\n')
  fo.close()

scrape_top_100()