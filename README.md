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

## 新版

基于 Flask 开发的一个基于网页的 WYSIWYG(所见即所得) 富文本编辑器应用 [wtdf.io](https://wtdf.io/)
