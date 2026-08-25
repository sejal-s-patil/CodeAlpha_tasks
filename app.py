import streamlit as st
import requests
from bs4 import BeautifulSoup
import pandas as pd
from urllib.parse import urljoin

st.set_page_config(page_title="Web Data Scraper", layout="wide")

st.title("🌐 Web Data Scraper & Dataset Generator")
st.write("Extract product information from a webpage and create a custom dataset.")

# URL input
url = st.text_input(
    "Enter website URL:",
    "https://books.toscrape.com/"
)

# Scrape button
if st.button("🚀 Start Scraping"):

    try:
        # Send request to website
        response = requests.get(
            url,
            headers={
                "User-Agent": "Mozilla/5.0"
            },
            timeout=10
        )

        # Check whether request was successful
        if response.status_code != 200:
            st.error(f"Could not access website. Status code: {response.status_code}")

        else:
            # Parse HTML
            soup = BeautifulSoup(response.text, "html.parser")

            products = []

            # Find products
            items = soup.select("article.product_pod")

            for item in items:

                # Product name
                name_tag = item.select_one("h3 a")

                if name_tag:
                    name = name_tag.get("title", "N/A")
                    link = urljoin(url, name_tag.get("href", ""))

                else:
                    name = "N/A"
                    link = "N/A"

                # Price
                price_tag = item.select_one(".price_color")

                if price_tag:
                    price = price_tag.text.strip()
                else:
                    price = "N/A"

                # Rating
                rating_tag = item.select_one(".star-rating")

                if rating_tag:
                    rating = rating_tag.get("class")[1]
                else:
                    rating = "N/A"

                # Add information to list
                products.append({
                    "Product Name": name,
                    "Price": price,
                    "Rating": rating,
                    "Product URL": link
                })

            # Convert to DataFrame
            df = pd.DataFrame(products)

            if df.empty:
                st.warning("No data was found on this webpage.")

            else:
                st.success(f"Successfully scraped {len(df)} products!")

                # Display dataset
                st.subheader("📊 Extracted Dataset")
                st.dataframe(df, use_container_width=True)

                # Dataset statistics
                st.subheader("📈 Dataset Information")

                col1, col2, col3 = st.columns(3)

                col1.metric("Products", len(df))
                col2.metric("Columns", len(df.columns))
                col3.metric("Missing Values", df.isnull().sum().sum())

                # Download CSV
                csv = df.to_csv(index=False)

                st.download_button(
                    label="⬇️ Download Dataset as CSV",
                    data=csv,
                    file_name="scraped_dataset.csv",
                    mime="text/csv"
                )

    except requests.exceptions.RequestException as e:

        st.error(f"Error while accessing website: {e}")

    except Exception as e:

        st.error(f"Something went wrong: {e}")