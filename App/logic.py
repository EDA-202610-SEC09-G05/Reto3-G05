import time
import csv

csv.field_size_limit(2147483647)

from DataStructures.Map import map_separate_chaining as mc
from DataStructures.Tree import red_black_tree as rbt
from DataStructures.List import array_list as al
from DataStructures.List import sort as sort
from DataStructures.List import single_linked_list as sl

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


def req_2(catalog, fuel_type, min_hp, max_hp):
    start_time = get_time()

    results_tree = rbt.new_map()
    total_price = 0
    total_hp = 0
    count = 0

    for sale in catalog["all_sales"]["elements"]:
        if sale["fuel_type"].lower() != fuel_type.lower():
            continue

        horsepower = int(sale["horsepower"])
        if horsepower < min_hp or horsepower > max_hp:
            continue

        base_price = float(sale["base_price"])
        model = sale["model"]

        key = (horsepower, base_price, model)
        rbt.put(results_tree, key, sale)

        total_price += base_price
        total_hp += horsepower
        count += 1

    ordered_sales = al.new_list()

    keys_sl = rbt.key_set(results_tree)
    keys = sl.to_py_list(keys_sl)

    for key in keys:
        sale = rbt.get(results_tree, key)
        al.add_last(ordered_sales, sale)

    avg_price = total_price / count if count > 0 else 0
    avg_hp = total_hp / count if count > 0 else 0
    exec_time = delta_time(start_time, get_time())

    if al.size(ordered_sales) > 12:
        first = al.sub_list(ordered_sales, 0, 6)
        last = al.sub_list(ordered_sales, al.size(ordered_sales) - 6, 6)

        trimmed = al.new_list()
        for i in range(al.size(first)):
            al.add_last(trimmed, al.get_element(first, i))
        for i in range(al.size(last)):
            al.add_last(trimmed, al.get_element(last, i))

        ordered_sales = trimmed

    return {
        "time_ms": exec_time,
        "total_sales": count,
        "avg_price": avg_price,
        "avg_horsepower": avg_hp,
        "sales": ordered_sales
    }


def req_3(catalog):
    """
    Retorna el resultado del requerimiento 3
    """
    # TODO: Modificar el requerimiento 3
    pass


def req_4(catalog):
    """
    Retorna el resultado del requerimiento 4
    
    USAR COLAS DE PRIORIDAD
    
    """
    # TODO: Modificar el requerimiento 4
    pass


def req_5(catalog, hp_ref, delta, top_n):
    start_time = get_time()

    min_hp = hp_ref - delta
    max_hp = hp_ref + delta

    color_stats = {}
    total_vehicles = 0

    for sale in catalog["all_sales"]["elements"]:
        hp = int(sale["horsepower"])
        if hp < min_hp or hp > max_hp:
            continue

        color = sale["color"]
        total_vehicles += 1

        if color not in color_stats:
            color_stats[color] = {
                "count": 0,
                "hp_sum": 0
            }

        color_stats[color]["count"] += 1
        color_stats[color]["hp_sum"] += hp

    result_tree = rbt.new_map()

    for color, data in color_stats.items():
        count = data["count"]
        avg_hp = data["hp_sum"] / count
        key = (-count, -avg_hp, color)
        rbt.put(result_tree, key, {
            "color": color,
            "count": count,
            "avg_hp": avg_hp
        })

    ordered = al.new_list()

    keys_sl = rbt.key_set(result_tree)
    keys = sl.to_py_list(keys_sl)

    for key in keys:
        al.add_last(ordered, rbt.get(result_tree, key))

    if al.size(ordered) > top_n:
        ordered = al.sub_list(ordered, 0, top_n)

    exec_time = delta_time(start_time, get_time())

    return {
        "time_ms": exec_time,
        "total_vehicles": total_vehicles,
        "top_colors": ordered
    }

def req_6(catalog):
    """
    Retorna el resultado del requerimiento 6
    
    OPCIONAL USAR COALS DE PRIORIDAD 
    
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
