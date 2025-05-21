def filter_by_category(df, category):
    return df[df['categoria'] == category]

def filter_by_country(df, country):
    return df[df['pais'] == country]

def filter_by_top_visitors(df, n=5):
    return df.sort_values(by='visitas', ascending=False).head(n)

def filter_by_top_spending(df, n=5):
    return df.sort_values(by='avg_spending_usd', ascending=False).head(n)
