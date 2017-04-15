# Simple note

## Installation

```bash
pip install Flask qiniu
pip install -r requirements.txt
# Copy your production config file
cp config/development.py config/production.py
python ./manage.py install
python ./manage.py runserver -h 127.0.0.1 -p 4096
```
