# Python Flask modal.tokai

## Description

**Name**: modal.tokai Flask Application

**Description**: The modal.tokai application is a state-of-the-art Flask-based chatbot application delivering robust functionality and convenience to its users. It has an intuitive onboarding flow to guide new users. The application is architected based on sound software engineering principles including proper exception handling, data validation, rigorous testing, thorough documentation, progress tracking, separation of concerns, Flask's templating system, stringent security measures, custom error pages, caching, exhaustive logging system, and modularity. 

## New Updates

As part of our continued commitment to improve and evolve the modal.tokai application, significant updates have been made. Notably, the application now runs on Angular 17, which means that all frontend functionalities have been augmented to augment usability and accessibility.

Ensure your Python version is updated to Python3.12 and Angular to 17, as the app now requires these updated versions.  

The UI has been enhanced significantly with great attention to details. All components of prototype-main have been built out in line with a user-friendly design philosophy. The application adapts properly to different screen sizes, making it versatile and mobile-friendly. It also features improved page navigation, better state management, and optimized data fetch operations. 

An upgrade to Angular 17 also brings in align with modern trends and practices in web development, which will consequently enhance developer experiences in the continuance of the project.

## Deployment using Docker

The deployment of modal.tokai has been simplified with Docker. Provided you have Docker installed, starting up the service should be as simple as following the subsequent instructions.

### Getting Started

These instructions will help you get a copy of the project up and running on your local machine for development and testing purposes. 

### Prerequisites

Ensure you have the latest version of Docker and Docker-compose installed on your machine. For installation guide check [here](https://docs.docker.com/install/)

### Installation

1. Clone this repository using `git`:
    ```bash
    git clone https://github.com/<username>/modal.tokai
    ```

2. Navigate to the repository's directory:
    ```bash
    cd modal.tokai
    ```

3. Build the Docker image with the following command:
    ```bash
    docker build -t modal-tokai-image .
    ```

4. After successful image build, initiate the Docker Compose with:
    ```bash
    docker-compose up
    ```

The application will now be accessible at localhost:8000  

## Deployment on Kinsta

<!-- Same content for deployment -->

## Executing Test Cases

<!--- Existing content should remain here --->

## User Support

<!-- Same content for User Support -->

## Angular 17 Setup and Deployment

### Prerequisites

Ensure you have the latest version of Node.js and npm installed on your machine. For installation guide check [here](https://nodejs.org/en/download/)

### Installation

1. To build the Angular 17 application, navigate to the root directory and install dependencies with:

    ```bash
    npm install
    ```

2. Build the Angular app with the following command:

    ```bash
    ng build --prod
    ```

3. The built files will be available under `dist/`. These are the files to be deployed on the server.

## nginx setup and configuration

1. Install nginx on your machine. For installation guide check [here](https://nginx.org/en/docs/install.html)

2. Modify the nginx configuration file located at `/etc/nginx/nginx.conf` and add the following:

    ```
    server {
        listen 80;
        server_name localhost;
        
        location / {
            root /path/to/your/angular/dist;
            try_files $uri $uri/ /index.html;
        }

        # other configurations...
    }
    ```
  
3. Restart the nginx server:

    ```bash
    service nginx restart
    ```

This part of setting up Angular 17 application and nginx server is important for making the codebase fully usable for further deployment.