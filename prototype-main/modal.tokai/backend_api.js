const APP_CONFIG = require('./app-config');
const {
    DB_CONNECTION,
    API_KEYS,
    ENVIRONMENT_SETUP_VARS,
    CREDENTIAL_VARS,
    CLONE_VARS
} = require('./vars');

const User = require('./models/user');
const Clone = require('./models/clone');
const Payment = require('./models/payment');
const Environment = require('./models/environment');
const Credential = require('./models/credential');

const axios = require('axios');
const express = require('express');
const router = express.Router();

router.post('/startCloneTraining', function(req, res) {
    let cloneData = CLONE_VARS;
    // Code to start clone training here using cloneData
    res.status(200).json({message: 'CloneTrainingStarted'});
});

router.post('/connectToSocialMedia', function(req, res) {
    let socialMediaCredentials = CREDENTIAL_VARS.SOCIAL_MEDIA_CREDENTIALS;
    // Code to connect to social media platforms here using socialMediaCredentials
    res.status(200).json({message: 'SocialMediaConnected'});
});

router.post('/processPayment', function(req, res) {
    let paymentDetails = CREDENTIAL_VARS.PAYMENT_DETAILS;
    // Code to process payment here using paymentDetails
    res.status(200).json({message: 'PaymentProcessed'});
});

router.post('/setupEnvironment', function(req, res) {
    let environmentSetupDetails = ENVIRONMENT_SETUP_VARS;
    // Code to set up programming environment here using environmentSetupDetails
    res.status(200).json({message: 'EnvironmentSetup'});
});

router.post('/enterCredentials', function(req, res) {
    let credentials = CREDENTIAL_VARS;
    // Code to allow users to enter their credentials here using credentials
    res.status(200).json({message: 'CredentialsEntered'});
});

router.post('/submitSpecialRequest', function(req, res) {
    // Extract special request from req.body.specialRequest
    // Code to handle special request for future development here
    res.status(200).json({message: 'SpecialRequestSubmitted'});
});

module.exports = router;