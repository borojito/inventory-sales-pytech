import csv

def leer_productos(ruta_archivo):
    """
    Lee los datos de un archivo CSV y los imprime en formato estructurado.
    Args:
        ruta_archivo (str): Ruta al archivo CSV.
    Returns:
        list: Lista de diccionarios con los datos de cada producto.
    """
    productos = []
    with open(ruta_archivo, mode='r', encoding='utf-8') as archivo:
        lector = csv.DictReader(archivo)
        for fila in lector:
            productos.append(fila)
    return productos

def leer_ventas(ruta_archivo):

    ventas = []
    with open(ruta_archivo, mode='r', encoding='utf-8') as archivo:
        lector = csv.DictReader(archivo)
        for fila in lector:
            ventas.append(fila)
    return ventas


def leer_ventas(ruta_archivo):
    ventas = []

    with open(ruta_archivo, mode='r', encoding='utf-8') as archivo:
        lector = csv.DictReader(archivo)

        for fila in lector:
            ventas.append(fila)

    return ventas

#*****************************************

# PROCESAR DATOS DE PRODUCTOS Y VENTAS

# Leer archivos
lista_productos = leer_productos("productos.csv")
ventas = leer_ventas("ventas.csv")


# actualizar el stock de productos según las ventas

for producto in lista_productos:

    stock_actual = int(producto["stock_inicial"])
    id_producto = producto["id_producto"]

    for venta in ventas:

        if venta["id_producto"] == id_producto:
            total_vendido = int(venta["cantidad"])

            if total_vendido <= stock_actual:
                stock_actual -= total_vendido

    producto["stock_final"] = stock_actual

# CREAR ARCHIVO DE SALIDA
with open("inventario_actualizado.csv", mode="w", newline="", encoding="utf-8") as archivo:

    columnas = [
        "id_producto",
        "nombre_producto",
        "precio",
        "stock_inicial",
        "stock_final"
    ]

    escritor = csv.DictWriter(archivo, fieldnames=columnas)

    escritor.writeheader()
    escritor.writerows(lista_productos)

print("Archivo inventario_actualizado.csv creado correctamente")

#****************************************

# REPORTE DE VENTAS

ingresos_totales = 0

producto_mas_vendido = ""
cantidad_mas_vendida = 0

producto_mayor_ingreso = ""
mayor_ingreso = 0

errores = []

# RECORRER PRODUCTOS
for producto in lista_productos:

    id_producto = producto["id_producto"]
    nombre = producto["nombre_producto"]
    precio = float(producto["precio"])

    stock_actual = int(producto["stock_inicial"])

    unidades_vendidas = 0
    ingresos_producto = 0

    for venta in ventas:

        if venta["id_producto"] == id_producto:

            cantidad = int(venta["cantidad"])

            # VALIDAR STOCK REAL
            if cantidad > stock_actual:

                errores.append(
                    f"No hay suficiente stock para '{nombre}' ({id_producto})"
                )

            else:

                stock_actual -= cantidad

                unidades_vendidas += cantidad

                total = cantidad * precio

                ingresos_producto += total

                ingresos_totales += total


    # PRODUCTO MÁS VENDIDO
    if unidades_vendidas > cantidad_mas_vendida:

        cantidad_mas_vendida = unidades_vendidas
        producto_mas_vendido = nombre
        id_mas_vendido = id_producto


    # PRODUCTO CON MÁS INGRESOS
    if ingresos_producto > mayor_ingreso:

        mayor_ingreso = ingresos_producto
        producto_mayor_ingreso = nombre
        id_mayor_ingreso = id_producto

# CREAR ARCHIVO TXT
with open("reporte_ventas.txt", "w", encoding="utf-8") as archivo:

    archivo.write("=== Reporte de Ventas PyTech Store ===\n\n")

    archivo.write(
        f"Ingresos Totales: ${ingresos_totales:,.2f}\n\n"
    )

    archivo.write(
        f"Producto Más Vendido (unidades): "
        f"'{cantidad_mas_vendida}' "
        f"({id_mas_vendido}), "
        f"con {cantidad_mas_vendida} unidades.\n"
    )

    archivo.write(
        f"Producto con Mayores Ingresos: "
        f"'{mayor_ingreso}' "
        f"({id_mayor_ingreso}), "
        f"generando ${mayor_ingreso:,.2f}.\n"
    )

    archivo.write("--- Ventas No Procesadas ---\n")

    for error in errores:
        archivo.write(f"- {error}\n")


print("Reporte generado correctamente")