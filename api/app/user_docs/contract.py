from django.template.loader import render_to_string

from app.main_users.models import CustomUser

def genereate_contract_text(user: CustomUser):
    contract_text = ''
    if hasattr(user, 'user_info') and user.legal_status == 'PS':
        context = {
            'user': user,
            'first_name': user.user_info.first_name,
            'last_name': user.user_info.last_name,
            'bank': user.user_bank.first()
        }
        contract_text = render_to_string('user_doc/contract_phisic.html', context)
    elif user.legal_status == 'LG' and user.user_info.company is not None:
        context = {
            'user_company': user.user_info.company,
            'user_data': user,
            'bank': user.user_bank.first()
        }
        contract_text = render_to_string('user_doc/contract_lower.html', context)
    return contract_text