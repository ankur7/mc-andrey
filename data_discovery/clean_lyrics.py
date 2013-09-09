from os import listdir
from os.path import isfile, join

def supercat(dir):
  onlyfiles = [ f for f in listdir(dir) if isfile(join(dir,f)) ]
  combined_files = open('combined_all_raw', 'wb')
  for filename in onlyfiles:
    temp = open('C:\Users\Shahid Chohan\Desktop\mcandrey\songdump\\'+filename)
    combined_files.write(temp.read())
    temp.close()
  combined_files.close()

def remove_short_sentences(file):
  f = open(file)
  lines = f.readlines()
  f.close()
  cleaned = open('combined_all_cleaned', 'wb')
  import string
  exclude = set(string.punctuation)
  for line in lines:
    if(len(line.split(' ')) > 4):
      line = ''.join(ch for ch in line if ch not in exclude)
      line = ' '.join(line.split()) + '\n'
      cleaned.write(line)
  cleaned.close()

supercat('C:\Users\Shahid Chohan\Desktop\mcandrey\songdump')
remove_short_sentences('combined_all_raw')