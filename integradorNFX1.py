from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor, QFont
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtGui import QPixmap
from PyQt5.QtGui import QIcon
# from PyQt5.QtWidgets import QApplication, QMainWindow, QGridLayout, QWidget, QToolBar, QLabel, QPushButton, QHBoxLayout, QLineEdit, QFileDialog, QMessageBox
from PyQt5.QtWidgets import QTableWidget, QApplication, QDialog, QVBoxLayout, QLabel, QPushButton, QTableWidget, QTableWidgetItem, QTextEdit, QWidget, QDateEdit
from PyQt5.QtCore import QDate
from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QTextEdit, QWidget
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QSpacerItem, QSizePolicy
from datetime import datetime
import sqlite3



from functions.precios import precios_C
from functions.precios import agrupar_precios
from functions.efectivo import layout_efectivo
from functions.efectivo import generar_archivo_efectivo
from functions.resumen import generar_archivo_efectivo_resumen
from functions.flotillas import layout_flotillas
from functions.flotillas import generar_archivo_flotillas

from functions.historial import guardar_datos
from functions.historial import conectar_db
from functions.historial import ventanaemergenteB

from functions.vista_historial import vistaHistorial
from functions.vista_historial import obtenerdatosHistorial


#conciliacion bancaria vista


# from functions.reset import resetprogram

# QApplication, QMainWindow, QGridLayout, QWidget, QToolBar, QLabel, QPushButton, QHBoxLayout, QLineEdit
import pandas as pd
import os





