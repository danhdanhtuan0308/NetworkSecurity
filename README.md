# Network Security Project


This project is a FastAPI-based application for network security tasks, such as training models and making predictions on network data (e.g., phishing detection). It includes a CI/CD pipeline, Docker support/AWS ECR, AWS s3 Bucket , and MongoDB integration and deployment using FastAPI/AWs EC2 Instance. 


## Project Structure

```
.
├── .env                # Environment variables
├── .gitignore         # Git ignore file
├── app.py             # FastAPI application
├── Dockerfile         # Dockerfile for containerization
├── main.py            # Main entry point for the application
├── push_data.py       # Script to push data to the database
├── README.md          # Project documentation (this file)
├── requirements.txt   # Python dependencies
├── setup.py           # Python package setup
├── test_mongodb.py    # MongoDB connection test script
├── .github/
│   └── workflows/
│       └── main.yml   # GitHub Actions CI/CD workflow
├── data_schema/
│   └── schema.yaml    # Data schema definition
├── final_models/
│   ├── model.pkl      # Trained model
│   └── preprocessor.pkl # Preprocessing pipeline
├── network_data/
│   └── phisingData.csv # Sample dataset
├── network_security/
│   ├── __init__.py
│   ├── cloud/         # Cloud-related utilities
│   ├── components/    # Pipeline components
│   ├── constant/      # Constants for the project
│   ├── entity/        # Entity definitions
│   ├── exception/     # Custom exceptions
│   ├── logging/       # Logging utilities
│   ├── pipeline/      # Training and deployment pipelines
│   └── utils/         # Utility functions
├── notebooks/         # Jupyter notebooks for experimentation
├── prediction_output/ # Directory for storing prediction outputs
└── templates/         # HTML templates for FastAPI
```

## Installation

### 1. Clone the Repository
```bash
git clone https://github.com/your-username/your-repo.git
cd your-repo
```

### 2. Install Dependencies
Create a virtual environment and install the required Python packages:
```bash
python -m venv venv
source venv/bin/activate  
pip install -r requirements.txt
```

### 3. Set Up Environment Variables
Create a `.env` file in the root directory and add the following (adjust values as needed):
```
MONGO_URI=mongodb://localhost:27017
DATABASE_NAME=network_security_db
AWS_ACCESS_KEY_ID=your_access_key
AWS_SECRET_ACCESS_KEY=your_secret_key
ECR_REGISTRY=your-ecr-registry
```

### 4. Run the Application
Start the FastAPI application:
```bash
python app.py
```
Access the API documentation at [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs).

## Docker Instructions

### 1. Build the Docker Image
```bash
docker build -t network-security-app .
```

### 2. Run the Docker Container
```bash
docker run -d -p 8000:8000 --env-file .env network-security-app
```

## CI/CD Pipeline
The project uses GitHub Actions for CI/CD, defined in `.github/workflows/main.yml`. The workflow includes:

### Continuous Integration
- **Checkout code**: Pulls the latest code from the repository.
- **Lint the repository**: Runs linting to ensure code quality.
- **Run unit tests**: Executes tests to verify functionality.

### Continuous Delivery
- **Build and push Docker images**: Creates a Docker image and pushes it to Amazon ECR.
- **Deploy the container**: Deploys the container to a self-hosted runner.

## Key Files
- **`app.py`**: Defines the FastAPI application with endpoints for training and prediction.
- **`Dockerfile`**: Configuration for containerizing the application.
- **`main.yml`**: GitHub Actions workflow for CI/CD.
- **`requirements.txt`**: Lists the Python dependencies.
- **`setup.py`**: Metadata and setup for the Python package.

## Contributing
Contributions are welcome! Follow these steps:
1. Fork the repository.
2. Create a new branch for your feature or bug fix (`git checkout -b feature-name`).
3. Commit your changes (`git commit -m "Add feature"`).
4. Push to your fork (`git push origin feature-name`).
5. Submit a pull request.

## Remember to set-up AWS to run along 
- AWS IAM : Access & Secret Access
- AWS S3 Bucket : Model.pkl and Preprocessor.pkl 
- AWS EC2 Instance : Deployment with FastAPI 
- AWS ECR : Container