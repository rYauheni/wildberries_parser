# WildberriesParser
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
   python main.py --ids_source <file_path>
   ```

   for Linux:

   ```commandline
   python3 main.py --ids_source <file_path>
   ```

3. Run tests
   ```commandline
   python -m unittest discover -s tests -p "test_*.py" -v
   ```