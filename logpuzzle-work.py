#!/usr/bin/python
# Copyright 2010 Google Inc.
# Licensed under the Apache License, Version 2.0
# http://www.apache.org/licenses/LICENSE-2.0

# Google's Python Class
# http://code.google.com/edu/languages/google-python-class/

import os
import re
import sys
import urllib.request

"""Logpuzzle exercise
Given an apache logfile, find the puzzle urls and download the images.

Here's what a puzzle url looks like:
10.254.254.28 - - [06/Aug/2007:00:13:48 -0700] "GET /~foo/puzzle-bar-aaab.jpg HTTP/1.0" 302 528 "-" "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.6) Gecko/20070725 Firefox/2.0.0.6"
"""
def get_key(rec_url):
    dash = re.search(r'([\w/]+)-(\w+).(\w+)',rec_url)
    if dash:
        print(dash.group(3))
        return dash.group(2)
    else:
        return rec_url

def read_urls(filename):
  """Returns a list of the puzzle urls from the given log file,
  extracting the hostname from the filename itself.
  Screens out duplicate urls and returns the urls sorted into
  increasing order."""
  # +++your code here+++
  """    
  link = re.search(r'_(\S+)',filename)
  if link:
        prefix = 'http://' + link.group(1)
        
  f = open(filename,'r')
  data = f.read()
  list_urls = re.findall(r'(\S+puzzle\S+)',data)
  
  suffix = sorted(list(set(list_urls)))

  imgid = re.search(r'([\S]+)(-)(\w+)(.jpg)',suffix[0])
  final_urls = []  
  if imgid:
      invrs_names = []  
      inv_suffix  = []
      for s in suffix:
            imgid = re.search(r'([\S]+)(-)(\w+)(.jpg)',s)
            invrs_names.append((imgid.group(1),imgid.group(2),imgid.group(3),imgid.group(4)))

      invrs_names.sort(key=get_key)          
      for name in invrs_names:
            dirc = ''
            dirc = name[0]+name[1]+name[2]+name[3]
            inv_suffix.append(dirc)
      for s in inv_suffix:
            final_urls.append(prefix+s)

            
#  for s in suffix:
#       final_urls.append(prefix+s)
#        print(s)
      
        
  return (final_urls)
  """


  #++++++++New Code Starts Here
  
  link = re.search(r'_(\S+)',filename)
  if link:
        prefix = 'http://' + link.group(1)
  
  url_dict = {}
  f = open(filename)
  for line in f:
        path = re.search(r'(\S+puzzle\S+)',line)
        if path:
            url_dict[prefix+path.group()] = 1            
  print(sorted(url_dict.keys(),key=get_key))
  sys.exit("END!!")
        
def download_images(img_urls, dest_dir):
  """Given the urls already in the correct order, downloads
  each image into the given directory.
  Gives the images local filenames img0, img1, and so on.
  Creates an index.html in the directory
  with an img tag to show each local image file.
  Creates the directory if necessary.
  """
  # +++your code here+++
  indx_file = re.search(r'(\w+)dir',dest_dir)
  indx_file_name = indx_file.group(1)+'index.html'  

  f_index = open(indx_file_name,"w+")
  f_index.write('<help>')
  f_index.write('<verbatim>\n<html>\n<body>\n>')

  if not os.path.exists(dest_dir):
    os.mkdir(dest_dir)    
  i=0
  print('Retriving.......')
  for url in img_urls:
        dest_path = dest_dir+'/img'+str(i)
        i+=1
        urllib.request.urlretrieve(url, dest_path)
        f_index.write('<img src="'+dest_path+'">')
  
  f_index.write('\n</body>\n</html>')
  f_index.close()
  
def main():
  args = sys.argv[1:]

  if not args:
    print('usage: [--todir dir] logfile ')
    sys.exit(1)

  todir = ''
  if args[0] == '--todir':
    todir = args[1]
    del args[0:2]

  img_urls = read_urls(args[0])

  if todir:
    download_images(img_urls, todir)
  else:
    print('\n'.join(img_urls))
  
  print("Process Completed!!!!!!!!!!")
if __name__ == '__main__':
  main()
