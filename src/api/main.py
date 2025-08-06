from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from logger import logger
from .model_loader import load_model_safe, device
from . import model_loader
from .preprocess_image import apply_transformation
from .predictor import predict_image
from PIL import Image
import io



app = FastAPI(
    title='Skin disease classification API',
    description='AI - powered skin classifier API',
    version="1.0.0"
)



# Enable CORS for external clients
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



@app.on_event('startup')
async def startup():
    logger.info('Starting up API')
    try:
        load_model_safe()  
        logger.info('Model loaded successfully during startup')
    except Exception as e:
        logger.error(f'Startup failed: {str(e)}')
        raise e



@app.get('/')
async def root():
    return {
        "Message": "Skin disease classification API",
        "Status": "running",
        "Version": "1.0.0",
        'Model': 'Loaded' if model_loader.model is not None else 'Not loaded'
    }



@app.get('/health')
async def health_check():
    return {
        'Status': 'healthy',
        'Model loaded': 'Successfully',
        'device': str(device)
    }




@app.post('/predict')
async def predict_skin_disease(file: UploadFile = File(...)):
    """Predicts skin disease from an uploaded image"""

    if model_loader.model is None or model_loader.label_encoder is None:
        logger.error('Model not Loaded')
        raise HTTPException(status_code=503, detail="Model not available, try again later :(")

    try:
     
        content = await file.read()
        if len(content) == 0:
            raise HTTPException(status_code=400, detail="Received Empty file")

        # Open image
        image = Image.open(io.BytesIO(content))
        if image.mode != 'RGB':
            image = image.convert('RGB')

        # Preprocess for EfficientNet-B3
        image = apply_transformation(image, device)

        # Prediction
        prediction = predict_image(model_loader.model, model_loader.label_encoder, image, device)
        logger.info(f'Prediction successful: {prediction.get("predicted_class","Unknown")}')

        # Return structured JSON
        return JSONResponse(
            content={
                "Success": True,
                "prediction": prediction,
                "filename": file.filename,
            }
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Prediction failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Prediction failed: {str(e)}")
