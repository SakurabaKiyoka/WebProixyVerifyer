import requests
import asyncio
import aiohttp
import json
print("Downloading the proxylist...please wait...")
# The proxylist raw json data.
url = r'https://raw.githubusercontent.com/fate0/proxylist/master/proxy.list'
# You can modify the url to what you want to test.If your network is no problem,but you can see only fail or bad,please try to manually modify it.
testurl = r'http://katfile.com/rvgso7bl9xe1/DJSOUND-181022-RJ236247-991F7E3E_1.part1.rar.html'# just for demo,you can modify it for anyother page.
timeouttime = 8  # seconds
blackwords = [
    'disconnect',
    'banned',
    'denied',
    'locked',
    'forbidden',
    'Please complete',
    '429 Too',
    'Delay between',
    'is not available',
    'blocked'
    #'blackwords', at the end of list,please don't add ",". 
]

r = requests.get(url)  # Temp data of fetched data.
with open('proxy.json', 'wb') as f:  # open file to storage the fetched data.
    f.write(r.content)  # write to file
data = []  # set a empty list
with open('proxy.json') as fi:  # load file
    for line in fi:
        data.append(json.loads(line))  # load file's each line to the data list

with open('listall.txt', 'w') as fa:  # create file
    i = 0  # loop initialization
    while i < len(data):  # set max loop times
        fa.write(str(data[i]['type'])+"://"+str(data[i]['host'])+":" +
                 str(data[i]['port'])+'\n')  # write the decoded data to file
        i += 1

with open('listipport.txt', 'w') as fip:  # create file
    j = 0  # loop initialization
    while j < len(data):  # set max loop times
        # write the decoded data to file
        fip.write(str(data[j]['host'])+":"+str(data[j]['port'])+'\n')
        j += 1

with open('list.csv', 'w') as fcsv:  # create file
    k = 0  # loop initialization
    fcsv.write("host,port,country,type,response_time\n")  # output csv header
    while k < len(data):  # set max loop times
        fcsv.write(str(data[k]['host'])+","+str(data[k]['port'])+","+str(data[k]['country'])+","+str(
            data[k]['type'])+","+str(data[k]['response_time'])+'\n')  # write the decoded data to file
        k += 1

timeout = aiohttp.ClientTimeout(total=timeouttime)
print ("Please input what type of ip you want to verify?\n")#ip list selector
print ("[1]Verify all fetched IP(if you don't know how to do,please select this)\n")
print ("[2]Verify those available IP is whatever still available\n(Make sure you execute this script for the first time)\n")
select = int(input("You select:"));
if (select==1):
    lis = open('listipport.txt', 'r').read().split('\n')  # read decoded file
elif (select==2):
    lis = open('proxyok.txt', 'r').read().split('\n')  # read ok IP
glis = []


async def test(url, session, semaphore, ip):# Test program
    with await semaphore:
        try:
            async with session.get(url, proxy='http://'+ip, ) as response:
                content = await response.read()
            page = content.decode()  # decode the target page's content
            for blackword in blackwords:# Loop check blackwords
                if blackword in page:
                    print('bad  ' + ip)
                    return
            print('ok   ' + ip)
            return ip
        except:
            print('fail ' + ip)
            return


async def work():# Network Connection
    async with aiohttp.ClientSession(timeout=timeout) as session:
        tasks = []
        semaphore = asyncio.Semaphore(8)
        for ip in lis:
            task = asyncio.ensure_future(test(testurl, session, semaphore, ip))
            tasks.append(task)
        scheduled = asyncio.gather(*tasks)
        r = await scheduled
        ok = [i for i in r if isinstance(i, str)]
        with open('proxyok.txt', 'w') as file:# Write out the result
            file.write('\n'.join(ok))

loop = asyncio.get_event_loop()
loop.run_until_complete(work())
loop.close()
