import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the data
df = pd.read_csv("game_data.csv")

# -------------------------------
# 1. Data Snapshot & Descriptions
# -------------------------------
print("\n---Column Names ---")
# Manually assigning column names based on what you expect them to be
df.columns = ['Game ID', 'Move Number', 'Row', 'Col', 'Action', 'Board State', 
              'Mines Flagged', 'Hidden Cells', 'Safe', 'Game Outcome']
df.columns = df.columns.str.strip()  # Remove any leading/trailing spaces from column names
print(df.columns)

# -------------------------------
# 2. Preprocessing & Cleaning
# -------------------------------
# Handle missing numerical data by filling it with the median
df['Row'].fillna(df['Row'].median())
df['Col'].fillna(df['Col'].median())
df['Mines Flagged'].fillna(df['Mines Flagged'].median())
df['Hidden Cells'].fillna(df['Hidden Cells'].median())

# Filling missing categorical values with the mode
df['Action'].fillna(df['Action'].mode()[0])
df['Board State'].fillna(df['Board State'].mode()[0])

# Filter out ongoing games
df_filtered = df[df['Game Outcome'] != 'Ongoing']

# Convert 'safe' and 'outcome' to categorical
df['Safe'] = df['Safe'].astype('category')
df['Game Outcome'] = df['Game Outcome'].astype('category')
df['Action'] = df['Action'].astype('category')

## Fill missing 'Board State' values with empty strings and convert to strings
df['Board State'] = df['Board State'].fillna("").astype(str)

# Now safely apply len() to calculate board_state_length
df['board_state_length'] = df['Board State'].apply(len)

# Optional: convert 'board_state' to length or complexity metric
df['board_state_length'] = df['Board State'].apply(len)

# Drop board_state if not analyzing as text
df.drop(columns=['Board State'])

# -------------------------------
# 3. Visualizations
# -------------------------------
# Histograms for numeric features
df.hist(figsize=(12, 8))
plt.suptitle("Distributions of Numeric Features")
plt.tight_layout()
plt.show()

# Count plot of outcomes (after filtering ongoing games)
sns.countplot(x='Game Outcome', data=df_filtered)
plt.title("Game Outcomes")
plt.show()

# Safe vs Mines Flagged
sns.boxplot(x='Safe', y='Mines Flagged', data=df)
plt.title("Mines Flagged by Safe Move")
plt.show()

# Correlation matrix
numeric_df = df.select_dtypes(include=['int64', 'float64'])
correlation = numeric_df.corr()
sns.heatmap(correlation, annot=True, cmap='coolwarm')
plt.title("Correlation Matrix")
plt.show()

# -------------------------------
# 4. Interpretation Hints
# -------------------------------
print("\n--- Interpretation Notes ---")
print("• Safe moves tend to have lower hidden cell counts.")
print("• Game outcomes may correlate with how early mines are flagged.")
print("• Longer board_state strings may represent more complex positions.")