class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.filtroslayout = QHBoxLayout()
       
        

   # inicializar la variable de total_venta en 0
        self.total_venta = 0
        self.total_efectivo = 0 
        self.total_flotillas = 0
        self.diferencia = 0
        self.total_autojarreos = 0
        self.N_len = 0  
      
        self.obtenerdatosHistorial = obtenerdatosHistorial(self)
        self.vistaHistorial = vistaHistorial(self)
        self.setCentralWidget(self.vistaHistorial)
       
        
        
        

        self.setWindowIcon(QIcon('imagenes/02EnerfenixLOGO_Transparente01.png'))
        self.setWindowTitle("Integrador fenix")
        self.resize(1320, 820)

        central_widget = QWidget()
        # central_widget.setStyleSheet("background-color: blue; border: 1px solid black; border-radius: 10px;")
        self.grid_layout = QGridLayout()
        

        self.vistaHistorial = vistaHistorial()
        
        central_widget.setLayout(self.grid_layout)
        self.setCentralWidget(self.vistaHistorial)
        

        central_widget.setLayout(self.grid_layout)
        self.setCentralWidget(central_widget)
    
        

        # Crear la barra de herramientas
        self.toolbar = QToolBar()
        self.addToolBar(self.toolbar)  # Agregar la barra de herramientas a la ventana principal
        

       
        
        # Crear el logo
        ruta_imagen = "imagenes/01EnerfenixLOGO_Transparente01.png"
        logo = QLabel()
        logo.setPixmap(QPixmap(ruta_imagen))
        logo.setScaledContents(True)
        logo.setFixedSize(150,54)
        # logo.setStyleSheet("color: red; font-size: 43px; font-weight: bold; font-family: Arial;")
        self.toolbar.addWidget(logo)
   
        #contenedor de botones
        button_container = QWidget()
        button_layout = QHBoxLayout()
        button_container.setLayout(button_layout)

        
        
      # vrear los botones para los layout de la ventana
        boton1 = QPushButton("Efectivo")
        
        boton1.setStyleSheet("""
                             background-color: #00224D;
                             color: white; 
                             font-size: 20px; 
                             font-weight: bold; 
                             border-radius: 4px; 
                             padding: 10px;                             
                             """)
        boton1.setCursor(QCursor(Qt.PointingHandCursor))
        boton1.clicked.connect(lambda: generar_archivo_efectivo(self.df))
        button_layout.addWidget(boton1)
        
       

        boton2 = QPushButton("Credito")
        boton2.setStyleSheet("""
                             background-color: #5D0E41; 
                             color: white; 
                             font-size: 20px; 
                             font-weight: bold; 
                             border-radius: 4px;  
                             padding: 10px;                             
                             """)
        
        boton2.setCursor(QCursor(Qt.PointingHandCursor))
        boton2.clicked.connect(lambda: generar_archivo_flotillas(self.df))
        button_layout.addWidget(boton2) 

        boton3 = QPushButton("Resumen Efectivo")
        boton3.setStyleSheet("""
                             background-color:#FF204E;
                             color: white; 
                             font-size: 20px; 
                             font-weight: bold; 
                             border-radius: 4px; 
                             padding: 10px;
                             """)
        boton3.setCursor(QCursor(Qt.PointingHandCursor))
        button_layout.addWidget(boton3)
        boton3.clicked.connect(lambda: generar_archivo_efectivo_resumen(self.df), )
        

        #agregar el contenedor de botones layots al toolbar
        self.toolbar.addWidget(button_container)
        

        # crear un contenedor para el label y el entry del archivo
        file_container = QWidget()
        file_container.setFixedWidth(550)
        file_container.setFixedHeight(60)
        
        file_layout = QHBoxLayout()
        

        #crear el label del archivo
        label = QLabel("Cargar archivo:")
        label.setStyleSheet("""font-size: 12px; font-weight: bold; font-family: Arial; color:gray;""")  

        file_container.setLayout(file_layout)
        label.setFixedWidth(90)
        file_layout.addWidget(label)

        self.file_input = QLineEdit()
        self.file_input.setFixedWidth(250)
        self.file_input.setFixedHeight(30)
        self.file_input.setStyleSheet("""color: blue;""")
        file_layout.addWidget(self.file_input)

        
        boton_examinar = QPushButton("Examinar")
        boton_examinar.setFixedWidth(100)
        boton_examinar.setStyleSheet("""
                                     background-color:#00224D;
                                     color: white;
                                     font-size: 17px;
                                     font-weight: bold;
                                     border-radius: 100;
                                     padding: 10px;
                                     border-radius: 4px;                                
                                     """"")
        boton_examinar.clicked.connect(self.abrir_archivo)
        file_layout.addWidget(boton_examinar)

        # Agegar el contenedor de archivo al toolbar
        self.toolbar.addWidget(file_container)

        # configurar el estilo de los botones de la barra
        self.toolbar.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)


        # crear menu de hamburguesa
        menu = QMenu()

        # crear las acciones del menu
        action1 = menu.addAction("Ventas")
        
        action2 = menu.addAction("Conciliacion")
        
        action3 = menu.addAction("Historial")

        # añadir las acciones al menu
        button_menu = QToolButton()
        button_menu.setText('☰')
        button_menu.setFixedWidth(70)
        button_menu.setFixedHeight(40)
        button_menu.setStyleSheet("""font-size: 20px;""")
        button_menu.setMenu(menu)
        button_menu.setPopupMode(QToolButton.InstantPopup)

        # añadir el boton a la barra de herramientas
        self.toolbar.addWidget(button_menu)
    


        action2.triggered.connect(lambda: print('esta es la accion 2'))
        action1.triggered.connect(lambda: print('esta es la accion 1'))
   
        
        
       

        spacer = QWidget()
        spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        self.toolbar.addWidget(spacer)

        botn_recargar = QToolButton()
        botn_recargar.setText('↻')
        botn_recargar.setFixedWidth(40)
        botn_recargar.setFixedHeight(40)
        botn_recargar.setStyleSheet("""
                                     font-size: 30px;
                                     color: #fff; 
                                     font-weight: boldd;
                                     background-color: red;
                                     border-radius: 20px;
                                    """)
        self.toolbar.addWidget(botn_recargar)
        botn_recargar.clicked.connect(self.resetProgram)

        # crear layout de grilla
        self.grid_layout = QGridLayout()
        self.setLayout(self.grid_layout)
        
        # seconToolbar = QToolBar()
        # seconToolbar.setFixedWidth(150)

       


       
 


