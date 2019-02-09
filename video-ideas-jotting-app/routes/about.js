var express = require('express');
var route = express.Router();

/* GET users listing. Dont put 'already mentioned app.use route again' */
route.get('/', function(req, res, next) {
    //res.send('respond with a resource');
    console.log('respond about');
    res.render('about');
});

module.exports = route;
