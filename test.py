import cx_Oracle
con=cx_Oracle.connect('C##Xinru','123456','localhost:1521/XE')
cur = con.cursor()
cur.execute("select * from beeGenes where gi = '147907436'")
for result in cur:
    print(result)
    print(result[1].read())

cur.close()
con.close()