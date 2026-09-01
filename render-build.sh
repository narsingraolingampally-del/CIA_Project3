#!/usr/bin/env bash
set -o errexit

echo "========================================"
echo "Installing Microsoft ODBC Driver 18"
echo "========================================"

# Install Microsoft repository package
curl -sSL -O https://packages.microsoft.com/config/debian/$(grep VERSION_ID /etc/os-release | cut -d '"' -f 2 | cut -d '.' -f 1)/packages-microsoft-prod.deb

dpkg -i packages-microsoft-prod.deb

rm packages-microsoft-prod.deb

# Update package lists
apt-get update

# Install Microsoft ODBC Driver 18
ACCEPT_EULA=Y apt-get install -y msodbcsql18

# Install unixODBC development libraries
apt-get install -y unixodbc-dev

echo "========================================"
echo "Checking installed ODBC drivers"
echo "========================================"

odbcinst -q -d

echo "========================================"
echo "Installing Python dependencies"
echo "========================================"

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