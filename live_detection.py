import urllib.request, json 
import time
import numpy as np
import collections
import csv
import pickle

filename = "knn.sav"
loaded_model = pickle.load(open(filename,'rb'))

frames = list()
dst_entropy = list()
src_entropy = list()
proto_entropy = list()
bps_in = list()
bps_out = list()
flows = list()
sample_ipd = list()
sample_ips = list()

test_list = list()

while True:
    for i in range(0,50):

        #packets 
        with urllib.request.urlopen("http://localhost:8008/metrics/json") as url:
            data = json.loads(url.read().decode())
            frames.append(data['ix_frames'])

        with urllib.request.urlopen("http://localhost:8008/app/fabric-view-master/scripts/fabric-view.js/metric/json") as url:
            data = json.loads(url.read().decode())
            flows.append(data['top-5-flows']['-other-'])

        with urllib.request.urlopen("http://localhost:8008/flows/json") as url:
            data = json.loads(url.read().decode())
            for z in range(0,len(data)):
                if data[z]['name'] == "flowgraph-pair" :
                    temp = data[z]['flowKeys'].split(',')
                    sample_ips.append(temp[0])
                    sample_ipd.append(temp[1])
            C = collections.Counter(sample_ipd)
            counts  = np.array(list(C.values()),dtype=float)
            #counts  = np.array(l,dtype=float)
            prob    = counts/counts.sum()
            shanon_entropy = (-prob*np.log2(prob)).sum()
            #print(shanon_entropy)
            dst_entropy.append(shanon_entropy)

            C = collections.Counter(sample_ips)
            counts  = np.array(list(C.values()),dtype=float)
            #counts  = np.array(l,dtype=float)
            prob    = counts/counts.sum()
            shanon_entropy = (-prob*np.log2(prob)).sum()
            #print(shanon_entropy)
            src_entropy.append(shanon_entropy)	
            sample_ips=list()
            sample_ipd=list()

        with urllib.request.urlopen("http://localhost:8008/app/dashboard-example-master/scripts/metrics.js/metric/json") as url:
            data = json.loads(url.read().decode())
            l = list()
            v = data['top-5-protocols']
            #print(v)
            m= list(v.values())
            l.extend(m[:len(v)-1])
            #print(l)
            counts  = np.array(l,dtype=float)
            prob    = counts/counts.sum()
            shanon_entropy = (-prob*np.log2(prob)).sum()
            #print ('entropy of protocol : '+ str(shannon_entropy))
            #print('BPS : ' + str(data['bps']))
            proto_entropy.append(shanon_entropy)
            bps_in.append(data['bps_in'])
            bps_out.append(data['bps_out'])

        time.sleep(2)
        print()

        #print('frames : ' + str(frames))
        #print('dst : '+str(dst_entropy))
        #print('src : ' + str(src_entropy))
        #print('proto: ' +str(proto_entropy))
        #print('bps_in : ' + str(bps_in))
        #print('bps_out : ' + str(bps_out))
        #print('flows : ' + str(flows))
        print('Iteration : '  + str(i) )
        test_list.append(list([frames[i],dst_entropy[i],src_entropy[i],proto_entropy[i],bps_in[i],bps_out[i],flows[i]]))

    import numpy as np
    test = np.array(test_list)
    print(test)
    count = 0
    # result = loaded_model.predict(test)
    # for x in result:
    #     if x is 1:
    #         count++
    # print(count*2)
    time.sleep(10)










