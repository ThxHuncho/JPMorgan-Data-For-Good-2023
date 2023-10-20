import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import folium
from statsmodels.tsa.statespace.sarimax import SARIMAX
from sklearn.metrics import mean_squared_error, mean_absolute_error
import numpy as np

# Disable the warning for PyplotGlobalUse
st.set_option('deprecation.showPyplotGlobalUse', False)


# Define the pages
pages = {
    "Home": "Home",
    "Map Analysis": "Map Analysis",
    "Time Analysis": "Time Analysis",
    "Partners Analysis": "Partners Analysis",
    "Donations Prediction": "Donations Prediction",
    "Perfect donor": "Perfect donor"
}

# Create a sidebar with page selection
selected_page = st.sidebar.selectbox("Select a page", list(pages.keys()))

# Load the data
data = pd.read_excel("shared_data_read_only/Invoice and Opportunities.xlsx")
data2 = pd.read_excel("shared_data_read_only/Invoice and Opportunities.xlsx")
invoice_opportunities = pd.read_excel('shared_data_read_only/Invoice and Opportunities.xlsx')

# Load the data part 2
business_account = pd.read_excel('shared_data_read_only/Business Account.xlsx')
contacts = pd.read_excel('shared_data_read_only/Contacts.xlsx')
invoice_opportunities = pd.read_excel('shared_data_read_only/Invoice and Opportunities.xlsx')
items_opportunities = pd.read_excel('shared_data_read_only/Items and Opportunities.xlsx')


# Main content
if selected_page == "Home":
    st.title("Home Page")


    # Association's Mission (in bold)
    # Introduction and Mission
    st.header("📊 Sport dans la Ville Data Analysis Tool 📈")
    st.markdown("This app aims to provide data analysis support for the Sport dans la Ville association. It serves as a tool to help the organization with data analysis in a clean and organized manner, eliminating the need for a dedicated data science team.")

    # Mission
    st.write("<b>Mission:</b>", unsafe_allow_html=True)
    st.write("For 25 years, Sport dans la Ville has been the leading association for integration through sport in France. All the programs set up by Sport dans la Ville enable the social and professional integration of the 10,000 young people registered with the association, actively participating in their progress and personal development.")

    # Context (in bold)
    st.write("<b>Context:</b>", unsafe_allow_html=True)
    st.write("Sport dans la Ville supports various communities in France by making sports more accessible to youth through running multiple sports activities, building out sports fields, and much more.")
    st.write("Sport dans la Ville is looking to better understand its current donor base to maximize funding support and increase donations.")
    st.write("Additionally, Sport Dans La Ville wants to better understand trends in donation timing, the impact of external economic factors, donor loyalty, and those who donate via multiple channels (e.g., sponsorship, events, apprenticeship tax, profit, etc.).")
    st.write("Through your analysis of the provided data sets and understanding of Sport dans la Ville's mission, share your insights on ways to increase fundraising, anticipate revenue streams, and advance their mission. Your proposal may also include recommendations for additional research or changes to data collection for improved insights.")

    
elif selected_page == "Map Analysis":
    st.title("Map Analysis Page")
    # Explanation for Map Analysis Page
    st.write("🗺️ Welcome to the 'Map Analysis' page! Here, we explore the geographical distribution of our donors. Understanding where our donors come from is vital to our mission. It helps us identify areas where we can improve engagement, seek new opportunities for support, and assess our presence in different regions. In this analysis, the map points are color-coded to provide insights. Green points represent active donors who continue to support our cause. Blue points indicate prospects who have shown interest in supporting us, and red points signify inactive donors. Analyzing the geographic data equips us with the knowledge to tailor our outreach and optimize our fundraising strategy. Your expertise in location-based analysis plays a crucial role in our mission. 🌍")
    st.write("This is the Map Analysis Page. You can perform spatial data analysis or visualization here.")
    # Link to the HTML map file
    st.subheader("Client Locations Map")
    st.write("You can view the client locations map by downloading the html file provided and clicking the link below:")
    st.markdown("[View Client Locations Map](file:///Users/aligonzalezlobo/Downloads/partners_locations_map.html)")
    # Add an image from a local file
    st.image('image1.png', caption='Map Analysis Overview', use_column_width=True)

    

