# Use official Python image
FROM python:3.11-slim

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y curl gnupg supervisor

# Install Node.js (for frontend)
RUN curl -fsSL https://deb.nodesource.com/setup_18.x | bash - \
    && apt-get install -y nodejs

# Install Python dependencies
COPY backend/requirements.txt backend/requirements.txt
RUN pip install --no-cache-dir -r backend/requirements.txt

# Copy backend and frontend code
COPY backend ./backend
COPY frontend ./frontend

# Copy Supervisor config
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

# Expose ports if needed
EXPOSE 8000
EXPOSE 3000

# Start both servers via supervisor
CMD ["/usr/bin/supervisord"]
