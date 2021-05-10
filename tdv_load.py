from rrgg.rrgg_institucional_load import rrgg_institucional_load
from rrgg.rrgg_corporativo_load import rrgg_corporativo_load
from rrgg.rrgg_empresa_load import rrgg_empresa_load
from rrgg.rrgg_pyme_load import rrgg_pyme_load
import pandas as pd
import csv

class tdv_load:
    
    #Constructor
    def __init__(self, ruta, cartera, fecha):
        print("Creando TDV")
        self.fecha = fecha
        self.ruta = ruta
        
        self.corporativo = rrgg_corporativo_load(self.ruta, cartera)
        self.empresa = rrgg_empresa_load(self.ruta, cartera)
        self.institucional = rrgg_institucional_load(self.ruta, cartera)
        self.pyme = rrgg_pyme_load(self.ruta, cartera)
        
        self.df = pd.concat([self.corporativo.df, self.empresa.df, self.institucional.df, self.pyme.df]).groupby(['mis']).sum().reset_index()
            
        self.dfMonto = self.df.rename(columns={'monto': 'TDV'})
        print("DRV - TDV monto total: ", self.dfMonto['TDV'].sum(), "\n")
        
        self.df['monto'] = self.df['monto'].astype(str)
        for i in range(len(self.df['monto'])):
            self.df['monto'][i]=self.df['monto'][i].replace('.',',')
        
        self.df = self.df.assign(fecha = self.fecha)
    
    def to_csv(self):
        self.df.to_csv(self.ruta + '\\rchivos csv\\tdv.csv', index = False, header=True, sep='|', encoding='latin-1', quoting=csv.QUOTE_NONE)