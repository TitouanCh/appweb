# annotation/management/commands/import_sequences.py
from django.core.management.base import BaseCommand
from django.utils import timezone
from annotation.views import add_sequence  # Import de la vue add_sequence
from django.core.files.uploadedfile import SimpleUploadedFile
from authentication.models import BioinfoUser
import os
from annotation.views import import_sequences

class Command(BaseCommand):
    help = 'Charge toutes les séquences depuis les fichiers FASTA dans le dossier data'

    def handle(self, *args, **kwargs):
        statue_dic = {'CDS':"Coding DNA Sequence",'Genome_complet':"Full Genome", 'Liste_Peptides':"Peptide Sequence"}
        data_dir = 'data/'  # Dossier où sont stockés les fichiers
        for status_folder in statue_dic.keys():
            status_dir = os.path.join(data_dir, status_folder)

            if not os.path.exists(status_dir):
                self.stdout.write(self.style.ERROR(f"Dossier {status_dir} non trouvé"))
                continue

            # Parcours les fichiers dans chaque sous-dossier
            for fasta_file in os.listdir(status_dir):
                if fasta_file.endswith(".fasta") or fasta_file.endswith(".fa") :  # Seulement les fichiers .fasta
                    self.stdout.write(f"Traitement du fichier {fasta_file}...")

                    # Chemin complet du fichier FASTA
                    fasta_path = os.path.join(status_dir, fasta_file)
                    
                    # Appeler la fonction `add_sequence` avec un fichier fictif dans la commande
                    with open(fasta_path, 'rb') as f:
                        file_data = SimpleUploadedFile(fasta_file, f.read(), content_type='text/plain')
                    # Appeler la fonction pour importer les séquences
                        try:
                            new_sequence_ids, invalid_sequences = import_sequences(
                                fasta_file=file_data,
                                status=statue_dic[status_folder],  
                                owner=None,  
                                new_genome_name=fasta_file,  
                                existing_genome=None,
                                random_owner=True
                            )
                            if invalid_sequences:
                                self.stdout.write(self.style.WARNING(f"Attention, certaines séquences sont invalides : {', '.join(str(i) for i in invalid_sequences)}"))
                            self.stdout.write(self.style.SUCCESS(f"Fichier {fasta_file} importé avec succès"))
                        except Exception as e:
                            self.stdout.write(self.style.ERROR(f"Erreur lors de l'import du fichier {fasta_file}: {str(e)}"))
                        self.stdout.write(self.style.SUCCESS(f"Fichier {fasta_file} importé avec succès"))

