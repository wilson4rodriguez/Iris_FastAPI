from fastapi import APIRouter, HTTPException, status
import numpy as np
import joblib
from models import Prediction_Input
from models import Prediction_Output

#No hay hiperparametros

#No hay Scaler o tokenizer

#Cargamos el modelo
model = joblib.load("model.pkl")

router = APIRouter()

preds=[]

#Metodo GET
@router.get('/ml')
def get_preds():
    return preds

#Metodo POST
@router.post('/ml',status_code=201,response_model=Prediction_Output)
def predict(pred_input:Prediction_Input):
    #convert input to rigth data
    list_inp= [list(pred_input.text_input.split(","))]
    arr2d=np.array(list_inp)
    #predict data
    prediction_f = model.predict(arr2d)
    #dict to convert numbers to text
    dict_res={0:"Setosa",1:"Versicolor",2:"Virginica"}
    prediction_dict={"id":str(pred_input.id),
                     "text_input":str(pred_input.text_input),
                     "pred":str(dict_res[prediction_f[0]])}
    preds.append(prediction_dict)
    return prediction_dict

#Metodo PUT
@router.put('/ml/{id}', status_code=202)
def update_preds(id:int,text_input_p:str,pred_p:str):
    for pred in preds:
        if int(pred["id"])==int(id):
            pred["text_input"] =str(text_input_p)
            pred["pred"] = str(pred_p)
            return {"message": "Pred updated successfully"}
    else:
        HTTPException(status_code=404,detail="Pred not found")

#Metodo DELETE
@router.delete('/ml/{id}')
def delete_preds(id:int):
    for pred in preds:
        if int(pred["id"])==id:
            preds.remove(pred)
            return {"message": "Pred deleted successfully"}
    else:
        HTTPException(status_code=404,detail="Pred not found")

