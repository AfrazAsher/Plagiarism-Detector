# Plagiarism-Detector

## Getting Started

Install python 3.9.18
Install vs Code or any other text editor of your choose

#### Setting up a virtual environment

First, create a virtual environment to isolate your project dependencies:

```bash
python -m venv pd
```

#### Activating the virtual environment

Activate the virtual environment using the command below:

- On Windows:

  ```bash
  pd\Scripts\activate
  ```

- On MacOS/Linux:

  ```bash
  source pd/bin/activate
  ```

#### Installing dependencies

Install all the required libraries using the following command:

```bash
pip install -r requirements.txt
```

#### Go To plagiarism_detector

```
cd plagiarism_detector
```

#### Migrations

```
python manage.py makemigrations
```

```
python manage.py migrate
```

### Running the Application

Now you can run the application using:

```
python manage.py runserver
```
