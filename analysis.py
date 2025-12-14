"""
ReviewInsight - Text Analytics & Summary Report Generator
A beginner-friendly NLP project for analyzing product reviews

Author: Week-2 Generative AI Learning Project
"""

import pandas as pd
import re
from collections import Counter
from datetime import datetime
import nltk
from nltk.corpus import stopwords

# Download required NLTK data (run once)
try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    print("Downloading NLTK stopwords...")
    nltk.download('stopwords', quiet=True)


def load_data(filepath='data/reviews.csv'):
    """
    Load product reviews from CSV file.
    
    Args:
        filepath (str): Path to the CSV file
        
    Returns:
        pd.DataFrame: DataFrame containing reviews
        
    Raises:
        FileNotFoundError: If CSV file doesn't exist
    """
    try:
        df = pd.read_csv(filepath)
        print(f"✓ Successfully loaded {len(df)} reviews from {filepath}")
        return df
    except FileNotFoundError:
        print(f"✗ Error: File '{filepath}' not found.")
        print("Please ensure the CSV file exists in the correct location.")
        raise
    except Exception as e:
        print(f"✗ Error loading data: {str(e)}")
        raise


def clean_text(text):
    """
    Clean and preprocess text data.
    
    Steps:
    1. Convert to lowercase
    2. Remove punctuation and special characters
    3. Remove extra whitespace
    4. Remove numbers
    
    Args:
        text (str): Raw text to clean
        
    Returns:
        str: Cleaned text
    """
    if pd.isna(text):
        return ""
    
    # Convert to string and lowercase
    text = str(text).lower()
    
    # Remove URLs
    text = re.sub(r'http\S+|www\S+', '', text)
    
    # Remove email addresses
    text = re.sub(r'\S+@\S+', '', text)
    
    # Remove punctuation and special characters
    text = re.sub(r'[^a-zA-Z\s]', ' ', text)
    
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text).strip()
    
    return text


def get_common_words(text_list, top_n=20):
    """
    Find the most common words after removing stopwords.
    
    Args:
        text_list (list): List of cleaned text strings
        top_n (int): Number of top words to return
        
    Returns:
        list: List of tuples (word, frequency)
    """
    # Get English stopwords
    stop_words = set(stopwords.words('english'))
    
    # Add custom stopwords common in reviews
    custom_stopwords = {
        'product', 'item', 'thing', 'really', 'also', 'would',
        'get', 'got', 'one', 'much', 'even', 'still', 'well'
    }
    stop_words.update(custom_stopwords)
    
    # Combine all text and tokenize
    all_words = []
    for text in text_list:
        words = text.split()
        # Filter: remove stopwords and short words (less than 3 characters)
        filtered_words = [
            word for word in words 
            if word not in stop_words and len(word) >= 3
        ]
        all_words.extend(filtered_words)
    
    # Count word frequencies
    word_freq = Counter(all_words)
    
    return word_freq.most_common(top_n)


def compute_statistics(df, review_column='review_text'):
    """
    Compute statistical metrics about the reviews.
    
    Args:
        df (pd.DataFrame): DataFrame containing reviews
        review_column (str): Name of column with review text
        
    Returns:
        dict: Dictionary containing various statistics
    """
    stats = {}
    
    # Basic counts
    stats['total_reviews'] = len(df)
    stats['non_empty_reviews'] = df[review_column].notna().sum()
    stats['empty_reviews'] = df[review_column].isna().sum()
    
    # Text length statistics (in words)
    df['word_count'] = df[review_column].apply(
        lambda x: len(str(x).split()) if pd.notna(x) else 0
    )
    stats['avg_review_length'] = df['word_count'].mean()
    stats['min_review_length'] = df['word_count'].min()
    stats['max_review_length'] = df['word_count'].max()
    stats['median_review_length'] = df['word_count'].median()
    
    # Character length statistics
    df['char_count'] = df[review_column].apply(
        lambda x: len(str(x)) if pd.notna(x) else 0
    )
    stats['avg_char_length'] = df['char_count'].mean()
    
    # Rating statistics (if available)
    if 'rating' in df.columns:
        stats['avg_rating'] = df['rating'].mean()
        stats['min_rating'] = df['rating'].min()
        stats['max_rating'] = df['rating'].max()
        stats['rating_distribution'] = df['rating'].value_counts().to_dict()
    
    return stats


