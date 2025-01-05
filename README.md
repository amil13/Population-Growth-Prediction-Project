
# Population Growth Project

**Author:** Amil Shrivastava

## Introduction

The **Population Growth Project** is a demonstration of data engineering, machine learning, and web application skills. It integrates multiple components to process and visualize population trends in Barcelona, including:

- **Data Cleaning**: Prepares raw CSV data from the Opendata of Ajuntament of Barcelona for analysis.
- **Backend Storage**: Stores the cleaned data in a Django backend using SQLite.
- **API Development**: Facilitates interaction between the frontend and backend via Django APIs.
- **Machine Learning**: Applies a linear regression model to predict population trends for the next three years.
- **Data Visualization**: Displays historical and predicted population data through a Streamlit-based frontend.

## Prerequisites

Before running the project, ensure the following tools are installed:

- **Docker**
- **Python 3.10 or above** - for running the Python-based Streamlit visualization tool.

## How to Run

1. Clone the repository to your local machine.
2. Navigate to the `Population Growth Project` directory.
3. Run the following command to start the project:

   ```bash
   python .\runit.py
   ```

## To Stop and Clean

To stop all services and clean up the containers, run:

```bash
docker-compose down
```
