import pandas as pd

# Load the CSV file into a DataFrame
df = pd.read_csv('ww.csv')

# Print the initial number of rows
print("Initial number of rows:", len(df))

# Drop duplicates and keep the first occurrence
df = df.drop_duplicates(keep='first')

# Print the number of rows after removing duplicates
print("Number of rows after removing duplicates:", len(df))

# Save the DataFrame back to a CSV file
df.to_csv('3333.csv', index=False)
