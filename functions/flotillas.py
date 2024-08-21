import pandas as pd
from PyQt5.QtWidgets import QApplication, QFileDialog
import sys

def layout_flotillas(df):
    df['Cliente'] = df['Cliente'].fillna('')
    clientes_excluidos = ['', 'TARJETA DE CREDITO','TARJETA DE DEBITO', 'TRANSFERENCIA ELECTRONICA DE FONDOS', 'EFECTICARD', 'TICKET CAR']
    df_flotillas = df[(df['TipoLiquidacion'] == 'FLOTILLAS') | (~df['Cliente'].isin(clientes_excluidos))]
    
    df_flotillas[~((df_flotillas['Cliente'] == 'TRANFERENCIA ELECTRONICA DE FONDOS') & (df_flotillas['TipoPago'] == 'FLOTILLAS') & (df_flotillas['TipoLiquidacion'] == 'FLOTILLAS'))]
    
    TotalFlotillas = df_flotillas['Importe'].sum()
    
   
    
   
    # print('flotillas', TotalFlotillas)
    # print(df_flotillas['Cliente'])
    NFlotillas = df_flotillas.shape[0]
   
    
   
    
    
    return df_flotillas, TotalFlotillas, NFlotillas




nombre_archivo = '' 




def generar_archivo_flotillas(df):
    df['Cliente'] = df['Cliente'].fillna('')
    clientes_excluidos = ['', 'TARJETA DE CREDITO','TARJETA DE DEBITO', 'TRANSFERENCIA ELECTRONICA DE FONDOS', 'EFECTICARD', 'TICKET CAR']
    df_flotillas = df[(df['TipoLiquidacion'] == 'FLOTILLAS') | (~df['Cliente'].isin(clientes_excluidos))].copy()
    
    df_flotillas[~((df_flotillas['Cliente'] == 'TRANFERENCIA ELECTRONICA DE FONDOS') & (df_flotillas['TipoPago'] == 'FLOTILLAS') & (df_flotillas['TipoLiquidacion'] == 'FLOTILLAS'))]
    mask = df_flotillas['Cliente'] == 'SISTEMA MUNICIPAL PARA EL DESARROLLO INTEGRAL DE LA FAMILIA DEL MUNICIPIO DE EZEQUIEL MONTES QRO'
    df_flotillas.loc[mask, 'Cliente'] = 'SISTEMA MUNICIPAL PARA EL DESARROLLO INTEGRAL DE LA FAMILIA DEL MUNICIPIO DE EZEQUI'

    df_flotillas['Fecha'] = pd.to_datetime(df_flotillas['Fecha'], errors='coerce')

    df_flotillas['Fecha'] = df_flotillas['Fecha'].dt.strftime('%d/%m/%y')

    df_flotillas['Subsidiaria'] = ''
    df_flotillas['Ubicacion'] = ''

    columnas_flotillas = ['nota_id', 'Cliente', 'Fecha', 'Subsidiaria', 'Ubicacion','Producto', 'Volumen', 'Precio', 'Importe']
    

    def cambiar_nombre_de_producto(row, df_flotillas):
        if row['EstablecimientoID'] == 109052 and row['Producto'] in ['MAGNA', 'DIESEL', 'PREMIUM']:
            df_flotillas['Ubicacion'] = '1'
            df_flotillas['Subsidiaria'] = '6'
            return 'ABE-' + row['Producto']
        
        elif row['EstablecimientoID'] == 106536 and row['Producto'] in ['MAGNA', 'DIESEL', 'PREMIUM']:
            df_flotillas['Ubicacion'] = '3'
            df_flotillas['Subsidiaria'] = '5'
            return 'JDMPM - ' + row['Producto']
        
        elif row['EstablecimientoID'] == 1501329 and row['Producto'] in ['MAGNA', 'DIESEL', 'PREMIUM']:
            df_flotillas['Ubicacion'] = '2'
            df_flotillas['Subsidiaria'] = '3'
            return 'GDQ - ' + row['Producto']
        
        elif row['EstablecimientoID'] == 117933 and row['Producto'] in ['MAGNA', 'DIESEL', 'PREMIUM']:
            df_flotillas['Ubicacion'] = '5'
            df_flotillas['Subsidiaria'] = '4'
            return 'WEHE - ' + row['Producto']
        
        elif row['EstablecimientoID'] == 510949 and row['Producto'] in ['MAGNA', 'DIESEL', 'PREMIUM']:
            df_flotillas['Ubicacion'] = '7'
            df_flotillas['Subsidiaria'] = '8'
            return 'GLC-' + row['Producto']
        elif row['EstablecimientoID'] == 108161 and row['Producto'] in ['MAGNA', 'DIESEL', 'PREMIUM']:
            df_flotillas['Ubicacion'] = '10'
            df_flotillas['Subsidiaria'] = '10'
            return 'SCFT - ' + row['Producto']
        
        else:
            return row['Producto']
        
    df_flotillas['Producto'] = df_flotillas.apply(lambda row: cambiar_nombre_de_producto(row, df_flotillas), axis=1)

    df_flotillas = df_flotillas[columnas_flotillas]

    df_flotillas = df_flotillas.rename(columns={
        'nota_id': 'ID Externo',
        'TipoPago': 'Cliente',
        'Fecha': 'Fecha',
        'Subsidiaria': 'Subsidiaria',
        'Ubicacion': 'Ubicación',
        'Producto': 'Artículo',
        'Volumen': 'Cantidad',
        'Precio': 'Tarifa (precio unitario)',
        'Importe': 'BASE'
    })

    

    # df_flotillas = df_flotillas[['ID EXTERNOS', 'Cliente', 'Fecha', 'Subsidiaria', 'Ubicación', 'Artículo', 'Cantidad', 'Tarifa (precio unitario)', 'BASE']]

    
   
   
     
    
    app = QApplication.instance() if QApplication.instance() else QApplication(sys.argv)

    file_path, _ = QFileDialog.getSaveFileName(None, "Guardar archivo", "", "CSV UTF-8 (delimitado por comas) (*.csv)")

                       

    if file_path:
        df_flotillas.to_csv(file_path, encoding='utf-8', sep=',', index=False)
        print(df_flotillas)

        print("Archivo guardado")
       

    return df_flotillas

