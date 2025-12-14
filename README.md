# ReviewInsight – Text Analytics & Summary Report Generator

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Status](https://img.shields.io/badge/Status-Active-success.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

A beginner-friendly Natural Language Processing (NLP) project that analyzes product review datasets and generates comprehensive summary reports using text analytics techniques.

## 📋 Description

ReviewInsight is an automated text analytics tool designed to process and analyze customer product reviews. It performs text cleaning, statistical analysis, and word frequency analysis to extract meaningful insights from customer feedback data. The system generates professional summary reports that can inform business decisions and product improvements.

## ✨ Features

- **CSV Data Loading**: Seamlessly imports product review datasets
- **Text Preprocessing**: Cleans text by removing punctuation, URLs, emails, and normalizing case
- **Stopword Removal**: Filters out common English words using NLTK
- **Word Frequency Analysis**: Identifies the most frequently mentioned terms
- **Statistical Computing**: Calculates review length, rating distributions, and data quality metrics
- **Automated Reporting**: Generates formatted text reports with visualizations
- **Insight Generation**: Provides actionable business insights based on data patterns

## 🛠️ Tech Stack

- **Python 3.8+**: Core programming language
- **pandas**: Data manipulation and CSV handling
- **NLTK**: Natural Language Processing and stopword removal
- **Regular Expressions (re)**: Text cleaning and pattern matching
- **Collections**: Word frequency counting

## 📁 Folder Structure
reviewinsight/
│
├── data/
│   └── reviews.csv              # Input dataset (50 sample reviews)
│
├── analysis.py                  # Main analysis script
├── report.txt                   # Generated analysis report (auto-created)
├── requirements.txt             # Python dependencies
└── README.md                    # Project documentation
## 🚀 How to Run

### Step 1: Clone or Download the Project
```bash
# If using git
git clone <repository-url>
cd reviewinsight

# Or simply create the folder structure manually
```

### Step 2: Create a Virtual Environment (Recommended)
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Download NLTK Data
```bash
python -c "import nltk; nltk.download('stopwords')"
```

### Step 5: Run the Analysis
```bash
python analysis.py
```

### Step 6: View the Generated Report
```bash
# The report will be saved as report.txt
# Open it with any text editor
```

## 📊 Sample Output