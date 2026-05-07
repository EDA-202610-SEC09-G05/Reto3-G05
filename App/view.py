import sys
from tabulate import tabulate
from App import logic as l
from DataStructures.Map import map_separate_chaining as mc

def new_logic():
    """
        Se crea una instancia del controlador
    """
    return l.new_logic()

def print_menu():
    print("Bienvenido")
    print("0- Cargar información")
    print("1- Ejecutar Requerimiento 1")
    print("2- Ejecutar Requerimiento 2")
    print("3- Ejecutar Requerimiento 3")
    print("4- Ejecutar Requerimiento 4")
    print("5- Ejecutar Requerimiento 5")
    print("6- Ejecutar Requerimiento 6")
    print("7- Salir")

def load_data(control):
    """
    Carga de datos
    """

    while True:
        print("Ingrese el tamaño del archivo:")
        print("1) test")
        print("2) small")
        print("3) medium")
        print("4) large")
        opcion = input("Seleccione una opción: ").strip().lower()

        match opcion:
            case("1"):
                opcion = "test"
                break
            case("2"):
                opcion = "small"
                break
            case("3"):
                opcion = "medium"
                break
            case("4"):
                opcion = "large"
                break
            case _:
                print("Opción inválida. Debe ingresar un número entre 1 y 4.")

    catalog, dtime, total, first_five, last_five = l.load_data(control, opcion)

    print("\n" + "=" * 80)
    print("RESUMEN DE CARGA")
    print("=" * 80)

    resumen = [
        ["Archivo cargado", f"mercedes_sales_{opcion}.csv"],
        ["Tiempo de carga (ms)", round(dtime, 2)],
        ["Total de ventas cargadas", total]
    ]

    print(tabulate(resumen, headers=["Campo", "Valor"], tablefmt="fancy_grid"))

    print("\n" + "=" * 80)
    print("PRIMERAS 5 VENTAS")
    print("=" * 80)

    print(tabulate(first_five, headers="keys", tablefmt="fancy_grid"))

    print("\n" + "=" * 80)
    print("ÚLTIMAS 5 VENTAS")
    print("=" * 80)

    print(tabulate(last_five, headers="keys", tablefmt="fancy_grid"))

    return catalog


def print_req_1(control):
    print("\n" + "=" * 80)
    print("REQUERIMIENTO 1: Ventas por modelo y rango de precio")
    print("=" * 80)

    while True:
        model = input("Ingrese el modelo a consultar: ").strip()

        try:
            price_min = float(input("Ingrese el precio mínimo: "))
            price_max = float(input("Ingrese el precio máximo: "))
        except ValueError:
            print("Valor inválido. Ingrese precios numéricos.")
            continue

        if price_min > price_max or price_min < 0 or price_max < 0:
            print("Rango de precios inválido. Intente nuevamente.")
            continue

        break

    resumen, ventas = l.req_1(control, model, price_min, price_max)

    print("\n" + "=" * 80)
    print("RESUMEN DEL REQUERIMIENTO 1")
    print("=" * 80)

    print(tabulate(resumen, headers=["Campo", "Valor"], tablefmt="fancy_grid"))

    print("\n" + "=" * 80)
    print("VENTAS FILTRADAS")
    print("=" * 80)

    if len(ventas) == 0:
        print("No se encontraron ventas para el modelo y rango especificados.")
        return

    print(tabulate(ventas, headers="keys", tablefmt="fancy_grid"))


