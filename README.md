# CSV Parser application

## run server

python manage.py runserver

## Bundle frontend

cd frontend
npm run dev

## run docker

Build the container image.
$ docker build -t config .
Start your container
$ docker run -p 8000:8000 config

## clear pycache

Get-ChildItem -Path . -Recurse -Filter **pycache** | Remove-Item -Force -Recurse
Get-ChildItem -Path . -Recurse -Filter **.pyc** | Remove-Item -Force

## Possible improvements

create a general context for the app:

- When deleting or adding data to the database, it will automatically refresh the table
- Add a job that automatically fetch data using either

  - Automatically Fetching Data with Lambda Functions: In this approach, we will leverage AWS Lambda functions, which are serverless computing services provided by Amazon Web Services. With Lambda functions, we can create a scheduled job that periodically fetches data from a specified data source, such as an API or a database. We can configure the Lambda function to run at specific intervals using AWS CloudWatch Events. For example, we can schedule the Lambda function to fetch data every hour or daily.

  - Automatically Fetching Data with Apache Airflow: Apache Airflow is an open-source platform that allows us to create, schedule, and monitor workflows. Using Apache Airflow, we can design a data ingestion pipeline that automatically fetches data from the desired data source. Airflow provides a wide range of operators, including Python operators, to execute tasks. We can use Python operators to write the logic to fetch data and then schedule the workflow to run at defined intervals or on specific time-based schedules.

In both approaches, the fetched data can be processed further, stored in a database, analyzed, or used for other downstream tasks, depending on the specific use case and requirements of the application. The choice between using AWS Lambda functions or Apache Airflow depends on factors like existing infrastructure, preferences, scalability needs, and the complexity of the data ingestion process.

- Responsive Design: Ensure that the component displays and functions well on different screen sizes and devices.
- Code Refactoring: Break down the component into smaller, more manageable components for better code organization and reusability.
- Error Handling: Implement error handling for the API requests to provide a better user experience in case of network or server errors.
- Pagination or Infinite Scroll: Add pagination or implement an infinite scroll feature if the file list is large to improve performance and user experience.
- Sorting: Add the ability to sort the table columns based on various criteria (e.g., filename, size, creation date, etc.).
- Confirmation Modals: Use confirmation modals when performing actions like uploading data or deleting files to prevent accidental actions.
- Feedback and Loading States: Provide better loading and feedback states during API requests or time-consuming operations.
- Testing: Write unit tests for the component to ensure its correctness and prevent regressions in the future.
- Optimization: Optimize the API calls and data handling to improve the performance of the component.
- Error Messages: Display more descriptive error messages when encountering errors during data upload or deletion.
- Styling: Improve the overall visual styling and layout to enhance the user interface.
