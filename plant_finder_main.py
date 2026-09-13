
import sqlite3

connection = sqlite3.connect('gardening.db')

cursor = connection.cursor()
cursor.execute("PRAGMA foreign_keys = ON;") #Ensures data integrity for foreign keys

cursor.execute('''create table if not exists plant(
    id integer primary key autoincrement,
    name text,
    description text,
    ph_min integer,
    ph_max integer,
    sunlight text,
    water_frequency text
    );''')

cursor.execute('''create table if not exists soil_type(
    id integer primary key autoincrement,
    name text
    );''')
    
cursor.execute('''create table if not exists plant_soil(
    id integer primary key autoincrement,
    plant_id integer,
    soil_type_id integer,
    foreign key(plant_id) references plant(id),
    foreign key(soil_type_id) references soil_type(id)
    );''')

#Sets up soil types
cursor.execute('''insert or ignore into soil_type (id, name) values (1, 'Gravel');''')
cursor.execute('''insert or ignore into soil_type (id, name) values (2, 'Clay');''')
cursor.execute('''insert or ignore into soil_type (id, name) values (3, 'Sand');''')

#Sets up plant-soil mapping
plant_soil_mappings = [
    {'id':1, 'plant_id': 1, 'soil_type_id': 1},
    {'id':2, 'plant_id': 1, 'soil_type_id': 2},
    {'id':3, 'plant_id': 2, 'soil_type_id': 2},
    {'id':4, 'plant_id': 3, 'soil_type_id': 3},
    {'id':5, 'plant_id': 4, 'soil_type_id': 2},
    {'id':6, 'plant_id': 4, 'soil_type_id': 3},
    {'id':7, 'plant_id': 5, 'soil_type_id': 1},
    {'id':8, 'plant_id': 6, 'soil_type_id': 3},
    {'id':9, 'plant_id': 7, 'soil_type_id': 1},
    {'id':10, 'plant_id': 8, 'soil_type_id': 2},
    {'id':11, 'plant_id': 9, 'soil_type_id': 3},
    {'id':12, 'plant_id': 10, 'soil_type_id': 1},
    {'id':13, 'plant_id': 10, 'soil_type_id': 2}
]

#Sets up plants
plants = [
    {'id': 1, 'name': 'Rose', 'description': 'A beautiful flowering plant', 'ph_min': 6, 'ph_max': 7, 'sunlight': 'Full Sun', 'water_frequency': 'Once a week'},
    {'id': 2, 'name': 'Tulip', 'description': 'A colorful spring flower', 'ph_min': 5, 'ph_max': 8, 'sunlight': 'Partial Sun', 'water_frequency': 'Twice a week'},
    {'id': 3, 'name': 'Cactus', 'description': 'A drought-tolerant succulent', 'ph_min': 7, 'ph_max': 8, 'sunlight': 'Full Sun', 'water_frequency': 'Once every two weeks'},
    {'id': 4, 'name': 'Fern', 'description': 'A shade-loving plant', 'ph_min': 5, 'ph_max': 6, 'sunlight': 'Partial Shade', 'water_frequency': 'Twice a week'},
    {'id': 5, 'name': 'Orchid', 'description': 'An exotic flowering plant', 'ph_min': 6, 'ph_max': 7, 'sunlight': 'Indirect Sunlight', 'water_frequency': 'Once a week'},
    {'id': 6, 'name': 'Bamboo', 'description': 'A fast-growing grass', 'ph_min': 5, 'ph_max': 6, 'sunlight': 'Full Sun to Partial Shade', 'water_frequency': 'Once a week'},
    {'id': 7, 'name': 'Lavender', 'description': 'A fragrant herb', 'ph_min': 6, 'ph_max': 8, 'sunlight': 'Full Sun', 'water_frequency': 'Once a week'},
    {'id': 8, 'name': 'Sunflower', 'description': 'A tall flowering plant', 'ph_min': 6, 'ph_max': 7, 'sunlight': 'Full Sun', 'water_frequency': 'Once a week'},
    {'id': 9, 'name': 'Aloe Vera', 'description': 'A medicinal succulent', 'ph_min': 7, 'ph_max': 8, 'sunlight': 'Full Sun', 'water_frequency': 'Once every two weeks'},
    {'id': 10, 'name': 'Daisy', 'description': 'A cheerful flowering plant', 'ph_min': 6, 'ph_max': 7, 'sunlight': 'Full Sun to Partial Shade', 'water_frequency': 'Once a week'}
]

def execute_request(request, value):
    connection = sqlite3.connect('gardening.db')
    try:
        cursor = connection.cursor()
        cursor.execute("PRAGMA foreign_keys = ON;") #Ensures data integrity for foreign keys

        cursor.execute(request, value)
        results = cursor.fetchall()
        # for row in results: #Prints relevant database rows
        #     return(row)
        return results

    finally:
            connection.close()

def data_input(search_option, soil_type, ph_min, ph_max):

    #search_option = input("Search by soil type or pH range? (Enter 'soil' or 'ph' - 'exit' to quit): ").strip().lower()

    if search_option == 'soil':
        #soil_type = input("Enter soil type (Gravel, Clay, Sand): ").strip().capitalize()
        request = "SELECT plant.id, plant.name, plant.description, plant.ph_min, plant.ph_max, plant.sunlight, plant.water_frequency FROM plant JOIN plant_soil ON plant.id = plant_soil.plant_id JOIN soil_type on plant_soil.soil_type_id = soil_type.id WHERE soil_type.name = (?);"
        return execute_request(request, [soil_type])

    elif search_option == 'ph':
        #ph_min = int(input("Enter minimum pH value: ").strip())
        #ph_max = int(input("Enter maximum pH value: ").strip())
        request = "SELECT id, name, description, ph_min, ph_max, sunlight, water_frequency FROM plant WHERE (ph_min BETWEEN ? AND ?) OR (ph_max BETWEEN ? AND ?);"
        return execute_request(request, [ph_min, ph_max, ph_min, ph_max])

    #elif search_option == 'exit':
        # print("Exiting the program.")
        #  break

    # else:
    #     return "Invalid option. Please enter 'soil' or 'ph'."


refresh = False #Set to True to refresh database with new data

if refresh:
    for plant in plants:
        sql = f"insert or ignore into plant (id, name, description, ph_min, ph_max, sunlight, water_frequency) values ('{plant['id']}', '{plant['name']}', '{plant['description']}', {plant['ph_min']}, {plant['ph_max']}, '{plant['sunlight']}', '{plant['water_frequency']}')"
        cursor.execute(sql)

    for mapping in plant_soil_mappings:
        sql = f"insert or ignore into plant_soil (id, plant_id, soil_type_id) values ('{mapping['id']}', '{mapping['plant_id']}', '{mapping['soil_type_id']}')"
        cursor.execute(sql)


# search_option = input("Search by soil type or pH range? (Enter 'soil' or 'ph' - 'exit' to quit): ").strip().lower()

# if search_option == 'soil':
#     soil_type = input("Enter soil type (Gravel, Clay, Sand): ").strip().capitalize()
#     results = data_input(search_option, soil_type, None, None)
#     for row in results:
#         print(row)

# elif search_option == 'ph':
#     ph_min = int(input("Enter minimum pH value: ").strip())
#     ph_max = int(input("Enter maximum pH value: ").strip())
#     results = data_input(search_option, None, ph_min, ph_max)
#     for row in results:
#         print(row)

# elif search_option == 'exit':
#     print("Exiting the program.")

# else:
#     print("Invalid option. Please enter 'soil' or 'ph'.")



connection.commit() #Makes changes and closes database
connection.close()