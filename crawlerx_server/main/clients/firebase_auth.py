import requests


class FirebaseAuth:

    def __init__(self, request_token, user_id):
        self.token_id = request_token
        self.user_id = user_id

    def check_user_validity(self):
        try:
            url = 'https://identitytoolkit.googleapis.com/v1/accounts:lookup?key=AIzaSyD88ucXoxhnfm3iNUA-FJ-zg-0GrJKT-Zo'
            data = '{  "idToken": " ' + self.token_id + '" }'

            response = requests.post(url, data=data, headers={"Content-Type": "application/json"})
            if (response.status_code % 100) == 2:
                # TODO: check the user_id for more validity check
                return True
            else:
                return False
        except:
            return False
