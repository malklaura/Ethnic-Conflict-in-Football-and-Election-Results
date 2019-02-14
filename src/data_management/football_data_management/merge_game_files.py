import csv
import glob
from bld.project_paths import project_paths_join as ppj

csv_list = glob.glob(ppj("OUT_DATA_FOOTBALL_FINAL", "*.csv"))

# First determine the field names from the top line of each input file
# Comment 1 below
colnames_list = []
for filename in csv_list:
  with open(ppj("OUT_DATA_FOOTBALL_FINAL", filename), "r", newline="") as f_in:
    reader = csv.reader(f_in)
    headers = next(reader)
    for h in headers:
      if h not in colnames_list:
        colnames_list.append(h)

# Then copy the data
with open(ppj("OUT_DATA_FOOTBALL", "football_final.csv"), "w", newline="") as f_out:   # Comment 2 below
  writer = csv.DictWriter(f_out, filenames=colnames_list)
  writer.writeheader()
  for filename in df_list:
    with open(ppj("OUT_DATA_FOOTBALL_CSV", filename), "r", newline="") as f_in:
      reader = csv.DictReader(f_in, delimiter = ";")  # Uses the field names in this file
      for line in reader:
        # Comment 3 below
        writer.writerow(line)

