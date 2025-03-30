# Generated by Django 5.1.7 on 2025-03-30 09:13

import pgvector.django.indexes
import pgvector.django.vector
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='PaikdabangMenuDocument',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('page_content', models.TextField()),
                ('metadata', models.JSONField(default=dict)),
                ('embedding', pgvector.django.vector.VectorField(dimensions=1536, editable=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'indexes': [pgvector.django.indexes.HnswIndex(ef_construction=64, fields=['embedding'], m=16, name='paikdabang_menu_doc_idx', opclasses=['vector_cosine_ops'])],
            },
        ),
    ]
