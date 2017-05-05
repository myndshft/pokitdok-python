alias python=/usr/local/bin/pypy
curl -SL 'https://bootstrap.pypa.io/get-pip.py' | pypy
pip install --upgrade pip
cd /app/pokitdok/
python setup.py develop
python setup.py test