# se crea la caja de layout para la ubicacion de la venta        
        self.caja = QWidget()
        self.caja.setFont(QFont('Arial', 15))
        self.grid_layout.addWidget(self.caja, 0, 0)
        self.caja.setStyleSheet("""background-color: #17153B; color: white; font-size: 15px; font-weight: bold; padding: 5px; border-radius: 5px;""")
        self.caja.setFixedHeight(50)
        self.caja.setFixedWidth(520)
        self.caja_layout = QHBoxLayout()
        self.caja.setLayout(self.caja_layout)

        self.widgetTablas = QWidget()
        self.layoutTablas = QHBoxLayout()
        self.widgetTablas.setLayout(self.layoutTablas)
        self.widgetTablas.setFixedWidth(1200)
        self.widgetTablas.setFixedHeight(220)
        self.grid_layout.addWidget(self.widgetTablas, 1, 0, 1, 3)


        
        self.ubicacion_de_venta = QLabel("Venta de: ", self)
        self.ubicacion_de_venta.setStyleSheet(""" 
                                              font-size: 20px;
                                              font-weight: 600;
                                              font-family: Arial;
                                              """)
      
        self.caja_layout.addWidget(self.ubicacion_de_venta)

        # subsidiarias = [("ABEL", 6, 1, '0000109052'), ("J.DOLORES", 5, 3, '0000106536'), ("GASOFAR", 3, 2, '0001501329'), ("WEHENDY", 4, 5, '0000117933'), ("JARDINES", 8, 7, '0000510949')]
        subsidiarias = [("ABEL", 6, 1, '0000109052'), ("J.DOLORES", 5, 3, '0000106536'), ("GASOFAR", 3, 2, '0001501329'), ("WEHENDY", 4, 5, '0000117933'), ("CHALCO", 8, 7, '0000510949'), ("S.COMONFORT", 10, 10,'0000108161')]
        subsidiarias_dict = {id: nombre for nombre, _, _, id in subsidiarias}

# se crean las tablas junto con sus encabezados
        
        headersTablaIeps = ['combustible', 'precio', 'IEPS']
        headersTablaVentas = ['Total de venta', 'Efectivo', 'Credito', 'Diferencia', 'Autojarreos']
       


      
        self.tablaVenta = QTableWidget()  
        self.tablaVenta.setColumnCount(5)
        self.tablaVenta.setRowCount(1)


        # self.widgetTablas.addWidget(self.tablaVenta)
        self.layoutTablas.addWidget(self.tablaVenta)
        self.tablaVenta.setHorizontalHeaderLabels(headersTablaVentas)
        self.tablaVenta.setFixedWidth(520)
        self.tablaVenta.setFixedHeight(200)

        # espaciador = QSpacerItem(5, 500, QSizePolicy.Minimum, QSizePolicy.Expanding)
        # self.grid_layout.addItem(espaciador, 2, 0, 1, 3)
        
#total de venta en la tabla de totales
        total_venta_str = str(self.total_venta)
        self.tablaVenta.setItem(0,0, QTableWidgetItem(total_venta_str))

#total de efectivo en la tabla de totales
        total_efectivo_str = str(self.total_efectivo)
        self.tablaVenta.setItem(0,1, QTableWidgetItem(total_efectivo_str))

#total de flotillas en la tabla de totales
        total_flotillas_str = str(self.total_flotillas)
        self.tablaVenta.setItem(0,2, QTableWidgetItem(total_flotillas_str))
        
#diferencia en la tabla de totales
        diferencia_str = str(self.diferencia)
        self.tablaVenta.setItem(0,3, QTableWidgetItem(diferencia_str))

