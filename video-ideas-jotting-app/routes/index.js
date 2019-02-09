var express = require('express');
var router = express.Router();

/* GET home page. */
router.get('/', function(req, res, next) {
    console.log("Coming to index");
    res.render('index', { title: 'VidIde' });
});

module.exports = router;
