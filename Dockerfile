# Use official Python slim image for backend
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    gnupg \
    supervisor \
    build-essential \
    git \
    ffmpeg

# Install Node.js for frontend (Next.js)
RUN curl -fsSL https://deb.nodesource.com/setup_18.x | bash - && \
    apt-get install -y nodejs

# -------------------------
# 🔧 Install Backend Dependencies
# -------------------------
COPY backend/requirements.txt backend/requirements.txt
RUN pip install --no-cache-dir -r backend/requirements.txt

# -------------------------
# 📁 Copy Project Code
# -------------------------
COPY backend ./backend
COPY frontend ./frontend

# -------------------------
# 🔧 Install Frontend Dependencies and Build
# -------------------------
WORKDIR /app/frontend
RUN npm install && npm run build

# -------------------------
# 🔄 Return to Root
# -------------------------
WORKDIR /app

# -------------------------
#  Copy Supervisor Config
# -------------------------
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

# -------------------------
# 📡 Expose Ports
# -------------------------
EXPOSE 8000 3000

# -------------------------
# 🚀 Start Backend + Frontend Together
# -------------------------
CMD ["/usr/bin/supervisord"]
