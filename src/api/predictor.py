import torch
import numpy as np
from logger import logger
from exception import MyException


def predict_image(model , label_encoder , image_tensor , device):

        """
        This function receives a trained model, label encoder, an image, and the device (CPU/GPU),
        and returns the predicted class label for the given image using the model.
        """

        try:
            logger.info('Starting image prediction...')

            model.eval()

            with torch.no_grad():
                  
                  # forward pass
                outputs = model(image_tensor)
                logger.info(f'Model outputs shape : {outputs.shape}')

                # Applying softmax to convert logits into probabilities
                prob = torch.softmax(outputs , dim = 1)



                # Finding the class with the highest probability 
                confidence , predicted_idx = torch.max(prob , dim =1)


                # converting tensor indices to actual values
                predicted_idx_value = predicted_idx.cpu().item()
                confidence_value = confidence.cpu().item()


                # Getting the class name using the label encoder
                predicted_class = label_encoder.classes_[predicted_idx_value]

                logger.info(f'Predicted class  : {predicted_class}')
                logger.info(f'Confidence score :{confidence_value}')


                # Getting probabilities for all classes
                all_probs = prob.cpu().numpy()[0] # remves batch dimension


                # creating dictionary mapping class names to probabilities 
                class_probabilities = {}

                for i, class_name in enumerate(label_encoder.classes_):
                   class_probabilities[class_name] = float(all_probs[i])


                            # Sort classes by probability (highest first)
                sorted_predictions = dict(
                    sorted(class_probabilities.items(), 
                            key=lambda x: x[1], 
                            reverse=True)
                )
                
                              
                    # Log top 3 predictions for debugging
                top_3 = list(sorted_predictions.items())[:3]
                logger.info("Top 3 predictions:")
                for class_name, prob in top_3:
                    logger.info(f"  {class_name}: {prob:.4f}")
                
                # Return structured results
                return {
                    "predicted_class": predicted_class,
                    "confidence": confidence_value,
                    "all_predictions": sorted_predictions
                }
                    
        except Exception as e:
            error_msg = f"Prediction error: {str(e)}"
            logger.error(error_msg)
            raise Exception(error_msg)



