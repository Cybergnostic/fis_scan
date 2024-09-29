import requests
from bs4 import BeautifulSoup
import re

def scrape_receipt_data(url):
    """Скрепује JSON податке о рачуну и метаподатке са веб странице suf.purs.gov.rs и враћа JSON фајл са подацима о рачуну и метаподацима"""

    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')

        # Екстракција токена из script тага
        script_tags = soup.find_all('script', type='text/javascript')
        for script_tag in script_tags:
            if 'viewModel.Token' in script_tag.text:
                match = re.search(r"viewModel\.Token\('([^']+)'\)", script_tag.text)
                if match:
                    token = match.group(1)
                    break
        else:
            print("Грешка: Токен није пронађен у script таговима.")
            return None

        # Екстракција броја рачуна (invoiceNumber)
        invoice_number_element = soup.find('span', {'id': 'invoiceNumberLabel'})
        if invoice_number_element:
            invoice_number = invoice_number_element.text.strip()
        else:
            print("Грешка: Број рачуна није пронађен на страници.")
            return None

        # Екстракција метаподатака
        metadata = {}
        for form_group in soup.find_all('div', class_='form-group'):
            label_element = form_group.find('label', class_='col-form-label')
            if label_element:
                label_text = label_element.text.strip()
                value_element = form_group.find('span') 
                if value_element:
                    value_text = value_element.text.strip()
                    metadata[label_text] = value_text

    
        payload = {
            'invoiceNumber': invoice_number,
            'token': token
        }

        response = requests.post('https://suf.purs.gov.rs/specifications', data=payload)
        response.raise_for_status()

        data = response.json()

        result = {
            'metadata': metadata,
            'items': data['items'] 
        }

        return result

    except requests.exceptions.RequestException as e:
        print(f"Грешка при скенирању података: {e}")
        return None