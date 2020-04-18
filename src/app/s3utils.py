from storages.backends.s3boto3 import S3Boto3Storage

MediaRootS3Boto3Storage = lambda: S3Boto3Storage(location="uploads")
