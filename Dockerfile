# Start with a base Python image
FROM python:3.9.18

# Set the working directory
WORKDIR /app

# Copy the requirements.txt file into the container
COPY requirements.txt /tmp/

# Install the Python dependencies
RUN pip install --no-cache-dir -r /tmp/requirements.txt

# Copy the rest of your application's source code
COPY . /app

# Make port 8501 available to the world outside this container
EXPOSE 8501

# Define the command to run your application
CMD ["streamlit", "run", "streamlit_app/streamlit_app.py"]
