import pandas as pd
import glob as gb
import csv
#Maestro de Tarjetas MDP Enero 2021 v3
class tdc_juridica_load:
    
    #Constructor
    def __init__(self, ruta, cartera, fecha):
        print("Creando tdc juridica")
        self.fecha = fecha
        self.rutaOrigin = ruta
        self.ruta = ruta
        self.nombre_archivo = '\\Maestro de Tarjetas Clientes'
        for file in gb.glob(self.ruta + self.nombre_archivo + '*.xlsx'):
            self.ruta = file
        self.df = pd.read_excel(self.ruta, usecols = 'A:O', header=0, sheet_name = "CUENTAS MADRES JURIDICAS", index_col=False, keep_default_na=True, dtype=str)
        self.df = self.df.rename(columns={"Codigo cliente": 'mis'})
        print("TDC Juridico totales: ", len(self.df.index))
        
        self.nombre_archivo = '\\Maestro de Tarjetas MDP'
        for file in gb.glob(self.ruta + self.nombre_archivo + '*.xlsx'):
            self.ruta = file
        self.dfPersona = pd.read_excel(self.ruta, usecols = 'A:O', header=0, index_col=False, keep_default_na=True, dtype=str)
        self.dfPersona = self.dfPersona.rename(columns={"Codigo cliente": 'mis'})
        print("TDC Personas totales: ", len(self.dfPersona.index))
        
        self.df = pd.concat([self.df, self.dfPersona]).groupby(['mis']).sum().reset_index()
        
        self.df = pd.merge(self.df, cartera, how='inner', right_on='MisCliente', left_on='mis')
        
        self.df = self.df.groupby(['mis'], as_index=False).agg({'mis': 'first'})
        
        self.df = self.df.assign(fecha = self.fecha)
    
    def get_usable(self):
        df = self.df.assign(uso = 1)
        df = df.rename(columns={'uso': 'TDC Jurídica'})
        
        return df.groupby(['mis'], as_index=False).agg({'TDC Jurídica': 'first'})
    
    def to_csv(self):
        self.df.to_csv(self.rutaOrigin + '\\rchivos csv\\tdc_juridico.csv', index = False, header=True, sep='|', encoding='latin-1', quoting=csv.QUOTE_NONE)
    
#pf = linea_cir_load(r'C:\Users\bc221066\Documents\José Prieto\Insumos Cross Selling\Enero').df