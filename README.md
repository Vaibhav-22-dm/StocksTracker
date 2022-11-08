# StocksTracker

## About the Project
This is a django app made for an assignment of an internship selection process.
In this django app I have created a StocksTracker where multiple users can login and create their own custom watchlists of stocks.

## Installation 

To install the following app on your local system follow the steps given below:

- Install Python 3.10.7
- Install virtualenv
- Create a folder by whatever name your want to give. Example: Valkyrie Drones
- Open the Valkyrie Drones folder in VS Code. Open the terminal.
- Create a virtual environment: 
    ```
    virtualenv myenv
    ```
- Switch to the newly created environment:
    ```
    cd myenv/Scripts
    ```
    ```
    ./activate
    ```
- Return Back to the parent directory:
    ```
    cd ../../
    ```
- Clone the repository:
    ```
    git clone https://github.com/Vaibhav-22-dm/StocksTracker.git
    ```
- Change directory to newly cloned repository:
    ```
    cd Valkyrie Drones
    ```
- Build the environment using the given requirements:
    ```
    pip install -r requirements.txt
    ```

- Start the django server:
    ```
    python manage.py runserver
    ```

- Visit the folloing link - 
    ```
    http://127.0.0.1:8000/tracker/signup/
    ```

- Create an Account
- Click on Sign In on navbar
- Enter the credentials and login
- Click on watchlists on navbar
- Click on create to create watchlist
- Fill up the form and press Create
- To add stocks to your watchlist, visit the dashboard and and click on add button and then fill up the form.
