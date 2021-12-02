from settings.celery import app

from cli.models import File


@app.task
def delete_file(file_id: int):
    file = File.objects.get(id=file_id)
    file.delete()
