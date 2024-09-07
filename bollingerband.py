import pandas as pd
import matplotlib.pyplot as plt

# Load data
df = pd.read_csv('aapl_us_d.csv')

# Automatically detect columns
columns = df.columns
print("Detected columns:", columns)

# Ensure 'Date' column is present and set it as index
if 'Date' in columns:
    df['Date'] = pd.to_datetime(df['Date'])
    df.set_index('Date', inplace=True)
else:
    raise KeyError("'Date' column not found in the dataset")

# Check if required columns are present
required_columns = ['Open', 'High', 'Low', 'Close', 'Volume']
for col in required_columns:
    if col not in df.columns:
        raise KeyError(f"'{col}' column not found in the dataset")

# Calculate Bollinger Bands
window = 20
df['Rolling Mean'] = df['Close'].rolling(window=window).mean()
df['Rolling Std'] = df['Close'].rolling(window=window).std()
df['Bollinger High'] = df['Rolling Mean'] + (df['Rolling Std'] * 2)
df['Bollinger Low'] = df['Rolling Mean'] - (df['Rolling Std'] * 2)

# Plot
plt.figure(figsize=(14, 7))
plt.plot(df.index, df['Close'], label='Closing Price', color='blue')
plt.plot(df.index, df['Rolling Mean'], label='Rolling Mean (SMA)', color='orange')
plt.plot(df.index, df['Bollinger High'], label='Bollinger High', color='red', linestyle='--')
plt.plot(df.index, df['Bollinger Low'], label='Bollinger Low', color='green', linestyle='--')

plt.fill_between(df.index, df['Bollinger Low'], df['Bollinger High'], color='lightgray', alpha=0.5)
plt.title('Bollinger Bands for Apple Stock')
plt.xlabel('Date')
plt.ylabel('Price')
plt.legend()
plt.grid(True)

# Save plot as an image file
plt.savefig('bollinger_bands.png')
print("Plot saved as 'bollinger_bands.png'")
