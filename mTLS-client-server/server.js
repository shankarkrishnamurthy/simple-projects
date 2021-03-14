const https = require('https');
const fs = require('fs');

const hostname = 'localhost';
const port = 3000;

const options = { 
    ca: fs.readFileSync('ca.crt'), 
    cert: fs.readFileSync('server.crt'), 
    key: fs.readFileSync('server.key'), 
    rejectUnauthorized: true,
    requestCert: true, 
}; 

const server = https.createServer(options, (req, res) => {
  res.statusCode = 200;
  res.setHeader('Content-Type', 'text/plain');
  res.end('Hello World');
});

server.listen(port, hostname, () => {
  console.log(`Server running at http://${hostname}:${port}/`);
});
