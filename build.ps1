cd content_enum
cargo build --release

# najlepiej stworzyc wirtualne srodowisko pythona uzywajac komendy python -m venv venv
# a nastepnie aktywowac je komenda .\venv\Scripts\activate
# skrypt build.ps1 zaciaga zaleznosci pythona do aktywowanego srodowiska

cd ..
pip install -r requirements.txt