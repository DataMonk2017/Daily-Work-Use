# Learning Script
## This is a file to record every point.

```python
####################################################################################
#list all files end with 'txt' in Python
# way 1
import os
for file in os.listdir("/mydir"):
    if file.endswith(".txt"):
        print(os.path.join("/mydir", file))
#way 2
import glob, os
os.chdir("/mydir")
for file in glob.glob("*.txt"):
    print(file)


#or if you want to traverse directory, use os.walk:
import os
for root, dirs, files in os.walk("/mydir"):
    for file in files:
        if file.endswith(".txt"):
             print(os.path.join(root, file))    
             
             
             
####################################################################################
#get the request info before sending out
import requests

req = requests.Request('POST','http://stackoverflow.com',headers={'X-Custom':'Test'},data='a=1&b=2')
prepared = req.prepare()

def pretty_print_POST(req):
    """
    At this point it is completely built and ready
    to be fired; it is "prepared".

    However pay attention at the formatting used in 
    this function because it is programmed to be pretty 
    printed and may differ from the actual request.
    """
    print('{}\n{}\n{}\n\n{}'.format(
        '-----------START-----------',
        req.method + ' ' + req.url,
        '\n'.join('{}: {}'.format(k, v) for k, v in req.headers.items()),
        req.body,
    ))

pretty_print_POST(prepared)

#then use the result to send 
s = requests.Session()
s.send(prepared)

####################################################################################
# find tags with only certain attributes
soup = BeautifulSoup(html)
results = soup.findAll("td", {"valign" : "top"})

#To return tags that have only the valign="top" attribute, you can check for the length of the tag attrs property :
from BeautifulSoup import BeautifulSoup

html = '<td valign="top">.....</td>\
        <td width="580" valign="top">.......</td>\
        <td>.....</td>'

soup = BeautifulSoup(html)
results = soup.findAll("td", {"valign" : "top"})

for result in results :
    if len(result.attrs) == 1 :
        print result

####################################################################################
#dump json file
#provided that the object only contains objects that JSON can handle (lists, tuples, strings, dicts, numbers, None, True and False), you can dump it as json.dump:

import json
with open('outputfile', 'w') as fout:
    json.dump(your_list_of_dict, fout)
    

####################################################################################
#replace
str1.replace('letterneedtoreplace','letteryouwanttouse')

####################################################################################
#reading the whole content
file.read()

####################################################################################
#get dict keys
dict1.keys()


####################################################################################
'''
python unicode:
this problem is a big headache. when trying to save a file, you had better ignore errors. For example,
more advanced option:
https://stackoverflow.com/questions/14630288/unicodeencodeerror-charmap-codec-cant-encode-character-maps-to-undefined

'''
with open(filename, 'r',encoding='utf-8',errors = 'ignore') as f:
    data = f.readlines()
    
#when you are trying to save a response to a file from html, you could get the encoding of the html as follows:
# useful link: https://stackoverflow.com/questions/14592762/a-good-way-to-get-the-charset-encoding-of-an-http-response-in-python
# https://stackoverflow.com/questions/5419/python-unicode-and-the-windows-console/32176732#32176732

response = requests.get(link)
response.encoding #utf-8
#Then you use the encoding response in saving files. or
r.text # may use `chardet` to auto-detect encoding

```