elif selected_page == "Time Analysis":
    st.title("Time Analysis Page")
    
    # Explanation for Time Analysis Page
    st.write("⏰ Welcome to the 'Time Analysis' page! Here, we explore the dynamics of donations over time. We examine the total amount of donations and the total number of donations to uncover trends, patterns, and seasonality in our data. We'll delve deeper into the analysis to understand critical aspects such as the standard deviation of donation amounts, the mean of donation amounts, and more. Understanding time series data is essential for identifying seasonality events and making accurate forecasts. By analyzing the temporal dimension of our data, we can better plan for the future and optimize our fundraising efforts. Your expertise in time series analysis is crucial to achieving this goal. 📈")

    st.write("This is the Time Analysis Page. You can analyze time-series data or patterns here.")
    
    # Sidebar filters
    st.sidebar.header("Data Filters")
    
    # Filter by date range with default values
    start_date = st.sidebar.date_input("Start Date", pd.to_datetime("2021-01-01"))
    end_date = st.sidebar.date_input("End Date", pd.to_datetime("2023-10-10"))

    # Convert start_date and end_date to datetime objects
    start_date = pd.to_datetime(start_date)
    end_date = pd.to_datetime(end_date)

    filtered_data = data[(data["Date"] >= start_date) & (data["Date"] <= end_date)]
    filtered_data2 = data2[(data2["Date"] >= start_date) & (data2["Date"] <= end_date)]
    invoice_opportunities = invoice_opportunities[(invoice_opportunities["Date"] >= start_date) & (invoice_opportunities["Date"] <= end_date)]

    # Filter by customer number
    customer_number = st.sidebar.text_input("Customer Number")
    if customer_number:
        filtered_data = filtered_data[filtered_data["Customer"] == customer_number]
        filtered_data2 = filtered_data2[filtered_data2["Customer"] == customer_number]

    # Select time frequency (day, week, or month)
    time_frequency = st.sidebar.radio("Time Frequency", ["Week", "Month"], index=1)
    if time_frequency == "Week":
        filtered_data = filtered_data.resample("W", on="Date").sum()
    elif time_frequency == "Month":
        filtered_data = filtered_data.resample("M", on="Date").sum()

    # Total Amount Donated
    st.header("Total Amount Donated vs Number of Donations Over Time")
    
    # Define the mapping of time frequencies
    time_frequency_mapping = {
        "Week": "W",
        "Month": "M",
    }

    # Convert 'Date' column to datetime
    filtered_data2['Date'] = pd.to_datetime(filtered_data2['Date'])

    # Group the data by the time frequency (day, week, or month) and count the rows
    donation_counts = filtered_data2.resample(time_frequency_mapping[time_frequency], on='Date').size().reset_index(name='Donation Count')
    
        # Create a wide figure for a side-by-side plot hereeeeeeeeeeeeeeeeeeeeeeeeeeeeee
    fig, ax1 = plt.subplots(figsize=(14, 7))

    # Plot 'Amount donated' in red with a solid line on the left y-axis
    color = 'tab:red'
    ax1.set_xlabel('Time')
    ax1.set_ylabel('Amount donated', color=color)
    sns.lineplot(x=filtered_data.index, y='Amount', data=filtered_data, ax=ax1, color=color, label='Amount donated')
    ax1.tick_params(axis='y', labelcolor=color)

    # Create a second y-axis for 'Number of donations'
    ax2 = ax1.twinx()

    # Plot 'Number of donations' in blue with a dashed line on the right y-axis
    color = 'tab:blue'
    ax2.set_ylabel('Number of donations', color=color)
    sns.lineplot(x=donation_counts['Date'], y='Donation Count', data=donation_counts, ax=ax2, color=color, label='Number of donations', linestyle='--')
    ax2.tick_params(axis='y', labelcolor=color)

    # Set titles and labels
    plt.title('Donations Over Time')
    ax1.set_xlabel('Time')

    # Add legend to differentiate the lines
    lines, labels = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines + lines2, labels + labels2, loc='upper left')

    # Display the combined plot in Streamlit
    st.pyplot(fig)
    
    
    # Additional Analysis (Mean, Rate, Rolling Mean, Std Deviation)
    st.header("Additional Analysis")


    # Convert the 'Date' column to a datetime object
    invoice_opportunities['Date'] = pd.to_datetime(invoice_opportunities['Date'])


    # Group by weeks and calculate statistics
    stats = invoice_opportunities.resample(time_frequency_mapping[time_frequency], on='Date').agg({
        'Amount': 'mean',                            # Mean of donations
        'Opportunity ID': 'count',                   # Number of donations
    })

    # Calculate the rate: amount of donations / number donations
    stats['Rate'] = stats['Amount'] / stats['Opportunity ID']

    # Calculate the rolling mean (moving average) using a window size of 4 weeks
    stats['Rolling Mean'] = stats['Amount'].rolling(window=4).mean()

    # Calculate the standard deviation of the amount of donations
    stats['Std Deviation'] = stats['Amount'].rolling(window=4).std()

    # Create separate tables for each statistic
    mean_table = stats[['Amount']]
    rate_table = stats[['Rate']]
    rolling_mean_table = stats[['Rolling Mean']]
    std_deviation_table = stats[['Std Deviation']]

    # Create subplots for tables
    fig, axes = plt.subplots(nrows=2, ncols=2, figsize=(12, 8))

    # Plot the tables
    mean_table.plot(ax=axes[0, 0], title='Mean of Donations (Amount/Nb Donations)', legend=False)
    rate_table.plot(ax=axes[0, 1], title='Donation Rate (Amount/Opportunity ID)', legend=False)
    rolling_mean_table.plot(ax=axes[1, 0], title='Rolling Mean (4 weeks) of Amount', legend=False)
    std_deviation_table.plot(ax=axes[1, 1], title='Standard Deviation of the Amount of the Donations', legend=False)

    # Increase the spacing between subplots
    fig.subplots_adjust(wspace=0.5, hspace=0.5)

    # Display the tables
    st.pyplot(fig)

