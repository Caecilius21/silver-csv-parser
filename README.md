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

### Code wise

- Unit Testing: Add ;ore comprehensive unit tests to cover all the components, models, and views of the application. Test for different scenarios, edge cases, and error handling to ensure the application's stability.

- Validation and Error Handling: Implement proper validation for incoming data from CSV files and S3. Handle potential errors gracefully and provide meaningful error messages to users.

### Design wide

- When deleting or adding data to the database, it will automatically refresh the table
- Frontend Enhancements: Improve the frontend's design and user interface to make it more user-friendly and intuitive. Improve the overall visual styling and layout to enhance the user interface.

- Sorting: Add the ability to sort the table columns based on various criteria (e.g., filename, size, creation date, etc.).

### Functionality wise

- Add a job that automatically fetch data using either

  - Automatically Fetching Data with Lambda Functions: In this approach, we will leverage AWS Lambda functions, which are serverless computing services provided by Amazon Web Services. With Lambda functions, we can create a scheduled job that periodically fetches data from a specified data source, such as an API or a database. We can configure the Lambda function to run at specific intervals using AWS CloudWatch Events. For example, we can schedule the Lambda function to fetch data every hour or daily.

  - Automatically Fetching Data with Apache Airflow: Apache Airflow is an open-source platform that allows us to create, schedule, and monitor workflows. Using Apache Airflow, we can design a data ingestion pipeline that automatically fetches data from the desired data source. Airflow provides a wide range of operators, including Python operators, to execute tasks. We can use Python operators to write the logic to fetch data and then schedule the workflow to run at defined intervals or on specific time-based schedules.

In both approaches, the fetched data can be processed further, stored in a database, analyzed, or used for other downstream tasks, depending on the specific use case and requirements of the application. The choice between using AWS Lambda functions or Apache Airflow depends on factors like existing infrastructure, preferences, scalability needs, and the complexity of the data ingestion process.

- Feedback on Ingestion Status: Provide real-time feedback to the user during CSV data ingestion, showing the progress and status of each file ingestion.

### Infrastructure wise

- Frontend: Host the built static files on AWS S3, which provides scalable and cost-effective storage for static content.
  Enable S3 bucket public access and configure a content delivery network (CDN) like Amazon CloudFront for faster content delivery.

- Backend: Use AWS Elastic Container Registry (ECR) to store Docker container images securely.
  Deploy the backend application using AWS Elastic Container Service (ECS) or AWS Elastic Kubernetes Service (EKS) for container orchestration.

- Database: Use Amazon RDS (Relational Database Service) to set up a managed PostgreSQL database for data storage.
  Configure the database instance, including backups, scaling options, and security settings.

- File Storage: Utilize AWS S3 to store CSV files uploaded by users securely (DONE)

- Task Execution: For long-running tasks like CSV data ingestion, use AWS Lambda to execute the tasks asynchronously in a serverless environment.
  Implement AWS Step Functions to orchestrate the ingestion process and handle errors gracefully.

- Monitoring and Logging: Enable AWS CloudWatch for monitoring and logging application performance metrics and logs.
  Configure alarms and notifications to receive alerts for critical events.

### Explaining technical choices:

Django (Backend):

- Robust and Scalable Backend: Django is a powerful and well-established Python web framework, known for its scalability and robustness. It provides a solid foundation for building complex applications.
- Built-in ORM and Admin Interface: Django's Object-Relational Mapping (ORM) simplifies database interactions, allowing you to focus on business logic. The built-in admin interface makes it easy to manage database records during development.
- Rich Ecosystem: Django has a large and active community, which means you can find plenty of resources, libraries, and packages to extend functionality and solve common challenges.
- Security Features: Django comes with built-in security features, such as protection against common web vulnerabilities like CSRF and SQL injection.

React (Frontend):

- Component-Based UI Development: React's component-based architecture allows for the creation of reusable UI components, leading to a more modular and maintainable codebase.
- Virtual DOM and Performance: React's Virtual DOM efficiently updates only the necessary parts of the actual DOM, improving performance and reducing rendering overhead.
- State Management: React's state management, combined with tools like Redux or React Context, makes it easier to manage application state and data flow, especially in large applications.
- Rich Ecosystem: React has a vast ecosystem of libraries and tools, including state management solutions, UI component libraries, and development tools, making it easier to build feature-rich and visually appealing UIs.
