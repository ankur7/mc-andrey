import os
import re
import html5lib, lxml, lxml.cssselect
import requests

BASE_URL = 'http://search.azlyrics.com/search.php'

def get_top_result(title, artist):
  r = requests.get(BASE_URL,params={'q':title})
  raw_html = r.text
  page = html5lib.parse(raw_html,
                        treebuilder='lxml',
                        namespaceHTMLElements=False)

  # Find result with closest matching artist
  css_query = '.sen b'
  selector = lxml.cssselect.CSSSelector(css_query)
  match = selector(page)
  top_match = 100
  index = 0
  count = 0
  for m in match:
    if m.text is not None and m.text.upper() == m.text:
      lev_dist = levenshtein(m.text.lower(), artist.lower())
      if lev_dist < top_match:
        top_match = lev_dist
        index = count
      count+=1

  if top_match < 5:
    css_query = '.sen a'
    selector = lxml.cssselect.CSSSelector(css_query)
    match = selector(page)
    if index < len(match):
      return ''.join([char for char in match[index].get('href')])
  return None

def extract_lyrics(url):
  if url is None:
    return None

  r = requests.get(url)
  raw_html = r.text
  start_index = raw_html.find('<!-- start of lyrics -->')
  end_index = raw_html.find('<!-- end of lyrics -->')
  lyrics = raw_html[start_index+24:end_index]
  # Remove html tags
  lyrics = re.sub('<[^<]+?>', '', lyrics)
  # Remove things in brackets
  lyrics = re.sub('\[.+?\]', '', lyrics)
  # Remove things in parens
  lyrics = re.sub('\(.*?\)', '', lyrics)
  # Remove empty lines/newlines
  lyrics = os.linesep.join([s for s in lyrics.splitlines() if s])
  return lyrics

def save_lyrics(skip=0):
  f = open('top100raw')
  entries = f.readlines()
  entries = entries[skip:]
  for entry in entries:
    rank, artist, title = entry.split('|')
    title = title.rstrip('\n')
    lyrics_url = get_top_result(title, artist)
    lyrics = extract_lyrics(lyrics_url)
    if lyrics is not None:
      fo = open("../songdump/%s-%s-%s" % (rank, artist, title), "wb")
      fo.write(lyrics)
      fo.close()
  f.close()

def levenshtein(s1, s2):
  s1 = s1.lower()
  s2 = s2.lower()
  dex1 = s1.find(' ft. ')
  if(dex1 != -1):
    s1 = s1[0:dex1]
  dex2 = s2.find(' ft. ')
  if(dex2 != -1):
    s2 = s2[0:dex1]

  dex1 = s1.find(' & ')
  if(dex1 != -1):
    s1 = s1[0:dex1]
  dex2 = s2.find(' & ')
  if(dex2 != -1):
    s2 = s2[0:dex1]

  if len(s1) < len(s2):
    return levenshtein(s2, s1)

  if len(s2) == 0:
    return len(s1)

  previous_row = xrange(len(s2) + 1)
  for i, c1 in enumerate(s1):
    current_row = [i + 1]
    for j, c2 in enumerate(s2):
      insertions = previous_row[j + 1] + 1
      deletions = current_row[j] + 1
      substitutions = previous_row[j] + (c1 != c2)
      current_row.append(min(insertions, deletions, substitutions))
    previous_row = current_row

  return previous_row[-1]