# /Documents/portfolio/Dockerfile

# 1. Base Image and Working Directory 
FROM python:3.12
WORKDIR /app

# Set the HOME environment variable to the working directory.
# This is for Reflex/Python modules running as non-root (user 1000)
# to correctly place cache and config files inside the writable volume mount.
ENV HOME /app
RUN apt-get update && apt-get install -y bash && rm -rf /var/lib/apt/lists/*
# --- Layer 1: Dependencies (for caching) ---
# Copy ONLY the requirements file
COPY requirements.txt .
# Install dependencies. This layer is cached well.
RUN pip install -r requirements.txt

# --- Layer 2: Application Code ---
# Copy ALL other files from your local project directory into the container's /app
# The '.' is essential here, meaning copy everything from the build context.
COPY . .

# 2. Expose Ports and Command 
EXPOSE 3000
EXPOSE 8000
CMD ["reflex", "run"]