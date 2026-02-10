# DeepTune Experiment Results

## Overview  

To reproduce the experiments detailed in this repository, it would require access to the actual implementation code of DeepTune. Unfortunately, due to our intellectual property (IP) policies, we are unable to share this proprietary code. This policy is in place to protect our intellectual property and ensure compliance with our organizational guidelines.  

## Base Prediction Accuracy  

The table below summarizes the base prediction accuracy (1 being 100% accuracy) of DeepTune. *Failure accuracy* and *Run accuracy* indicate the prediction accuracy for failure and application running (non-failure) events. The MAE refers to the normalized mean absolute error.  
  
| **Application** | **Failure accuracy** | **Run accuracy** | **Performance prediction normalized MAE** |  
|------------------|----------------------|------------------|-------------------------------------------|  
| Nginx            | 0.796                | 0.397            | 0.273                                     |  
| Redis            | 0.789                | 0.310            | 0.361                                     |  
| SQLite           | 0.742                | 0.456            | 0.112                                     |  
| NPB              | 0.755                | 0.455            | 0.359                                     |  
  
