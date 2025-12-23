# base image
FROM python:3.12.1-slim

# workdir
WORKDIR /app

# copy requirements and install dependencies
COPY requirements.txt . 

# run 
RUN pip install --no-cache-dir -r requirements.txt

# copy rest application code
COPY . .

# port
EXPOSE 8000

# command to start application
CMD ["uvicorn","app:app","--host","0.0.0.0","--port","8000"]

