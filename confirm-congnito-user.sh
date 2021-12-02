aws --region us-west-1 cognito-idp admin-set-user-password \
  --user-pool-id ${COGNITO_USER_POOL_ID} \
  --username '' \
  --password '' \
  --permanent
