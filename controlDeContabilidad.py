import pandas as pd 
import os
import json

def obtenerXML(carpeta):
	facturas=pd.DataFrame()
	for archivo in os.listdir(carpeta):
		print('Leyendo ', archivo)
		if not archivo.endswith('.xml'): continue
		f = open(os.path.join(carpeta,archivo), "r", encoding="UTF-8").read()
		facturas=facturas.append({'xml':f}, ignore_index=True)
	return facturas

def extraerTags(factura):
	for c in config['campos']:
		#Para cada campo deseado 
		factura[c]=''
		#Buscar el tag o tags
		for t in config['campos'][c]:
			#Separar el tag en campo atributo:
			tag=t.split(' ')
			elemento=factura['xml'].split('<{}'.format(tag[0]))
			if len(elemento)>=2:
				elemento=elemento[1]
				#Encontrar el atributo
				atributo=elemento.split('{}="'.format(tag[1]))
				if len(atributo)>=2:
					factura[c]=atributo[1].split('"')[0]
	return factura

#Obtener el archivo config
config=None
with open("config.json", "r") as jsonfile:
    config = json.load(jsonfile)
    print("Read successful")


#obtener los xmls en las carpetas 
recibidas=obtenerXML('FacturasRecibidas')
emitidas=obtenerXML('FacturasEmitidas')


recibidas=recibidas.apply(extraerTags, axis=1)
recibidas.to_excel('FacturasRecibidas.xlsx')
emitidas=emitidas.apply(extraerTags, axis=1)
emitidas.to_excel('FacturasEmitidas.xlsx')