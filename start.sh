export PORT=5000
unset PIP_USER

if [ ! -d "venv" ]; then
  echo "Creating virtual environment..."
  python3 -m venv venv --system-site-packages
fi

source venv/bin/activate

if [ -f "requirements.txt" ]; then
  echo "Checks..."
  pip instlal -r requirements.txt || echo "Failed instakk requirements.txt"
fi

echo "Starting application"
python main.py
