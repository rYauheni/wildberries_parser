# WildberriesParser

**WildberriesParser** is an application designed specifically for sellers on the popular trading platform Wildberries. It is a tool that helps track the emergence of new negative reviews on products and provides the ability to promptly respond to them. WildberriesParser is a reliable assistant in managing reputation and increasing customer satisfaction levels on the Wildberries platform.

### Project Goals:

Increasing customer satisfaction: Providing sellers with the ability to promptly respond to negative reviews helps improve the quality of service and products, thereby increasing customer satisfaction.
Brand reputation management: Thanks to prompt monitoring and response to negative reviews, sellers can maintain a positive reputation for their brand on the Wildberries platform.
Increasing conversion: Quick response to negative reviews helps prevent customer loss and increase sales conversion.

### Tasks Solved:

Tracking negative reviews: The application automatically scans reviews for a seller's products on the Wildberries platform and highlights negative reviews.
Seller notification: When a new negative review appears, the application instantly notifies the seller, providing information about it.
Reputation monitoring: The application provides statistics on the number of negative reviews, helping the seller assess the overall reputation of their brand on the platform.

### Key Features:

Automatic review tracking.
Filtering and highlighting of negative reviews.
Seller notification of new negative reviews.
Provision of brand reputation statistics and analytics.
___

## Technologies

[![Python](https://img.shields.io/badge/Python-3.12-%23FFD040?logo=python&logoColor=white&labelColor=%23376E9D)](https://www.python.org/downloads/release/python-3123/)

[![TelegramAPI](https://img.shields.io/badge/TelegramAPI-%23293133)](https://core.telegram.org/bots/api)
[![Requests](https://img.shields.io/badge/Requests-%23293133)](https://pypi.org/project/requests/)
[![UnitTest](https://img.shields.io/badge/UnitTest-%23293133)](https://docs.python.org/3/library/unittest.html)
[![JSON](https://img.shields.io/badge/JSON-%23293133)](https://www.json.org/json-en.html)


[![GitHub](https://img.shields.io/badge/GitHub-%23000000?logoColor=white&labelColor=%23293133&logo=github)](https://github.com/)

___

## Installation

Run the following commands to bootstrap your environment.

For Windows:

```commandline
git clone https://github.com/rYauheni/wildberries_parser.git

python -m venv venv
venv\Scripts\activate

pip install -r requirements.txt

copy .env.template .env

```

For Linux:

```commandline
git clone https://github.com/rYauheni/wildberries_parser.git

python3 -m venv venv
source venv/bin/activate

pip install -r requirements.txt

cp .env.template .env
```

___

## QuickStart

1. Determine the value of environment variables in the file `.env`

2. Run the app:

   for Windows:

   ```commandline
   python main.py --ids-file-path <file_path>
   ```

   for Linux:

   ```commandline
   python3 main.py --ids-file-path <file_path>
   ```

3. Run tests
   ```commandline
   python -m unittest discover -s tests -p "test_*.py" -v
   ```

 ___

## Contributing

Bug reports and/or pull requests are welcome
___

## License

The app is dedicated to the public domain under the CC0 license
___