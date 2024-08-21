from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QTableWidget, QTableWidgetItem, QPushButton,QMessageBox
from PyQt5.QtCore import Qt
import sqlite3
from PyQt5.QtGui import QColor

class vistaHistorial(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.configurarUI()

    def configurarUI(self):
        titulo = QLabel("Historial de precios")
        titulo.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(titulo)

        self.tablaHistorial = QTableWidget()
        self.layout.addWidget(self.tablaHistorial)
        self.cargarDatos()

    def cargarDatos(self):
        conn = sqlite3.connect('database/database.sqlite')
        cursor = conn.cursor()
        try:
             
            cursor.execute('SELECT * FROM historial')
            registros = cursor.fetchall()
    
            self.tablaHistorial.setRowCount(len(registros))
            self.tablaHistorial.setColumnCount(10)
            self.tablaHistorial.setHorizontalHeaderLabels(["ID", "Fecha", "Establecimiento", "Precio Magna", "IEPS Magna", "Precio Diesel", "IEPS Diesel", "Precio Premium", "IEPS Premium"])
    
    
    
            for i, registro in enumerate(registros):
                # for j, valor in enumerate(registro):
                    for j in range((9)):
                        item = QTableWidgetItem(str(registro[j]))
                        if i % 2 == 0:
                            item.setBackground(Qt.gray)
                    #    self.tablaHistorial.setItem(i, j, QTableWidgetItem(str(registro[j])))
                        self.tablaHistorial.setItem(i, j, item)
                    

                    btn_eliminar = QPushButton("Eliminar")
                    btn_eliminar.setStyleSheet("background-color: red; color: white;")

                    self.tablaHistorial.setCellWidget(i, 9, btn_eliminar)


        except sqlite3.Error as e:
             print(f"Error al acceder a la base de datos: {e}")
        finally:
             cursor.close()
             conn.close()

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

    
    


def obtenerdatosHistorial(self):
            conn = sqlite3.connect('database/database.sqlite')
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM historial")
            datos = cursor.fetchall()
            conn.close()

            return datos


