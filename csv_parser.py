import argparse
import csv
import datetime
import logging
import uuid
import os
from pathlib import Path

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
logging.basicConfig(filename=f'csv_parser.log {datetime.datetime.now().replace(second=0, microsecond=0)}',
                    filemode='w', format='%(name)s - %(levelname)s - %(message)s')

begin_time = datetime.datetime.now()


def read_file():
    parser = argparse.ArgumentParser()
    parser.add_argument("file_path", type=Path)
    p = parser.parse_args()
    file_path = p.file_path
    if not file_path.exists():
        logging.error(f"{str(datetime.datetime.now().replace(microsecond=0))}: File not found at {file_path}")
        print(f"{str(datetime.datetime.now().replace(microsecond=0))}: Cannot find file at {file_path}")
        return
    if p.file_path.suffix != ".csv":
        logging.error(f"{str(datetime.datetime.now().replace(microsecond=0))}: "
                      f"{p.file_path.name} file is not a CSV file")
        print(f"{str(datetime.datetime.now().replace(microsecond=0))}: Cannot process this file")
        return
    else:
        logging.info(f"{str(datetime.datetime.now().replace(microsecond=0))}: "
                     f"Reading the file {p.file_path.name} given in the arguments of the script")
        print(f"{str(datetime.datetime.now().replace(microsecond=0))}: "
              f"Reading file {p.file_path.name}")
        write_file(file_path)


def get_file_name():
    filename = "shipments" + "data" + "_" + str(datetime.datetime.today().date()) + "_" + str(uuid.uuid4())[
                                                                                          -4:] + ".csv"
    return filename


def write_file(path):
    try:
        with open(path) as f:
            reader = csv.reader(f, delimiter=",")
            filename = get_file_name()
            print(f"{str(datetime.datetime.now().replace(microsecond=0))}: "
                  f"Writing the new file with the name of {filename}")
            logger.info(f"{str(datetime.datetime.now().replace(microsecond=0))}: "
                        f"Making the new file named {filename} in the {os.getcwd()}")

            with open(filename, "w") as formatted_file:
                writer = csv.writer(formatted_file)
                count = 0
                header_cols = next(reader)
                writer.writerow(map(str.strip, header_cols))
                for row in reader:
                    try:
                        datetime_obj = datetime.datetime.strptime(row[1], '%d-%m-%Y')
                        row[1] = str(datetime_obj.date())
                        writer.writerow(map(str.strip, row))
                        count += 1
                        print(f"{str(datetime.datetime.now().replace(microsecond=0))}: "
                              f"Successfully formatted row number {count}")
                        logger.info(f"{str(datetime.datetime.now().replace(microsecond=0))}: "
                                    f"Written row number {count} in new file")
                    except:
                        os.remove(filename)
                        print(f"{str(datetime.datetime.now().replace(microsecond=0))}: Row number {count} "
                              f"doesn't matches the date format as dd-mm-yyyy")
                        logger.error(f"{str(datetime.datetime.now().replace(microsecond=0))}: Row number {count} "
                                     f"doesn't matches the date format as dd-mm-yyyy")
                        return

                resp_msg = f"{str(datetime.datetime.now().replace(microsecond=0))}: " \
                           f"{count} rows are successfully written into the new file with the name of {filename} " \
                           f"in {os.getcwd()} in {datetime.datetime.now() - begin_time} seconds"
                print(resp_msg)
    except Exception as e:
        os.remove(filename)
        print(f"{str(datetime.datetime.now().replace(microsecond=0))}: {e}")
        logger.error(f"{str(datetime.datetime.now().replace(microsecond=0))}: {e.args[0]}")
        return


if __name__ == "__main__":
    read_file()
