# your_app_name/management/commands/import_csv.py
import csv
# import os
from django.core.management.base import BaseCommand
# from django.db.models import Q
from mainapp.models import Interface, Protein
import pandas as pd

class Command(BaseCommand):
    help = 'Import data from tab-delimited file into the Interface model'

    
    def handle(self, *args, **kwargs):
        Interface.objects.all().delete() #this will delete all records
        file_path = "static/downloads/interface/v2h_binary_list_with_ires_iseq_category_seq_20231012.txt"
        dat = pd.read_csv(file_path,sep='\t').dropna()
        # with open(file_path, 'r') as file:
        #     csv_reader = csv.DictReader(file,delimiter='\t')
        cnt = 1
        for _,row in dat.iterrows():
                # break
            try:
                if row['Viral_ires'] == "-":
                    Vires = ""
                else:
                    Vires = row['Viral_ires']
                if row['Human_ires'] == "-":
                    Hires = ""
                else:
                    Hires = row['Human_ires']
                Interface.objects.create(
                    id=cnt,
                    source=row["family"],
                    p1_ires=Vires,
                    p2_ires=Hires,
                    p1 = Protein.objects.get(id=row['Viral_protein_uid']),
                    p2 = Protein.objects.get(id=row['Human_protein_uid'])
                )
                cnt = cnt + 1
            except:
                print(f"{row['id']}:{row['Viral_protein_uid']}-{row['Human_protein_uid']} is already in the database")

        self.stdout.write(self.style.SUCCESS('CSV data imported successfully.'))