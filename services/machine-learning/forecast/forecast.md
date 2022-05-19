# Amazon Forecast

## General info
* fully managed service to deliver highly accurate forecasts with ML
* "AutoML" chooses best model for our time series data
    * ARIMA, DeepAR, ETS, NPTS, Prophet
* works with any time series
    * price, promotions, economic performance etc
    * can combine with associated data to find relationship
* inventory planning, financial planning, resource planing
* based on "dataset groups", "predictors", "forecasts"

look at historical series of data (time series data) to create a forecast

same technology than Amazon.com

just needed to provide historical data + any additional data that we believe may impact the forecasts

fully managed service, no servers to provision, no model to build, train and deploy

use it instead of Amazon Sagemaker Linear Learner for regression analysis **if we need the least amount of effort**

service easy to use to predict time series data

## Use cases
* retail
* financial planning
* supply chain
* healthcare
* inventory management