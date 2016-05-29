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
	return bin2ip(red)
	
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
	return bin2ip(broadcast)

#COMPARACIÓN DA MÁSCARA DE RED COAS ANTIGUAS CLASES
def clase(mask):
	if mask == "255.0.0.0":
		return "A"
	elif mask == "255.255.0.0":
		return "B"
	elif mask == "255.255.255.0":
		return "C"
	else:
		return "None"

#ÁMBITO IP (PÚBLICA OU PRIVADA)
def ambito(ip):
	if red(ip,"255.0.0.0") == "10.0.0.0":
		return "Direccion Privada"
	elif red(ip,"255.240.0.0") == "172.16.0.0":
		return "Direccion Privada"
	elif red(ip,"255.255.0.0") == "192.168.0.0":
		return "Direccion Privada"
	elif ip[:7] == "169.154":
		return "APIPA (Automatic Private IP Addressing)"
	elif ip == "255.255.255.255":
		return "Broadcast limitado (difusion)"
	elif ip[:3].isdigit() and int(ip[:3]) >= 224:
		return "Direccion reservada para Investigación"
	elif ip == "0.0.0.0":
		return "Ruta predeterminada"
	elif ip[:3] == "127":
		return "Bucle Local"
	else:
		return "Direccion Publica"
		
#TIPO DE DIRECCIÓN (HOST, RED, BROADCAST, ETC)
def tipo(ip,mask):
	if mask == "255.255.255.255":
		return "Host"
	elif ip == "0.0.0.0":
		return "Ruta predeterminada"
	elif ip[:3] == "127":
		return "Bucle Local"
	elif ip == "255.255.255.255":
		return "Broadcast limitado (difusion)"
	elif ip[:3].isdigit() and int(ip[:3]) >= 224:
		return "Direccion reservada para Investigación"
	elif ip[:7] == "169.154":
		return "APIPA (Automatic Private IP Addressing)"
	elif ip == red(ip,mask):
		return "Direccion de Red"
	else:
		return "Host"

#NÚMERO DE SUBREDES TEÓRICAS
def n_subr_teoricas(bin_mask):
	bit_1 = 0
	for bit in bin_mask:
		if bit == "1":
			bit_1 += 1
	return "2^"+str(bit_1)+" = "+str(2 ** bit_1)
	
#NÚMERO DE HOSTS TEÓRICOS
def n_hosts_teoricos(bin_mask):
	bit_0 = 0
	bit_1 = 0
	for bit in bin_mask:
		if bit == "0":
			bit_0 += 1
		else:
			bit_1 += 1
	return ["2^"+str(bit_0)+" = "+str(2 ** bit_0),
			"Total: "+str((2 ** bit_1) * 2 ** bit_0)]
			
#COMMUTACIÓNS DE BITS
def comm(n):
	t_bits = 2**n
	list_bits = []
	valor = 0
	for x in range(t_bits):
		valor_bin = dec2bin(valor)
		valor_bin = ("0"*(n-len(str(valor_bin))))+str(valor_bin)
		list_bits.append(valor_bin)
		valor += 1
	return list_bits

#DICCIONARIO DE SUBREDES
def subredes(red,mask,num,s_mask_bits):
	bit_1 = 0
	dict_subr = {}
	for bit in mask:
		if bit == "1":
			bit_1 += 1
	if num:
		bin_num = dec2bin(num)
		num_bits = len(str(bin_num))
		s_mask_bits = bit_1 + num_bits
	s_mask_bits = min(s_mask_bits,31)
	s_mask_bits = max(s_mask_bits,bit_1)
	bytes_subred = s_mask_bits-bit_1
	n_subredes = 2**bytes_subred
	n_hosts_x_subred = 2**(32-s_mask_bits)
	mask_subred = ("1"*s_mask_bits)+("0"*(32-s_mask_bits))
	bits_subredes = comm(bytes_subred)
	print "Numero de Subredes:\t"+str(len(bits_subredes))
	print "Hosts por Subred:\t"+str((2**(32-s_mask_bits))-2)
	print "Mascara:\t\t"+bin2ip(mask_subred)+"\t"+mask_subred
	print "Subredes:"
	for sub in bits_subredes:
		subred = red[:bit_1]+sub+red[bit_1+bytes_subred:]
		print (subred+"\t"+bin2ip(subred)+"/"+str(s_mask_bits)+
			" \t::Rango: "+bin2ip(int(subred)+1)+"-"+
			bin2ip(broadcast_bin(subred,mask_subred)))
	
	
#CLASE
class rede():
	def __init__(self,ip,mask="255.255.255.255"):
		self.ip = [ip,ip2bin(ip)]
		self.mask = [mask,ip2bin(mask),
					"/"+str(len([x for x in ip2bin(mask) if x=="1"]))]
		red_b = red_bin(self.ip[1],self.mask[1])
		self.red = [bin2ip(red_b),red_b]
		broadcast_b = broadcast_bin(self.ip[1],self.mask[1])
		self.broadcast = [bin2ip(broadcast_b),broadcast_b]
		self.clase = clase(self.mask[0])
		self.ambito = ambito(self.ip[0])
		self.tipo = tipo(self.ip[0],self.mask[0])
		#self.n_subrs_teoricas = n_subr_teoricas(self.mask[1])
		self.n_hosts_teorcios = n_hosts_teoricos(self.mask[1])
		self.all = [self.ip,self.mask,self.red,self.broadcast,
					self.clase,self.ambito,self.tipo,
					self.n_hosts_teorcios]
	def __repr__(self):
		string_repr = ""
		for name,info in zip(["Address:","Netmask:","Network:","Broadcast:",
							"Clase:\t","Ambito:\t", "Tipo:\t",
							"Numero Hosts Teoricos:"],
							self.all):
			if type(info).__name__=="list":
				string_repr += name+"\t"+"\t".join([str(x) for x in info])+"\n"
			else:
				string_repr += name+"\t"+str(info)+"\n"
		return string_repr
	def subredes(self,n=0,mask=0):
		return subredes(self.red[1],self.mask[1],n,mask)
		
		