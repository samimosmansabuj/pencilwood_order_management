import json
from django.core.management import call_command
from django.db import connection

# Ensure Django settings are properly set up
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "pencilwood_order_management.settings")
import django
django.setup()

# Custom export function
def export_data(app_label, output_file):
    with open(output_file, 'w', encoding='utf-8') as f:
        call_command('dumpdata', app_label, stdout=f)

# Call the function with 'order' app and desired output filename
export_data('account', 'account_data.json')

# open terminal and write "python export_data.py" then enter for export data....
