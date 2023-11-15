from rest_framework import serializers

from .models import ReferalLink, Company_Doc


class ReferalLinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReferalLink
        fields = ['name', 'email', 'specialization', 'work_links', 'file1', 'file2', 'file3', 'file4', 'file5']



class CompanyDocSerializer(serializers.ModelSerializer):
    class Meta:
        model = Company_Doc
        fields = ['id', 'name', 'desc', 'slug', 'file']