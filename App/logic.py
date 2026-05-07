import time
import csv

from tabulate import tabulate

csv.field_size_limit(2147483647)

from DataStructures.Priority_queue import priority_queue as pq
from DataStructures.Map import map_separate_chaining as mc
from DataStructures.Tree import red_black_tree as rbt
from DataStructures.List import array_list as al
from DataStructures.List import single_linked_list as sl
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

    return catalog, dtime, size, format_data(first_five), format_data(last_five)



# Formato y limpieza de datos

def clean_text(value):
    if value is None or value == "":
        return "Unknown"
    return value.strip()

def clean_number(value, isint=True):
    if value.isdigit():
        if isint:
            return int(value)
        else:
            return float(value)
    else:
        return 0
    
def format_sale(row):
    sale = {
        "model": clean_text(row.get("Model")),
        "year": clean_number(row.get("Year")),
        "region": clean_text(row.get("Region")),
        "color": clean_text(row.get("Color")),
        "fuel_type": clean_text(row.get("Fuel Type")),
        "base_price": clean_number(row.get("Base Price (USD)"), False),
        "horsepower": clean_number(row.get("Horsepower")),
        "sales_volume": clean_number(row.get("Sales Volume")),
        "turbo": clean_text(row.get("Turbo"))
    }
    return sale

def format_data(sales):
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

def format_req_4_data(top_models):
    
    formatted = []

    for stat in top_models["elements"]:
        
        count = mc.get(stat, "count")

        avg_price = mc.get(stat, "sum_price") / count if count > 0 else 0
        avg_hp = mc.get(stat, "horsepower") / count if count > 0 else 0
        turbo_percent = (mc.get(stat, "turbo") / count) * 100 if count > 0 else 0

        sale = mc.get(stat, "best")
        
        best_horsepower = [{
            "Model": sale["model"],
            "Year": sale["year"],
            "Tipo Combustible": sale["fuel_type"],
            "Color": sale["color"],
            "Precio Base (USD)": sale["base_price"],
            "Horsepower": sale["horsepower"],
            "Turbo": sale["turbo"]
        }]

        formatted.append({
            "Model": mc.get(stat, "model"),
            "Vehículos vendidos": count,
            "Precio promedio": round(avg_price, 2),
            "Horsepower promedio": round(avg_hp, 2),
            "Turbo Yes (%)": round(turbo_percent, 2),
            "Mejor Horsepower": tabulate(best_horsepower, headers="keys", tablefmt="fancy_grid")
        })

    return formatted

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

def req_1(catalog, model, price_min, price_max):
    """
    Retorna el resultado del requerimiento 1
    """
    inicio = get_time()

    model_tree = mc.get(catalog["model_index"], model)

    ventas_filtradas = al.new_list()
    suma_precios = 0

    if model_tree is not None:
        grupos = rbt.values(model_tree, price_min, price_max)
        
        for grupo in grupos:
            for sale in grupo:
                al.add_last(ventas_filtradas, sale)
                suma_precios += sale["base_price"]

    sort.merge_sort(ventas_filtradas, compare_sales_req1, al)

    total = al.size(ventas_filtradas)

    promedio_precio = suma_precios / total if total > 0 else 0

    ventas_mostrar = get_first_last_sales(ventas_filtradas, 6)

    dtime = delta_time(inicio, get_time())

    resumen = [
        ["Tiempo de ejecución (ms)", round(dtime, 2)],
        ["Total unidades vendidas", total],
        ["Promedio de precio", round(promedio_precio, 2)]
    ]

    return resumen, format_data(ventas_mostrar)


def req_2(catalog, fuel_type, min_hp, max_hp):
    start_time = get_time()

    results_tree = rbt.new_map()
    total_price = 0
    total_hp = 0
    count = 0

    for sale in catalog["all_sales"]["elements"]:
        if sale["fuel_type"].lower() != fuel_type.lower():
            continue

        horsepower = sale["horsepower"]
        if horsepower < min_hp or horsepower > max_hp:
            continue

        base_price = sale["base_price"]
        model = sale["model"]

        key = (horsepower, base_price, model)
        rbt.put(results_tree, key, sale)

        total_price += base_price
        total_hp += horsepower
        count += 1

    ordered_sales = al.new_list()

    keys = rbt.key_set(results_tree)["elements"]

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



