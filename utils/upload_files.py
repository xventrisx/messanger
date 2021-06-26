import uuid


def upload_file_instance(instance, filename):
    ext = filename.split(".")[-1]
    filename = f"{uuid.uuid4()}.{ext}"
    return f"{instance.__class__.__name__.lower()}/{filename}"
