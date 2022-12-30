set -ev
source .env
gcloud config set project smartenergy-backend

gcloud services enable \
  run.googleapis.com \
  sql-component.googleapis.com \
  sqladmin.googleapis.com \
  compute.googleapis.com \
  cloudbuild.googleapis.com \
  secretmanager.googleapis.com \
  artifactregistry.googleapis.com


gcloud builds submit --pack image=gcr.io/${PROJECT_ID}/myimage --project ${PROJECT_ID}
gcloud builds submit --config migrate.yaml --project ${PROJECT_ID} --substitutions _REGION=$REGION
gcloud run deploy django-cloudrun \
  --platform managed \
  --region $REGION \
  --image gcr.io/${PROJECT_ID}/myimage \
  --set-cloudsql-instances ${PROJECT_ID}:${REGION}:myinstance \
  --set-secrets APPLICATION_SETTINGS=application_settings:latest \
  --service-account $SERVICE_ACCOUNT \
  --allow-unauthenticated \
  --project ${PROJECT_ID}

gcloud run services update django-cloudrun \
  --platform managed \
  --region $REGION \
  --image gcr.io/${PROJECT_ID}/myimage \
  --project ${PROJECT_ID}