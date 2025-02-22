# Use an official Python runtime
FROM python:3.11

# Set the working directory
WORKDIR /app

# Copy requirements file first (for caching optimization)
COPY requirements.txt /app/

# Install NumPy & Pandas first (to prevent version conflicts)
RUN pip install --no-cache-dir numpy==1.23.5 pandas==1.5.3

# Install remaining dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project
COPY . /app

# Expose Flask's port
EXPOSE 5000

# Run the Flask app
CMD ["python", "app.py"]
