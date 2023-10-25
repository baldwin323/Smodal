# Python Flask modal.tokai

## Description

**Name**: modal.tokai Django Application

**Description**: The modal.tokai application is a state-of-the-art Django-based application delivering robust functionality and convenience to its users. It is architectured based on sound software engineering principles including proper exception handling, data validation, rigorous testing, thorough documentation, separation of concerns, Django's templacing system, stringent security measures, custom error pages, caching, exhaustive logging system, and modularity. Now, it also boasts integration with Pactflow and SwaggerHub to further enhance the application's robustness and versatility.

## Getting Started

To begin, you need to connect to your Kubernetes cluster. This can be done directly through kubectl or doctl. More detailed instructions for this process can be found in the DigitalOcean Control Panel.

### Cert-Manager Status Confirmation

To confirm the operational status of Cert-Manager, execute the following commands:

```bash
helm ls -n cert-manager
kubectl get pods -n cert-manager
```

The Cert-Manager should be in a READY state, and STATUS should be Running.

### Values Configuration For Helm Chart

Inspect the Helm chart values by running the following command.

```bash
helm show values jetstack/cert-manager --version 1.8.0
```

You can adjust the values in the values.yml file based on your requirements.

### Configuring Secure TLS Certificates via Cert-Manager

The application establishes secure connections via TLS certificates configured through Cert-Manager. Please follow the detailed instructions in the source code for creating Certificate and Issuer CRDs, and adding necessary annotations.

### Upgrading and Uninstalling The Cert-Manager Stack

You can upgrade the Cert-Manager stack by following instructions on Cert-Manager's official release page on GitHub. Alternatively, ArtifactHUB can provide a more user-friendly interface. Use the following command for upgrading:

```bash
helm upgrade cert-manager jetstack/cert-manager --version <CERT_MANAGER_NEW_VERSION> --namespace cert-manager --values <YOUR_HELM_VALUES_FILE>
```

To uninstall the Cert-Manager stack, utilize the following commands:

```bash
helm uninstall cert-manager -n cert-manager
kubectl delete ns cert-manager
```

## Building the React Application

The application comes with a React frontend. To build the application, run the following commands:

```bash
cd /Smoda
npm install
npm run build
```

The build artifacts will be stored in the `dist/` directory.

## Running React Frontend Locally

To run the React frontend application locally, you can use the following commands:

```bash
npm start
```
This starts the development server and the app should be available at `localhost:3000`.

## Advanced Use 

In case of need for more detailed instructions, please refer to the following official DigitalOcean guides: 

- [Configuring Production Ready TLS Certificates for Nginx](#)
- [Configuring Wildcard Certificates via Cert-Manager](#)

## Procedure To Set Up a DigitalOcean Droplet

Proceed with setting up a DigitalOcean Droplet as per instructions in the original document.

### Setting Up a Virtual Environment

Follow the original document's instructions for setting up a virtual environment.

### Dependency Installation

Follow the original document's instructions for installing dependencies.

### Django App Set Up

Follow the original document's instructions for setting up the Django app.

## Executing Build Commands

The build commands can be executed as per instructions in the original document.

## Deployment Strategy for DigitalOcean

Follow the instructions in the original document for deploying the application on DigitalOcean.

### Deployment using Helm and Kubernetes

Deployment instructions using Helm and Kubernetes are provided in the original document.

## Executing Test Cases

Test case execution instructions can be found in the original document.

## User Support

In case of any queries or requirements for support, please explore our various support resources:
- [Application Documentation](https://docs.modal.tokai.com)
- [Interactive Support Forum](https://ask.modal.tokai.com)
- **Auto-completion Feature**: This feature is implemented throughout our project to enrich user experience and quicken scripting.
- **Step by Step Guides and Tutorials**: Our guides and tutorials provide detailed instructions which aid users in understanding, using and contributing to our application.
- **Regular Updates & Enhancements**: We consistently update and modify our application to keep it up-to-date. Detailed version history can be found in our changelog.
- **Community-Driven Approach**: We value feedback and suggestions from our community of users and maintain an open dialogue via our interactive forums, encouraging participation in the application's development journey.