def print_req_2(control):
    print("\n" + "=" * 80)
    print("REQUERIMIENTO 2: Ventas por tipo de combustible y rango de horsepower")
    print("=" * 80)

    fuel_type = input("Ingrese el tipo de combustible: ").strip()
    min_hp = int(input("Ingrese el horsepower mínimo: "))
    max_hp = int(input("Ingrese el horsepower máximo: "))

    result = l.req_2(control, fuel_type, min_hp, max_hp)

    print("\n" + "=" * 80)
    print("RESUMEN DEL REQUERIMIENTO 2")
    print("=" * 80)

    resumen = [
        ["Tipo de combustible", fuel_type],
        ["Horsepower mínimo", min_hp],
        ["Horsepower máximo", max_hp],
        ["Tiempo de ejecución (ms)", round(result["time_ms"], 2)],
        ["Total de ventas encontradas", result["total_sales"]],
        ["Promedio de precio (USD)", round(result["avg_price"], 2)],
        ["Promedio de horsepower", round(result["avg_horsepower"], 2)]
    ]

    print(tabulate(resumen, headers=["Campo", "Valor"], tablefmt="fancy_grid"))

    sales_list = result["sales"]
    shown = l.al.size(sales_list)

    headers = [
        "Model",
        "Year",
        "Fuel Type",
        "Color",
        "Base Price (USD)",
        "Horsepower",
        "Turbo"
    ]

    print("\n" + "=" * 80)
    print("VENTAS FILTRADAS")
    print("=" * 80)

    if result["total_sales"] <= 12:
        table = []
        for i in range(shown):
            sale = l.al.get_element(sales_list, i)
            table.append([
                sale["model"],
                sale["year"],
                sale["fuel_type"],
                sale["color"],
                sale["base_price"],
                sale["horsepower"],
                sale["turbo"]
            ])
        print(tabulate(table, headers=headers, tablefmt="fancy_grid"))
    else:
        print("\n" + "-" * 80)
        print("PRIMERAS 6 VENTAS")
        print("-" * 80)

        first_table = []
        for i in range(6):
            sale = l.al.get_element(sales_list, i)
            first_table.append([
                sale["model"],
                sale["year"],
                sale["fuel_type"],
                sale["color"],
                sale["base_price"],
                sale["horsepower"],
                sale["turbo"]
            ])
        print(tabulate(first_table, headers=headers, tablefmt="fancy_grid"))

        print("\n" + "-" * 80)
        print("ÚLTIMAS 6 VENTAS")
        print("-" * 80)

        last_table = []
        for i in range(6, 12):
            sale = l.al.get_element(sales_list, i)
            last_table.append([
                sale["model"],
                sale["year"],
                sale["fuel_type"],
                sale["color"],
                sale["base_price"],
                sale["horsepower"],
                sale["turbo"]
            ])
        print(tabulate(last_table, headers=headers, tablefmt="fancy_grid"))


def print_req_3(control):
    print("\n" + "=" * 80)
    print("REQUERIMIENTO 3: Ventas por año, tipo de combustible y rango de precio")
    print("=" * 80)

    year = int(input("Ingrese el año: "))
    fuel_type = input("Ingrese el tipo de combustible: ").strip()
    min_price = float(input("Ingrese el precio mínimo (USD): "))
    max_price = float(input("Ingrese el precio máximo (USD): "))

    result = l.req_3(control, year, fuel_type, min_price, max_price)

    print("\n" + "=" * 80)
    print("RESUMEN DEL REQUERIMIENTO 3")
    print("=" * 80)

    resumen = [
        ["Año", year],
        ["Tipo de combustible", fuel_type],
        ["Precio mínimo (USD)", min_price],
        ["Precio máximo (USD)", max_price],
        ["Tiempo de ejecución (ms)", round(result["time_ms"], 2)],
        ["Total de ventas encontradas", result["total_sales"]],
        ["Promedio de precio (USD)", round(result["avg_price"], 2)]
    ]

    print(tabulate(resumen, headers=["Campo", "Valor"], tablefmt="fancy_grid"))

    sales_list = result["sales"]
    total_real = result["total_sales"]
    total_mostrar = l.al.size(sales_list)

    print("\n" + "=" * 80)
    print("VENTAS FILTRADAS")
    print("=" * 80)

    if total_mostrar == 0:
        print("No se encontraron ventas que cumplan los criterios.")
        return

    headers = [
        "Model",
        "Year",
        "Fuel Type",
        "Color",
        "Base Price (USD)",
        "Horsepower",
        "Turbo"
    ]

    if total_real <= 12:
        table = []
        for i in range(total_mostrar):
            sale = l.al.get_element(sales_list, i)
            table.append([
                sale["model"],
                sale["year"],
                sale["fuel_type"],
                sale["color"],
                sale["base_price"],
                sale["horsepower"],
                sale["turbo"]
            ])

        print(tabulate(table, headers=headers, tablefmt="fancy_grid"))

    else:
        print("\n" + "-" * 80)
        print("PRIMERAS 6 VENTAS")
        print("-" * 80)

        first_table = []
        for i in range(6):
            sale = l.al.get_element(sales_list, i)
            first_table.append([
                sale["model"],
                sale["year"],
                sale["fuel_type"],
                sale["color"],
                sale["base_price"],
                sale["horsepower"],
                sale["turbo"]
            ])

        print(tabulate(first_table, headers=headers, tablefmt="fancy_grid"))

        print("\n" + "-" * 80)
        print("ÚLTIMAS 6 VENTAS")
        print("-" * 80)

        last_table = []
        for i in range(6, 12):
            sale = l.al.get_element(sales_list, i)
            last_table.append([
                sale["model"],
                sale["year"],
                sale["fuel_type"],
                sale["color"],
                sale["base_price"],
                sale["horsepower"],
                sale["turbo"]
            ])

        print(tabulate(last_table, headers=headers, tablefmt="fancy_grid"))


