import torch
import torch.nn as nn
import numpy as np
import os
from sklearn.preprocessing import LabelEncoder
from torchvision.models import efficientnet_b3
from src.logger import logger
from src.exception import MyException
import sys


# Global variable to store Model and label encoder 

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
model = None
label_encoder = None


def get_custom_efficientb3(num_classes = 10):

    """
    This function create custom efficent b3 model which is being used while training

    """

    logger.info('Creating custom efficentNet b3 model ')

    

    # loading efficientNet-B3 architecture without (pre trained weights)
    model = efficientnet_b3(pretrained = False )

    # replacing the custom classifier with my custom one which i used in training

    model.classifier = nn.Sequential(

        nn.LazyLinear(2000),
        nn.BatchNorm1d(2000), 
        nn.ReLU(),           
        nn.Dropout(0.4),      
        
        # Second layer
        nn.Linear(2000, 1024),
        nn.BatchNorm1d(1024),
        nn.ReLU(),
        nn.Dropout(0.4),
        
        # Third layer
        nn.Linear(1024, 512),
        nn.BatchNorm1d(512),
        nn.ReLU(),
        nn.Dropout(0.4),
        
        # Output layer
        nn.Linear(512, num_classes)
    )

    model = model.to(device)
    logger.info(f"Model created and moved to {device}")

    return model



def load_model_safe():

    """ Safely loads the trained model and label encoder from checkpoint file. """

    global model , label_encoder

    try:

        logger.info('Starting model loading process.....')

        checkpoint_path = 'model_path/best_skin_disease_model_enhanced.pth'


        if not os.path.exists(checkpoint_path):
            error_msg = f"Model not found at {checkpoint_path}"
            logger.error(error_msg)
            raise MyException(error_msg , sys)
        

        logger.info(f"Loading checkpoint from  : {checkpoint_path}")


        # Add numpy.dtype to safe globals as suggested in the warning
        safe_globals = [
            LabelEncoder,
            np.ndarray,
            np.dtype,  # Add this as suggested in the warning
            np.core.multiarray._reconstruct,
            np._core.multiarray._reconstruct,
        ]


        try:
            # Adding safe globals before attempting to load
            torch.serialization.add_safe_globals(safe_globals)
            
            # loading safely first
            checkpoint = torch.load(checkpoint_path, map_location=device, weights_only=True)



        except Exception as safe_error:
            # it is also safe bcz i trained it :)
            logger.warning(f"Safe loading failed : {safe_error}")
            logger.info(f"Attempting to load with weights_only = False")

            checkpoint = torch.load(checkpoint_path, map_location=device, weights_only=False) 

        # verifying that checkpoint contain required components or not
        required_keys = ['label_encoder','model_state_dict']
        missing_keys = [key for key in required_keys if key not in checkpoint]



        if missing_keys:
            error_msg = f"checkpoint file is missing required keys : {missing_keys}"
            logger.error(error_msg)
            raise MyException(error_msg,sys)



        # fetching label encoder 
        label_encoder = checkpoint['label_encoder']
        num_classes = len(label_encoder.classes_)


        logger.info(f"Found {num_classes} classes")



        # creating model architecture with correct number of output classes
        model = get_custom_efficientb3(num_classes=num_classes)

        # Loading the trained weights into the model
        model.load_state_dict(checkpoint['model_state_dict'])


        # setting model to eval mode , so dropout and batchnorm get disabled
        model.eval()

        logger.info(f"Model loaded successfully and set to evaluation mode")
        logger.info(f"Model is running on: {device}")
        logger.info(f"Available classes: {label_encoder.classes_.tolist()}")

    except Exception as e:
      error_msg = f"Failed to load model: {str(e)}"
      logger.error(error_msg)
      raise MyException(error_msg, sys)
    

