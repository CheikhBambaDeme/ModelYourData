"""
Data Analysis Utilities for ModelYourData.
Contains functions for various data analysis operations:
- Linear Regression
- Clustering (KMeans)
- Distribution Plots
- Statistical Summary
- EDA Report
- Correlation Matrix
"""

import io
import base64
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend for server
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.linear_model import LinearRegression
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.impute import SimpleImputer


# Set plot style
plt.style.use('seaborn-v0_8-whitegrid')
sns.set_palette(['#2E7D32', '#4CAF50', '#81C784', '#A5D6A7', '#C8E6C9'])


def load_csv(file_path):
    """
    Load a CSV file into a pandas DataFrame.
    
    Args:
        file_path: Path to the CSV file
        
    Returns:
        pandas.DataFrame: Loaded data
    """
    try:
        df = pd.read_csv(file_path)
        return df
    except Exception as e:
        raise ValueError(f"Error loading CSV: {str(e)}")


def get_numeric_columns(df):
    """Get list of numeric columns from DataFrame."""
    return df.select_dtypes(include=[np.number]).columns.tolist()


def get_categorical_columns(df):
    """Get list of categorical columns from DataFrame."""
    return df.select_dtypes(include=['object', 'category']).columns.tolist()


def fig_to_base64(fig):
    """
    Convert matplotlib figure to base64 encoded string.
    
    Args:
        fig: matplotlib.figure.Figure object
        
    Returns:
        str: Base64 encoded PNG image
    """
    buffer = io.BytesIO()
    fig.savefig(buffer, format='png', dpi=150, bbox_inches='tight', 
                facecolor='white', edgecolor='none')
    buffer.seek(0)
    image_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
    plt.close(fig)
    return image_base64


def generate_table_preview(df, max_rows=20):
    """
    Generate HTML table preview of the DataFrame.
    
    Args:
        df: pandas.DataFrame
        max_rows: Maximum number of rows to display
        
    Returns:
        dict: Contains HTML table, shape info, and column info
    """
    # Get basic info
    shape = df.shape
    columns_info = []
    
    for col in df.columns:
        dtype = str(df[col].dtype)
        null_count = int(df[col].isnull().sum())  # Convert to native int
        columns_info.append({
            'name': col,
            'dtype': dtype,
            'null_count': null_count
        })
    
    # Generate HTML table
    preview_df = df.head(max_rows)
    html_table = preview_df.to_html(
        classes='data-table',
        index=False,
        na_rep='NaN',
        max_cols=15
    )
    
    return {
        'html': html_table,
        'rows': shape[0],
        'columns': shape[1],
        'columns_info': columns_info,
        'numeric_columns': get_numeric_columns(df),
        'categorical_columns': get_categorical_columns(df)
    }


def perform_linear_regression(df, x_column=None, y_column=None):
    """
    Perform linear regression analysis.
    
    Args:
        df: pandas.DataFrame
        x_column: Name of the x variable column (optional)
        y_column: Name of the y variable column (optional)
        
    Returns:
        dict: Contains plot image, R² score, coefficients
    """
    numeric_cols = get_numeric_columns(df)
    
    if len(numeric_cols) < 2:
        raise ValueError("Need at least 2 numeric columns for linear regression")
    
    # Auto-select columns if not provided
    if x_column is None or x_column not in numeric_cols:
        x_column = numeric_cols[0]
    if y_column is None or y_column not in numeric_cols:
        y_column = numeric_cols[1] if len(numeric_cols) > 1 else numeric_cols[0]
    
    # Prepare data
    data = df[[x_column, y_column]].dropna()
    X = data[x_column].values.reshape(-1, 1)
    y = data[y_column].values
    
    # Fit model
    model = LinearRegression()
    model.fit(X, y)
    y_pred = model.predict(X)
    
    # Calculate R² score
    r2_score = model.score(X, y)
    
    # Create plot
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Scatter plot
    ax.scatter(X, y, alpha=0.6, c='#4CAF50', label='Data points', s=50)
    
    # Regression line
    ax.plot(X, y_pred, color='#2E7D32', linewidth=2, label=f'Regression line (R²={r2_score:.4f})')
    
    ax.set_xlabel(x_column, fontsize=12)
    ax.set_ylabel(y_column, fontsize=12)
    ax.set_title(f'Linear Regression: {y_column} vs {x_column}', fontsize=14, fontweight='bold')
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    image_base64 = fig_to_base64(fig)
    
    return {
        'image': image_base64,
        'r2_score': float(round(r2_score, 4)),
        'coefficient': float(round(model.coef_[0], 4)),
        'intercept': float(round(model.intercept_, 4)),
        'x_column': x_column,
        'y_column': y_column,
        'equation': f'y = {model.coef_[0]:.4f}x + {model.intercept_:.4f}'
    }


