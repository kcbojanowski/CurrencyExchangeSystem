# 💸Zielone Check - Currency Exchange System

Zielone Check is a web application that allows users to check the current currency charts, simulate currency exchange, and monitor their profit live. 
The application is built using Python and JavaScript, and utilizes the Frankfurt API for currency data and AmCharts for graphing.

## Authors
- [Kacper Bojanowski](https://github.com/kcbojanowski)
- [Mateusz Potaśnik](https://github.com/PotasnikM)
- [Bartosz Szymański](https://github.com/szymanskji)
## Features

- Check current currency charts from [Frankfurter API](https://www.frankfurter.app)
- Display currency graphs with [AmCharts](https://www.amcharts.com)
- Simulate currency exchange with your own profile
- Monitor your profit calculated live

## Installation
Clone this repository: 
``` bash
git clone https://github.com/your-username/ZieloneCheck
```
Change directory to the project directory:
``` bash
cd stronka
```
Create a virtual environment and activate it:
On Windows: 
``` bash
python -m venv venv
```
``` bash
venv\Scripts\activate
```
On macOS/Linux:
``` bash
python3 -m venv venv
```
``` bash
source venv/bin/activate
```
Install the required packages: 
``` bash
pip install -r requirements.txt
```
Set up the database by running 
``` bash
python create_db.py
```
Run the application: 
``` bash
python app.py
```

## Usage 
Once the application is running, open a web browser and navigate to http://localhost:5000 to access the application.

### - Currency Charts
The currency charts page displays the current exchange rates for a variety of currencies. The data is fetched from the Frankfurt API and updated every minute.

### - Currency Graph
The currency graph page displays a graph of historical exchange rates for two selected currencies. The graph is generated using AmCharts and allows the user to interact with the data.

### - Currency Exchange Simulation
The currency exchange simulation page allows the user to simulate buying and selling currencies with a virtual balance. The user can set their own exchange rates and monitor their profit in real-time.

## License
This project is licensed under the MIT License. See the LICENSE file for more information.
