var express = require('express');
var path = require('path');
var formidable = require('formidable');
app = express();

var port = process.env.PORT || 1729;

app.use(express.static(path.join(__dirname, '/')));

app.post("/", () => console.log("Redirect called. post on /"));

/*   https://www.npmjs.com/package/formidable#readme   */
app.post("/upload", function (req, res) {
    var form = new formidable.IncomingForm(), files = [], fields = [];
    //<name> is the value of 'name' attribute in HTML input tag
    form.on('fileBegin', function (name, file) {
        console.log(file.path + ' -> ' + __dirname + '/uploads/' + file.name + ' vs ' + name);
        file.path = __dirname + '/uploads/' + file.name;
    });
    form.on('file', function (name, file) {
        console.log('Uploaded ' + file.name + ' : ' + name);
    });
    form.on('field', function (name, value) {
        console.log("field encountered");
    });
    form.on('end', () => {
        res.statusCode = 303; // 307 will reinitiate a POST. 303/302 will do GET
        res.setHeader('Location', "/");
        res.end();
    });
    form.parse(req);
});
app.listen(port);


