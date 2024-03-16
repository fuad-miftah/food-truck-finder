# Food Truck Finder

Food Truck Finder is a Django web application that helps users find the closest food trucks based on their location and preferences.

## Table of Contents

- [Features](#features)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
- [Usage](#usage)
- [Why Use Euclidean Distance](#WhyUseEuclideanDistance)
- [Why Use CSV Directly](#WhyUseCSVDirectly)

## Features

- Search: Users can search for food trucks based on their current location, facility type, and food items.
- Distance Calculation: The application calculates the distance between the user's location and each food truck using the Euclidean distance algorithm.
- Results: Displays a list of the closest food trucks along with their details such as address, facility type, and food items.

## Getting Started

### Prerequisites

Make sure you have the following installed:

- [Python](https://www.python.org/downloads)
- Django: Install Django using pip:

```
pip install Django
```

### Installation

1. Clone the repository:

```
git clone https://github.com/fuad-miftah/food-truck-finder.git
```

2. Install the required dependencies:

```
pip install -r requirements.txt
```

3. Start the Django development server:

```
python manage.py runserver
```

4. Access the application in your browser at http://localhost:8000/.

## Usage

1. Open the application in your browser.

2. Fill out the form with your location details and any additional filters (facility type, food items).

3. Submit the form to see a list of the closest food trucks based on your input.

## WhyUseEuclideanDistance

In this application, Euclidean distance algorithm is used to calculate distances between locations within one city. This decision was made because:

Simplicity: The Euclidean distance algorithm is easy to understand and implement, making it suitable for this project's scope.

Applicability: Since the project focuses on finding food trucks within a city, the curvature of the Earth can be ignored for short distances, making the Euclidean distance a practical choice.

Efficiency: For small-scale applications like this one, the computational efficiency of the Euclidean distance algorithm is sufficient, and the overhead of using more complex algorithms is unnecessary.

## WhyUseCSVDirectly

In this application, we directly read from the CSV file (food-truck-data.csv) to store and retrieve food truck information instead of saving it to a database. This approach was chosen because:

Simplicity: Using a CSV file simplifies the setup and maintenance of the application, as there is no need to manage a database system.

Ease of Access: For small-scale applications like this one, directly reading from a CSV file is more straightforward and efficient than setting up and managing a database.

Data Integrity: Since the data is static and doesn't require frequent updates, storing it in a CSV file is a practical choice.
