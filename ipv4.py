# -*- coding: utf-8 -*-

#DECIMAL A BINARIO	
def dec2bin(dec):
	decimal = int(dec)
	binario = ""
	while True:
		binario += str(decimal % 2)
		decimal = decimal / 2
		if decimal == 0:
			break
	return int(binario[::-1])

#BIANRIO A DECIMAL
def bin2dec(bin):
	binario = str(bin)
	decimal = 0
	for n in range(len(binario)):
		decimal += int(binario[::-1][n]) * 2**n
	return decimal

#IP EN FORMATO DECIMAL A BINARIO
def ip2bin(ip):
	binario = ""
	for d in ip.split("."):
		b = str(dec2bin(d))
		b = "0"*(8-len(b)) + b
		binario += b
	return binario

#IP EN FORMATO BINARIO A DECIMAL
def bin2ip(bin):
	binario = str(bin)
	bytes_bin = []
	for t in range(0,32,8):
		bytes_bin.append(binario[t:t+8])
	bytes_ip = []
	for b in bytes_bin:
		bytes_ip.append(str(bin2dec(b)))
	return ".".join(bytes_ip)
	
#DIRECCIÓN DE RED
def red_bin(ip_bin,mask_bin):
	red = ""
	for i,m in zip(ip_bin,mask_bin):
		if i == "1" and m == "1":
			red += "1"
		else:
			red += "0"
	return red

#DIRECCIÓN DE RED CON DATOS EN FORMATO DECIMAL PUNTEADO
def red(ip,mask):
	red = ""
	ip_bin = ip2bin(ip)
	mask_bin = ip2bin(mask)
	for i,m in zip(ip_bin,mask_bin):
		if i == "1" and m == "1":
			red += "1"
		else:
			red += "0"
	return bin2dec(red)
	
#BROADCAST DE RED CON DATOS EN FORMATO DECIMAL PUNTEADO
def broadcast_bin(ip_bin,mask_bin):
	broadcast = ""
	red_b = red_bin(ip_bin,ip_bin)
	for r,m in zip(red_b,mask_bin):
		if m == "1":
			broadcast += r
		else:
			broadcast += "1"
	return broadcast

#BROADCAST DE RED CON DATOS EN FORMATO DECIMAL PUNTEADO
def broadcast(ip,mask):
	broadcast = ""
	ip_bin = ip2bin(ip)
	mask_bin = ip2bin(mask)
	red_bin = red(ip,mask)
	for r,m in zip(red_bin,mask_bin):
		if m == "1":
			broadcast += r
		else:
			broadcast += "1"
	return bin2dec(broadcast)

class rede():
	def __init__(self,ip,mask="255.255.255.255"):
		self.ip = [ip,ip2bin(ip)]
		self.mask = [mask,ip2bin(mask)]
		red_b = red_bin(self.ip[1],self.mask[1])
		self.red = [bin2ip(red_b),red_b]
		broadcast_b = broadcast_bin(self.ip[1],self.mask[1])
		self.broadcast = [bin2ip(broadcast_b),broadcast_b]
		if self.mask[0] == "255.0.0.0":
			self.clase = "A"
		elif self.mask[0] == "255.255.0.0":
			self.clase = "B"
		elif self.mask[0] == "255.255.255.0":
			self.clase = "C"
		else:
			self.clase = None
		self.all = [self.ip,self.mask,self.red,self.broadcast,self.clase]
	def __repr__(self):
		string_repr = ""
		for name,info in zip(["Address","Netmask","Network","Broadcast","Clase"],self.all):
			if type(info).__name__=="list":
				string_repr += name+":\t"+info[0]+"\t"+info[1]+"\n"
			else:
				string_repr += name+":\t\t"+info+"\n"
		return string_repr
		
		