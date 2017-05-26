from google.cloud import storage
import google.auth
from google.oauth2 import service_account
from google.cloud.storage import Blob


def authorized_client(cred_file_path, project_name):
    credentials = service_account.Credentials.from_service_account_file(
        cred_file_path)
    client = storage.Client(credentials=credentials, project=project_name)
    return client


def get_bucket(client, bucket_name):
    bkt = client.get_bucket(bucket_name)
    return bkt


def upload_public_file(client, bkt, file_name):
    # file_name in Blob constructor is the file name you want to have on GCS
    blob = Blob(file_name, bkt)
    # file_name in open function is the one that actually sits on your hard drive
    with open(file_name, 'rb') as my_file:
        blob.upload_from_file(my_file)
    # after uploading the blob, we set it to public, so that it's accessible with a simple link
    blob.make_public(client)


def send_file_to_google_cloud(file_name="example.jpg",
                              cred_file_path='path-to-json-with-credentials',
                              project_name="your-project-name",
                              bucket_name="your-bucket-name"):
    client = authorized_client(cred_file_path=cred_file_path,
                               project_name=project_name)
    bkt = get_bucket(client, bucket_name=bucket_name)
    try:
        upload_public_file(client, bkt, file_name=file_name)
    except:
        print("Couldn't upload file to GCS")
        raise
