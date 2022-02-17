# Facilitate performance analysis of the tables in the database
reddit_corpus_pre = {
    'month_list': ['2021-01', '2021-02', '2021-03', '2021-04', '2021-05', '2021-06', '2021-07', '2021-08', '2021-09',
                   '2021-10', '2021-11'],
    'count_list': [5854247, 4644290, 2361654, 1417778, 1339675, 2129259, 1083788, 1007205, 1001595, 919366, 956266]
}
sample_unprocessed_data = {
    'id': [2, 3564, 10546, 26582],
    'body': ['Man that GME cult thread is pure comedy',
             'Think about what https://twitter.com/jimcramer/status \n said',
             'TSLA not even close to enough rockets 🚀🚀🚀🚀',
             '[removed]'],
    'created_utc': ['2021-02-16 10:15:31', '2021-08-21 05:56:02', '2021-10-15 20:12:05', '2021-11-12 06:00:00']
}
pre_stats = {
    'Month': ['2021-01', '2021-02', '2021-03', '2021-04', '2021-05', '2021-06', '2021-07', '2021-08', '2021-09',
              '2021-10', '2021-11'],
    'Corpus': [5854247, 4644290, 2361654, 1417778, 1339675, 2129259, 1083788, 1007205, 1001595, 919366, 956266],
    'First Stage Cleaning': [4407690, 3170538, 1944148, 1219579, 1228267, 1633043, 892856, 838996, 822080, 758369,
                             800428],
    'Second Stage Cleaning': [4395910, 3163680, 1940536, 1217629, 1226330, 1630385, 891664, 837718, 820812, 757317,
                              799202]
}
stock_symbol_stats = {
    'Comment contains stock symbol': ["False", "True"],
    'Number of comments': [14926159, 2755024]
}
stock_data_set = {
    'Exchange': ['NASDAQ', 'NYSE', 'AMEX'],
    'Total Stocks Listed': [4884, 3181, 275],
    'Market Cap > $50M': [3255, 2577, 186],
    'Stock Price > $3': [3618, 3094, 168]
}
# EDA
top_10_mentioned_stocks = {
    'Stock': ['GME', 'AMC', 'BB', 'PLTR', 'TSLA', 'RH', 'NOK', 'RKT', 'AMD', 'TLRY'],
    'Company': ['GameStop Corp.', 'AMC Entertainment Holdings, Inc.', 'BlackBerry Limited',
                'Palantir Technologies Inc,', 'Tesla, Inc.', 'RH, Inc.', 'Nokia Corporation', 'Rocket Companies, Inc.',
                'Advanced Micro Devices, Inc', 'Tilray Brands, Inc.'],
    'Count': [517224, 209970, 140441, 76165, 76020, 63948, 47086, 32206, 30151, 28382]
}
# Sentiment Analysis
textblob_distribution = {
    'Sentiment': ['Polarity', 'Subjectivity', 'Intensity'],
    'Description': ['Negative vs Positive', 'Objective vs Subjective', 'Modification of next word'],
    'Value': ['(-1.0 => +1.0)', '(+0.0 => +1.0)', '(*0.5 => *2.0)']
}
vader_distribution = {
    'Sentiment': ['Positive', 'Negative', 'Neutral'],
    'Compound score': ['compound score >= 0.05', 'compound score > -0.05 and compound score < 0.05',
                       'compound score <= -0.05']
}
