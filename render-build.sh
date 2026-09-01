```bash
#!/usr/bin/env bash
set -e

echo "========================================"
echo "Installing system dependencies"
echo "========================================"

apt-get update

apt-get install -y \
    curl \
    gnupg \
    unixodbc \
    unixodbc-dev

echo "========================================"
echo "Installing Microsoft ODBC Driver 18"
echo "========================================"

# Add Microsoft package repository
curl -sSL https://packages.microsoft.com/keys/microsoft.asc \
    | gpg --dearmor \
    > /usr/share/keyrings/microsoft-prod.gpg

echo "deb [arch=amd64 signed-by=/usr/share/keyrings/microsoft-prod.gpg] https://packages.microsoft.com/debian/12/prod bookworm main" \
    > /etc/apt/sources.list.d/mssql-release.list

apt-get update

# Install Microsoft ODBC Driver 18
ACCEPT_EULA=Y apt-get install -y msodbcsql18

echo "========================================"
echo "Checking ODBC drivers"
echo "========================================"

odbcinst -q -d

echo "========================================"
echo "Installing Python dependencies"
echo "========================================"

pip install --upgrade pip
pip install -r requirements.txt

echo "========================================"
echo "Collecting static files"
echo "========================================"

python manage.py collectstatic --noinput

echo "========================================"
echo "Running migrations"
echo "========================================"

python manage.py migrate

echo "========================================"
echo "BUILD COMPLETE"
echo "========================================"
```
