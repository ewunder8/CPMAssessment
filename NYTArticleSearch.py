import requests
import json
import os
import pandas as pd


def NYTArticleSearch(pDate: str):
    """
    Returns 10 rows of NYT articles based on date query.

    API_KEY must be saved as environment variable to access.

    """
    apiKey = os.environ.get('API_KEY')

    url = f"https://api.nytimes.com/svc/search/v2/articlesearch.json?fq=pub_date:(\"{pDate}\")&api-key={apiKey}"
    payload = {}
    headers = {}

    response = requests.request("GET", url, headers=headers, data=payload)

    data = response.text
    dict = json.loads(data)
    response_dict = dict['response']['docs']
    df = pd.json_normalize(response_dict)

    col_names = ['_id', 'pub_date', 'headline.main',
                 'print_section', 'word_count', 'snippet']
    df_report = df[col_names]
    df_report = df_report.rename(
        columns={'headline.main': 'headline', 'print_section': 'section'})
    # string only 50 chars
    df_report['snippet'] = df_report['snippet'].str.slice(0, 50)

    df_report.to_csv('Articles042023.csv')
