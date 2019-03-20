## Setup to run the code

The Project uses python 3.6. It is best practice to use a clean python version by using a virtual enviroment.
In order to install the needed libraries, I recommend also install pip

### Install pip and virtualenv
1. Installing pip:
``` $ sudo apt-get install python-pip ```
2. Install virtualenv: 
``` $ pip install virtualenv ```

#### 2. Create and initialize virtualenv for the project:
1. cd into the project folder and create a virtualenviroment called venv:
``` $ virtualenv venv ```
2. acitivate virtualenv running:
``` $ source venv/bin/activate ```
3. set python intepreter to python 3.6
``` $ virtualenv -p /usr/bin/python3.6 venv ```
    
#### 3. Install python packages using requirements.txt
``` $ pip install -r requirements.txt ```

#### 4. Install jupyter notebook 
1. Install iPython kernel
``` $ pip install ipykernel ```
2. activate kernel on venv
``` $ ipython kernel install --user --name=venv ```
