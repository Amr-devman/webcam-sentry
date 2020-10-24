import os
from datetime import datetime, timedelta, date

from utilities.db_functions import create_houskeeper , select_query, insert_query


def remove_old_data():
	## this function will NOT create a new housekeeper db, if the db exist then
	## all creation operations are passed, you can consider this as noop if the app
	## is not running for the first time 
	housekeeper_filename = "housekeeper"
	create_houskeeper(housekeeper_filename)

	db_list = os.listdir("dbs")
	## we do not want to houskeep our housekeeper
	_ = db_list.pop(db_list.index(f'{housekeeper_filename}.db'))

	stored_dbs = select_query(	f"{housekeeper_filename}.db",
								["userid", "join_date", "expiry_date"],
								 "keeper")

	for db in db_list:
		db_without_extension = db.split(".")[0]
		if db_without_extension not in stored_dbs["userid"].values:
			#if the user details have not been stored in the keeper db
			#then make a new entry

			db_unix_epoch = os.path.getmtime(f"./dbs/{db}")
			join_date = datetime.fromtimestamp(db_unix_epoch)
			expiry_date = join_date + timedelta(days=7)

			insert_query(	f"{housekeeper_filename}.db",
							["userid", "join_date", "expiry_date"],
							(db_without_extension, join_date, expiry_date),
							"keeper")

		else:
			#if the user details are there then check if the user data has expired
			#if so then remove the user data
			stored_entry = stored_dbs.loc[stored_dbs["userid"] == db_without_extension]
			expiry_date = stored_entry["expiry_date"].values[0]
			expiry_date = datetime.strptime(expiry_date, "%Y-%m-%d %H:%M:%S.%f")

			delta = expiry_date - datetime.now()
			
			#condition to check if we bypassed the expiry date
			if delta.days < 0:
				os.remove(f"./dbs/{db}")
				os.remove(f"./prev_images/{db_without_extension}.npy")
			else:
				pass

	






