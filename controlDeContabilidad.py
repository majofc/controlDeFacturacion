import pandas as pd 
import os
import json

'''
Obtiene todos los xmls que se encuentran en una carpeta dada y lo regresa como un dataframe, colocando en 
'''
def obtenerXML(carpeta):
	facturas=pd.DataFrame()
	for archivo in os.listdir(carpeta):
		print('Leyendo ', archivo)
		if not archivo.endswith('.xml'): continue
		f = open(os.path.join(carpeta,archivo), "r", encoding="UTF-8").read()
		facturas=facturas.append({'xml':f, 'Nombre de factura':archivo}, ignore_index=True)
	return facturas

'''
Recibe el texto del xml de la factura, va al archvio config y obtiene los datos de interes con su tag y attributo.
Si logra encontrarlos, los agrega al dataframe
'''
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

'''
Obtiene los xml en carpetaOrigen, obtiene los tags de config y guarda el resultado en un nombreResultado
'''
def obtenFacturas(carpetaOrigen, nombreResultado):
	facturas=obtenerXML(carpetaOrigen)
	facturas=facturas.apply(extraerTags, axis=1)
	facturas.to_excel(nombreResultado)



#Obtener el archivo config
config=None
with open("config.json", "r") as jsonfile:
    config = json.load(jsonfile)
    print("Read successful")


#Obtener los emitidos
obtenFacturas('FacturasEmitidas','FacturasEmitidas.xlsx')
#Obtener los recibidos
obtenFacturas('FacturasRecibidas','FacturasRecibidas.xlsx')

