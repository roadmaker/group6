import psycopg2
import location
def updateTable():
  try:
    connection = psycopg2.connect(user="postgres",
                                  password="postgres",
                                  host="172.17.0.2",
                                  port="5432",
                                  database="roadmakerDB")
    cursor = connection.cursor()
    print("Table Before updating record ")
    sql_select_query = """SELECT hashimage,image FROM imageshashed Where hashimage not in (Select hash from hash_location)"""
    cursor.execute(sql_select_query)
    record = cursor.fetchall()
    for i in range(len(record)):
      print(record[i][0])
      latlon = location.location(record[i][1])
      print("lat",latlon[0])
      print("lon",latlon[1])

      # Update single record now
      # sql_update_query = """Update public.hash_location set hash = %s where uid = %s"""
      sql_update_query = """insert into public.hash_location(hash,latitude,longitude) values(%s,%s,%s)"""
      
      cursor.execute(sql_update_query, (record[i][0], latlon[0],latlon[1]))
      connection.commit()
      count = cursor.rowcount
      print(count, "Record Updated successfully ")

    print("Table After updating record ")
    sql_select_query = """select * from public.imagesHashed"""
    cursor.execute(sql_select_query)
    record = cursor.fetchone()
    print(record)

  except (Exception, psycopg2.Error) as error:
    print("Error in update operation", error)
  finally:
    # closing database connection.
    if connection:
      cursor.close()
      connection.close()
      print("PostgreSQL connection is closed")

updateTable()