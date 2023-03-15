import json

#input file path
inputFile = open('trace_inception.json')
data = json.load(inputFile)
lst = data['traceEvents']
#Filter JSON result with keys
keys = ['name','dur']
omitNames = ['NoOp', '_Arg', '_Retval']
filteredLst = []
for d in lst:
  filteredRes = {}
  if d['name'] in omitNames:
    continue
  if 'dur' in d:
    for key in keys:
      filteredRes[key]=d[key]
    filteredLst.append(filteredRes)
  else:
    continue
#Calculate total time taken by each layer
resLst={}
totalTime = 0
for d in filteredLst:
  if d['name'] not in resLst.keys():
    resLst[d['name']]=0
  resLst[d['name']]+=int(d['dur'])
  totalTime+=int(d['dur'])
#Sorting data in descending order
resLst=dict(sorted(resLst.items(), key=lambda x:x[1], reverse=True))
totalTime=totalTime/1000
tmplst = resLst.copy()
for key in resLst:
  resLst[key]/=1000
  resLst[key]=str(resLst[key])+'ms'
#Display resLst	
print('==============================================================')
print('Time taken by each layer')
print('==============================================================')
for key in resLst:
  print(key,' :',resLst[key])
  
#Calculate percentage taken by each layer
print('==============================================================')
print('Percentage List for each layer')
print('==============================================================')
for key in tmplst:
  tmplst[key]/=1000
  print(key,' :',round((tmplst[key]/totalTime)*100, 2),'%')
print('==============================================================')
print('Total Time Taken: ',totalTime,'ms')
print('==============================================================')

inputFile.close()