# total de autojarreos en la tabla de totales
        autojarreos_total_str = str(self.total_autojarreos)
        self.tablaVenta.setItem(0,4, QTableWidgetItem(autojarreos_total_str))
             
# tabla de ieps
        self.tablaIeps = QTableWidget()
        self.tablaIeps.setColumnCount(3)
        self.tablaIeps.setRowCount(3)
        # self.widgetTablas.addWidget(self.tablaIeps)
        self.layoutTablas.addWidget(self.tablaIeps)
        self.tablaIeps.setFixedWidth(320)
        self.tablaIeps.setFixedHeight(200)
      
        self.tablaIeps.setHorizontalHeaderLabels(headersTablaIeps)

# agregar mMagna a la tabla ieps
        self.tablaIeps.setItem(0, 0, QTableWidgetItem("MAGNA"))
        item = QTableWidgetItem("MAGNA")
        item.setBackground(QColor('#A7D82E'))
        item.setForeground(QColor('white'))
        font = QFont()
        font.setBold(True)
        item.setFont(font)
        self.tablaIeps.setItem(0, 0, item)


# agregar diesel a la tabla ieps
        # self.tablaIeps.setItem(1, 0, QTableWidgetItem("DIESEL"))
        item = QTableWidgetItem("DIESEL")
        item.setBackground(QColor('#191919'))
        item.setForeground(QColor('#fff'))
        font = QFont()
        font.setBold(True)
        item.setFont(font)
        self.tablaIeps.setItem(1, 0, item)

# agregar premium a la tabla ieps
        # self.tablaIeps.setItem(2, 0, QTableWidgetItem("PREMIUM"))
        item = QTableWidgetItem("PREMIUM")
        item.setBackground(QColor('#FF204E'))
        item.setForeground(QColor('white'))
        font = QFont()
        font.setBold(True)
        item.setFont(font)
        self.tablaIeps.setItem(2, 0, item)

#tabla transacciones
        self.tabla_transacciones = QTableWidget()
        self.tabla_transacciones.setColumnCount(2)
        self.tabla_transacciones.setRowCount(1)
        self.tabla_transacciones.setFixedWidth(320)
        self.tabla_transacciones.setFixedHeight(200)
        self.layoutTablas.addWidget(self.tabla_transacciones)
     
        self.tabla_transacciones.setHorizontalHeaderLabels(['N transacciones','T-credito'])
        
        


