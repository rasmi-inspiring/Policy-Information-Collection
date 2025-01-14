# Use an official Python runtime as a parent image
FROM python:slim

# Set the working directory in the container
WORKDIR /policy-backend

# Copy only requirements.txt first to leverage Docker cache
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the Streamlit application code
COPY . .

# Expose the port Streamlit uses
EXPOSE 8501

# Command to start the Streamlit app
CMD ["streamlit", "run", "app/main.py"]
