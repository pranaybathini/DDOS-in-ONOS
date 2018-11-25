import urllib.request, json 
import time
import numpy as np
import collections
import csv

frames = list()
dst_entropy = list()
src_entropy = list()
proto_entropy = list()
bps_in = list()
bps_out = list()
flows = list()
sample_ipd = list()
sample_ips = list()

#change file name to no_attack before attack and collect data
#attack to no_attack ratio should be 30:70 as DDOS attacks are rare in practice. You can still reduce the ratio of attack.
with open('attack.csv','w') as f:
	writer = csv.writer(f)							
	ps = ['frames','dst_entropy','src_entropy','proto_entropy','bps_in','bps_out','flows','attack']
	writer.writerow(ps)


	for i in range(0,500):
	
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
		#during no_attack change last element of the list to 0
		writer.writerow([frames[i],dst_entropy[i],src_entropy[i],proto_entropy[i],bps_in[i],bps_out[i],flows[i],1])
			


		
		
				
	


