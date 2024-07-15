import pandas as pd

# Define file paths
metadata_path = '/Users/jeevaharidas/Desktop/project/34100133_MetaData.csv'
data_path = '/Users/jeevaharidas/Desktop/project/34100133.csv'

# Load the datasets
metadata_df = pd.read_csv(metadata_path)
data_df = pd.read_csv(data_path)

# Drop columns with a high percentage of missing values in both datasets
metadata_df_cleaned = metadata_df.drop(columns=['URL', 'Cube Notes', 'Archive Status', 'Frequency', 'Start Reference Period', 'End Reference Period', 'Total number of dimensions'])
data_df_cleaned = data_df.drop(columns=['SYMBOL'])

# Drop rows with missing values in the metadata dataset
metadata_df_cleaned = metadata_df_cleaned.dropna()

# For the data dataset, fill missing 'DGUID' with a placeholder and drop rows where 'VALUE' is missing
data_df_cleaned['DGUID'] = data_df_cleaned['DGUID'].fillna('Unknown')
data_df_cleaned = data_df_cleaned.dropna(subset=['VALUE'])

# Save the cleaned datasets to the project folder
metadata_cleaned_path = '/Users/jeevaharidas/Desktop/project/cleaned_34100133_MetaData.csv'
data_cleaned_path = '/Users/jeevaharidas/Desktop/project/cleaned_34100133.csv'

metadata_df_cleaned.to_csv(metadata_cleaned_path, index=False)
data_df_cleaned.to_csv(data_cleaned_path, index=False)

print(f"Cleaned metadata saved to {metadata_cleaned_path}")
print(f"Cleaned data saved to {data_cleaned_path}")
