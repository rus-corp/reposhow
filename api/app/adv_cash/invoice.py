from django.template.loader import render_to_string, get_template
from rest_framework import generics
from django.http import HttpResponse, HttpResponseServerError
# from xhtml2pdf import pisa
from rest_framework.response import Response as RestResponse


from app.main_users.models import CustomUser
from .serializers import InvoiceSerializer

# class GenerateInvoice(generics.CreateAPIView):
#     def post(self, request, *args, **kwargs):
#         user = request.user
#         data = {
#             'company_name': user.user_info.company.company_name 
#         }
#         # serializer = InvoiceSerializer(data=data)
        
#         # if serializer.is_valid():
#         #     context = serializer.validated_data
#         response = HttpResponse(content_type='application/pdf')
#         response['Content-Disposition'] = 'attachment; filename="invoice.pdf"'
#         html_template = get_template('invoice/entry.html')
#         html = html_template.render(data)
#         pisa_status = pisa.CreatePDF(html, dest=response)
        
#         if not pisa_status.error:
#             return response
#         return HttpResponseServerError('faile')





def generate_invoicve(user: CustomUser, type):
    contract_text = ''
    if type == 'entry':
        if user.legal_status == 'LG':
            if user.user_info.company is not None:
                context = {
                    'company': user.user_info.company
                }
                invoice_text = render_to_string('invoice/entry.html', context)
            else:
                raise ValueError('Need company info')
        else:
            raise ValueError('Unsoported invoice type')
        
        
# def generate_pdf_invoice(request):
#     template = get_template('deposit.html')
#     context = 