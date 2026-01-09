from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, computed_field
from typing import Literal, Annotated, Optional
import pickle
import pandas as pd

with open('model.pkl', 'rb') as f:
    model = pickle.load(f)


app = FastAPI()
tier1_cities = [
    "Mumbai",
    "Delhi",
    "Bengaluru",
    "Chennai",
    "Hyderabad",
    "Kolkata",
    "Pune",
    "Ahmedabad"
]

tier2_cities = [
    "Nagpur",
    "Indore",
    "Bhopal",
    "Jaipur",
    "Chandigarh",
    "Coimbatore",
    "Kochi",
    "Trivandrum",
    "Visakhapatnam",
    "Vijayawada",
    "Madurai",
    "Trichy",
    "Salem",
    "Udaipur",
    "Jodhpur",
    "Kota",
    "Gwalior",
    "Jabalpur",
    "Raipur",
    "Bhilai",
    "Ranchi",
    "Bokaro",
    "Durgapur",
    "Asansol",
    "Siliguri",
    "Patna",
    "Gaya",
    "Muzaffarpur",
    "Bhubaneswar",
    "Cuttack",
    "Rourkela",
    "Sambalpur"
]


## pydantic model to validate incomming data

class UserInput(BaseModel):

    age: Annotated[int, Field(..., gt = 0, lt = 120, description='Age of the user')]
    weight: Annotated[float, Field(..., gt = 0, description='weight of the user')]
    height: Annotated[float, Field(..., gt = 0, lt = 2.5, description='Height of the user')]
    income_lpa:Annotated[float, Field(..., gt = 0, description='Age of the user in lpa')]
    smoker: Annotated[bool, Field(..., description='Is user a Smoker')]
    city: Annotated[str, Field(..., description='city of the user')]
    occupation:Annotated[Literal ['Student', 'Engineer', 'HR Executive', 'Designer',
       'Sales Executive', 'Data Analyst', 'Software Engineer', 'Manager',
       'Architect', 'Entrepreneur', 'Business Owner', 'Contractor',
       'Teacher', 'Factory Manager', 'Pensioner'], Field(..., description='occupation  of the user')]
    
    @computed_field
    @property
    def bmi(self) -> float:
        return round(self.weight/(self.height**2), 2)
    
    @computed_field
    @property
    def lifestyle_risk(self) -> str:
        if self.smoker and self.bmi > 30:
          return "High"
        elif self.smoker or self.bmi > 25:
          return "Medium"
        else:
          return "Low"
        

    @computed_field
    @property
    def age_group(self) -> str:
       if self.age < 25:
        return "Young"
       elif self.age < 45:
        return "Adult"
       elif self.age < 60: 
        return "Middle_Aged"
       return "Senior"
    
    @computed_field
    @property
    def city_tier(self) -> int:
     if self.city in tier1_cities:
      return 1
     elif self.city in tier2_cities:
      return 2
     else: 
      return 3

       

@app.post('/predict')
def predict_premium(data: UserInput):
  
  input_df = pd.DataFrame([{
    'bmi' : data.bmi,
    'age_group' : data.age_group,
    'lifestyle_risk' : data.lifestyle_risk,
    'city_tier' : data.city_tier,
    'income_lpa' : data.income_lpa,
    'occupation' : data.occupation
  }])

  prediction = model.predict(input_df)[0]

  return JSONResponse(status_code=200, content={'predicted_category' : prediction})
  

