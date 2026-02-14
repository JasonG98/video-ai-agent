from pathlib import Path
from uuid import uuid4
import boto3
from botocore.exceptions import BotoCoreError, ClientError
from app.config import get_settings


class StorageService:
    def __init__(self) -> None:
        self.settings = get_settings()

    def _s3_client(self):
        return boto3.client(
            "s3",
            endpoint_url=self.settings.s3_endpoint,
            aws_access_key_id=self.settings.s3_access_key,
            aws_secret_access_key=self.settings.s3_secret_key,
            region_name=self.settings.s3_region,
        )

    def save_file(self, filename: str, content: bytes, content_type: str) -> tuple[str, str]:
        """保存文件到 MinIO/S3，失败则落本地。"""
        key = f"uploads/{uuid4()}_{filename}"
        if self.settings.storage_backend in {"minio", "s3"}:
            try:
                client = self._s3_client()
                client.put_object(Bucket=self.settings.s3_bucket, Key=key, Body=content, ContentType=content_type)
                return key, f"{self.settings.s3_endpoint}/{self.settings.s3_bucket}/{key}"
            except (BotoCoreError, ClientError):
                pass

        local_dir = Path(self.settings.local_storage_path)
        local_dir.mkdir(parents=True, exist_ok=True)
        path = local_dir / key.replace("/", "_")
        path.write_bytes(content)
        return key, str(path)
