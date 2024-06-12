import joblib
import pandas as pd

model = joblib.load('/Users/ana-maria/Desktop/AppLicenta/CloudCompass/app/ai_model/newModel.joblib')

# Load historical data
historical_data = pd.read_csv('/Users/ana-maria/Desktop/AppLicenta/CloudCompass/app/ai_model/historical_data.csv')

# Function to get previous price
def get_previous_price(origin, destination, airline_company, date):
    filtered_data = historical_data[
        (historical_data['Origin'] == origin) & 
        (historical_data['Dest'] == destination) & 
        (historical_data['AirlineCompany'] == airline_company) 
    ]
    
    if filtered_data.empty:
        return 0  # Default value or handle as needed
    
    previous_price = filtered_data.sort_values(by='Date', ascending=False).iloc[0]['Price']
    return previous_price

def predict_price(year, quarter, origin, dest, miles, num_tickets_ordered, airline_company, date):
    # Get the previous price from historical data
    previous_price = get_previous_price(origin, dest, airline_company, date)
    
  
    input_data = pd.DataFrame({
        'Year': [year],
        'Quarter': [quarter],
        'Origin': [origin],
        'Dest': [dest],
        'Miles': [miles],
        'NumTicketsOrdered': [num_tickets_ordered],
        'AirlineCompany': [airline_company],
        'price_itinID_lag1': [previous_price]
    })
    
  
    prediction = model.predict(input_data)
    
    return prediction[0]
