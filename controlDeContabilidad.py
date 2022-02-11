import pandas as pd 
import xml.etree.ElementTree as ET
import os

def obtenerXML(carpeta):
	facturas=pd.DataFrame()
	path = carpeta
	for archivo in os.listdir(path):
		print('Leyendo ', archivo)
		if not archivo.endswith('.xml'): continue
		fullname = os.path.join(path, archivo)
		xml = ET.parse(fullname)
		facturas=facturas.append({'xml':xml}, ignore_index=True)
	return facturas

print(obtenerXML('FacturasRecibidas').shape)
print(obtenerXML('FacturasEmitidas').shape)
