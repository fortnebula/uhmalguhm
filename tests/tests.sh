if [[ $1 = create_user ]] 
then
    curl -H "Content-Type: application/json" -X POST   -d '{"username":"test1","password":"test1"}' http://localhost:5000/api/v1/user/create
    curl -H "Content-Type: application/json" -X POST   -d '{"username":"test2","password":"test2"}' http://localhost:5000/api/v1/user/create
    curl -H "Content-Type: application/json" -X POST   -d '{"username":"test3","password":"test3"}' http://localhost:5000/api/v1/user/create
    curl -H "Content-Type: application/json" -X POST   -d '{"username":"test4","password":"test4"}' http://localhost:5000/api/v1/user/create
fi

if [[ $1 = create_token ]] 
then
    unset ACS
    export ACS=$(curl -H "Content-Type: application/json" -X POST   -d '{"username":"test1","password":"test1"}' http://localhost:5000/api/v1/token/issue |grep access_token |cut -d '"' -f4)
    echo $ACS
fi

if [[ $1 = create_image ]] 
then
    unset ACS
    export ACS=$(curl -H "Content-Type: application/json" -X POST   -d '{"username":"test1","password":"test1"}' http://localhost:5000/api/v1/token/issue |grep access_token |cut -d '"' -f4)
    curl -H "Authorization: Bearer $ACS"  -H "Content-Type: application/json" -X POST -d '{"image":"nginx", "tag":"latest"}' http://localhost:5000/api/v1/container/create
    curl -H "Authorization: Bearer $ACS"  -H "Content-Type: application/json" -X POST -d '{"image":"ubuntu", "tag":"latest"}' http://localhost:5000/api/v1/container/create
fi


