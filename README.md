# Python Flask modal.tokai

## Description

**Name**: modal.tokai Flask Application

**Description**: The modal.tokai application is a state-of-the-art Flask-based chatbot application delivering robust functionality and convenience to its users. It has an intuitive onboarding flow to guide new users. The application is architected based on sound software engineering principles including proper exception handling, data validation, rigorous testing, thorough documentation, progress tracking, separation of concerns, Flask's templating system, stringent security measures, custom error pages, caching, exhaustive logging system, and modularity. It now comes wrapped in a docker container which makes it easy to set up and use.

## New Updates

Ensure your Python version is updated to Python3.12 and Angular to 17, as the app now requires these updated versions. 

The UI of the application is intentionally designed with proper theming and responsiveness in mind. It adapts properly to different screen sizes, making it mobile-friendly. It features loading spinners to indicate processing requests. The application also prompts for user feedback periodically to continuously refine its capabilities.

It only requires internet connection and a browser to function effectively, and can be powered on with a single click similar to a web or mobile app.

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

To deploy modal.tokai on Kinsta, follow these instructions:

1. Navigate to your Kinsta Dashboard.
2. Select the 'Sites' option from the left-hand menu and choose 'Add Site'.
3. Input the desired settings and click 'Add Site'.
4. Now under the 'Sites' menu, select your site, and click on the 'Info' tab.
5. Under the 'SFTP/SSH' section, you can find your SSH/SFTP details. Use this info to enable Git and SSH on your Kinsta site.
6. Log in to your Kinsta site via SSH and clone your Git repository.
7. After successful repository cloning, navigate to your site's root directory (/www/your_site/public), and setup the .env file with your environment variables.
8. Finally, you can deploy the application using the init script.

Ensure the code is clean and all functions and classes have appropriate comments documenting their behavior. Keep track of all environment variables and make sure they are correctly loaded in all instances.


### Kinsta Start Commands
To start the modal.tokai application on Kinsta use the command:

```
gunicorn app:app
```

This command starts the Gunicorn server with app:app being the location of the python WSGI application.

### Kinsta Environmental Variables
Sensitive information such as configurations, secret keys, passwords are stored as environmental variables on Kinsta. These variables can be accessed through the following location:

```
/etc/profile.d/kinsta_prompt.sh
```

## Executing Test Cases

<!--- Existing content should remain here --->

## User Support

For any issues or required assistance, refer to the Help section where you can find help documents, FAQs, and feedback forms. Should you need further assistance, please don't hesitate to contact us through the provided options.

Your opinion is important to us, so please feel free to provide your feedback through our forms. We believe in continuous improvement, and your input serves as the driving force behind it.

We encourage you to explore our comprehensive Help documents and FAQs before reaching out for support, as they often contain the answers to many common questions.

## Angular 17 Setup and Deployment

## Prerequisites

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
This part of setting up Angular 17 application and nginx server is important for making the codebase fully useable for further deployment.