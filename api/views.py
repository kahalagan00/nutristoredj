from django.shortcuts import render
import json

# Create your views here.

from django.http import JsonResponse
from django.db import connection

def get_products(request):
  with connection.cursor() as cursor:
    cursor.execute("SELECT * FROM products") 
    columns = [col[0] for col in cursor.description]
    rows = cursor.fetchall()
      
  data = []
  for row in rows:
      row_dict = dict(zip(columns, row))  # Combine column names with row values
      # Parse the `nutritional_facts` column if it exists
      if 'nutritional_facts' in row_dict and isinstance(row_dict['nutritional_facts'], str):
        try:
          row_dict['nutritional_facts'] = json.loads(row_dict['nutritional_facts']) # Actual parsing?
        except json.JSONDecodeError: 
          pass  # Leave it as-is if parsing fails
      data.append(row_dict)
  

  return JsonResponse({'data': data})