def generate_report(common_words, statistics, output_file='report.txt'):
    """
    Generate a formatted text report with analysis results.
    
    Args:
        common_words (list): List of (word, frequency) tuples
        statistics (dict): Dictionary of computed statistics
        output_file (str): Path to save the report
    """
    report_lines = []
    
    # Header
    report_lines.append("=" * 80)
    report_lines.append("REVIEWINSIGHT - TEXT ANALYTICS REPORT")
    report_lines.append("=" * 80)
    report_lines.append(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    report_lines.append("")
    
    # Section 1: Dataset Overview
    report_lines.append("1. DATASET OVERVIEW")
    report_lines.append("-" * 80)
    report_lines.append(f"Total Reviews: {statistics['total_reviews']:,}")
    report_lines.append(f"Valid Reviews: {statistics['non_empty_reviews']:,}")
    report_lines.append(f"Empty Reviews: {statistics['empty_reviews']:,}")
    report_lines.append("")
    
    # Section 2: Text Statistics
    report_lines.append("2. TEXT STATISTICS")
    report_lines.append("-" * 80)
    report_lines.append(f"Average Review Length: {statistics['avg_review_length']:.2f} words")
    report_lines.append(f"Median Review Length: {statistics['median_review_length']:.1f} words")
    report_lines.append(f"Shortest Review: {statistics['min_review_length']} words")
    report_lines.append(f"Longest Review: {statistics['max_review_length']} words")
    report_lines.append(f"Average Character Count: {statistics['avg_char_length']:.2f} characters")
    report_lines.append("")
    
    # Section 3: Rating Analysis (if available)
    if 'avg_rating' in statistics:
        report_lines.append("3. RATING ANALYSIS")
        report_lines.append("-" * 80)
        report_lines.append(f"Average Rating: {statistics['avg_rating']:.2f} / 5.0")
        report_lines.append(f"Rating Range: {statistics['min_rating']} - {statistics['max_rating']}")
        report_lines.append("")
        report_lines.append("Rating Distribution:")
        for rating in sorted(statistics['rating_distribution'].keys(), reverse=True):
            count = statistics['rating_distribution'][rating]
            percentage = (count / statistics['total_reviews']) * 100
            bar = "█" * int(percentage / 2)
            report_lines.append(f"  {rating} stars: {count:4d} ({percentage:5.1f}%) {bar}")
        report_lines.append("")
    
    # Section 4: Most Common Words
    section_num = 4 if 'avg_rating' in statistics else 3
    report_lines.append(f"{section_num}. MOST COMMON WORDS (TOP 20)")
    report_lines.append("-" * 80)
    report_lines.append(f"{'Rank':<6} {'Word':<20} {'Frequency':<12} {'Visual'}")
    report_lines.append("-" * 80)
    
    max_freq = common_words[0][1] if common_words else 1
    for idx, (word, freq) in enumerate(common_words, 1):
        bar_length = int((freq / max_freq) * 30)
        bar = "▓" * bar_length
        report_lines.append(f"{idx:<6} {word:<20} {freq:<12,} {bar}")
    report_lines.append("")
    
    # Section 5: Key Insights
    section_num += 1
    report_lines.append(f"{section_num}. KEY INSIGHTS")
    report_lines.append("-" * 80)
    
    # Generate insights
    insights = []
    
    # Insight 1: Review engagement
    avg_len = statistics['avg_review_length']
    if avg_len < 15:
        insights.append("• Reviews are brief, suggesting quick feedback or limited engagement")
    elif avg_len > 50:
        insights.append("• Reviews are detailed, indicating high customer engagement")
    else:
        insights.append("• Reviews have moderate length, showing standard engagement levels")
    
    # Insight 2: Top themes
    if common_words:
        top_3_words = [word for word, _ in common_words[:3]]
        insights.append(f"• Most discussed topics: '{top_3_words[0]}', '{top_3_words[1]}', '{top_3_words[2]}'")
    
    # Insight 3: Rating sentiment (if available)
    if 'avg_rating' in statistics:
        avg_rating = statistics['avg_rating']
        if avg_rating >= 4.0:
            insights.append(f"• Strong positive sentiment (avg rating: {avg_rating:.2f}/5.0)")
        elif avg_rating >= 3.0:
            insights.append(f"• Mixed sentiment (avg rating: {avg_rating:.2f}/5.0)")
        else:
            insights.append(f"• Negative sentiment trend (avg rating: {avg_rating:.2f}/5.0)")
    
    # Insight 4: Data quality
    empty_pct = (statistics['empty_reviews'] / statistics['total_reviews']) * 100
    if empty_pct > 10:
        insights.append(f"• Data quality concern: {empty_pct:.1f}% empty reviews")
    else:
        insights.append("• Good data quality with minimal missing reviews")
    
    for insight in insights:
        report_lines.append(insight)
    
    report_lines.append("")
    report_lines.append("=" * 80)
    report_lines.append("End of Report")
    report_lines.append("=" * 80)
    
    # Write to file
    report_content = "\n".join(report_lines)
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(report_content)
    
    print(f"\n✓ Report successfully generated: {output_file}")
    return report_content


def main():
    """
    Main execution function that orchestrates the analysis pipeline.
    """
    print("\n" + "=" * 80)
    print("REVIEWINSIGHT - TEXT ANALYTICS & SUMMARY REPORT GENERATOR")
    print("=" * 80 + "\n")
    
    try:
        # Step 1: Load data
        print("STEP 1: Loading data...")
        df = load_data('data/reviews.csv')
        
        # Step 2: Clean text
        print("\nSTEP 2: Cleaning and preprocessing text...")
        review_column = 'review_text'
        
        # Check if column exists
        if review_column not in df.columns:
            print(f"Column '{review_column}' not found. Available columns: {list(df.columns)}")
            # Try to find a review column
            possible_names = ['review', 'text', 'comment', 'feedback', 'Review', 'Text']
            for name in possible_names:
                if name in df.columns:
                    review_column = name
                    print(f"Using column: '{review_column}'")
                    break
        
        df['cleaned_text'] = df[review_column].apply(clean_text)
        print(f"✓ Cleaned {len(df)} reviews")
        
        # Step 3: Compute statistics
        print("\nSTEP 3: Computing statistics...")
        statistics = compute_statistics(df, review_column)
        print(f"✓ Calculated {len(statistics)} statistical metrics")
        
        # Step 4: Find common words
        print("\nSTEP 4: Analyzing word frequencies...")
        cleaned_texts = df['cleaned_text'].tolist()
        common_words = get_common_words(cleaned_texts, top_n=20)
        print(f"✓ Identified top {len(common_words)} most common words")
        
        # Step 5: Generate report
        print("\nSTEP 5: Generating summary report...")
        report = generate_report(common_words, statistics)
        
        # Display preview
        print("\n" + "=" * 80)
        print("REPORT PREVIEW")
        print("=" * 80)
        print(report[:1000] + "\n... (see report.txt for full content)")
        
        print("\n" + "=" * 80)
        print("✓ ANALYSIS COMPLETE!")
        print("=" * 80)
        print("\nNext steps:")
        print("1. Open 'report.txt' to view the complete analysis")
        print("2. Review the insights and statistics")
        print("3. Use findings to inform business decisions")
        print()
        
    except Exception as e:
        print(f"\n✗ Error during analysis: {str(e)}")
        print("Please check your data file and try again.")
        raise


if __name__ == "__main__":
    main()