# agregar la tabla de layout efectivo
        # self.tablaLayoutEfectivo = QTableWidget()
        # self.tablaLayoutEfectivo.setColumnCount(9)
        # self.tablaLayoutEfectivo.setRowCount(3)
        # self.tablaLayoutEfectivo.setHorizontalHeaderLabels(headersTablelayoutEfectivo)
        self.widgetHistorialPrecios = QWidget()
        self.WidgethistorialPreciosLayout = QVBoxLayout()
        self.widgetHistorialPrecios.setLayout(self.WidgethistorialPreciosLayout)
        contenedorFiltros = QWidget()
        contenedorFiltros.setFixedWidth(550)
        

       



        tituloHistorialPrecios = QLabel("Historial de precios")
        self.filtroslayout = QHBoxLayout()
        tituloHistorialPrecios.setAlignment(Qt.AlignCenter)
        # self.filtroslayout.setAlignment(Qt.AlignCenter)
        
        contenedorFiltros.setLayout(self.filtroslayout)
        contenedorFiltros.setFixedWidth(980)
        contenedorFiltros.setFixedHeight(50)
        

        labelEstablecimiento = QLabel("Subsidiaria:")
        labelEstablecimiento.setStyleSheet("""font-size: 15px; color: grey; padding: 4px; border-radius: 5px; border: 1px solid gray;""")
        labelFechaInicio = QLabel("Fecha inicio:")
        labelFechaInicio.setStyleSheet("""font-size: 15px; color: grey; padding: 4px; border-radius: 5px; border: 1px solid gray;""")
        labelFechaFin = QLabel("Fecha fin:")
        labelFechaFin.setStyleSheet("""font-size: 15px; color: grey; padding: 4px; border-radius: 5px; border: 1px solid gray;""")

        self.comBoxEstablecimientos = QComboBox()
        self.fechaInicio = QDateEdit()
        self.fechaInicio.setDate(QDate.currentDate())
        self.fechaInicio.setFixedWidth(150)
        self.fechaInicio.setStyleSheet("""font-size: 15px; color: grey; padding: 4px; border-radius: 5px; border: 1px solid gray;""")
        self.fechaInicio.setCalendarPopup(True)

        self.fechaFin = QDateEdit()
        self.fechaFin.setDate(QDate.currentDate())
        self.fechaFin.setFixedWidth(150)
        self.fechaFin.setStyleSheet("""font-size: 15px; color: grey; padding: 4px; border-radius: 5px; border: 1px solid gray;""")
        self.fechaFin.setCalendarPopup(True)



        self.comBoxEstablecimientos = QComboBox()
        self.comBoxEstablecimientos.setStyleSheet("""font-size: 15px; color: grey; padding: 4px; border-radius: 5px; border: 1px solid gray;""")
        self.comBoxEstablecimientos.setFixedWidth(150)
        self.comBoxEstablecimientos.addItem("Todos")
        self.comBoxEstablecimientos.addItems([nombre for nombre, _, _, _ in subsidiarias])
        self.comBoxEstablecimientos.currentIndexChanged.connect(
             lambda: (
                  print(f"Opcion seleccionada:{self.comBoxEstablecimientos.currentText()}"),
                        self.cargarDatos(subsidiarias_dict.get(self.comBoxEstablecimientos.currentText()))
             )[1])
        
        self.filtroslayout.addWidget(labelEstablecimiento)
        self.filtroslayout.addWidget(self.comBoxEstablecimientos)
        self.filtroslayout.addWidget(labelFechaInicio)
        self.filtroslayout.addWidget(self.fechaInicio)
        
        self.filtroslayout.addWidget(labelFechaFin)
        self.filtroslayout.addWidget(self.fechaFin)

        self.WidgethistorialPreciosLayout.addWidget(tituloHistorialPrecios)
        self.WidgethistorialPreciosLayout.addWidget(contenedorFiltros)
        self.btnactualizar = QPushButton("Actualizar")
        self.btnactualizar.setFixedWidth(150)
        self.btnactualizar.setStyleSheet("""background-color: #071952; color: white; font-size: 15px; font-weight: bold; padding: 5px; border-radius: 5px;""")  
        self.filtroslayout.addWidget(self.btnactualizar) 
        self.btnactualizar.clicked.connect(self.actualizardatosHistorial)
        



       
        tituloHistorialPrecios.setStyleSheet("""
                                                font-size: 20px;
                                                font-weight: 600;
                                             """)
        tituloHistorialPrecios.setAlignment(Qt.AlignCenter)
        


        self.tablaHistorial = QTableWidget()

        self.tablaHistorial.setColumnCount(10)
        self.tablaHistorial.setHorizontalHeaderLabels(["ID", "Fecha", "Establecimiento", "Precio Magna", "Precio DIESEL ", "Precio PREMIUM", "IEPS MAGNA", "IEPS DIESEL", "IEPS PREMIUM", "Eliminar"])
        

        self.cargarDatos()
        self.actualizardatosHistorial()

    def eliminarRegistro(self, row):
      id_a_eliminar = self.tablaHistorial.item(row, 0).text()
      conn = sqlite3.connect('database/database.sqlite')
      cursor = conn.cursor()

      try:
           cursor.execute("DELETE FROM historial WHERE id = ?", (id_a_eliminar,))
           conn.commit()

           print(" Registro con  ID {id_a_eliminar} eliminado correctamente")

           self.cargarDatos()
      except:
           print("Error al eliminar el registro: {e}")
      finally:
           cursor.close()
           conn.close()
    
    def actualizardatosHistorial(self):
        establecimientoID = self.comBoxEstablecimientos.currentText()
       
      
        self.cargarDatos(establecimientoID)


    def cargarDatos(self, establecimientoID=None, fechaInicio=None, fechaFin=None):
        conn = sqlite3.connect('database/database.sqlite')
        cursor = conn.cursor()
        try:
            query = 'SELECT * FROM historial'
            params = []
           

            if establecimientoID and establecimientoID != "Todos":
                #  query = 'SELECT * FROM historial WHERE establecimientoID = ? ORDER BY fecha DESC'
                # conditions.append('establecimientoID = ?')
                query += ' WHERE establecimientoID = ?'
                params.append(establecimientoID)
            elif fechaInicio and fechaFin:
                query += " WHERE strftime('%Y-%m-%d', fecha) BETWEEN ? AND ?"
                params.extend([fechaInicio, fechaFin])
            query += ' ORDER BY fecha DESC' 

                #  cursor.execute(query, (establecimientoID,))
            print("Consulta SQL:", query)
            print("parametros:", params)

            
            cursor.execute(query, params)
            registros = cursor.fetchall()
            
            
            self.comBoxEstablecimientos.currentIndexChanged.connect(self.actualizardatosHistorial)
            self.tablaHistorial.setRowCount(len(registros))
            self.tablaHistorial.setColumnCount(10)
            self.tablaHistorial.setHorizontalHeaderLabels(["ID", "Fecha", "Establecimiento", "Precio Magna", "Precio DIESEL", "Precio Premium", "IEPS Magna", "IEPS Diesel", "IEPS Premium", "Eliminar"])
            self.tablaHistorial.setColumnWidth(0, 15)
            

            for i, registro in enumerate(registros): 
                    for j in range(9):
                        item = QTableWidgetItem(str(registro[j]))
                        if i % 2 == 0:
                            item.setBackground(QColor(220, 220, 220))
                        self.tablaHistorial.setItem(i, j, item)
                        # self.tablaHistorial.setItem(i, j, QTableWidgetItem(str(registro[j])))
                    
                        btnEliminar = QPushButton("Eliminar")
                        btnEliminar.setStyleSheet("background-color: #FF0000; color: white; font-weight: bold; padding: 3px; border-radius: 5px;")
                        btnEliminar.clicked.connect(lambda _, row=i: self.eliminarRegistro(row))
                        self.tablaHistorial.setCellWidget(i, 9, btnEliminar)
                       

        except sqlite3.Error as e:
               print(f"Error al acceder a la base de datos: {e}")
        finally:
                cursor.close()
                conn.close()

        self.WidgethistorialPreciosLayout.addWidget(self.tablaHistorial)
        self.grid_layout.addWidget(self.widgetHistorialPrecios, 4, 0, 1, 1)
        # self.WidgethistorialPreciosLayout.addWidget(self.widgetHistorialPrecios)
        self.tablaHistorial.setFixedHeight(300)
        self.grid_layout.addWidget(self.widgetHistorialPrecios, 4, 0, 1, 3)


        # self.tablaLayoutCredito = QTableWidget()
        # self.tablaLayoutCredito.setColumnCount(9)
        # self.tablaLayoutCredito.setRowCount(3)
        # self.grid_layout.addWidget(self.tablaLayoutCredito, 5, 0, 3, 3)
        # self.tablaLayoutCredito.setHorizontalHeaderLabels(headerTablelayoutCredito)

