FROM python:3.12-slim-bookworm

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Install system packages required for SQL Server
RUN apt-get update && apt-get install -y \
    curl \
    gnupg \
    apt-transport-https \
    unixodbc \
    unixodbc-dev \
    && rm -rf /var/lib/apt/lists/*

# Add Microsoft package repository
RUN curl -sSL https://packages.microsoft.com/keys/microsoft.asc \
    | gpg --dearmor \
    > /usr/share/keyrings/microsoft-prod.gpg

RUN echo "deb [arch=amd64 signed-by=/usr/share/keyrings/microsoft-prod.gpg] https://packages.microsoft.com/debian/12/prod bookworm main" \
    > /etc/apt/sources.list.d/mssql-release.list

# Install Microsoft ODBC Driver 18
RUN apt-get update && \
    ACCEPT_EULA=Y apt-get install -y msodbcsql18 && \
    rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy Django project
COPY . .

# Collect static files
RUN python manage.py collectstatic --noinput

# Verify SQL Server ODBC driver
RUN odbcinst -q -d

EXPOSE 10000

CMD gunicorn core.wsgi:application --bind 0.0.0.0:10000
