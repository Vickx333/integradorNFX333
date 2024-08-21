import pandas as pd
import sys
from PyQt5.QtWidgets import QApplication, QDialog, QTableWidget, QVBoxLayout, QTableWidgetItem


def precios_C( df):
    # print("Precios de los productos")
# filtrar por productos
    df = df[df['Producto'].isin(['DIESEL', 'MAGNA', 'PREMIUM'])]

# agregar productos y obtener el precio
    grupo = df.groupby('Producto')['Precio'].first()


    # precioMagna = grupo['MAGNA']
    # precioDiesel = grupo['DIESEL']
    # precioPremium = grupo['PREMIUM']
    precioMagna = precioDiesel = precioPremium = 0

    # print(grupo)

    cuotaMagna = 0.545050
    cuotaDiesel = 0.452358
    cuotaPremium = 0.665062
    litros = 10

    if 'MAGNA' in grupo:
        precioMagna = grupo['MAGNA']
    if 'DIESEL' in grupo:
        precioDiesel = grupo['DIESEL']
    if 'PREMIUM' in grupo:
        precioPremium = grupo['PREMIUM']
# calculo ieps MAGNA
    iepsMagna = litros * cuotaMagna
    #print("IEPS Magna: ", iepsMagna)

    precioTotalMagna = (litros * precioMagna ) - iepsMagna
    #print("Precio Total Magna: ", precioTotalMagna.round(2))

    subtotalMagna = precioTotalMagna / 1.16
    #print("Subtotal Magna: ", subtotalMagna.round(2))

    ivaMagna = subtotalMagna * 0.16
    #print("IVA Magna: ", ivaMagna.round(2))

    iepsfinalMagna = (iepsMagna* 100) / subtotalMagna
    # print("IEPS Final Magna: ", iepsfinalMagna.round(8))

# caulculo ieps DIESEL

    iepsDiesel = litros * cuotaDiesel
    #print("IEPS Diesel: ", iepsDiesel)

    precioTotalDiesel = (litros * precioDiesel ) - iepsDiesel
    #print("Precio Total Diesel: ", precioTotalDiesel.round(2))

    subtotalDiesel = precioTotalDiesel / 1.16
    #print("Subtotal Diesel: ", subtotalDiesel.round(2))

    ivaDiesel = subtotalDiesel * 0.16
    #print("IVA Diesel: ", ivaDiesel.round(2))

    iepsfinalDiesel = (iepsDiesel* 100) / subtotalDiesel
    # print("IEPS Final Diesel: ", iepsfinalDiesel.round(8))

# calculo ieps PREMIUM
    
    iepsPremium = litros * cuotaPremium
    #print("IEPS Premium: ", iepsPremium)

    precioTotalPremium = (litros * precioPremium ) - iepsPremium
    #print("Precio Total Premium: ", precioTotalPremium.round(2))

    subtotalPremium = precioTotalPremium / 1.16
    #print("Subtotal Premium: ", subtotalPremium.round(2))

    ivaPremium = subtotalPremium * 0.16
    #print("IVA Premium: ", ivaPremium.round(2))

    iepsfinalPremium = (iepsPremium* 100) / subtotalPremium
    # print("IEPS Final Premium: ", iepsfinalPremium.round(8))





# recorrer cada grupo

    return precioMagna, precioDiesel, precioPremium, iepsfinalMagna, iepsfinalDiesel, iepsfinalPremium


def agrupar_precios(df):
    df_precio = df[df['Producto'].isin(['DIESEL', 'MAGNA', 'PREMIUM'])]
    grupos = df_precio.groupby(['Producto', 'Precio']).size().reset_index(name='Cantidad')
    # print(grupos)

    # Clase de la ventana emergente
    class GruposDialog(QDialog):
        def __init__(self, grupos, parent=None):
            super().__init__(parent)
            self.setWindowTitle("Grupos de Precios")
            self.resize(400, 300)

            # Inicializar QTableWidget
            self.tableWidget = QTableWidget()
            self.tableWidget.setRowCount(len(grupos))
            self.tableWidget.setColumnCount(len(grupos.columns))
            self.tableWidget.setHorizontalHeaderLabels(grupos.columns)

            # Llenar la tabla con los datos
            for i in range(len(grupos)):
                for j in range(len(grupos.columns)):
                    self.tableWidget.setItem(i, j, QTableWidgetItem(str(grupos.iloc[i, j])))

            # Layout
            layout = QVBoxLayout()
            layout.addWidget(self.tableWidget)
            self.setLayout(layout)

    # Mostrar la ventana emergente
    app = QApplication.instance() if QApplication.instance() else QApplication(sys.argv)
    dialog = GruposDialog(grupos)
    dialog.exec_()

    return grupos