# tabla numero de transacciones
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        central_widget.setLayout(self.grid_layout)

    def resetProgram(self):
        print('Resetting program...')

        valores_ieps = []
        for fila in range(self.tablaIeps.rowCount()):
            for columna in range(self.tablaIeps.columnCount()):
                item = self.tablaIeps.item(fila, columna)       
                if item is not None:
                    valores_ieps.append(item.text())
                else:
                    valores_ieps.append("")
        


        self.total_venta = 0
        self.total_efectivo = 0
        self.total_flotillas = 0
        self.diferencia = 0
        self.total_autojarreos = 0

        self.tablaVenta.setItem(0, 0, QTableWidgetItem(str(self.total_venta)))
        self.tablaVenta.setItem(0, 1, QTableWidgetItem(str(self.total_efectivo)))
        self.tablaVenta.setItem(0, 2, QTableWidgetItem(str(self.total_flotillas)))
        self.tablaVenta.setItem(0, 3, QTableWidgetItem(str(self.diferencia)))
        self.tablaVenta.setItem(0, 4, QTableWidgetItem(str(self.total_autojarreos)))

        self.ubicacion_de_venta.setText("Venta de: ")        

        for fila in range(self.tablaIeps.rowCount()):
            if fila == 0 or fila ==1 or fila == 2:
                self.tablaIeps.setItem(fila, 1,  QTableWidgetItem('0'))
                self.tablaIeps.setItem(fila, 2,  QTableWidgetItem('0'))
            
        
        return

    def abrir_archivo(self):
        self.df = None
        file_name, _ = QFileDialog.getOpenFileName(self, "Archivos Excel (*.xlsx)")

        if file_name:
           try:
              self.df = pd.read_excel(file_name, skiprows=2, dtype={'EstablecimientoID': str})
           except Exception as e:
                 QMessageBox.warning(self, 'Error', f'Error al abrir el archivo: {e}')
                 return

        
        # self.df = pd.read_excel(file_name, skiprows=2, dtype={'EstablecimientoID': str})

      
        if self.df is not None:
           
           fecha = self.df['Fecha'].iloc[0].strftime('%d/%m/%Y')
           establecimientoID = self.df['EstablecimientoID'].iloc[0]
        #    datos = print('los datos')
           self.cargarDatos()

           
           
           
           self.Fecha = self.df['Fecha'] = pd.to_datetime(self.df['Fecha'])
           self.fecha_unica = self.df['Fecha'].iloc[0].strftime('%d/%m/%Y')
       
           fecha_min = self.df['Fecha'].min().strftime('%d/%m/%Y')
           fecha_max = self.df['Fecha'].max().strftime('%d/%m/%Y')
       
           gruposDePrecios = agrupar_precios(self.df)
       
           if (self.df['EstablecimientoID'] == '0000109052').any():
                self.ubicacion_de_venta.setText(f'Venta de: ABEL  del {self.fecha_unica}')
           elif (self.df['EstablecimientoID'] == '0000106536').any():
                self.ubicacion_de_venta.setText(f'Venta de: J.DOLORES del {self.fecha_unica}')
           elif (self.df['EstablecimientoID'] == '0001501329').any():
                self.ubicacion_de_venta.setText(f'Venta de: GASOFAR del  del {self.fecha_unica} ')
           elif (self.df['EstablecimientoID'] == '0000117933').any():
                self.ubicacion_de_venta.setText(f'Venta de: WEHENDY del  del {self.fecha_unica} ')
           elif (self.df['EstablecimientoID'] == '0000510949').any():
                self.ubicacion_de_venta.setText(f'Venta de: JARDINES  del {self.fecha_unica}')
           elif (self.df['EstablecimientoID'] == '0000108161').any():
                self.ubicacion_de_venta.setText(f'Venta de: S. SCOMONFORT  del {self.fecha_unica}')
           
           else:
                self.ubicacion_de_venta.setText('Venta de: Otra ubicacion')
                # print('la ubicacion es ',self.df['EstablecimientoID'].head())
         
           
           
          
        else:
            print('no se encontro el archivo')

        if file_name:
            file_name_only = os.path.basename(file_name)
            self.file_input.setText(file_name_only)
        #     print(file_name)
            self.df = pd.read_excel(file_name, skiprows=2)
        #     print(self.df)

