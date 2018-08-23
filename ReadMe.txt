****************************
	 Brew Ireland 2018
		CraftMaps
 UCD Capstone Project Setup
****************************

- Requirements
-- Anaconda: https://anaconda.org/anaconda/python
-- PyCharm: https://www.jetbrains.com/pycharm/download/#section=windows
-- MySQL Workbench: https://dev.mysql.com/downloads/workbench/


Step 1:
Install Anaconda, PyCharm & MySQL


Step 2:
Run PyCharm and download git plug-in


Step 3:
Run Anaconda prompt and download Django


Step 4:
Using Anaconda prompt again, create a Django project in your C:/ drive and name it CraftMaps


Step 5:
In MySQL Workbench, create a database and name it craftmapsdb


Step 6:
-6A:
Using the PyCharm, open the django project C:/CraftMaps and load it into the environment 

-6B:
Using the git plug-in, link the CraftMaps git account and pull the project into PyCharm


Step 7:
use the requirements.txt file to download the required libraries into the 


Step 8:
Using the Anaconda prompt, run the following commands:
-7A: Activate CraftMaps
-7B: python manage.py makemigrations
-7C: python manage.py migrate


Step 9:
Copy the python notebook files located in the C:/CraftMaps/Data_Workload folder
into your local user directory or somewhere you can located the files in the 
Jupyter framework.

Step 10:
-A: make sure your database is running
-B: Using Jupyter notebook, run both Data_Entry notebooks and let them finish running


Step 11:
Using anaconda prompt once again, run the following command: python manage.py runserver
- make sure that you still have your CraftMaps project active.


Step 12:
Open your favourite web browser (Explorer, Chrome etc...) and enter into the search "localhost:8000"
- you should see the project running.
