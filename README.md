## uhmalguhm
 uh *mal* guhm

 The purpose of this project is to provide a easy to use interface to spin up virtual machines that user docker images as an overlay to the root filesystem.

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

Currently there are no docs, however a system for documentation is in-flight

### Examples for use
To use the api, first a user needs to be created

```
curl -H "Content-Type: application/json" -X POST   -d '{"username":"test","password":"test"}' http://localhost:5000/register
```
Now that you have a user, you can request an access token using the token endpoint

```
curl -H "Content-Type: application/json" -X POST   -d '{"username":"test","password":"test"}' http://localhost:5000/token
```
