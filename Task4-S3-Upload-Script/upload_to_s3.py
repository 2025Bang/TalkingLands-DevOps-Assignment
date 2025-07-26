import boto3, os, argparse, logging
from boto3.s3.transfer import TransferConfig
from botocore.exceptions import ClientError
from datetime import datetime

logging.basicConfig(filename='upload.log', level=logging.INFO)

def multipart_upload(s3, bucket, key, file_path):
    config = TransferConfig(multipart_threshold=100 * 1024 * 1024)
    try:
        s3.upload_file(file_path, bucket, key, Config=config)
        logging.info(f"{datetime.now()} - Uploaded {file_path} ({os.path.getsize(file_path)} bytes) to {bucket}/{key}")
    except ClientError as e:
        logging.error(f"{datetime.now()} - ERROR uploading {file_path}: {e}")
        raise

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--file', required=True)
    parser.add_argument('--bucket', required=True)
    parser.add_argument('--key', default=None)
    parser.add_argument('--profile', default=None)
    args = parser.parse_args()

    session = boto3.Session(profile_name=args.profile) if args.profile else boto3.Session()
    s3 = session.client('s3')

    file_path = args.file
    file_size = os.path.getsize(file_path)
    key = args.key or os.path.basename(file_path)

    multipart_upload(s3, args.bucket, key, file_path)

if __name__ == "__main__":
    main()
