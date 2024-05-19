import joblib
import pandas as pd

model = joblib.load('./ai_model/elasticNetModel.joblib')
encoder = joblib.load('./ai_model/encoder.joblib')

def predict_price(year, quarter, origin, dest, miles, num_tickets_ordered, airline_company):
    input_data = pd.DataFrame({
        'Year': [year],
        'Quarter': [quarter],
        'Origin': [origin],
        'Dest': [dest],
        'Miles': [miles],
        'NumTicketsOrdered': [num_tickets_ordered],
        'AirlineCompany': [airline_company]
    })

    input_data_encoded = encoder.transform(input_data)
    
    prediction = model.predict(input_data_encoded)
    
    return prediction[0]
