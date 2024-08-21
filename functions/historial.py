import sys 
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QMessageBox, QLabel, QBoxLayout
import sqlite3
from datetime import datetime
import pandas as pd
import os


def conectar_db():
    conn = sqlite3.connect('database/database.sqlite')
    cursor = conn.cursor()

    cursor.execute(''' CREATE TABLE IF NOT EXISTS historial(
                   id INTEGER PRIMARY KEY,
                   fecha DATE,
                   establecimientoID INTEGER,
                   precioMagna REAL,
                   iepsfinalMagna REAL,
                   precioDiesel REAL,
                   iepsfinalDiesel REAL,
                   precioPremium REAL,
                   iepsfinalPremium REAL
                   )''')
    return conn


def guardar_datos(fecha, establecimientoID, precioMagna,iepsfinalMagna, precioDiesel,iepsfinalDiesel, precioPremium,iepsfinalPremium):
    
    establecimiento_nombres = {
        '0000109052': 'ABEL',
        '0000106536': 'J.DOLORES',
        '0001501329': 'GASOFAR',
        '0000117933': 'WEHENDY',
        '0000510949': 'CHALCO',
        '0000108161': 'S. COMONFORT'
    }

    nombre_establecimiento = establecimiento_nombres.get(establecimientoID, establecimientoID)


    conn = conectar_db()
    cursor = conn.cursor()

    cursor.execute('''SELECT * FROM historial WHERE fecha = ? AND  establecimientoID = ?
                      AND precioMagna = ? AND iepsfinalMagna = ? AND precioDiesel = ? 
                   ''', (fecha, nombre_establecimiento, precioMagna, precioDiesel, precioPremium))
    registro = cursor.fetchone()
    if registro:
        print("ya exsite un registro cone sta fecha. no se guardara el nuevo registro")
    else: 
        
          cursor.execute('INSERT INTO historial(fecha, establecimientoID, precioMagna, iepsfinalMagna, precioDiesel, iepsfinalDiesel, precioPremium,   iepsfinalPremium) VALUES(?,?,?,?,?,?,?,?)',
                         (fecha, nombre_establecimiento, precioMagna,iepsfinalMagna, precioDiesel,iepsfinalDiesel, precioPremium,iepsfinalPremium))
    conn.commit()
    conn.close()    




class ventanaemergenteB(QWidget):
    def __init__(self, parent, fecha, establecimientoID, precioMagna,iepsfinalMagna, precioDiesel,iepsfinalDiesel, precioPremium,   iepsfinalPremium):
        super().__init__()
        self.fecha = fecha
        self.establecimientoID = establecimientoID
        self.precioMagna = precioMagna
        self.iepsfinalMagna = iepsfinalMagna
        self.precioDiesel = precioDiesel
        self.iepsfinalDiesel = iepsfinalDiesel
        self.precioPremium = precioPremium
        self.iepsfinalPremium = iepsfinalPremium 
        
      


        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
       
        self.labelFecha = QLabel(f"Fecha: {self.fecha}")
        layout.addWidget(self.labelFecha)
       
        self.labelPrecioMagna = QLabel(f"Precio Magna: {self.precioMagna}")
        layout.addWidget(self.labelPrecioMagna)

        self.LabelIEPSMagna = QLabel(f"IEPS Magna: {self.iepsfinalMagna}")
        layout.addWidget(self.LabelIEPSMagna)

        self.labelPrecioDiesel = QLabel(f"Precio Diesel: {self.precioDiesel}")
        layout.addWidget(self.labelPrecioDiesel)

        self.LabelIEPSDiesel = QLabel(f"IEPS Diesel: {self.iepsfinalDiesel}")
        layout.addWidget(self.LabelIEPSDiesel)

        self.labelPrecioPremium = QLabel(f"Precio Premium: {self.precioPremium}")
        layout.addWidget(self.labelPrecioPremium)
        
        self.LabelIEPSPremium = QLabel(f"IEPS Premium: {self.iepsfinalPremium}")
        layout.addWidget(self.LabelIEPSPremium)

        
        self.btnGuardar = QPushButton('Guardar')
        self.btnGuardar.clicked.connect(self.on_guardar)
        layout.addWidget(self.btnGuardar)
    
    
        self.btnOmitir = QPushButton('Omitir')
        self.btnOmitir.clicked.connect(self.on_omitir)  
        layout.addWidget(self.btnOmitir)

        

        self.setLayout(layout)
        self.setWindowTitle('Guardar Historial')
        self.show()
 
    def mostrarDatos(self):
        conn = conectar_db()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM historial ORDER BY fecha DESC')
        registros = cursor.fetchall()
        for registro in registros:
           # print(registros)
             print("seguardocorrectamente")
           
        conn.commit()
        conn.close() 

    

    def on_guardar(self):
        fecha = self.fecha.strftime('%d-%m-%y') if hasattr(self.fecha, 'strftime') else str (self.fecha)
        iepsfinalMagna = round(self.iepsfinalMagna, 8)
        iepsfinalDiesel = round(self.iepsfinalDiesel, 8)
        iepsfinalPremium = round(self.iepsfinalPremium, 8)
        
        guardar_datos(fecha, self.establecimientoID, self.precioMagna, self.precioDiesel, self.precioPremium, iepsfinalMagna, iepsfinalDiesel, iepsfinalPremium)
        print('guardando datos...')
        # print(f"Tipo de fecha: {type(self.fecha)}")
        if __name__ == '__main__':
            app = QApplication(sys.argv)
            df = pd.read_xlsx('database/database.xlsx')
            
            fecha = df['Fecha'].unique()
            establecimientoID = df['establecimientoID'].unique()
            df_magna = self.df[self.df['Producto'] == 'MAGNA']
            precioMagna = df_magna['Precio'].unique()

            df_diesel = df[df['Producto'] == 'DIESEL']  
            precioDiesel = df_diesel['Precio'].unique()

            df_premium = df[df['Producto'] == 'PREMIUM']
            precioPremium = df_premium['Precio'].unique()
            venta = ventanaemergenteB(fecha, self.establecimientoID, self.precioMagna, self.iepsfinalMagna, self.precioDiesel, self.iepsfinalDiesel, self.precioPremium, self.iepsfinalPremium)
            sys.exit(app.exec())
        self.mostrarDatos()
        self.close()


    def on_omitir(self):
        print('Omitiendo datos...')
        self.close()


        

        

            
