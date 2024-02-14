
import pandas as pd
from duckduckgo_search import DDGS

queries = [
    "Identify the industry in which Canoo operates, along with its size, growth rate, trends, and key players",
    "Analyze Canoo's main competitors, including their market share, products or services offered, pricing strategies, and marketing efforts",
    "Identify key trends in the market, including changes in consumer behavior, technological advancements, and shifts in the competitive landscape",
    "Gather information on Canoo's financial performance, including its revenue, profit margins, return on investment, and expense structure."
]

# Initialize an empty DataFrame to store the results
final_df = pd.DataFrame()

for query in queries:
    with DDGS() as ddgs:
        results = [{'title': r['title'], 'url': r['href']} for r in ddgs.text(query, max_results=10)]

        # Create a DataFrame from the results
        df = pd.DataFrame(results)

        # Concatenate the current DataFrame with the final DataFrame
        final_df = pd.concat([final_df, df], ignore_index=True)

# Print the final DataFrame
print(final_df)



# Print a message indicating the export is complete
print("CSV file exported successfully.")

# Export the final DataFrame to a CSV file
final_df.to_csv('search_results.csv', index=False)

