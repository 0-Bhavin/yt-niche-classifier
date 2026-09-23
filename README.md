# YT Niche Classifier

An API-driven data tool that automates the collection and preparation of YouTube video data for niche classification. The system utilizes the YouTube Data API to retrieve comprehensive metadata from over 100 videos across various target niches, eliminating the need for manual data collection.

Repository: [0-Bhavin/yt-niche-classifier](https://github.com/0-Bhavin/yt-niche-classifier)

---

## Tech Stack

* **Language:** Python
* **API:** YouTube Data API v3
* **Data Manipulation & Analysis:** Pandas, NumPy
* **Machine Learning:** Scikit-learn / Custom ML pipelines
* **Data Processing:** Regular Expressions, JSON/CSV handling

---

## Key Features

* **Automated Data Harvesting:** Connects directly with the YouTube Data API to fetch structured metadata (titles, descriptions, tags, view counts, and channel statistics) for target categories.
* **Intelligent Preprocessing:** Cleans raw API responses by removing duplicates, handling missing values, filtering irrelevant text, and tokenizing text fields.
* **Analysis-Ready Datasets:** Transforms unstructured JSON payloads into clean, structured tabular formats suitable for immediate model consumption.
* **ML Training Pipeline Support:** Structures features and labels to support the training, testing, and validation phases of machine learning niche classifiers.

---

## Project Structure

```text
yt-niche-classifier/
│
├── data/
│   ├── raw/            # Raw JSON responses from the YouTube Data API
│   └── processed/      # Cleaned and feature-engineered datasets
│
├── src/
│   ├── collector.py    # Handles API requests and data retrieval
│   ├── preprocessor.py # Cleans, filters, and formats raw metadata
│   └── pipeline.py     # Orchestrates end-to-end data preparation
│
├── requirements.txt    # Project dependencies
├── .env.example        # Template for API key configuration
└── README.md           # Project documentation
```

---

## Getting Started

### Prerequisites

* Python 3.8 or higher
* A Google Cloud Console account with a valid YouTube Data API v3 key

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/0-Bhavin/yt-niche-classifier.git
   cd yt-niche-classifier
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use: venv\Scripts\activate
   ```

3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Configure your environment variables:
   Create a `.env` file in the root directory and add your YouTube API key:
   ```env
   YOUTUBE_API_KEY=your_api_key_here
   ```

---

## Usage

1. **Collect Data:**
   Configure your target niches and search queries inside the collection script, then execute the data fetcher:
   ```bash
   python src/collector.py
   ```

2. **Preprocess Data:**
   Run the preprocessing module to clean raw responses and output a structured dataset:
   ```bash
   python src/preprocessor.py
   ```

3. **Train the Classifier:**
   Feed the processed dataset into your machine learning pipeline for niche classification training and validation.