# buscar fecha unica
            fechas_unicas = self.df['Fecha'].dropna().dt.date.unique()
            

# contar el numero de fechas
            numero_de_fechas = len(fechas_unicas)

# saber si hay mas ded una fecha en el archivo
            if numero_de_fechas > 1:
                  
                  fechas_unicas_str = [fecha.strftime('%d/%m/%Y') for fecha in fechas_unicas]

                  alert_message = f' Sam! se encontraron {numero_de_fechas} fechas en el archivo: {", ".join(fechas_unicas_str)} '

                  QMessageBox.warning(self, 'Advertencia', alert_message)
                                 
# muestra el total de venta en la tabla de totales
            self.total_venta = self.df['Importe'].sum().round(2)
        #     print(self.total_venta)
            total_venta_str = str(self.total_venta)
            self.tablaVenta.setItem(0,0,QTableWidgetItem(total_venta_str))
# muestra el total de efectivo en la tabla de totales            
            _, self.total_efectivo = layout_efectivo(self.df)
            total_efectivo_str = str(self.total_efectivo.round(2))
            self.tablaVenta.setItem(0,1,QTableWidgetItem(total_efectivo_str))
# muestra el total de flotillas en la tabla de totales            
            _,self.total_flotillas, self.NFlotillas = layout_flotillas(self.df)
            total_flotillas_str = str(self.total_flotillas.round(2))
            self.tablaVenta.setItem(0,2,QTableWidgetItem(total_flotillas_str))
