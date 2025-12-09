# ModelYourData

A Django-based web application for uploading CSV files, visualizing data, applying analytical operations, and downloading generated visualizations.

## Features

- **Drag & Drop File Upload**: Easily upload CSV files via drag & drop or file browser
- **Data Table Preview**: View your data in a clean, paginated table
- **Linear Regression**: Analyze relationships between numeric variables
- **Clustering (KMeans)**: Group similar data points automatically
- **Distribution Plots**: Visualize data distributions with histograms and KDE
- **Statistical Summary**: Get comprehensive statistics about your dataset
- **Full EDA Report**: Generate complete exploratory data analysis reports
- **Correlation Matrix**: Understand relationships between all numeric variables
- **Scatter Plots**: Create custom scatter plots with any two variables
- **Histograms**: Detailed histograms with mean and median lines
- **Box Plots**: Compare distributions across multiple variables
- **Export Visualizations**: Download any visualization as PNG

## Tech Stack

- **Backend**: Django 4.2+
- **Server**: Gunicorn
- **Data Processing**: Pandas, NumPy
- **Machine Learning**: Scikit-learn
- **Visualization**: Matplotlib, Seaborn
- **Frontend**: Vanilla JavaScript, CSS3
- **Static Files**: WhiteNoise

## Quick Start

### Prerequisites

- Python 3.9+
- pip (Python package manager)

### Installation

1. Clone or navigate to the project directory:
   ```bash
   cd /home/lacrevette/Desktop/Dev/ModelYourData
   ```

2. Create and activate a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Run database migrations:
   ```bash
   python manage.py migrate
   ```

5. Collect static files:
   ```bash
   python manage.py collectstatic --noinput
   ```

### Running the Application

#### Production Mode (Gunicorn)

```bash
chmod +x run.sh
./run.sh
```

Or manually:
```bash
gunicorn modelyourdata.wsgi:application --bind 127.0.0.1:8000 --workers 2
```

#### Development Mode

```bash
chmod +x run_dev.sh
./run_dev.sh
```

Or manually:
```bash
python manage.py runserver
```

### Access the Application

Open your browser and navigate to: **http://127.0.0.1:8000**

## Project Structure

```
ModelYourData/
├── manage.py                 # Django management script
├── requirements.txt          # Python dependencies
├── run.sh                   # Production run script (Gunicorn)
├── run_dev.sh               # Development run script
├── README.md                # This file
│
├── modelyourdata/           # Django project settings
│   ├── __init__.py
│   ├── settings.py          # Project configuration
│   ├── urls.py              # Root URL configuration
│   ├── wsgi.py              # WSGI entry point
│   └── asgi.py              # ASGI entry point
│
├── dataanalysis/            # Main application
│   ├── __init__.py
│   ├── admin.py             # Admin configuration
│   ├── apps.py              # App configuration
│   ├── forms.py             # Form definitions
│   ├── models.py            # Database models
│   ├── urls.py              # App URL patterns
│   ├── views.py             # View functions
│   └── utils/               # Utility modules
│       ├── __init__.py
│       └── analysis.py      # Data analysis functions
│
├── templates/               # HTML templates
│   ├── base.html            # Base template
│   └── dataanalysis/
│       ├── landing.html     # Landing page
│       ├── analysis.html    # Analysis page
│       └── error.html       # Error page
│
├── static/                  # Static files
│   ├── css/
│   │   ├── style.css        # Main stylesheet
│   │   └── analysis.css     # Analysis page styles
│   └── js/
│       ├── main.js          # Common utilities
│       ├── upload.js        # Upload functionality
│       └── analysis.js      # Analysis operations
│
├── media/                   # User uploaded files
│   ├── uploads/             # Uploaded CSV files
│   └── results/             # Generated visualizations
│
└── staticfiles/             # Collected static files (production)
```

## Usage

1. **Upload Data**: On the landing page, drag & drop a CSV file or click "Browse Files"
2. **View Data**: After upload, you'll see a preview of your data with basic statistics
3. **Apply Operations**: Use the operation panel on the right to apply various analyses
4. **Configure Parameters**: Some operations allow you to select columns or adjust parameters
5. **Export Results**: Click "Export" to download the current visualization as PNG

## Supported Operations

| Operation | Description | Parameters |
|-----------|-------------|------------|
| Data Table | Preview the raw data | Max rows |
| Statistics | Descriptive statistics | None |
| Full EDA | Complete exploratory analysis | None |
| Linear Regression | Regression analysis | X and Y columns |
| Clustering | KMeans clustering | Number of clusters |
| Distribution | Distribution plots | Column (optional) |
| Correlation | Correlation matrix | None |
| Scatter Plot | Scatter plot | X and Y columns |
| Histogram | Histogram with stats | Column, bins |
| Box Plot | Box plots comparison | Columns |

## Configuration

### Environment Variables

For production, set these environment variables:

```bash
export DJANGO_SECRET_KEY='your-secret-key-here'
export DEBUG=False
export ALLOWED_HOSTS='your-domain.com'
```

### File Upload Limits

The default maximum file size is 10MB. To change this, modify `settings.py`:

```python
FILE_UPLOAD_MAX_MEMORY_SIZE = 10485760  # 10MB
DATA_UPLOAD_MAX_MEMORY_SIZE = 10485760  # 10MB
```

## License

This project is open source and available under the MIT License.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
