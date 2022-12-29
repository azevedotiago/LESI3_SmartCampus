PROJECT_ID=$(gcloud config get-value core/project)

REGION=europe_west2

SERVICE_ACCOUNT=$(gcloud iam service-accounts list \
    --filter cloudrun-serviceaccount --format "value(email)")

GS_BUCKET_NAME=${PROJECT_ID}-media

echo DATABASE_URL=\"postgres://djuser:${DJPASS}@//cloudsql/${PROJECT_ID}:${REGION}:myinstance/mydatabase\" > .env

echo GS_BUCKET_NAME=\"${GS_BUCKET_NAME}\" >> .env

echo SECRET_KEY=\"$(cat /dev/urandom | LC_ALL=C tr -dc 'a-zA-Z0-9' | fold -w 50 | head -n 1)\" >> .env

echo DEBUG=\"True\" >> .env

gcloud secrets delete application_settings
gcloud secrets create application_settings --data-file .env

gcloud secrets add-iam-policy-binding application_settings \
  --member serviceAccount:${SERVICE_ACCOUNT} --role roles/secretmanager.secretAccessor