# muestra la diferencia en la tabla de totales           
            self.diferencia = self.total_efectivo + self.total_flotillas - self.total_venta
            diferencia_str = str(self.diferencia.round(2))
        #     print('la direfencia es: ',self.diferencia.round(2))   
            self.tablaVenta.setItem(0,3,QTableWidgetItem(diferencia_str))
# muestra el total de autojarreos en la tabla de totales           
            self.total_autojarreos = self.df[self.df['TipoPago'] == 'AUTO JARREOS']
        #     print(self.total_autojarreos)
            self.autojarreos_total = self.total_autojarreos['Importe'].sum()
            self.tablaVenta.setItem(0,4,QTableWidgetItem(str(self.autojarreos_total.round(2))))
            
                
# llamar a la funcion preciosC con el Dataframe          
            precioMagna, precioDiesel, precioPremium, iepsfinalMagna, iepsfinalDiesel, iepsfinalPremium = precios_C(self.df)
            self.tablaIeps.setItem(0, 1, QTableWidgetItem(str(precioMagna)))
            self.tablaIeps.setItem(1, 1, QTableWidgetItem(str(precioDiesel)))
            self.tablaIeps.setItem(2, 1, QTableWidgetItem(str(precioPremium)))

# se agregan los valores del ipes por combustibel a la tabla 
            self.tablaIeps.setItem(0, 2, QTableWidgetItem(str(round(iepsfinalMagna,8))))
            self.tablaIeps.setItem(1, 2, QTableWidgetItem(str(round(iepsfinalDiesel,8))))
            self.tablaIeps.setItem(2, 2, QTableWidgetItem(str(round(iepsfinalPremium,8))))

# agregar numero de transacciones a la tabla de transacciones
            self.tabla_transacciones.setItem(0,1, QTableWidgetItem(str(self.NFlotillas)))

            
            self.ventanaemergenteB = ventanaemergenteB(self, fecha, establecimientoID, precioMagna,iepsfinalMagna, precioDiesel, iepsfinalDiesel, precioPremium, iepsfinalPremium)
            self.ventanaemergenteB.show()

        
        
        
                


app = QApplication([])
window = MainWindow()
window.show()
app.exec_()