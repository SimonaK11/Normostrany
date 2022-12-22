# WEB TOOL FOR ESTIMATION OF DOCUMENT SIZE

This project is written in the Django framework. It contains tool that analyzes thesis in PDF file in order to get statictics about its size. Those statistics are about text, images and chapters.

## How to run the project locally

Install **python** and **pip**. Then in command line install **virtualenvwrapper** for the virtual enviroment (example for Windows):
```
pip install virtualenvwrapper-win
```
Create the virtual enviroment or switch to the created enviroment:
```
mkvirtualenv thesistool
```
```
workon thesistool
```
Go to the project folder. Dependencies of this project are in the *requirements.txt* file and can be installed in the virtual enviroment where the application runs.
```
pip install -r requirements.txt
```
Now run the server:
```
python manage.py runserver
```
The application is going to run on the localhost. The tool is on the /standardpages endpoint.

## Deployment

The server settings is located in the *Procfile*. Version of Python runtime version is in *runtime.txt* file. Dependencies of this project are in the *requirements.txt* file.

## Author

* **Simona Kuželová (Dlouhá)** - (xdlouh06@vutbr.cz)
