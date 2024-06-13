i have incorporated a total of 6 APIS IN this codebase
they are:


         curl --location 'http://127.0.0.1:8000/user/create' \
        --header 'Content-Type: application/json' \
        --data-raw '{
            "name": "manoj1",
            "username": "manoj15",
            "mobilenumber": "mobile15",
            "email": "manojreddy5234@gmail.com"
        
        }'




        curl --location 'http://127.0.0.1:8000/user/addRide' \
        --header 'Content-Type: application/json' \
        --data '{
          "from_location": "mum",
          "to_location": "blr",
          "date": "2024-02-14",
          "receiver_mobilenumber": "9502379475",
          "quantity": 10,
          "rider_id": 10,
          "medium": "train"
        }'


         curl --location 'http://127.0.0.1:8000/user/addTransportRequest' \
         --header 'Content-Type: application/json' \
         --data '{
           "from_location": "mum",
           "to_location": "blr",
           "date": "2024-02-13",
           "receiver_mobilenumber": "9502379475",
           "quantity": 5,
           "asset_type": "LAPTOP",
           "sensitivity": "NORMAL",
           "requester_id": 5
         }'





        curl --location 'http://127.0.0.1:8000/user/getTransportRequests?requester_id=5&pageno=0&pageSize=10' \
        --header 'Content-Type: application/json'




        curl --location 'http://127.0.0.1:8000/user/getMatchingRides?pageno=0&pageSize=10&request_id=1' \
        --header 'Content-Type: application/json'


        curl --location 'http://127.0.0.1:8000/user/applyForRide' \
        --header 'Content-Type: application/json' \
        --data '{
          "request_id": 1,
          "ride_id": 16
        }'
google_drive_link_of_screenshots: https://drive.google.com/drive/folders/1RgX0IZ9aeF7rcxTUNyjl8p6avxrkkJEq?usp=sharing
