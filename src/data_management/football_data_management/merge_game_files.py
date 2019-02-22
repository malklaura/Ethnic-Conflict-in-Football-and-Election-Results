import csv
import glob
from bld.project_paths import project_paths_join as ppj

if __name__ == '__main__':
  csv_list = glob.glob(ppj("OUT_DATA_FOOTBALL_FINAL", "*.csv"))

  # First determine column names by looping over all .csv files
  # and reading the headers.
  colnames_list = []
  for filename in csv_list:
    with open(ppj("OUT_DATA_FOOTBALL_FINAL", filename), "r", newline="") as f_in:
      reader = csv.reader(f_in)
      headers = next(reader)
      for h in headers:
        if h not in colnames_list:
          colnames_list.append(h)

  # Then construct combined csv by reading in each single .csv
  # file by using overall column list defined above.
  with open(ppj("OUT_DATA_FOOTBALL", "football_final.csv"), "w", newline="") as f_out:   # Comment 2 below
    writer = csv.DictWriter(f_out, fieldnames=colnames_list)
    writer.writeheader()
    for filename in csv_list:
      with open(ppj("OUT_DATA_FOOTBALL_FINAL", "{}".format(filename)), "r", newline="") as f_in:
        reader = csv.DictReader(f_in)  # Uses the field names in this file
        for line in reader:
          writer.writerow(line)


  df = pd.read_csv(ppj("OUT_DATA_FOOTBALL", "football_final.csv"), encoding='cp1252')
  # Split date into day, month and year and store in seperate columns.
  date_data = '(?P<fb_day>[^.]+).(?P<fb_month>[^.]+).(?P<fb_year>[^.]+)'
  df = pd.concat([df, df["date"].str.extract(date_data).astype(int)], axis=1)
  # To four digit integer.
  df["fb_year"] = df["fb_year"] + 2000
  # Save as csv.
  df.to_csv(ppj("OUT_DATA_FOOTBALL", "football_final.csv"))
