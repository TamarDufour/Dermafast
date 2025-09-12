import pandas as pd

df = pd.read_csv('golden_pages.csv')
df.drop(columns=['web-scraper-order','web-scraper-start-url','show_more','sniff_link', 'sniff_link-href'], inplace=True)
print(df.columns)

filtered_df = df[df['extra_info'].str.contains('שירותי', na=False)]

# clean 'extra_info' column to include only relevant info
filter = lambda x: x.replace('שירותי מרפאה נלווים', '').replace('שירותים בסניף', '')
filtered_df['extra_info'] = filtered_df['extra_info'].apply(filter)
filtered_df = filtered_df.groupby(['address', 'sniff_provider','phone_num', 'times'], as_index=False).agg({'extra_info': ' '.join})

# clean 'times' so it formated as a list of days and hours


# Save the cleaned dataframe to a new CSV file
filtered_df.to_csv('cleaned_golden_pages.csv', index=False)