from flask import Flask, render_template, jsonify, request
from src.pipeline.prediction_pipeline import PredictPipeline, CustomData
from src.exception.exception import CustomException
from src.logger.logger import logging
import sys

app=Flask(__name__)

@app.route("/")
def home_page():
    try:
        return render_template('index.html')
    except Exception as e:
        raise CustomException(e,sys)
    
@app.route("/predict", methods=['POST', "GET"])
def predict_datapoint():
    try:
        if request.method=="GET":
            return render_template('form.html')
        else:
            data=CustomData(
                carat=float(request.form.get("carat")),
                depth=float(request.form.get("depth")),
                table=float(request.form.get("table")),
                x=float(request.form.get("x")),
                y=float(request.form.get("y")),
                z=float(request.form.get("z")),
                cut=request.form.get("cut"),
                color=request.form.get("color"),
                clarity=request.form.get("clarity")
            )

            final_data = data.get_data_as_dataframe()
            pred_pipeline=PredictPipeline()
            pred=pred_pipeline.predict(final_data)

            result = round(pred[0],2)
            return render_template('result.html', final_result=result)

    except Exception as e:
        raise CustomException(e,sys)
    
if __name__=="__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)