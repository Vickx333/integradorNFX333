import pandas as pd
from PyQt5.QtWidgets import QApplication, QFileDialog
import sys


def generar_archivo_efectivo_resumen(df):
    df_efectivo = df.copy()
    df_efectivo = df_efectivo[['nota_id','Fecha','Producto','Volumen','Importe','TipoPago','Cliente','EstablecimientoID']].copy()

    
    
    df_efectivo = df[['nota_id','Fecha','Producto','Volumen','Importe','TipoPago','Cliente','EstablecimientoID']]    
    df_efectivo = df[(df['TipoPago'] == 'EFECTIVO') |
                      df['Cliente'].isin(['TARJETA DE CREDITO','TARJETA DE DEBITO',  'EFECTICARD', 'TICKET CAR'])]
    df_efectivo = df_efectivo.copy()
    df_efectivo.loc[:, 'Cliente'] = df_efectivo['Cliente'].apply(lambda x: 'EFECTIVO' if pd.isna(x) else x)
    df_efectivo.loc[:, 'TipoPago'] = df_efectivo['Cliente'].apply(lambda x: '' if pd.isna(x) else x)
    df_efectivo['TipoPago'] = df_efectivo['TipoPago'].replace('', 'EFECTIVO')

    df_otro = df_efectivo[~df_efectivo['Producto'].isin(['MAGNA', 'DIESEL', 'PREMIUM'])]

    df_transferencia = df[df['Cliente'] == 'TRANSFERENCIA ELECTRONICA DE FONDOS']
    df_otro = pd.concat([df_otro, df_transferencia])
    df_otro.loc[df_otro['Cliente'] == 'TRANSFERENCIA ELECTRONICA DE FONDOS', 'TipoPago'] = 'TRANSFERENCIA ELECTRONICA DE FONDOS'

    df_efectivo = df_efectivo[df_efectivo['Producto'].isin(['MAGNA', 'DIESEL', 'PREMIUM'])]
    
    df_efectivo.loc[(df_efectivo['Cliente'] == 'CASIMIRO RIVERA GAMES'), 'TipoPago'] = 'FLOTILLAS'
    df_efectivo.loc[(df_efectivo['Cliente'] == 'TRANFERENCIA ELECTRONICA DE FONDOS') & (df_efectivo['TipoPago'] == 'FLOTILLAS') & (df_efectivo['TipoLiquidacion'] == 'FLOTILLAS'), 'TipoPago'] = 'CREDITO LOCAL'
 
    df_efectivo['Subsidiaria'] = ''
    df_efectivo['Ubicacion'] = ''
    df_otro['Subsidiaria'] = ''
    df_otro['Ubicacion'] = ''

    def generarsiglas_de_pago(row):
        siglas_pago = {
            'EFECTIVO': 'E',
            'TARJETA DE CREDITO': 'TC',
            'TARJETA DE DEBITO': 'TD',
            'EFECTICARD': 'EC', 
            'TICKET CAR': 'TC'

        }
        fecha = pd.to_datetime(row['Fecha'], format='%d/%m/%y')
        df_otro['Fecha'] = pd.to_datetime(df_otro['Fecha'], format='%d/%m/%y')

        if row['TipoPago'] == 'EFECTIVO' and row['Producto'] in ['MAGNA', 'DIESEL', 'PREMIUM'] :
            return 'E' + fecha.strftime('%d%m%y')
           
        elif row['Cliente'] == '' and row['Producto'] in ['MAGNA', 'DIESEL', 'PREMIUM']:
            return 'E' + fecha.strftime('%d%m%y')
        elif row['Producto'] in ['MAGNA', 'DIESEL', 'PREMIUM']:
              return siglas_pago.get(row['Cliente'], '') + fecha.strftime('%d%m%y')
                
        else:
            return str(int(row['nota_id']))
    
    df_efectivo['nota_id'] = df_efectivo.apply(generarsiglas_de_pago, axis=1)

    columnas_Efectivo = ['nota_id','Fecha','Producto','Volumen','Precio','Subsidiaria','Ubicacion','Importe','TipoPago']
    columnas_otro = ['nota_id','Fecha','Producto','Volumen','Precio','Subsidiaria','Ubicacion','Importe','TipoPago']
  
   
    
    def cambiar_nombre_de_producto(row):
        if row['EstablecimientoID'] == 109052 and row['Producto'] in ['MAGNA', 'DIESEL', 'PREMIUM']:
            df_efectivo['Ubicacion'] = '1'
            df_efectivo['Subsidiaria'] = '6'
            return 'ABE-' + row['Producto']

        elif row['EstablecimientoID'] == 106536 and row['Producto'] in ['MAGNA', 'DIESEL', 'PREMIUM']:
            df_efectivo['Ubicacion'] = '3'
            df_efectivo['Subsidiaria'] = '5'
            return 'JDMPM - ' + row['Producto']
        
        elif row['EstablecimientoID'] == 1501329 and row['Producto'] in ['MAGNA', 'DIESEL', 'PREMIUM']:
            df_efectivo['Ubicacion'] = '2'
            df_efectivo['Subsidiaria'] = '3'
            return 'GDQ - ' + row['Producto']
        
        elif row['EstablecimientoID'] == 117933 and row['Producto'] in ['MAGNA', 'DIESEL', 'PREMIUM']:
            df_efectivo['Ubicacion'] = '5'
            df_efectivo['Subsidiaria'] = '4'
            return 'WEHE - ' + row['Producto']
        
        elif row['EstablecimientoID'] == 510949 and row['Producto'] in ['MAGNA', 'DIESEL', 'PREMIUM']:
            df_efectivo['Ubicacion'] = '7'
            df_efectivo['Subsidiaria'] = '8'
            return 'GLC-' + row['Producto']
        elif row['EstablecimientoID'] == 108161 and row['Producto'] in ['MAGNA', 'DIESEL', 'PREMIUM']:
            df_efectivo['Ubicacion'] = '10'
            df_efectivo['Subsidiaria'] = '10'
            return 'SCFT - ' + row['Producto']
        
        else:
            if row['EstablecimientoID'] == 109052 and row['Producto'] in ['MAGNA', 'DIESEL', 'PREMIUM']:
                df_efectivo['Ubicacion'] = '1'
                df_efectivo['Subsidiaria'] = '6'
                return 'ABE-' + row['Producto']
            elif row['EstablecimientoID'] == 106536 and row['Producto'] in ['MAGNA', 'DIESEL', 'PREMIUM']:
                df_efectivo['Ubicacion'] = '3'
                df_efectivo['Subsidiaria'] = '5'
                return 'JDMPM - ' + row['Producto']
            elif row['EstablecimientoID'] == 1501329 and row['Producto'] in ['MAGNA', 'DIESEL', 'PREMIUM']:
                df_efectivo['Ubicacion'] = '2'
                df_efectivo['Subsidiaria'] = '3'
                return 'GDQ - ' + row['Producto']
            elif row['EstablecimientoID'] == 117933 and row['Producto'] in ['MAGNA', 'DIESEL', 'PREMIUM']:
                df_efectivo['Ubicacion'] = '5'
                df_efectivo['Subsidiaria'] = '4'
                return 'WEHE - ' + row['Producto']
            elif row['EstablecimientoID'] == 510949 and row['Producto'] in ['MAGNA', 'DIESEL', 'PREMIUM']:
                df_efectivo['Ubicacion'] = '7'
                df_efectivo['Subsidiaria'] = '8'
                return 'GLC-' + row['Producto']
            elif row['EstablecimientoID'] == 108161 and row['Producto'] in ['MAGNA', 'DIESEL', 'PREMIUM']:
                df_efectivo['Ubicacion'] = '10'
                df_efectivo['Subsidiaria'] = '10'
                return 'SCFT - ' + row['Producto']
            else:
                return row['Producto']
        
    df_efectivo['Producto'] = df_efectivo.apply(cambiar_nombre_de_producto, axis=1)   
    df_otro['Producto'] = df_otro.apply(cambiar_nombre_de_producto, axis=1)
    

    print(df_efectivo['EstablecimientoID'].unique())

    df_efectivo['Fecha'] = pd.to_datetime(df_efectivo['Fecha']).dt.strftime('%d/%m/%y') 
    df_efectivo = df_efectivo[columnas_Efectivo]
    df_otro = df_otro[columnas_otro]
    df_otro['Fecha'] = pd.to_datetime(df_otro['Fecha']).dt.strftime('%d/%m/%y')

   
    
    resumen = df_efectivo.groupby(['Producto',  'TipoPago']).agg({
        'Volumen': 'sum',
        'Importe': 'sum',
        'Precio': 'first',
        'Fecha': 'first',
        'Subsidiaria': 'first',
        'Ubicacion': 'first',
        'nota_id': 'first'

    }).reset_index()

   
    df_otro['Subsidiaria'] = resumen.at[0, 'Subsidiaria']
    df_otro['Ubicacion'] = resumen.at[0, 'Ubicacion']
    
    resumen = resumen.rename(columns={
        'nota_id':'ID Externo',
        'Fecha':'Fecha',
        'Producto':'Artículo',
        'Volumen':'Cantidad',
        'Precio':'Tarifa',
        'Subsidiaria':'Subsidiaria',
        'Ubicacion':'Ubicación',
        'Importe':'BASE',
        'TipoPago':'Metodo de pago'
        })
    

    

    df_otro = df_otro.rename(columns={
        'nota_id':'ID Externo',
        'Fecha':'Fecha',
        'Producto':'Artículo',
        'Volumen':'Cantidad',
        'Precio':'Tarifa',
        'Subsidiaria':'Subsidiaria',
        'Ubicacion':'Ubicación',
        'Importe':'BASE',
        'TipoPago':'Metodo de pago'
         })
    

    resumen = resumen[['ID Externo','Fecha','Artículo','Cantidad','Tarifa','Subsidiaria','Ubicación','BASE','Metodo de pago']]
    df_otro = df_otro [['ID Externo','Fecha','Artículo','Cantidad','Tarifa','Subsidiaria','Ubicación','BASE','Metodo de pago']]
  

    resumen = pd.concat([resumen, df_otro], ignore_index=True)
   
 
    print(resumen)
    app = QApplication.instance() if QApplication.instance() else QApplication(sys.argv)

    file_path, _ = QFileDialog.getSaveFileName(None, "Guardar archivo", "", "CSV UTF-8 (delimitado por comas) (*.csv)")

                       

    if file_path:
        resumen.to_csv(file_path, encoding='utf-8', sep=',', index=False)
        print("Archivo guardado")
     
    

    return resumen