def perform_clustering(df, n_clusters=3, columns=None):
    """
    Perform KMeans clustering analysis.
    
    Args:
        df: pandas.DataFrame
        n_clusters: Number of clusters
        columns: List of columns to use (optional)
        
    Returns:
        dict: Contains plot image and cluster info
    """
    numeric_cols = get_numeric_columns(df)
    
    if len(numeric_cols) < 2:
        raise ValueError("Need at least 2 numeric columns for clustering")
    
    # Select columns for clustering
    if columns is None or len(columns) < 2:
        columns = numeric_cols[:2]
    
    # Prepare data
    data = df[columns].dropna()
    
    # Impute missing values and scale
    imputer = SimpleImputer(strategy='mean')
    scaler = StandardScaler()
    
    X = imputer.fit_transform(data)
    X_scaled = scaler.fit_transform(X)
    
    # Fit KMeans
    kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
    clusters = kmeans.fit_predict(X_scaled)
    
    # Create plot
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Color palette
    colors = ['#2E7D32', '#4CAF50', '#81C784', '#FFA726', '#42A5F5', '#AB47BC', '#EF5350', '#26A69A']
    
    scatter = ax.scatter(data[columns[0]], data[columns[1]], 
                        c=[colors[c % len(colors)] for c in clusters],
                        alpha=0.7, s=60)
    
    # Plot centroids
    centroids_original = scaler.inverse_transform(kmeans.cluster_centers_)
    ax.scatter(centroids_original[:, 0], centroids_original[:, 1], 
              c='red', marker='X', s=200, edgecolors='black', linewidth=2,
              label='Centroids')
    
    ax.set_xlabel(columns[0], fontsize=12)
    ax.set_ylabel(columns[1], fontsize=12)
    ax.set_title(f'KMeans Clustering (k={n_clusters})', fontsize=14, fontweight='bold')
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    image_base64 = fig_to_base64(fig)
    
    # Calculate cluster sizes - convert numpy int64 to native int
    cluster_sizes = {int(k): int(v) for k, v in pd.Series(clusters).value_counts().sort_index().to_dict().items()}
    
    return {
        'image': image_base64,
        'n_clusters': int(n_clusters),
        'cluster_sizes': cluster_sizes,
        'columns_used': columns,
        'inertia': float(round(kmeans.inertia_, 4))
    }


def generate_distribution_plot(df, column=None):
    """
    Generate distribution plot for numeric columns.
    
    Args:
        df: pandas.DataFrame
        column: Specific column to plot (optional)
        
    Returns:
        dict: Contains plot image
    """
    numeric_cols = get_numeric_columns(df)
    
    if len(numeric_cols) == 0:
        raise ValueError("No numeric columns found for distribution plot")
    
    if column and column in numeric_cols:
        cols_to_plot = [column]
    else:
        cols_to_plot = numeric_cols[:6]  # Limit to 6 columns
    
    n_cols = len(cols_to_plot)
    n_rows = (n_cols + 1) // 2
    
    fig, axes = plt.subplots(n_rows, 2, figsize=(12, 4 * n_rows))
    axes = axes.flatten() if n_cols > 1 else [axes]
    
    for i, col in enumerate(cols_to_plot):
        ax = axes[i]
        data = df[col].dropna()
        
        # Histogram with KDE
        sns.histplot(data, kde=True, ax=ax, color='#4CAF50', alpha=0.7)
        ax.set_title(f'Distribution of {col}', fontsize=12, fontweight='bold')
        ax.set_xlabel(col)
        ax.set_ylabel('Frequency')
        ax.grid(True, alpha=0.3)
    
    # Hide unused subplots
    for j in range(i + 1, len(axes)):
        axes[j].set_visible(False)
    
    plt.tight_layout()
    image_base64 = fig_to_base64(fig)
    
    return {
        'image': image_base64,
        'columns_plotted': cols_to_plot
    }


