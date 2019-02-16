Author: Shankar, K (Feb 2019)
Description:
	A barebones javascript/nodejs/express app which authenticates with google using oauth20 client. scaffolded using 'express' generator. 
	- google-oauth20 barebones
	- no dependency on any database
	- check the 'google-oauth20-passportjs' project (shankar.krishna a/c)
	- oauth20 client based on google+ api library
	- web client configured with:
		- 'authorized javascript origins' : http://localhost:3000
		- 'Authorized redirect URIs' : http://localhost:3000/auth/google/callback

	- Routes supported:
		- http://localhost:3000/
		- http://localhost:3000/auth/google           
		- http://localhost:3000/auth/google/callback
		- http://localhost:3000/auth/verify
		- http://localhost:3000/auth/dashboard
		- http://localhost:3000/auth/logout

	- output in strategy callback of config/passport.js:
		- accessToken:
ya29.GluyBmtqURyqsfo7XFTUCUiXhOduyt0ibxnvuIloLh8sEEfk2mUM3YOga2zp1SGKSkAeODSPEVwwKBQ_KPEwPYIoPqfARvAHxEcA9hDsR9L89uncCClleU0wV3aW
		- profile:
{ id: '113169452484557206839',
  displayName: 'shankar krishna',
  name: { familyName: 'krishna', givenName: 'shankar' },
  emails: [ { value: 'kshan_77@yahoo.com', type: 'account' } ],
  photos:
   [ { value:
        'https://lh4.googleusercontent.com/-pvSk5Ou8oeg/AAAAAAAAAAI/AAAAAAAAAAA/ACevoQNH01c8MPlGK7aV-hrHm2njXxHOPg/mo/photo.jpg?sz=50' } ],
  gender: undefined,
  provider: 'google',
  _raw:
   '{\n "kind": "plus#person",\n "etag": "\\"k-5ZH5-QJvSewqvyYHTE9ETORZg/dSw6UTqjqxaGOrgWZw2-59TrtW8\\"",\n "emails": [\n  {\n   "value": "kshan_77@yahoo.com",\n   "type": "account"\n  }\n ],\n "objectType": "person",\n "id": "113169452484557206839",\n "displayName": "shankar krishna",\n "name": {\n  "familyName": "krishna",\n  "givenName": "shankar"\n },\n "image": {\n  "url": "https://lh4.googleusercontent.com/-pvSk5Ou8oeg/AAAAAAAAAAI/AAAAAAAAAAA/ACevoQNH01c8MPlGK7aV-hrHm2njXxHOPg/mo/photo.jpg?sz=50",\n  "isDefault": true\n },\n "isPlusUser": false,\n "language": "en",\n "verified": false\n}\n',
  _json:
   { kind: 'plus#person',
     etag: '"k-5ZH5-QJvSewqvyYHTE9ETORZg/dSw6UTqjqxaGOrgWZw2-59TrtW8"',
     emails: [ [Object] ],
     objectType: 'person',
     id: '113169452484557206839',
     displayName: 'shankar krishna',
     name: { familyName: 'krishna', givenName: 'shankar' },
     image:
      { url:
         'https://lh4.googleusercontent.com/-pvSk5Ou8oeg/AAAAAAAAAAI/AAAAAAAAAAA/ACevoQNH01c8MPlGK7aV-hrHm2njXxHOPg/mo/photo.jpg?sz=50',
        isDefault: true },
     isPlusUser: false,
     language: 'en',
     verified: false } }
	- 

