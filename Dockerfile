FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
  build-essential \
  curl \
  git \
  && rm -rf /var/lib/apt/lists/*

# Install Freqtrade (minimal version - no ML/RL to save space)
# This installs only essential dependencies without PyTorch, TensorFlow, Jupyter
RUN pip install --no-cache-dir freqtrade && \
  freqtrade install-ui

# Copy project files  
COPY user_data /app/user_data

# Create data directory
RUN mkdir -p /app/user_data/data

# Expose port for FreqUI (optional)
EXPOSE 8080

# Set environment
ENV PYTHONUNBUFFERED=1

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD freqtrade show-config --config user_data/config.json || exit 1

# Run bot
CMD ["freqtrade", "trade", "--config", "user_data/config.json", "--strategy", "GridScalpingHybrid"]
