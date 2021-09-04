import numpy as np
import pandas as pd
from flask import Flask,render_template,request
from flask_cors import cross_origin
import pickle

##intitalize flask object
app = Flask(__name__)

##load model
model = pickle.load(open("model.pkl","rb"))

@app.route("/")
@cross_origin()
def home():
    return render_template("index.html")

@app.route('/predict',methods=['GET','POST'])
@cross_origin()
def predict():
    if request.method == 'POST':

        ## Get Source value from web form
        Source = request.form['Source']
        s_Delhi = 0
        s_Mumbai = 0
        s_Kolkata = 0
        s_Chennai = 0

        if (Source == 'Delhi'):
            s_Delhi = 1
        elif (Source == 'Mumbai'):
            s_Mumbai = 1
        elif (Source == 'Kolkata'):
            s_Kolkata = 1
        elif (Source == 'Chennai'):
            s_Chennai = 1
        else:
            pass

        ## Get Destination value from web form
        Destination = request.form['Destination']
        d_Delhi = 0
        d_Cochin = 0
        d_Hyderabad = 0
        d_Kolkata = 0
        

        if (Destination == 'Delhi'):
            d_Delhi = 1
        elif (Destination == 'Cochin'):
            d_Cochin = 1
        elif (Destination == 'Hyderabad'):
            d_Hyderabad = 1
        elif (Destination == 'Kolkata'):
            d_Kolkata = 1
        else:
            pass

        ## Get Departure time from web form

        departure_date = request.form['Dep_Time']

        Day_of_Journey = int(pd.to_datetime(departure_date, format="%Y-%m-%dT%H:%M").day)
        Month_of_Journey = int(pd.to_datetime(departure_date, format="%Y-%m-%dT%H:%M").month)

        Dept_hr = int(pd.to_datetime(departure_date, format="%Y-%m-%dT%H:%M").hour)
        Dept_min = int(pd.to_datetime(departure_date, format="%Y-%m-%dT%H:%M").minute)

       ## Get Arrival time from web form

        arrival_date = request.form['Arrival_Time']

        Arrival_hr = int(pd.to_datetime(arrival_date, format="%Y-%m-%dT%H:%M").hour)
        Arrival_min = int(pd.to_datetime(arrival_date, format="%Y-%m-%dT%H:%M").minute)

       ## calculate duration

        Duration_hr = abs(Arrival_hr - Dept_hr)
        Duration_min = abs(Arrival_min - Dept_min)

        ## Get Airline from web form

        airline = request.form['airline']

        Airline_AirIndia = 0
        Airline_GoAir = 0
        Airline_IndiGo = 0
        Airline_JetAirways = 0
        Airline_JetAirwaysBusiness = 0
        Airline_Multiplecarriers = 0
        Airline_MultiplecarriersPremiumeconomy = 0
        Airline_SpiceJet = 0 
        Airline_Trujet = 0 
        Airline_Vistara = 0 
        Airline_VistaraPremiumeconomy = 0

        if (airline == 'Air India'):
            Airline_AirIndia = 1
        elif (airline == 'GoAir'):
            Airline_GoAir = 1
        elif (airline == 'IndiGo'):
            Airline_IndiGo = 1
        elif (airline == 'Jet Airways'):
            Airline_JetAirways = 1
        elif (airline == 'Jet Airways Business'):
            Airline_JetAirwaysBusiness = 1
        elif (airline == 'Multiple carriers'):
            Airline_Multiplecarriers = 1
        elif (airline == 'Multiple carriers Premium economy'):
            Airline_MultiplecarriersPremiumeconomy = 1
        elif (airline == 'SpiceJet'):
            Airline_SpiceJet = 1
        elif (airline == 'Trujet'):
            Airline_Trujet = 1
        elif (airline == 'Vistara'):
            Airline_Vistara = 1
        elif (airline == 'Vistara Premium economy'):
            Airline_VistaraPremiumeconomy = 1
        else:
            pass

        ## Get value of stopage from web form
        Total_Stops = int(request.form['stops'])

        ## Get value of Additional_Info from web form
        add_info = request.form['Additional Info']

        No_Info=0
        In_flight_meal_not_included=0
        No_checkin_baggage_included=0
        One_Short_layover=0
        Two_Long_layover=0
        Change_airports=0
        Business_class=0
        Red_eye_flight=0

        if (add_info == 'No_Info'):
            No_Info=1
        elif (add_info  == 'In_flight_meal_not_included'):
            In_flight_meal_not_included=1
        elif (add_info == 'No_check-in_baggage_included'):
            No_checkin_baggage_included=1
        elif (add_info == 'One_Short_layover'):
            One_Short_layover=1
        elif (add_info == 'Two_Long_layover'):
            Two_Long_layover=1
        elif (add_info == 'Change_airports'):
            Change_airports=1
        elif (add_info == 'Business_class'):
            Business_class=1
        elif (add_info == 'Red_eye_flight'):
            Red_eye_flight=1
        else:
            pass

        features = [Total_Stops, Day_of_Journey, Month_of_Journey,Dept_hr,Dept_min,Arrival_hr,Arrival_min,Duration_hr,Duration_min,
        s_Chennai,s_Delhi,s_Kolkata,s_Mumbai,d_Cochin,d_Delhi,d_Hyderabad,d_Kolkata,
        Airline_AirIndia,Airline_GoAir,Airline_IndiGo,Airline_JetAirways,Airline_JetAirwaysBusiness,Airline_Multiplecarriers,
        Airline_MultiplecarriersPremiumeconomy,Airline_SpiceJet,Airline_Trujet,Airline_Vistara,Airline_VistaraPremiumeconomy,
        One_Short_layover,Two_Long_layover,Business_class,Change_airports,In_flight_meal_not_included,No_Info,No_checkin_baggage_included,
        Red_eye_flight]

        prediction = model.predict([features])

        output = round(prediction[0],2)

        return render_template('index.html',prediction_text='Your Estimated Flight Price is Rs. {}'.format(output))
    return render_template('index.html')


#### calling main function
if __name__ == "__main__":
    app.run(debug=True)
