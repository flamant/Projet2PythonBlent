#!/bin/bash

python utils_encoding.py
python models.py
python init_db.py
python users.py
python product.py
python app.py