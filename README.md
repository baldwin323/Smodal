# Python Flask modal.tokai

## Description

**Name**: modal.tokai Flask Application

**Description**: The modal.tokai application is a state-of-the-art Flask-based chatbot application delivering robust functionality and convenience to its users. It has an intuitive onboarding flow to guide new users. The application is architected based on sound software engineering principles including proper exception handling, data validation, rigorous testing, thorough documentation, progress tracking, separation of concerns, Flask's templating system, stringent security measures, custom error pages, caching, exhaustive logging system, and modularity. It now comes wrapped in a docker container which makes it easy to set up and use.

The UI of the application is intentionally designed with proper theming and responsiveness in mind. It adapts properly to different screen sizes, making it mobile-friendly. It features loading spinners to indicate processing requests. The application also prompts for user feedback periodically to continuously refine its capabilities.

It only requires internet connection and a browser to function effectively, and can be powered on with a single click similar to a web or mobile app.

## Deployment using Docker

The deployment of modal.tokai has been simplified with Docker. Provided you have Docker installed, starting up the service should be as simple as following the subsequent instructions.

### Getting Started

These instructions will help you get a copy of the project up and running on your local machine for development and testing purposes. 

### Prerequisites

Ensure you have the latest version of Docker installed on your machine. For installation guide check [here](https://docs.docker.com/install/)

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

4. After successful image build, initiate the application with:
    ```bash
    docker run -p 8000:8000 modal-tokai-image
    ```
The application will now be accessible at localhost:8000

## Deployment using TeamCity

To automate the deployment of modal.tokai, we can utilize our build configuration template for TeamCity. 
The template can also be found within 'deploy.py' script and is methodically sequenced to perform stages such as unstaged changes check, pulling the latest version of application code, building Angular app, committing and pushing changes, building docker image and running docker compose.

### Prerequisites

Ensure you have TeamCity installed on your machine.

You can set up this configuration in your TeamCity project and correctly map the repository and steps to be executed. Once correctly set up, TeamCity will trigger builds and optionally deployments based on your criteria.

## Executing Test Cases

<!--- Existing content should remain here --->

## User Support

For any issues or required assistance, refer to the Help section where you can find help documents, FAQs, and feedback forms. Should you need further assistance, please don't hesitate to contact us through the provided options.

Your opinion is important to us, so please feel free to provide your feedback through our forms. We believe in continuous improvement, and your input serves as the driving force behind it.

We encourage you to explore our comprehensive Help documents and FAQs before reaching out for support, as they often contain the answers to many common questions.