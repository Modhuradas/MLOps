from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from model import predict_apartment_price

app = FastAPI(title="Real Estate Price Estimator")

class PropertyData(BaseModel):
    location: str
    area_sqm: float
    bedrooms: int

@app.get("/")
def home():
    return {"message": "Property valuation API is active"}

@app.post("/valuation")
def get_valuation(property_data: PropertyData):
    if property_data.area_sqm <= 0 or property_data.bedrooms <= 0:
        raise HTTPException(
            status_code=400,
            detail="Area and bedrooms must be positive numbers"
        )
    
    estimated_value = estimate_apartment_value(
        sqm=property_data.area_sqm,
        bedrooms=property_data.bedrooms,
        location=property_data.location
    )
    
    return {
        "location": property_data.location,
        "estimated_price_eur": estimated_value,
        "property_details": {
            "area": property_data.area_sqm,
            "bedrooms": property_data.bedrooms
        }
    }

if __name__ == "__main__":
    import uvicorn
    print("Server running at: http://127.0.0.1:3000")
    print("API Documentation: http://127.0.0.1:3000/docs")
    print("ReDoc: http://127.0.0.1:3000/redoc")
    uvicorn.run(app, host="127.0.0.1", port=3000)