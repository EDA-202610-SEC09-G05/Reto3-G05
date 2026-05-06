import sys
from tabulate import tabulate
from App import logic as l

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
    """
        Función que imprime la solución del Requerimiento 1 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 1
    pass


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
    """
        Función que imprime la solución del Requerimiento 3 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 3
    pass


def print_req_4(control):
    """
        Función que imprime la solución del Requerimiento 4 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 4
    pass


def print_req_5(control):
    """
        Función que imprime la solución del Requerimiento 5 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 5
    pass


def print_req_6(control):
    """
        Función que imprime la solución del Requerimiento 6 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 6
    pass

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

        elif int(inputs) == 5:
            print_req_6(control)

        elif int(inputs) == 7:
            working = False
            print("\nGracias por utilizar el programa") 
        else:
            print("Opción errónea, vuelva a elegir.\n")
    sys.exit(0)
