echo [$(date)]: "START"
echo [$(date)]: "add git user"
git config user.name "c17hawke"
git config user.email "sunny.c17hawke@gmail.com"
echo [$(date)]: "Creating conda env with python 3.10" # change py version as per your need
conda create --prefix ./env python=3.10 -y
echo [$(date)]: "activate env"
source activate ./env
echo [$(date)]: "installing the requirements" 
pip install -r requirements.txt
echo [$(date)]: "END" 
