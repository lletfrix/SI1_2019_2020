import os
import sys
import shutil


APP_FOLDER = "app/"
USERS_DATA_FOLDER = "usuarios/"
SESSIONS_DATA_FOLDER = "thesessions/"


def clean_users_data():
    folder = APP_FOLDER+USERS_DATA_FOLDER
    try:
        # Deleting EVERYTHING recursively at given folder (including the folder provided)
        shutil.rmtree(folder)
        # Recreating the folder provided (we don't want to delete it)
        os.mkdir(folder)
    except Exception as exc:
        print("Unable to clean users data: ", exc)
    return


def clean_sessions_data():
    folder = APP_FOLDER+SESSIONS_DATA_FOLDER
    for file in os.listdir(folder):
        file_path = os.path.join(folder, file)
        try:
            if os.path.isfile(file_path):
                # Deleting all files in the given folder
                os.unlink(file_path)
        except Exception as exc:
            print("Unable to clean sessions data: ", exc)
    return


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Insufficient input args")
        exit()
    if sys.argv[1] == 'users' or sys.argv[1] == '-u':
        clean_users_data()
    elif sys.argv[1] == 'sessions' or sys.argv[1] == '-s':
        clean_sessions_data()