def req_4(catalog, year, n):
    inicio = get_time()
    
    year_tree = mc.get(catalog["year_index"], year)
    model_stats = mc.new_map(300, 0.5)

    if year_tree is not None:
        grupos = rbt.value_set(year_tree)["elements"]

        for grupo in grupos:
            for sale in grupo:
                stats_req4(sale, model_stats)

    modelos = mc.value_set(model_stats)
    total_modelos = al.size(modelos)

    heap = pq.new_heap(False)

    for stat in modelos["elements"]:
        ventas = mc.get(stat, "count")
        avg_price = mc.get(stat, "sum_price") / ventas if ventas > 0 else 0
        priority_value = ventas * 1000000 + avg_price
        pq.insert(heap, priority_value, stat)

    top_models = al.new_list()
    count = 0

    while count < n and not pq.is_empty(heap):
        stat = pq.remove(heap)
        al.add_last(top_models, stat)
        count += 1

    dtime = delta_time(inicio, get_time())

    resumen = [
        ["Tiempo de ejecución (ms)", round(dtime, 2)],
        ["Total de modelos considerados", total_modelos]
    ]

    return resumen, format_req_4_data(top_models)

def req_5(catalog, hp_ref, delta, top_n):
    start_time = get_time()

    min_hp = hp_ref - delta
    max_hp = hp_ref + delta

    color_stats = {}
    total_vehicles = 0

    for sale in catalog["all_sales"]["elements"]:
        hp = sale["horsepower"]
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

    keys = rbt.key_set(result_tree)["elements"]

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
    if s1["year"] < s2["year"]:
        return True
    if s1["year"] > s2["year"]:
        return False

    if s1["base_price"] < s2["base_price"]:
        return True
    if s1["base_price"] > s2["base_price"]:
        return False

    return s1["model"] < s2["model"]

def compare_sales_req1(s1, s2):
    price1 = float(s1["base_price"])
    price2 = float(s2["base_price"])

    if price1 < price2:
        return True
    if price1 > price2:
        return False

    hp1 = float(s1["horsepower"])
    hp2 = float(s2["horsepower"])

    if hp1 > hp2:
        return True
    if hp1 < hp2:
        return False

    return s1["color"] < s2["color"]

def compare_sales_req4(sale, current):

    if current is None:
        return True

    if sale["horsepower"] > current["horsepower"]:
        return True

    if sale["horsepower"] < current["horsepower"]:
        return False

    if sale["base_price"] < current["base_price"]:
        return True

    if sale["base_price"] > current["base_price"]:
        return False

    return sale["year"] < current["year"]


# Funciones de ayuda

def get_first_last_sales(sales, amount):
    total = al.size(sales)

    if total <= amount * 2:
        return sales

    first = al.sub_list(sales, 0, amount)
    last = al.sub_list(sales, total - amount, amount)
    
    result = al.join_lists(first, last)

    return result

def stats_req4(sale, model_stats):
    modelo = sale["model"]
    
    if not mc.contains(model_stats, modelo):
        value = mc.new_map(3, 0.5)
        mc.put(value, "model", modelo)
        mc.put(value, "count", 0)
        mc.put(value, "sum_price", 0)
        mc.put(value, "horsepower", 0)
        mc.put(value, "turbo", 0)
        mc.put(value, "best", None)
        mc.put(model_stats, modelo, value)
   
    stats = mc.get(model_stats, modelo)
    mc.add_number(stats, "count", 1)
    mc.add_number(stats, "sum_price", sale["base_price"])
    mc.add_number(stats, "horsepower", sale["horsepower"])
    mc.add_number(stats, "turbo", 1 if sale["turbo"] == "Yes" else 0)
    if compare_sales_req4(sale, mc.get(stats, "best")):
        mc.put(stats, "best", sale)
        
    return model_stats

# Funciones de tiempo

def get_time():
    return float(time.perf_counter() * 1000)


def delta_time(start, end):
    return float(end - start)
