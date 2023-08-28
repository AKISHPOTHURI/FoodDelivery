from flask import Flask,request,render_template,jsonify
from src.pipeline.prediction_pipeline import CustomData,PredictPipeline


application=Flask(__name__)

app=application



@app.route('/')
def home_page():
    return render_template('index.html')

@app.route('/predict',methods=['GET','POST'])

def predict_datapoint():
    if request.method=='GET':
        return render_template('form.html')
    
    else:
        data=CustomData(
            # Delivery_person_Age=float(request.form.get('Delivery_person_Age')),
            # Delivery_person_Ratings = float(request.form.get('Delivery_person_Ratings')),
            # Restaurant_latitude = float(request.form.get('Restaurant_latitude')),
            # Restaurant_longitude = float(request.form.get('Restaurant_longitude')),
            # Delivery_location_latitude = float(request.form.get('Delivery_location_latitude')),
            # Delivery_location_longitude = float(request.form.get('Delivery_location_longitude')),
            # Weather_conditions = request.form.get('Weather_conditions'),
            # Road_traffic_density = request.form.get('Road_traffic_density'),
            # Vehicle_condition = request.form.get('Vehicle_condition'),
            # Type_of_order = request.form.get('Type_of_order'),
            # Type_of_vehicle = request.form.get('Type_of_vehicle'),
            # multiple_deliveries = request.form.get('multiple_deliveries'),
            # Festival = request.form.get('Festival'),
            # Type_of_City = request.form.get('Type_of_City'),
            # day_quaters = request.form.get('day_quaters'),
            # distance = request.form.get('distance')
            Delivery_person_Age=36.0,
            Delivery_person_Ratings = 3.0,
            Restaurant_latitude = 30.327968,
            Restaurant_longitude = 78.046106,
            Delivery_location_latitude = 30.397968,
            Delivery_location_longitude = 78.116106,
            Weather_conditions = 1.0,
            Road_traffic_density = 1.0,
            Vehicle_condition = 1.0,
            Type_of_order = 1.0,
            Type_of_vehicle = 1.0,
            multiple_deliveries = 1.0,
            Festival = 1.0,
            Type_of_City = 1.0,
            day_quaters = 1.0,
            distance = 10.52
        )
        final_new_data=data.get_data_as_dataframe()
        predict_pipeline=PredictPipeline()
        pred=predict_pipeline.predict(final_new_data)

        results=round(pred[0])

        return render_template('results.html',final_result=results)



if __name__=="__main__":
    app.run(host='0.0.0.0',debug=True,port=5000)