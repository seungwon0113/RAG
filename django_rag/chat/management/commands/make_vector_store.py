from pathlib import Path
from django.conf import settings
from django.core.management import BaseCommand
from chat import rag

class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument(
            "txt_file_path",
            type=str,
            help="VectorStore로 저장할 원본 텍스트 파일 경로",
        )

    def handle(self, *args, **options):
        txt_file_path = Path(options["txt_file_path"])

        doc_list = rag.load(txt_file_path)
        print(f"loaded {len(doc_list)} documents")

        doc_list = rag.split(doc_list)
        print(f"split into {len(doc_list)} documents")

        vector_store = rag.VectorStore.make(doc_list)
        vector_store.save(settings.VECTOR_STORE_PATH)