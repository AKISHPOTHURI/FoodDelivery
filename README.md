# Sensor-Fault-Detection

### Problem Statement

Predicting delivery time is a critical challenge for food delivery services like Zomato and Swiggy. Delivery time estimation directly impacts customer satisfaction and operational efficiency. Inaccurate predictions can lead to dissatisfied customers and inefficient use of delivery resources.

A straightforward and effective approach to this problem is by analyzing the distance between the restaurant (pickup point) and the customer's location (delivery point). By examining historical data on delivery times for various distances, we can develop a predictive model that leverages past delivery patterns to provide more accurate delivery estimates.

### Solution Proposed 

In this project, the focus is on predicting delivery times based on the distance between the pickup and delivery points. We use historical data on previous orders to determine how long similar deliveries took over comparable distances. By calculating average delivery times over various distances, we can create a model that accurately estimates the delivery time for new orders. This approach provides a reliable basis for delivery time predictions, helping to improve customer satisfaction and streamline delivery operations.

## Tech Stack Used

1. Python 
2. FastAPI 
3. Machine learning algorithms
4. Docker
5. MongoDB

## Infrastructure Required.

1. AWS S3
2. AWS EC2
3. AWS ECR
4. Git Actions
5. Terraform

## How to run?

Before we run the project, make sure that you are having MongoDB in your local system, with Compass since we are using MongoDB for data storage. You also need AWS account to access the service like S3, ECR and EC2 instances.

## Data Collections

![image](https://user-images.githubusercontent.com/57321948/193536736-5ccff349-d1fb-486e-b920-02ad7974d089.png)

## Project Archietecture

![image](https://user-images.githubusercontent.com/57321948/193536768-ae704adc-32d9-4c6c-b234-79c152f756c5.png)

## Deployment Archietecture

![image](https://user-images.githubusercontent.com/57321948/193536973-4530fe7d-5509-4609-bfd2-cd702fc82423.png)

### Step 1: Clone the repository

```bash
git clone https://github.com/AKISHPOTHURI/FoodDelivery.git
```

### Step 2- Create a conda environment after opening the repository

```bash
conda create -n sensor python=3.7.6 -y
```

```bash
conda activate sensor
```

### Step 3 - Install the requirements

```bash
pip install -r requirements.txt
```

### Step 4 - Export the environment variable

```bash
export AWS_ACCESS_KEY_ID=<AWS_ACCESS_KEY_ID>

export AWS_SECRET_ACCESS_KEY=<AWS_SECRET_ACCESS_KEY>

export AWS_DEFAULT_REGION=<AWS_DEFAULT_REGION>

export MONGODB_URL="mongodb+srv://<username>:<password>@ineuron-ai-projects.7eh1w4s.mongodb.net/?retryWrites=true&w=majority"

```

### Step 5 - Run the application server

```bash
python app.py
```

### Step 6. Train application

```bash
http://localhost:8080/train

```

### Step 7. Prediction application

```bash
http://localhost:8080/predict

```

## Run locally

1. Check if the Dockerfile is available in the project directory

2. Build the Docker image

```
docker build -t sensor . 

```

3. Run the Docker image

```
docker run -d -e AWS_ACCESS_KEY_ID="${{ secrets.AWS_ACCESS_KEY_ID }}" -e AWS_SECRET_ACCESS_KEY="${{ secrets.AWS_SECRET_ACCESS_KEY }}" -e AWS_DEFAULT_REGION="${{ secrets.AWS_DEFAULT_REGION }}" -e MONGODB_URL="${{ secrets.MONGODB_URL }}" -p 8080:8080 sensor
```