elif selected_page == "Partners Analysis":
    st.title("Partners Analysis Page")
    
    # Explanation for Partners Analysis Page
    st.write("🔍 Welcome to the 'Partners Analysis' page! Here, we dive deep into our partner data to gain insights into their customer types and sectors. We also identify the top three partners who have made the highest donations, as well as the top three in terms of loyalty. This analysis is instrumental in understanding our current donor base, optimizing fundraising strategies, and making data-driven decisions to advance our mission. Your contributions in this analysis help us maximize donor support and foster long-lasting partnerships. 🚀")

        
    # Sidebar filters
    st.sidebar.header("Data Filters")
    start_date = st.sidebar.date_input("Start Date", pd.to_datetime("2021-01-01"))
    end_date = st.sidebar.date_input("End Date", pd.to_datetime("2023-10-10"))

    # Convert start_date and end_date to datetime
    start_date = pd.to_datetime(start_date)
    end_date = pd.to_datetime(end_date)

    # Filter data based on the selected date range
    filtered_data3 = business_account[(business_account['Created On'] >= start_date) & (business_account['Created On'] <= end_date)]

    # Calculate total number of customers in each status category
    total_customers = len(filtered_data3)
    total_inactive_customers = len(filtered_data3[filtered_data3['Customer Status'] == 'Inactive'])
    total_active_customers = len(filtered_data3[filtered_data3['Customer Status'] == 'Active'])
    total_prospects_customers = len(filtered_data3[filtered_data3['Customer Status'] == 'Prospect'])

    # Create a pie chart to visualize the distribution of customer status
    labels = ['Inactive', 'Active', 'Prospect']
    sizes = [total_inactive_customers, total_active_customers, total_prospects_customers]
    colors = ['red', 'green', 'blue']
    fig, ax = plt.subplots()
    ax.pie(sizes, labels=labels, autopct='%1.1f%%', colors=colors, startangle=90)
    ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle

    # Display the analysis results
    st.header("Customer Status Analysis")
    st.markdown(f"<span style='color: black; font-size: 16px;'>Total Number of Customers:</span> <span style='color: black; font-size: 18px; font-weight: bold;'>{total_customers}</span>", unsafe_allow_html=True)
    st.markdown(f"<span style='color: red; font-size: 16px;'>Total Number of Inactive Customers:</span> <span style='color: red; font-size: 18px; font-weight: bold;'>{total_inactive_customers}</span>", unsafe_allow_html=True)
    st.markdown(f"<span style='color: green; font-size: 16px;'>Total Number of Active Customers:</span> <span style='color: green; font-size: 18px; font-weight: bold;'>{total_active_customers}</span>", unsafe_allow_html=True)
    st.markdown(f"<span style='color: blue; font-size: 16px;'>Total Number of Prospects Customers:</span> <span style='color: blue; font-size: 18px; font-weight: bold;'>{total_prospects_customers}</span>", unsafe_allow_html=True)
    st.pyplot(fig)

    # Group the data by Activity sector and count the customers
    # Get the number of unique sectors
    total_sectors = filtered_data3['Activity sector'].nunique()

    # Get the count of each sector
    sector_counts = filtered_data3['Activity sector'].value_counts()

    # Get the top 10 sectors and their counts
    top_10_sectors = sector_counts.head(10)

    # Calculate the percentage of each sector within the top 10
    sector_percentages = (top_10_sectors / top_10_sectors.sum() * 100).round(2)

    # Create a table with the top 10 sectors and their counts and percentages
    sector_table = pd.DataFrame({
        'Sector': top_10_sectors.index,
        'Count': top_10_sectors.values,
        'Percentage (%)': sector_percentages
    })

    # Create a column in the table for 'Others' and its count
    other_sectors_count = sector_counts[~sector_counts.index.isin(top_10_sectors.index)].sum()
    sector_table = sector_table.append({
        'Sector': 'Others',
        'Count': other_sectors_count,
        'Percentage (%)': (other_sectors_count / sector_counts.sum() * 100).round(2)
    }, ignore_index=True)

    # Display the analysis results in a table
    st.header("Sector Analysis")
    st.markdown(f"Total Number of Sectors: {total_sectors}")
    st.markdown("Top 10 Sectors Analysis (with Percentage):")
    st.table(sector_table) 



    # Load the datasets
    business_account = pd.read_excel('shared_data_read_only/Business Account.xlsx')
    contacts = pd.read_excel('shared_data_read_only/Contacts.xlsx')
    invoice_opportunities = pd.read_excel('shared_data_read_only/Invoice and Opportunities.xlsx')
    items_opportunities = pd.read_excel('shared_data_read_only/Items and Opportunities.xlsx')

    # Merge the tables to combine relevant information
    merged_data = business_account.merge(contacts, left_on='Business Account', right_on='Business Account', suffixes=('', '_contacts'))
    merged_data = merged_data.merge(invoice_opportunities, left_on='Business Account', right_on='Customer', suffixes=('', '_invoice'))
    merged_data = merged_data.merge(items_opportunities, left_on='Opportunity ID', right_on='Opportunity ID', suffixes=('', '_items'))

    # Group data by partners and calculate the total amount donated by each partner
    top_partners_amount = merged_data.groupby('Business Account')['Amount'].sum()

    
    # Group the data by partner and sum the amount donated
    partner_total_amount = invoice_opportunities.groupby('Customer')['Amount'].sum().reset_index()

    # Find the top 3 partners with the highest total amount donated
    top_3_partners_amount = partner_total_amount.nlargest(3, 'Amount')

    # Merge with the business_account table to get additional partner information
    top_3_partners_info = pd.merge(top_3_partners_amount, business_account, left_on='Customer', right_on='Business Account', how='left')

    # Select the relevant columns
    top_3_partners_info = top_3_partners_info[['Business Account', 'Amount', 'Activity sector', 'Partner type', 'City', 'Country Name', 'Class Name']]

    # Display the top 3 partners based on total amount donated
    st.header("Top 3 Partners by Total Amount Donated")
    st.table(top_3_partners_info)
    
    # Group the data by partner and count the number of donations
    partner_total_donations = invoice_opportunities.groupby('Customer').size().reset_index(name='Total Donations')

    # Find the top 3 most loyal partners with the highest total number of donations
    top_3_loyal_partners = partner_total_donations.nlargest(3, 'Total Donations')

    # Merge with the business_account table to get additional partner information
    top_3_loyal_partners_info = pd.merge(top_3_loyal_partners, business_account, left_on='Customer', right_on='Business Account', how='left')

    # Select the relevant columns
    top_3_loyal_partners_info = top_3_loyal_partners_info[['Business Account', 'Total Donations', 'Activity sector', 'Partner type', 'City', 'Country Name', 'Class Name']]

    # Display the top 3 most loyal partners based on the total number of donations
    st.header("Top 3 Most Loyal Partners by Total Number of Donations")
    st.table(top_3_loyal_partners_info)