def generate_statistical_summary(df):
    """
    Generate comprehensive statistical summary.
    
    Args:
        df: pandas.DataFrame
        
    Returns:
        dict: Contains HTML summary table and statistics
    """
    # Basic statistics
    desc_stats = df.describe(include='all').round(4)
    
    # Additional statistics - convert numpy types to native Python types
    stats_dict = {
        'Total Rows': int(len(df)),
        'Total Columns': int(len(df.columns)),
        'Numeric Columns': int(len(get_numeric_columns(df))),
        'Categorical Columns': int(len(get_categorical_columns(df))),
        'Total Missing Values': int(df.isnull().sum().sum()),
        'Memory Usage (KB)': float(round(df.memory_usage(deep=True).sum() / 1024, 2))
    }
    
    # Missing values by column
    missing_df = pd.DataFrame({
        'Column': df.columns.tolist(),
        'Missing Count': [int(x) for x in df.isnull().sum().values],
        'Missing %': [float(round(x, 2)) for x in (df.isnull().sum().values / len(df) * 100)]
    })
    
    html_stats = desc_stats.to_html(classes='data-table stats-table')
    html_missing = missing_df.to_html(classes='data-table missing-table', index=False)
    
    return {
        'summary_html': html_stats,
        'missing_html': html_missing,
        'basic_stats': stats_dict
    }


def generate_eda_report(df):
    """
    Generate comprehensive EDA report with multiple visualizations.
    
    Args:
        df: pandas.DataFrame
        
    Returns:
        dict: Contains multiple plot images and summary statistics
    """
    numeric_cols = get_numeric_columns(df)
    images = []
    
    # 1. Correlation Matrix (if numeric columns exist)
    if len(numeric_cols) >= 2:
        fig, ax = plt.subplots(figsize=(10, 8))
        corr_matrix = df[numeric_cols].corr()
        mask = np.triu(np.ones_like(corr_matrix, dtype=bool))
        sns.heatmap(corr_matrix, mask=mask, annot=True, fmt='.2f', 
                   cmap='Greens', ax=ax, vmin=-1, vmax=1,
                   linewidths=0.5, square=True)
        ax.set_title('Correlation Matrix', fontsize=14, fontweight='bold')
        plt.tight_layout()
        images.append({'type': 'correlation', 'image': fig_to_base64(fig)})
    
    # 2. Missing Values Heatmap
    if df.isnull().sum().sum() > 0:
        fig, ax = plt.subplots(figsize=(12, 6))
        sns.heatmap(df.isnull(), cbar=True, yticklabels=False, 
                   cmap=['#C8E6C9', '#D32F2F'], ax=ax)
        ax.set_title('Missing Values Heatmap', fontsize=14, fontweight='bold')
        ax.set_xlabel('Columns')
        ax.set_ylabel('Rows')
        plt.tight_layout()
        images.append({'type': 'missing', 'image': fig_to_base64(fig)})
    
    # 3. Box plots for numeric columns
    if len(numeric_cols) >= 1:
        n_cols_plot = min(6, len(numeric_cols))
        fig, axes = plt.subplots(1, n_cols_plot, figsize=(3 * n_cols_plot, 5))
        if n_cols_plot == 1:
            axes = [axes]
        
        for i, col in enumerate(numeric_cols[:n_cols_plot]):
            sns.boxplot(y=df[col], ax=axes[i], color='#4CAF50')
            axes[i].set_title(col, fontsize=10, fontweight='bold')
            axes[i].grid(True, alpha=0.3)
        
        plt.tight_layout()
        images.append({'type': 'boxplots', 'image': fig_to_base64(fig)})
    
    # 4. Pairplot (for first 4 numeric columns if available)
    if len(numeric_cols) >= 2:
        cols_for_pair = numeric_cols[:min(4, len(numeric_cols))]
        pair_df = df[cols_for_pair].dropna()
        
        if len(pair_df) > 0:
            fig = plt.figure(figsize=(10, 10))
            g = sns.pairplot(pair_df, diag_kind='kde', 
                           plot_kws={'alpha': 0.6, 'color': '#4CAF50'},
                           diag_kws={'color': '#2E7D32'})
            g.fig.suptitle('Pair Plot', y=1.02, fontsize=14, fontweight='bold')
            images.append({'type': 'pairplot', 'image': fig_to_base64(g.fig)})
    
    # Get statistical summary
    summary = generate_statistical_summary(df)
    
    return {
        'images': images,
        'summary': summary
    }


def generate_correlation_matrix(df):
    """
    Generate correlation matrix heatmap.
    
    Args:
        df: pandas.DataFrame
        
    Returns:
        dict: Contains plot image
    """
    numeric_cols = get_numeric_columns(df)
    
    if len(numeric_cols) < 2:
        raise ValueError("Need at least 2 numeric columns for correlation matrix")
    
    fig, ax = plt.subplots(figsize=(12, 10))
    corr_matrix = df[numeric_cols].corr()
    
    sns.heatmap(corr_matrix, annot=True, fmt='.2f', 
               cmap='Greens', ax=ax, vmin=-1, vmax=1,
               linewidths=0.5, square=True,
               cbar_kws={'shrink': 0.8})
    
    ax.set_title('Correlation Matrix', fontsize=14, fontweight='bold')
    plt.tight_layout()
    
    image_base64 = fig_to_base64(fig)
    
    return {
        'image': image_base64,
        'columns': numeric_cols
    }


