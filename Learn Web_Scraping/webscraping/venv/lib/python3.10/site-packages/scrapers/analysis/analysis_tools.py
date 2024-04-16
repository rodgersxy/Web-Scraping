import pandas as pd

def avg_rating_month_data(df_reviews):
    """
    Needs two columns: 'date_year_month_hide' and 'rating_star_cleaned_hide'
    """
    df = df_reviews.copy()
    df.date_year_month_hide = pd.to_datetime(df.date_year_month_hide)
    df.sort_values("date_year_month_hide", inplace=True)
    df["sum_rating"] =  df["rating_star_cleaned_hide"].cumsum()
    df["n_rating"] =  1
    df["n_rating"] =  df["n_rating"].cumsum()
    df["avg_rating_uptodate"] = df["sum_rating"] / df["n_rating"]
    agg_func = {
        "avg_rating_uptodate": "last",
        "rating_star_cleaned_hide": "mean"
    }
    df_months = df.groupby(["date_year_month_hide"]).agg(agg_func).stack().reset_index()
    df_rating_star = df_months[df_months.level_1 == "rating_star_cleaned_hide"].set_index(
                            ["date_year_month_hide", "level_1"]
                        ).unstack(
                            fill_value=0
                        ).asfreq(
                            'MS', fill_value=0
                        ).stack().sort_index(level=1).reset_index()

    df_avg = df_months[df_months.level_1 == "avg_rating_uptodate"].set_index(
                            ["date_year_month_hide", "level_1"]
                        ).unstack(
                            fill_value=0
                        ).asfreq(
                            'MS', method="ffill"
                        ).stack().sort_index(level=1).reset_index()

    df_months = pd.concat([df_rating_star, df_avg])

    df_months = pd.crosstab(
            df_months["level_1"],
            df_months["date_year_month_hide"],
            df_months[0],
            aggfunc="sum"
    )

    df_months.index = ["Average Rating up to Date", "Monthly Average Rating"]
    df_months.columns.name = "Date"

    return df_months

def n_rating_month(df_reviews):
    """
    Needs two columns: 'date_year_month_hide' and 'rating_star_cleaned_hide', 'text_cleaned_hide'
    """
    df = df_reviews.copy()
    df.date_year_month_hide = pd.to_datetime(df.date_year_month_hide)
    df_n_rating = df.groupby(
            ["date_year_month_hide", "rating_star_cleaned_hide"]
        )["text_cleaned_hide"].count().reset_index()
    df_n_rating = df_n_rating.set_index(
                                ["date_year_month_hide", "rating_star_cleaned_hide"]
                            ).unstack(
                                fill_value=0
                            ).asfreq(
                                'MS', fill_value=0
                            ).stack().sort_index(level=1).reset_index()

    df_n_rating = pd.crosstab(
            df_n_rating["rating_star_cleaned_hide"],
            df_n_rating["date_year_month_hide"],
            df_n_rating["text_cleaned_hide"],
            aggfunc="sum")

    df_n_rating.columns.name = "Date"
    df_n_rating.index.name = "Rating"

    return df_n_rating

def write_dfs(dict_dfs, filename):

    writer = pd.ExcelWriter(filename, engine='xlsxwriter')
    for sheetname, data in dict_dfs.items():
        data.to_excel(writer, sheet_name=sheetname)
    writer.save()

    print(f"{filename} saved")
    
    
def get_analysis(df, filename=""):
    df_avg_rating = avg_rating_month_data(df)
    df_n_rating = n_rating_month(df)

    dict_dfs = {
        "Reviews": df,
        "Average Rating": df_avg_rating,
        "N Rating": df_n_rating,
    }
    
    if filename:
        write_dfs(dict_dfs, filename)
    
    return dict_dfs