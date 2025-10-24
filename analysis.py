# ---------------------------------------------------------------
# Project Title : Netflix Data Analysis – Content Trends Analysis
# Internship    : AICTE x Vodafone Idea (VOIS)
# Author        : Mohammad Kasif Ansari
# ---------------------------------------------------------------

# 1️ Importing Required Libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Setting up visualization style
sns.set(style="whitegrid")
plt.rcParams['figure.figsize'] = (12, 6)

# ---------------------------------------------------------------
# 2️ Loading the Dataset
# ---------------------------------------------------------------
# Make sure the dataset file 'netflix_titles.csv' is in the same folder as this notebook
df = pd.read_csv("netflix_titles.csv")

# Basic dataset info
print(" Dataset Loaded Successfully!")
print("Shape of Dataset:", df.shape)
print("\nColumn Names:", df.columns.tolist())

# Checking for missing values
print("\nMissing Values in Each Column:\n")
print(df.isnull().sum())

# ---------------------------------------------------------------
# 3️ Data Cleaning and Preparation
# ---------------------------------------------------------------

# Dropping duplicate records if any
df.drop_duplicates(inplace=True)

# Filling missing values with placeholder text where needed
df['Director'].fillna("Unknown", inplace=True)
df['Cast'].fillna("Unknown", inplace=True)
df['Country'].fillna("Unknown", inplace=True)
df['Rating'].fillna(df['Rating'].mode()[0], inplace=True)

# Converting date column to datetime type
df['Release_Date'] = pd.to_datetime(df['Release_Date'], errors='coerce')

# Extracting year for analysis
df['Year'] = df['Release_Date'].dt.year

print("\n Data Cleaning Completed Successfully!")

# ---------------------------------------------------------------
# 4️ Basic Overview of Netflix Content
# ---------------------------------------------------------------

# Checking the number of Movies and TV Shows
print("\nCategory Distribution:\n")
print(df['Category'].value_counts())

# Checking top countries contributing content
print("\nTop 5 Countries by Content Count:\n")
print(df['Country'].value_counts().head(5))

# Displaying dataset range by years
print("\nDataset Covers Years from", int(df['Year'].min()), "to", int(df['Year'].max()))

# ---------------------------------------------------------------
# 5️ Movies vs TV Shows Trend Over the Years
# ---------------------------------------------------------------

type_trend = df.groupby(['Year', 'Category']).size().unstack(fill_value=0)

# Plotting the trend
type_trend.plot(kind='bar', stacked=False)
plt.title("Movies vs TV Shows Added per Year on Netflix")
plt.xlabel("Year")
plt.ylabel("Number of Titles")
plt.legend(title="Category")
plt.tight_layout()
plt.show()

# ---------------------------------------------------------------
# 6️ Analyzing Most Common Genres
# ---------------------------------------------------------------

# 'Listed_in' column contains comma-separated genres
if 'Listed_in' in df.columns:
    all_genres = df['Listed_in'].dropna().str.split(',').explode().str.strip()
    genre_counts = all_genres.value_counts().head(10)
    
    print("\nTop 10 Genres on Netflix:\n")
    print(genre_counts)
    
    # Visualization
    sns.barplot(x=genre_counts.values, y=genre_counts.index, palette='viridis')
    plt.title("Top 10 Genres on Netflix")
    plt.xlabel("Number of Titles")
    plt.ylabel("Genre")
    plt.tight_layout()
    plt.show()

# ---------------------------------------------------------------
# 7️ Country-Wise Contributions
# ---------------------------------------------------------------

country_counts = df['Country'].value_counts().head(10)

print("\nTop 10 Countries Contributing to Netflix Content:\n")
print(country_counts)

sns.barplot(x=country_counts.values, y=country_counts.index, palette="magma")
plt.title("Top 10 Countries Contributing Content to Netflix")
plt.xlabel("Number of Titles")
plt.ylabel("Country")
plt.tight_layout()
plt.show()

# ---------------------------------------------------------------
# 8️ Duration Analysis (Movies Only)
# ---------------------------------------------------------------

# Filtering only movies for duration analysis
movies = df[df['Category'] == 'Movie'].copy()

# Extracting numeric duration (in minutes)
movies['Minutes'] = movies['Duration'].str.replace(' min', '', regex=False)

# Keeping only numeric durations
movies = movies[movies['Minutes'].str.isnumeric()]
movies['Minutes'] = movies['Minutes'].astype(int)

# Plotting histogram of movie durations
plt.hist(movies['Minutes'], bins=20, color='skyblue', edgecolor='black')
plt.title("Distribution of Movie Durations on Netflix")
plt.xlabel("Duration (Minutes)")
plt.ylabel("Count")
plt.tight_layout()
plt.show()

# ---------------------------------------------------------------
# 9️ Summary of Insights
# ---------------------------------------------------------------

print("\n SUMMARY OF FINDINGS")
print("- Total Titles in Dataset:", len(df))
print("- Movies:", len(df[df['Category'] == 'Movie']))
print("- TV Shows:", len(df[df['Category'] == 'TV Show']))
print("\nTop 5 Genres:\n", genre_counts.head(5))
print("\nTop 5 Countries:\n", country_counts.head(5))

print("\n KEY INSIGHTS:")
print("1. Netflix’s content library has grown rapidly after 2016.")
print("2. Movies dominate the catalog, but TV Shows are growing faster since 2018.")
print("3. Drama and Comedy are the most popular genres.")
print("4. USA and India contribute the most titles.")
print("5. Increasing diversity after 2018 shows Netflix’s global expansion strategy.")