def print_req_4(control):
    print("\n" + "=" * 80)
    print("REQUERIMIENTO 4: Top N modelos más vendidos por año")
    print("=" * 80)

    year = int(input("Ingrese el año a consultar: "))
    n = int(input("Ingrese la cantidad N de modelos a mostrar: "))

    resumen, modelos = l.req_4(control, year, n)

    print("\n" + "=" * 80)
    print("RESUMEN DEL REQUERIMIENTO 4")
    print("=" * 80)

    print(tabulate(resumen, headers=["Campo", "Valor"], tablefmt="fancy_grid"))

    if len(modelos) == 0:
        print("\nNo se encontraron modelos para el año consultado.")
        return

    print("\n" + "=" * 80)
    print("TOP MODELOS MÁS VENDIDOS")
    print("=" * 80)

    table = []

    for stat in modelos:
        table.append([
            stat["Model"],
            stat["Vehículos vendidos"],
            stat["Precio promedio"],
            stat["Horsepower promedio"],
            stat["Turbo Yes (%)"]
        ])

    headers = [
        "Modelo",
        "Vehículos vendidos",
        "Precio promedio",
        "Horsepower promedio",
        "Turbo Yes (%)"
    ]

    print(tabulate(table, headers=headers, tablefmt="fancy_grid"))

    print("\n" + "=" * 80)
    print("MEJOR VEHÍCULO POR MODELO (MAYOR HORSEPOWER)")
    print("=" * 80)

    for stat in modelos:
        print(f"\nModelo: {stat['Model']}")
        print(stat["Mejor Horsepower"])



def print_req_5(control):
    print("\n" + "=" * 80)
    print("REQUERIMIENTO 5: Top N de colores con más ventas por rango de horsepower")
    print("=" * 80)

    hp_ref = int(input("Ingrese el horsepower de referencia: "))
    delta = int(input("Ingrese el delta de horsepower: "))
    top_n = int(input("Ingrese la cantidad N de colores a mostrar: "))

    result = l.req_5(control, hp_ref, delta, top_n)

    print("\n" + "=" * 80)
    print("RESUMEN DEL REQUERIMIENTO 5")
    print("=" * 80)

    resumen = [
        ["Horsepower de referencia", hp_ref],
        ["Delta de horsepower", delta],
        ["Rango considerado", f"[{hp_ref - delta}, {hp_ref + delta}]"],
        ["Tiempo de ejecución (ms)", round(result["time_ms"], 2)],
        ["Total de vehículos en el rango", result["total_vehicles"]]
    ]

    print(tabulate(resumen, headers=["Campo", "Valor"], tablefmt="fancy_grid"))

    colors_list = result["top_colors"]
    total = l.al.size(colors_list)

    print("\n" + "=" * 80)
    print("TOP COLORES")
    print("=" * 80)

    if total == 0:
        print("No se encontraron vehículos en el rango de horsepower.")
        return

    table = []
    for i in range(total):
        item = l.al.get_element(colors_list, i)
        table.append([
            item["color"],
            item["count"],
            round(item["avg_hp"], 2)
        ])

    headers = [
        "Color",
        "Número de vehículos vendidos",
        "Horsepower promedio"
    ]

    print(tabulate(table, headers=headers, tablefmt="fancy_grid"))


