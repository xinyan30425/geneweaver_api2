
import pandas as pd

# Replace 'your_file.txt' with the path to your file
df = pd.read_csv('gene_export_geneset_227303_2023-11-27.txt',sep="\t")  # specify the delimiter if it's not a comma

# Print the data type of each column
print(df.dtypes)