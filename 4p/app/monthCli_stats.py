import database as db
import sys
import os
import time
import pickle

FILENAME = "month_cli_stats.txt"
MEAN_ITER = 100
MONTH = 4
YEAR = 2015
MIN_THH = 50
INTERVAL = 5
BREAK1 = 1
NITER = 1000
PREPARE_0 = 0
PREPARE_1 = 1


def main(graphic_str):
    sum_time_prep0 = 0
    sum_time_prep1 = 0

    db_conn = db.dbConnect()

    # Prepare = 0
    for i in range(MEAN_ITER):
        t0=round(time.time() * 1000)
        dbr = db.getListaCliMes(db_conn, MONTH, YEAR, MIN_THH, INTERVAL, PREPARE_0, BREAK1, NITER)
        t1=round(time.time() * 1000)
        sum_time_prep0 += int(t1-t0)

    # Prepare = 1
    for i in range(MEAN_ITER):
        t0=round(time.time() * 1000)
        dbr = db.getListaCliMes(db_conn, MONTH, YEAR, MIN_THH, INTERVAL, PREPARE_1, BREAK1, NITER)
        t1=round(time.time() * 1000)
        sum_time_prep1 += int(t1-t0)

    db.dbCloseConnect(db_conn)

    # Getting mean time values
    mean_t_p0 = sum_time_prep0/MEAN_ITER
    mean_t_p1 = sum_time_prep1/MEAN_ITER

    # Storing collected data
    data = graphic_str+"_prepare=0 "+str(mean_t_p0)+"\n"+graphic_str+"_prepare=1 "+str(mean_t_p1)+"\n"
    if not os.path.isfile(FILENAME):
        f = open(FILENAME, "w")
        f.write(data)
        f.close()
    else:
        f = open(FILENAME, "a")
        f.write(data)
        f.close()

    return


if __name__ == "__main__":
    if len(sys.argv) > 1:
        main(sys.argv[1])
    else:
        print("Please, introduce graphic name")
