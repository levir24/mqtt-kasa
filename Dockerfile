# Use an official Python runtime as a parent image

FROM 
python:3.9-slim

# Set the working directory to /app
WORKDIR 
/mqttpaho

# Copy the current directory contents into the container at /app
COPY requirements.txt .
COPY mqttpaho.py .

# Install any needed packages specified in requirements.txt
RUN pip install --trusted-host pypi.python.org -r requirements.txt

# Define environment variable
ENV 
NAME mqttpaho

# Run app.py when the container launches
CMD ["python", "mqttpaho.py"]