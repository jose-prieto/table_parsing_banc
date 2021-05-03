import pandas as pd
import glob as gb

class inventario_ajustado_load:
    
    #Constructor
    def __init__(self, ruta, cartera, fecha):
        print("Creando inventario ajustado")
        self.rutaOrigin = ruta
        self.ruta = ruta
        self.nombre_archivo = '\\INVENTARIO AJUSTADO'
        for file in gb.glob(self.ruta + self.nombre_archivo + '*.xlsx'):
            self.ruta = file
        self.df = pd.read_excel(self.ruta, usecols = 'J,K,M,T', header=0, index_col=False, keep_default_na=True, sheet_name="INVENTARIO_DEL_DÍA", dtype=str)
        self.df = self.df[(self.df["CI O RIF"].str.startswith(("J", "R", "G", "F")))]
        self.df = self.df.rename(columns={'MIS': 'mis', 'VIGENTE': 'vigente'})
        self.df = pd.merge(self.df, cartera, how='inner', right_on='MisCliente', left_on='mis')
        self.df['vigente'] = self.df['vigente'].astype(float)
        self.dfDolar = self.df[(self.df["PRODUCTO AJUSTADO"] == "CRÉDITOS EN CUOTAS MONEDA EXTRANJERA")]
        self.dfDolar = self.dfDolar.groupby(['mis'], as_index=False).agg({'vigente': sum})
        self.dfBs = self.df[(self.df["PRODUCTO AJUSTADO"] != "CRÉDITOS EN CUOTAS MONEDA EXTRANJERA")]
        self.dfBs = self.dfBs.groupby(['mis'], as_index=False).agg({'vigente': sum})
        self.dfDolar = self.dfDolar.assign(fecha = fecha)
        self.dfBs = self.dfBs.assign(fecha = fecha)
    
    def to_csv(self):
        self.dfDolar.to_csv(self.rutaOrigin + '\\rchivos csv\credito_dolar.csv', index = False, header=True, sep='|')
        self.dfBs.to_csv(self.rutaOrigin + '\\rchivos csv\credito_vigente.csv', index = False, header=True, sep='|')
    
#todo = ah_unifica_load(r'C:\Users\José Prieto\Documents\Bancaribe\Marzo')
#bs = todo.dfBs
#dolar = todo.dfDolar