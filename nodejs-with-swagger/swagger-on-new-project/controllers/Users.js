'use strict';

var url = require('url');


var Users = require('./UsersService');


module.exports.usersGET = function usersGET (req, res, next) {
  Users.usersGET(req.swagger.params, res, next);
};

module.exports.usersPOST = function usersPOST (req, res, next) {
  Users.usersPOST(req.swagger.params, res, next);
};

module.exports.usersUserIdDELETE = function usersUserIdDELETE (req, res, next) {
  Users.usersUserIdDELETE(req.swagger.params, res, next);
};

module.exports.usersUserIdGET = function usersUserIdGET (req, res, next) {
  Users.usersUserIdGET(req.swagger.params, res, next);
};

module.exports.usersUserIdPUT = function usersUserIdPUT (req, res, next) {
  Users.usersUserIdPUT(req.swagger.params, res, next);
};
