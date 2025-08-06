from PIL import Image
import torch
from torchvision import transforms
from logger import logger
from exception import MyException
import sys

# This is the transformation which is required for efficientNet-B3
transformation = transforms.Compose([
    transforms.Resize(256),
    transforms.CenterCrop(224),
    transforms.ToTensor(),
    transforms.Normalize(
        mean=[0.485, 0.456, 0.406],  # efficientNet-B3 mean for RGB
        std=[0.229, 0.224, 0.225]    #  efficientNet-B3 std for RGB
    )
])


def apply_transformation(image : Image.Image , device):

    """
    This function recivers an image and convert into the required manner for EfficientNet-B3 model

    """

    try:
        logger.info('Image preprocessing started.....')

        
        # checking if image is in a RGB mode or not
        if image.mode != 'RGB':
            logger.info(f'converting image from {image.mode} to RGB')
            image = image.convert('RGB')


        # storing image size just for logging
        logger.info(f'The size of image is {image.size}')


        # Apply the actual transforamtion on the image
        image_tensor = transformation(image)


        # Model expects a batch of images , even one batch
        # converting (3,224,224) -> (1,3,224,224)
        image_tensor = image_tensor.unsqueeze(0)


        # moving tensor to specified device
        image_tensor.to(device)

        logger.info(f'Image preprocessing completed , Final tensor shape : {image_tensor.shape}')


        return image_tensor
    
    except Exception as e:
        error_msg = f"Error in preprocessing image for model : {str(e)}"
        logger.error(error_msg)
        raise MyException(error_msg,sys)