def print_req_6(control):
    print("\n" + "=" * 80)
    print("REQUERIMIENTO 6: Modelos con precio base más estable")
    print("=" * 80)

    year_min = int(input("Ingrese el año inicial: "))
    year_max = int(input("Ingrese el año final: "))
    price_min = float(input("Ingrese el precio mínimo (USD): "))
    price_max = float(input("Ingrese el precio máximo (USD): "))
    m = int(input("Ingrese la cantidad M de modelos a mostrar: "))

    result = l.req_6(control, year_min, year_max, price_min, price_max, m)

    print("\n" + "=" * 80)
    print("RESUMEN DEL REQUERIMIENTO 6")
    print("=" * 80)

    resumen = [
        ["Rango de años", f"[{year_min}, {year_max}]"],
        ["Rango de precios", f"[{price_min}, {price_max}]"],
        ["Tiempo de ejecución (ms)", round(result["time_ms"], 2)],
        ["Total de modelos considerados", result["total_models"]]
    ]

    print(tabulate(resumen, headers=["Campo", "Valor"], tablefmt="fancy_grid"))

    models_list = result["models"]

    if l.al.size(models_list) == 0:
        print("\nNo se encontraron modelos que cumplan los criterios.")
        return

    print("\n" + "=" * 80)
    print("MODELOS MÁS ESTABLES")
    print("=" * 80)

    table = []

    for i in range(l.al.size(models_list)):
        stat = l.al.get_element(models_list, i)
        table.append([
            stat["model"],
            stat["count"],
            round(stat["mean"], 2),
            round(stat["std"], 2),
            round(stat["stability"], 6),
            round(stat["avg_hp"], 2)
        ])

    headers = [
        "Modelo",
        "Ventas",
        "Precio promedio (μ)",
        "Desviación estándar (σ)",
        "Estabilidad (σ/μ)",
        "Horsepower promedio"
    ]

    print(tabulate(table, headers=headers, tablefmt="fancy_grid"))

    print("\n" + "=" * 80)
    print("VENTA REPRESENTATIVA POR MODELO")
    print("=" * 80)

    for i in range(l.al.size(models_list)):
        stat = l.al.get_element(models_list, i)
        sale = stat["representative"]

        print(f"\nModelo: {stat['model']}")
        print(tabulate([[
            sale["model"],
            sale["year"],
            sale["fuel_type"],
            sale["base_price"],
            sale["horsepower"],
            sale["turbo"]
        ]],
        headers=["Model", "Year", "Fuel Type", "Base Price (USD)", "Horsepower", "Turbo"],
        tablefmt="fancy_grid"))

# Se crea la lógica asociado a la vista
control = new_logic()

# main del ejercicio
def main():
    """
    Menu principal
    """
    working = True
    #ciclo del menu
    while working:
        print_menu()
        inputs = input('Seleccione una opción para continuar\n')
        if int(inputs) == 0:
            print("Cargando información de los archivos ....\n")
            data = load_data(control)
        elif int(inputs) == 1:
            print_req_1(control)

        elif int(inputs) == 2:
            print_req_2(control)

        elif int(inputs) == 3:
            print_req_3(control)

        elif int(inputs) == 4:
            print_req_4(control)

        elif int(inputs) == 5:
            print_req_5(control)

        elif int(inputs) == 6:
            print_req_6(control)

        elif int(inputs) == 7:
            working = False
            print("\nGracias por utilizar el programa") 
        else:
            print("Opción errónea, vuelva a elegir.\n")
    sys.exit(0)