elif selected_page == "Donations Prediction":
    st.header("Donations Prediction")

    # 1. Data Loading and Preprocessing
    data = pd.read_csv('TimesSeries.csv')
    data['Date'] = pd.to_datetime(data['Date'])
    data.set_index('Date', inplace=True)

    # Explanation of the task
    st.markdown("📈 Welcome to the 'Donations Prediction' page! Here, we'll apply SARIMA (Seasonal AutoRegressive Integrated Moving Average) "
                "to make predictions. Accurate forecasting enables us to optimize our strategies and make a lasting impact. 📅")


    # Splitting data for model evaluation
    train = data['Amount'][:-52]
    test = data['Amount'][-52:]

    # 3. Model Fitting with SARIMA
    model = SARIMAX(train, order=(1, 1, 1), seasonal_order=(1, 1, 1, 52))
    results = model.fit(disp=False)

    # 4. Forecasting on the Test Data
    forecast_test = results.get_forecast(steps=len(test))
    forecast_mean_test = forecast_test.predicted_mean

    # 5. Model Evaluation
    mse_test = mean_squared_error(test, forecast_mean_test)
    rmse_test = np.sqrt(mse_test)
    mae_test = mean_absolute_error(test, forecast_mean_test)

    st.write("Let's evaluate the model's performance on the test data.")
    st.write(f'Test MSE: {mse_test:.2f}')
    st.write(f'Test RMSE: {rmse_test:.2f}')
    st.write(f'Test MAE: {mae_test:.2f}')

    # 6. Forecasting for 2024
    st.write("Now, let's look ahead and make forecasts for the year 2024.")
    forecast_2024 = results.forecast(steps=52 + 52)
    forecast_2024 = forecast_2024['2024']

    # 7. Visualization of the Forecast
    st.write("Here, we visualize the SARIMA model's forecast for 2024 compared to historical data.")
    plt.figure(figsize=(16, 6))
    train.plot(label='Training Data', color='blue')
    test.plot(label='Test Data', color='orange')
    forecast_mean_test.plot(label='Forecast for Test Data', color='purple', linestyle='--')
    forecast_2024.plot(label='Forecast for 2024', color='green', linestyle='--')
    plt.title('SARIMA Model Forecast for 2024 vs. Historical Data')
    plt.xlabel('Date')
    plt.ylabel('Amount')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    st.pyplot()
    
    
if selected_page == "Perfect donor":
    st.title("Perfect donor")
    
    st.write("🚀 In addition to the analysis presented, we conducted a Machine Learning task to classify donors based on various variables, aiming to identify the profile of the 'perfect donor.' 🎯")
    
    st.write("Our classification model achieved an accuracy of 0.73, which allowed us to identify the most reliable donors based on specific criteria:")
    
    # Specify the criteria for the "perfect donor"
    criteria = {
        "Donor": "Partner",
        "Investment Choice": "Fonctionnement",
        "Class": "Headquarters",
        "Partner Type": "Individual"
    }
    
    st.write("The 'perfect donor' fits the following criteria:")
    
    for key, value in criteria.items():
        st.write(f"- {key}: {value}")
    
    st.write("Having a well-defined donor profile is crucial for the future, helping us make informed decisions on who to trust and prioritize when allocating resources and efforts. 🌟")
    
    # Add an image
    st.image("image5.png", caption="Perfect Donor Example")



