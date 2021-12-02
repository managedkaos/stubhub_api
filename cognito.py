from pycognito import Cognito
import os
stage = os.environ.get('OPERATION_MODE', "development")


COGNITO_USER_POOL_ID=os.environ.get('COGNITO_USER_POOL_ID')
COGNITO_CLIENT_ID=os.environ.get('COGNITO_CLIENT_ID')
COGNITO_CLIENT_SECRET=os.environ.get('COGNITO_CLIENT_SECRET')

u = Cognito(COGNITO_USER_POOL_ID,COGNITO_CLIENT_ID, client_secret=COGNITO_CLIENT_SECRET)

users = u.get_users(attr_map={"given_name":"first_name","family_name":"last_name","email":"email"})

for user in users:
    print(user)
