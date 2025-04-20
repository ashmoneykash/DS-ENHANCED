
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def load_data(path='ev_population.csv'):
    """Load and clean the EV dataset."""
    df = pd.read_csv(path)
    df.dropna(subset=['Make', 'Model', 'Model Year', 'Electric Vehicle Type'], inplace=True)
    df['Model Year'] = df['Model Year'].astype(int)
    df.columns = df.columns.str.strip()
    return df

def get_top_manufacturers(df, top_n=10):
    """Return a Series of top EV manufacturers."""
    return df['Make'].value_counts().head(top_n)

def get_ev_count_by_year(df):
    """Return EV registration count by year."""
    return df['Model Year'].value_counts().sort_index()

def get_ev_type_distribution(df):
    """Return distribution of EV types."""
    return df['Electric Vehicle Type'].value_counts()

def get_top_counties(df, top_n=10):
    """Return counties with the most EVs."""
    return df['County'].value_counts().head(top_n)

def get_range_by_year(df):
    """Return average range by model year."""
    if 'Electric Range' in df.columns:
        return df.groupby('Model Year')['Electric Range'].mean()
    return pd.Series(dtype='float64')

def plot_series(series, title, xlabel, ylabel, kind='bar', color='skyblue'):
    """Generic function to plot a pandas Series."""
    plt.figure(figsize=(10, 6))
    if kind == 'bar':
        series.plot(kind='bar', color=color)
    elif kind == 'line':
        series.plot(kind='line', marker='o', color=color)
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.tight_layout()
    return plt.gcf()
