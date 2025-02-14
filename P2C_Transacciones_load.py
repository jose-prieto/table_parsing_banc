from psycopg2.errors import ForeignKeyViolation
import pandas as pd
import glob as gb
import csv

class P2C_Transacciones_load:
    
    #Constructor
    def __init__(self, ruta, cartera, fecha):
        print("Creando p2c")
        self.nombre_archivo = '\P2C'
        self.rutaOrigin = ruta
        for file in gb.glob(ruta + self.nombre_archivo + '*.xlsx'):
            self.ruta = file
        self.df = pd.read_excel(self.ruta, usecols = 'A:G', header=0, index_col=False, keep_default_na=True)
        self.df['Monto de la operacion'] = self.df['Monto de la operacion'].astype(float)
        self.df = self.df.rename(columns={'RIF': 'rif', 'Monto de la operacion': 'monto'})
        self.df['rif'] = self.df['rif'].str.strip()
        
        print("P2C monto total: ", self.df['monto'].sum(), "\n")
        
        self.df = self.recorrerDF(self.df)
        self.df = pd.merge(self.df, cartera, how='inner', right_on='CedulaCliente', left_on='rif')
        self.df = self.df.groupby(['MisCliente'], as_index=False).agg({'monto': sum})
        self.df = self.df[(self.df["monto"] > 0)]
            
        self.df = self.df.rename(columns={"MisCliente": "mis"})
        
        self.df = self.df.assign(fecha = fecha)
        
    def get_monto(self):
        df = self.df
        df['monto'] = df['monto'].astype(str)
        for i in range(len(df['monto'])):
            df['monto'][i]=df['monto'][i].replace('.',',')
            
        df = df.rename(columns={'monto': 'P2C (Mensual)'})
        
        return df.groupby(['mis'], as_index=False).agg({'P2C (Mensual)': 'first'})
    
    def get_usable(self):
        df = self.df.assign(uso = 1)
        df = df.rename(columns={'uso': 'P2C (Mensual)'})
        
        return df.groupby(['mis'], as_index=False).agg({'P2C (Mensual)': 'first'})
    
    def quitarCeros(self, rifCliente):
        aux = rifCliente[1:]
        while (len(aux) < 9):
            aux = '0' + aux
        return rifCliente[0] + aux
    
    def recorrerDF(self, df):
        for indice_fila, fila in df.iterrows():
            df.at[indice_fila,"rif"] = self.quitarCeros(fila["rif"])
        return df
    
    def to_csv(self):
        self.df.to_csv(self.rutaOrigin + '\\rchivos csv\p2c.csv', index = False, header=True, sep='|', encoding='utf-8-sig', quoting=csv.QUOTE_NONE)
    
    def insertPg(self, conector):
        print("Insertando p2c")
        for indice_fila, fila in self.df.iterrows():
            try:
                conector.cursor.execute("INSERT INTO P2C (p2c_mis, p2c_monto, p2c_fecha) VALUES(%s, %s, %s)", 
                               (fila["mis"], 
                               fila["monto"], 
                               fila["fecha"]))
            except ForeignKeyViolation:
                pass
            except Exception as excep:
                print(type(excep))
                print(excep.args)
                print(excep)
                print("p2c")
            finally:
                conector.conn.commit()
    
#p2c = P2C_Transacciones_load(r'C:\Users\José Prieto\Documents\Bancaribe\Enero').to_csv()