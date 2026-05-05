import time
import csv

csv.field_size_limit(2147483647)

from DataStructures.Map import map_separate_chaining as mc
from DataStructures.Tree import red_black_tree as rbt
from DataStructures.List import array_list as al
from DataStructures.List import sort as sort

# Creacion del catalogo

def new_logic():
    """
    Crea el catalogo del reto 3.
    Se usan mapas y listas del paquete DataStructures.
    """
    catalog = {
        "all_sales": al.new_list(),
        "year_index": mc.new_map(20, 0.5),
        "model_index": mc.new_map(200, 0.5),
        "fuel_index": mc.new_map(20, 0.5),
        "horsepower_tree": rbt.new_map()
    }
    return catalog

# Carga de datos

def load_data(catalog, size):
    """
    Carga los datos del reto.

    Estructura cargada:
    - all_sales: lista con todas las ventas.
    - year_index: Year -> RBT(Base Price -> lista de ventas).
    - model_index: Model -> RBT(Base Price -> lista de ventas).
    - fuel_index: Fuel Type -> RBT(Horsepower -> lista de ventas).
    - horsepower_tree: RBT(Horsepower -> lista de ventas).
    """
    inicio = get_time()
    url = f"./data/mercedes_sales_{size}.csv"

    with open(url, encoding="utf-8") as f:
        filas = csv.DictReader(f)

        for dato in filas:

            sale = format_sale(dato)
            al.add_last(catalog["all_sales"], sale)

            load_year_index(catalog, sale)
            load_model_index(catalog, sale)
            load_fuel_index(catalog, sale)
            load_horsepower_tree(catalog, sale)

    sort.merge_sort(catalog["all_sales"], compare_sales_load, al)

    size = al.size(catalog["all_sales"])
    first_five = al.sub_list(catalog["all_sales"], 0, 5)
    last_five = al.sub_list(catalog["all_sales"], size - 5, 5)

    dtime = delta_time(inicio, get_time())

    return catalog, dtime, size, format_load_data(first_five), format_load_data(last_five)



# Formato y limpieza de datos

def clean_text(value):
    if value is None or value == "":
        return "Unknown"
    return value.strip()

def format_sale(row):
    """
    Normaliza los nombres de columnas del CSV.
    """
    sale = {
        "model": clean_text(row.get("Model")),
        "year": clean_text(row.get("Year")),
        "region": clean_text(row.get("Region")),
        "color": clean_text(row.get("Color")),
        "fuel_type": clean_text(row.get("Fuel Type")),
        "base_price": clean_text(row.get("Base Price (USD)")),
        "horsepower": clean_text(row.get("Horsepower")),
        "sales_volume": clean_text(row.get("Sales Volume")),
        "turbo": clean_text(row.get("Turbo"))
    }
    return sale

def format_load_data(sales):
    formatted_sales = []
    for sale in sales["elements"]:
        formatted_sales.append({
            "Model": sale["model"],
            "Year": sale["year"],
            "Tipo Combustible": sale["fuel_type"],
            "Color": sale["color"],
            "Precio Base (USD)": sale["base_price"],
            "Horsepower": sale["horsepower"],
            "Turbo": sale["turbo"]
        })
    return formatted_sales

# Carga de datos individual

def load_year_index(catalog, sale):
    year = sale["year"]
    price = sale["base_price"]

    tree = mc.get(catalog["year_index"], year)

    if tree is None:
        tree = rbt.new_map()
        mc.put(catalog["year_index"], year, tree)

    rbt.put(tree, price, sale, True)
    return catalog


def load_model_index(catalog, sale):
    model = sale["model"].lower()
    price = sale["base_price"]

    tree = mc.get(catalog["model_index"], model)

    if tree is None:
        tree = rbt.new_map()
        mc.put(catalog["model_index"], model, tree)

    rbt.put(tree, price, sale, True)
    return catalog


def load_fuel_index(catalog, sale):
    fuel_type = sale["fuel_type"].lower()
    horsepower = sale["horsepower"]

    tree = mc.get(catalog["fuel_index"], fuel_type)

    if tree is None:
        tree = rbt.new_map()
        mc.put(catalog["fuel_index"], fuel_type, tree)

    rbt.put(tree, horsepower, sale, True)
    return catalog


def load_horsepower_tree(catalog, sale):
    horsepower = sale["horsepower"]

    rbt.put(catalog["horsepower_tree"], horsepower, sale, True)
    return catalog


# Requerimientos

def req_1(catalog):
    """
    Retorna el resultado del requerimiento 1
    """
    # TODO: Modificar el requerimiento 1
    pass


def req_2(catalog):
    """
    Retorna el resultado del requerimiento 2
    """
    # TODO: Modificar el requerimiento 2
    pass


def req_3(catalog):
    """
    Retorna el resultado del requerimiento 3
    """
    # TODO: Modificar el requerimiento 3
    pass


def req_4(catalog):
    """
    Retorna el resultado del requerimiento 4
    """
    # TODO: Modificar el requerimiento 4
    pass


def req_5(catalog):
    """
    Retorna el resultado del requerimiento 5
    """
    # TODO: Modificar el requerimiento 5
    pass

def req_6(catalog):
    """
    Retorna el resultado del requerimiento 6
    """
    # TODO: Modificar el requerimiento 6
    pass


# Ordenamiento de carga

def compare_sales_load(s1, s2):
    """
    Orden de carga pedido por el enunciado:
    1. Year ASC
    2. Base Price ASC
    3. Model ASC
    """
    if s1["year"] < s2["year"]:
        return True
    if s1["year"] > s2["year"]:
        return False

    if s1["base_price"] < s2["base_price"]:
        return True
    if s1["base_price"] > s2["base_price"]:
        return False

    return s1["model"] < s2["model"]


# Funciones de tiempo

def get_time():
    return float(time.perf_counter() * 1000)


def delta_time(start, end):
    return float(end - start)
