import networkx as nx
from paramiko import Transport
from time import sleep
import sys, json
from mininet.net import Mininet
from mininet.node import Controller, RemoteController
from mininet.cli import CLI
from mininet.log import setLogLevel


def start_mininet(graph, n_ctrl):

	#Initialisation
	setLogLevel('info')
	net = Mininet()
	h = dict()
	nodes = list()
	s = dict()
	c = list()

	#Creating and adding controllers
	for i in range(1, n_ctrl+1):
		c.append(net.addController('c'+str(i), controller=RemoteController, ip="172.17.0." + str(i+1), port=6653))

	#Creating hosts and switches and connecting one host with each switch
	for node in graph.nodes():
		h[node] = net.addHost('h' + str(node))
		nodes.append(h[node])
		s[node] = net.addSwitch('s' + str(node))
		s[node].linkTo(h[node])

	#Creating links 
	for e in graph.edges():
		s[e[0]].linkTo(s[e[1]])

	net.build()
	
	#Starting controllers
	for ctrl in c:
		ctrl.start()
	
	#Assigning controllers to switches
	for node in graph.nodes():
		s[node].start(c)

	net.start()
	net.staticArp()
	CLI(net)

graph = nx.read_graphml('Abilene.graphml')
start_mininet(graph, 1)
