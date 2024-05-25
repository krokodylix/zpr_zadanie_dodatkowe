#!/bin/bash

cd content_enum
cargo build --release

# najlepiej stworzyc wirtualne srodowisko pythona uzywajac komendy python3 -m venv venv
# a nastepnie aktywowac je komenda source venv/bin/activate
# skrypt build.sh zaciaga zaleznosci pythona do aktywowanego srodowiska

cd ..
pip install -r requirements.txt