from django.core.management.base import BaseCommand
from blast_request.models import Database


class Command(BaseCommand):
    help = "Importe les bases de données NCBI et UniProt pour les redirections Blast"

    def handle(self, *args, **kwargs):
        databases = [
            {
                "name": "NCBI",
                "url": "https://blast.ncbi.nlm.nih.gov/Blast.cgi",
                "blastn_url": "https://blast.ncbi.nlm.nih.gov/Blast.cgi?PROGRAM=blastn&PAGE_TYPE=BlastSearch&LINK_LOC=blasthome&QUERY=",
                "blastp_url": "https://blast.ncbi.nlm.nih.gov/Blast.cgi?PROGRAM=blastp&PAGE_TYPE=BlastSearch&LINK_LOC=blasthome&QUERY=",
            },
            {
                "name": "UniProt",
                "url": "https://www.uniprot.org/blast/",
                "blastn_url": None,  # UniProt ne supporte que BlastP
                "blastp_url": "https://www.uniprot.org/blast/?sequence=",
            }
        ]

        for db_data in databases:
            db, created = Database.objects.update_or_create(
                name=db_data["name"],
                defaults=db_data
            )

            if created:
                self.stdout.write(self.style.SUCCESS(f"Base de données ajoutée : {db.name}"))
            else:
                self.stdout.write(self.style.WARNING(f" !!Base de données mise à jour!! : {db.name}"))
