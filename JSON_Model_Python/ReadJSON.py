import json

f = open('trace_inception.json')

data = json.load(f)

lst = data['traceEvents']
keyList = ['_Zen','Zen']
res = [d for d in lst for key in keyList if key in d['name']]
keys = ['name','dur']
newlst = []
for d in res:
  newres = {}
  for key in keys:
    newres[key]=d[key]
  newlst.append(newres)

newlst1={}

for d in newlst:
  if d['name'] not in newlst1.keys():
    newlst1[d['name']]=0
  newlst1[d['name']]+=int(d['dur'])

for key in newlst1:
  newlst1[key]/=1000
  newlst1[key]=str(newlst1[key])+' ms'	    
print(newlst1)

f.close()
