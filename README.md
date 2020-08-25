## uhmalguhm
 uh *mal* guhm

 The purpose of this project is to provide a easy to use interface to spin up virtual machines that use docker images as an overlay to the root filesystem.

 Essentially uhmalguhm will build an image that is very fast to boot up that is capable of consuming a Dockerfile.

 ### How to use this software
```
git clone https://github.com/fortnebula/uhmalguhm.git
cd uhmalguhm
pipenv shell
pip install -r requirements.txt
python3 main.py
```
### Where to find the documentation

Currently there are no docs, however a system for documentation is in-flight. This README serves as the documentation for usage.

### Register a user
To use the api, first a user needs to be created

```
curl -H "Content-Type: application/json" -X POST   -d '{"username":"test","password":"test"}' http://localhost:5000/register
```

A successful registration should return

```
{
    "status": "registered",
    "username": "test"
}
```

### Obtain an access and refresh token

Now that you have a user, you can request an access token using the token endpoint

```
curl -H "Content-Type: application/json" -X POST   -d '{"username":"test","password":"test"}' http://localhost:5000/token
```

This will return an access token and a refresh token

```
{
    "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE1OTgzNTU5MDIsIm5iZiI6MTU5ODM1NTkwMiwianRpIjoiZjNjODVkOTUtMzQ1Mi00MDM4LThhMmYtNDQzMjdmMDZkYjAzIiwiZXhwIjoxNTk4MzU2ODAyLCJpZGVudGl0eSI6InRlc3QxIiwiZnJlc2giOmZhbHNlLCJ0eXBlIjoiYWNjZXNzIn0.J2if1aJ5qWzLZHs389IpyA04qBZXlDGLF7W9G98wVt8",
    "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE1OTgzNTU5MDIsIm5iZiI6MTU5ODM1NTkwMiwianRpIjoiOWExYzBiMDMtZGZmZi00N2NlLWJhZmUtODE1M2U2NWM0NWMxIiwiZXhwIjoxNjAwOTQ3OTAyLCJpZGVudGl0eSI6InRlc3QxIiwidHlwZSI6InJlZnJlc2gifQ.LcfWa0xheY6r1T9x6z66Ho7wk2qSm2LdDXMTFGyJZKs"

```

### Refresh a token

If the access token expires, the refresh token method will issue a new access token

First export the refresh token to a variable so it's easier to work with

```
export REFRESH="eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE1OTgzNTU5MDIsIm5iZiI6MTU5ODM1NTkwMiwianRpIjoiOWExYzBiMDMtZGZmZi00N2NlLWJhZmUtODE1M2U2NWM0NWMxIiwiZXhwIjoxNjAwOTQ3OTAyLCJpZGVudGl0eSI6InRlc3QxIiwidHlwZSI6InJlZnJlc2gifQ.LcfWa0xheY6r1T9x6z66Ho7wk2qSm2LdDXMTFGyJZKs"
```

You can now use this refresh token to obtain a new access token by posting to the refresh endpoint

```
curl -H "Authorization: Bearer $REFRESH" -X POST http://localhost:5000/token/refresh
```

The API should return a new access token to extend the lifetime of your current session

```
{
    "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE1OTgzNTU5MjEsIm5iZiI6MTU5ODM1NTkyMSwianRpIjoiYmNhYWM2MjktNzBlNS00NDVlLWI3OTctODc1Mzc4OTE5MDNhIiwiZXhwIjoxNTk4MzU2ODIxLCJpZGVudGl0eSI6InRlc3QxIiwiZnJlc2giOmZhbHNlLCJ0eXBlIjoiYWNjZXNzIn0.TexDr4flGEkS_ZQmXPEvWBqGH5Wxya_xDALDOX9KKJ0"
}

```
