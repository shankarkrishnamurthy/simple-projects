'use strict';

exports.usersGET = function(args, res, next) {
  /**
   * parameters expected in the args:
  **/
    var examples = {};
  examples['application/json'] = "";
  if(Object.keys(examples).length > 0) {
    res.setHeader('Content-Type', 'application/json');
    res.end(JSON.stringify(examples[Object.keys(examples)[0]] || {}, null, 2));
  }
  else {
    res.end();
  }
  
}

exports.usersPOST = function(args, res, next) {
  /**
   * parameters expected in the args:
  * user (User)
  **/
    var examples = {};
  examples['application/json'] = {
  "lastName" : "aeiou",
  "firstName" : "aeiou",
  "_id" : "aeiou",
  "email" : "aeiou"
};
  if(Object.keys(examples).length > 0) {
    res.setHeader('Content-Type', 'application/json');
    res.end(JSON.stringify(examples[Object.keys(examples)[0]] || {}, null, 2));
  }
  else {
    res.end();
  }
  
}

exports.usersUserIdDELETE = function(args, res, next) {
  /**
   * parameters expected in the args:
  * userId (String)
  **/
    var examples = {};
  examples['application/json'] = {
  "lastName" : "aeiou",
  "firstName" : "aeiou",
  "_id" : "aeiou",
  "email" : "aeiou"
};
  if(Object.keys(examples).length > 0) {
    res.setHeader('Content-Type', 'application/json');
    res.end(JSON.stringify(examples[Object.keys(examples)[0]] || {}, null, 2));
  }
  else {
    res.end();
  }
  
}

exports.usersUserIdGET = function(args, res, next) {
  /**
   * parameters expected in the args:
  * userId (String)
  **/
    var examples = {};
  examples['application/json'] = {
  "lastName" : "aeiou",
  "firstName" : "aeiou",
  "_id" : "aeiou",
  "email" : "aeiou"
};
  if(Object.keys(examples).length > 0) {
    res.setHeader('Content-Type', 'application/json');
    res.end(JSON.stringify(examples[Object.keys(examples)[0]] || {}, null, 2));
  }
  else {
    res.end();
  }
  
}

exports.usersUserIdPUT = function(args, res, next) {
  /**
   * parameters expected in the args:
  * userId (String)
  * user (User)
  **/
    var examples = {};
  examples['application/json'] = {
  "lastName" : "aeiou",
  "firstName" : "aeiou",
  "_id" : "aeiou",
  "email" : "aeiou"
};
  if(Object.keys(examples).length > 0) {
    res.setHeader('Content-Type', 'application/json');
    res.end(JSON.stringify(examples[Object.keys(examples)[0]] || {}, null, 2));
  }
  else {
    res.end();
  }
  
}

