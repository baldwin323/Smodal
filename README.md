# Python Flask modal.tokai

## Description

**Name**: modal.tokai Flask Application

**Description**: The modal.tokai application is a state-of-the-art Flask-based chatbot application delivering robust functionality and convenience to its users. It has an intuitive onboarding flow to guide new users. The application is architected based on sound software engineering principles including proper exception handling, data validation, rigorous testing, thorough documentation, progress tracking, separation of concerns, Flask's templating system, stringent security measures, custom error pages, caching, exhaustive logging system, and modularity. It now comes wrapped in a docker container which makes it easy to set up and use.

## Updates

The application has been updated to start the frontend from the 'prototype-main' directory. Please note that the Procfile for the app is now included in the 'prototype-main' directory. 

Ensure your Python version is updated to Python3.12 and Angular to 17, as the app now requires these updated versions. 

The UI of the application is intentionally designed with proper theming and responsiveness in mind. It adapts properly to different screen sizes, making it mobile-friendly. It features loading spinners to indicate processing requests. The application also prompts for user feedback periodically to continuously refine its capabilities.

### Deployment using Docker

The deployment of modal.tokai has been simplified with Docker. Provided you have Docker installed, starting up the service should be as simple as following the subsequent instructions.

### Getting Started

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

3. Navigate to the 'prototype-main' directory. This is where the script to start the frontend and the Procfile are located:
    ```bash
    cd prototype-main
    ```

4. Build the Docker image with the following command:
    ```bash
    docker build -t modal-tokai-image .
    ```

5. After successful image build, initiate the Docker Compose with:
    ```bash
    docker-compose up
    ```

The application will now be accessible at localhost:8000

<!--- Rest of original content remains here --->