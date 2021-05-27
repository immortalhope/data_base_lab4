import pandas as pd
from config import Config
from pymongo import MongoClient
import json
import time
import csv


client = MongoClient(
    "mongodb://" + Config.host + ":" + Config.port + "/?readPreference=primary&appname=MongoDB%20Compass&ssl=false")
db = client[Config.database]
coll = db[Config.collection]

int_list = Config.int_columns_list
float_list = Config.float_columns_list
check_coll = db['check_collection']


# -----------------------------import_data-----------------------------
# ---------------------------------------------------------------------
def import_data(file, ins_rows_count):
    year = file[5:9]
    my_list = []
    new_ins_rows_count = ins_rows_count
    i = 1
    with open(file, "r", encoding="cp1251") as csv_file:
        csv_reader = csv.DictReader(csv_file, delimiter=';', quoting=csv.QUOTE_ALL)

        for j in range(ins_rows_count):
            next(csv_reader)
        for row in csv_reader:
            for x, y in row.items():
                if y == 'null':
                    row[x] = None
                elif x in int_list:
                    row[x] = int(row[x])
                elif x in float_list:
                    row[x] = float(row[x].replace(',', '.'))
            doc = row
            doc['year'] = int(year)
            my_list.append(doc)
            if i == 1000:
                try:
                    coll.insert_many(my_list, ordered=False)
                    new_ins_rows_count += i
                    check_coll.update({'file_name': file},
                                      {'file_name': file, 'rows_count': new_ins_rows_count, 'end_file': False})
                    i = 1
                    my_list = []
                except:
                    return -1

                continue
                # break
            else:
                i += 1

        if len(my_list) != 0:
            try:
                coll.insert_many(my_list, ordered=False)
                new_ins_rows_count += len(my_list)
                check_coll.update({'file_name': file},
                                  {'file_name': file, 'rows_count': new_ins_rows_count, 'end_file': True})
            except:
                return -1



# -----------------------------------------------------------------------
file_len = len(Config.file_list)
start_time = time.time()
for ind in range(file_len):
    file = Config.file_list[ind]
    year = int(file[5:9])
    if check_coll.count_documents({'file_name': file}) == 0:
        check_coll.insert_one({'file_name': file, 'rows_count': 0, 'end_file': False})

    inserted_rows_count = coll.count_documents({'year': year})
    import_data(file, inserted_rows_count)
end_time = time.time()
print('Data was loaded in ' + str(end_time - start_time) + ' seconds\n')
with open("loading_time.txt", "w") as file_t:
    file_t.write('Data was loaded in ' + str(end_time -start_time) + ' seconds\n')


query_res = coll.aggregate(
    [
    {"$match": {"physTestStatus":"Зараховано"}},
        {"$group": {
            "_id": {
                "year": "$year",
                "physPTRegName": "$physPTRegName"},
            "physBall100": {"$avg": "$physBall100"}
        }},

        {"$sort": {"_id": 1}}
    ])


with open('query_result.csv', 'w', encoding="utf-8") as file:
    csv_writer = csv.writer(file)
    csv_writer.writerow(['physBall100', 'year', 'ball_100'])

    for doc in query_res:
        year = doc["_id"]["year"]
        reg_name = doc["_id"]["physPTRegName"]
        ball = doc["physBall100"]
        csv_writer.writerow([reg_name, year, ball])