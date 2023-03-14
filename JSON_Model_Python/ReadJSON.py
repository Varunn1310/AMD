import json

f = open('trace_inception.json')

data = json.load(f)

lst = data['traceEvents']

keys = ['name','dur']
newlst = []
for d in lst:
  newres = {}
  if 'dur' in d:
    for key in keys:
      newres[key]=d[key]
    newlst.append(newres)
  else:
    continue

newlst1={}
total = 0
for d in newlst:
  if d['name'] not in newlst1.keys():
    newlst1[d['name']]=0
  newlst1[d['name']]+=int(d['dur'])
  total+=int(d['dur'])

newlst1=dict(sorted(newlst1.items(), key=lambda x:x[1], reverse=True))
total=total/1000
tmplst = newlst1.copy()
for key in newlst1:
  newlst1[key]/=1000
  newlst1[key]=str(newlst1[key])+'ms'	    
print(newlst1)

print('Percentage List for each layer')
for key in tmplst:
  tmplst[key]/=1000
  print(key,' :',(tmplst[key]/total)*100,'%')

print('Total Time Taken: ',total,'ms')

f.close()