def generate_scatter_plot(df, x_column=None, y_column=None):
    """
    Generate scatter plot for two numeric columns.
    
    Args:
        df: pandas.DataFrame
        x_column: X-axis column name
        y_column: Y-axis column name
        
    Returns:
        dict: Contains plot image
    """
    numeric_cols = get_numeric_columns(df)
    
    if len(numeric_cols) < 2:
        raise ValueError("Need at least 2 numeric columns for scatter plot")
    
    if x_column is None or x_column not in numeric_cols:
        x_column = numeric_cols[0]
    if y_column is None or y_column not in numeric_cols:
        y_column = numeric_cols[1]
    
    fig, ax = plt.subplots(figsize=(10, 6))
    
    data = df[[x_column, y_column]].dropna()
    ax.scatter(data[x_column], data[y_column], alpha=0.6, c='#4CAF50', s=50)
    
    ax.set_xlabel(x_column, fontsize=12)
    ax.set_ylabel(y_column, fontsize=12)
    ax.set_title(f'Scatter Plot: {y_column} vs {x_column}', fontsize=14, fontweight='bold')
    ax.grid(True, alpha=0.3)
    
    image_base64 = fig_to_base64(fig)
    
    return {
        'image': image_base64,
        'x_column': x_column,
        'y_column': y_column
    }


def generate_histogram(df, column=None, bins=30):
    """
    Generate histogram for a numeric column.
    
    Args:
        df: pandas.DataFrame
        column: Column name
        bins: Number of bins
        
    Returns:
        dict: Contains plot image
    """
    numeric_cols = get_numeric_columns(df)
    
    if len(numeric_cols) == 0:
        raise ValueError("No numeric columns found for histogram")
    
    if column is None or column not in numeric_cols:
        column = numeric_cols[0]
    
    fig, ax = plt.subplots(figsize=(10, 6))
    
    data = df[column].dropna()
    ax.hist(data, bins=bins, color='#4CAF50', alpha=0.7, edgecolor='#2E7D32')
    
    ax.set_xlabel(column, fontsize=12)
    ax.set_ylabel('Frequency', fontsize=12)
    ax.set_title(f'Histogram of {column}', fontsize=14, fontweight='bold')
    ax.grid(True, alpha=0.3, axis='y')
    
    # Add statistics
    mean_val = data.mean()
    median_val = data.median()
    ax.axvline(mean_val, color='#D32F2F', linestyle='--', linewidth=2, label=f'Mean: {mean_val:.2f}')
    ax.axvline(median_val, color='#1976D2', linestyle='--', linewidth=2, label=f'Median: {median_val:.2f}')
    ax.legend()
    
    image_base64 = fig_to_base64(fig)
    
    return {
        'image': image_base64,
        'column': column,
        'mean': float(round(mean_val, 4)),
        'median': float(round(median_val, 4)),
        'std': float(round(data.std(), 4))
    }


def generate_boxplot(df, columns=None):
    """
    Generate box plot for numeric columns.
    
    Args:
        df: pandas.DataFrame
        columns: List of columns to plot
        
    Returns:
        dict: Contains plot image
    """
    numeric_cols = get_numeric_columns(df)
    
    if len(numeric_cols) == 0:
        raise ValueError("No numeric columns found for box plot")
    
    if columns is None:
        columns = numeric_cols[:8]  # Limit to 8 columns
    
    fig, ax = plt.subplots(figsize=(12, 6))
    
    # Prepare data for boxplot
    data_to_plot = [df[col].dropna() for col in columns]
    
    bp = ax.boxplot(data_to_plot, labels=columns, patch_artist=True)
    
    # Color the boxes
    colors = ['#4CAF50', '#81C784', '#A5D6A7', '#C8E6C9', '#2E7D32', '#388E3C', '#43A047', '#66BB6A']
    for patch, color in zip(bp['boxes'], colors * (len(columns) // len(colors) + 1)):
        patch.set_facecolor(color)
        patch.set_alpha(0.7)
    
    ax.set_ylabel('Values', fontsize=12)
    ax.set_title('Box Plot Comparison', fontsize=14, fontweight='bold')
    ax.grid(True, alpha=0.3, axis='y')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    
    image_base64 = fig_to_base64(fig)
    
    return {
        'image': image_base64,
        'columns': columns
    }
