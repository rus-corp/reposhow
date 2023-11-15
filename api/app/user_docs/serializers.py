from rest_framework import serializers


from app.main_users.serializers import (
    UserSpecializationSerializer,
    UserInfoCompanySerializer,
)


from app.main_users.serializers import UserSpecializationSerializer, UserInfoCompanySerializer
from app.main_users.models import CustomUser, UserInfo, UserInfoCompany
from .models import UserDoc, BankAccount, Region, Country, Contract



class ContractSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contract
        fields = ['id', 'text',]



class RegionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Region
        fields = ["id", "name"]



class CountrySerializer(serializers.ModelSerializer):
    region = RegionSerializer(read_only=True)

    class Meta:
        model = Country
        fields = ["id", "name", "phone_code", "flag", "region"]
        read_only_fields = ["region"]
        extra_kwargs = {
            "name": {"validators": []},
        }


class UserDocsSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserDoc
        fields = [
            "document",
            "document_name",
            "personal_number",
            "document_number",
            "document_issued",
            "user",
        ]
        read_only_fields = [
            "user",
        ]


class BankAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = BankAccount
        fields = [
            "bank_name",
            "bank_address",
            "bank_bic",
            "bank_correspondent_account",
            "payment_account",
            "recipients_name",
            "user",
        ]
        read_only_fields = [
            "user",
        ]


class UserInfoSerializer(serializers.ModelSerializer):
    user_specializations = UserSpecializationSerializer(many=True, required=False)
    country = CountrySerializer(required=False)
    time_registered = serializers.DateField(source='user.date_joined', read_only=True)
    company = UserInfoCompanySerializer(required=False)

    class Meta:
        model = UserInfo
        fields = [
            "id",
            "polzunok",
            'time_registered',
            "first_name",
            "last_name",
            "father_name",
            "avatar",
            "on_vacation",
            "phone_number",
            "on_vacation",
            "date_of_birth",
            "cost_of_hour_work",
            "profile_description",
            "baner",
            "adress",
            "skill",
            "review_ratio",
            "user_specializations",
            "country",
            "company",
            'currency',
            'experience'
        ]
        read_only_fields = [
            "user",
        ]


class CustomUserPersonalAccount(serializers.ModelSerializer):
    user_docs = UserDocsSerializer(required=False)
    user_info = UserInfoSerializer(required=False)
    user_bank = BankAccountSerializer(many=True, required=True)
    rub_account = serializers.CharField(source='rub_acc.account_name', read_only=True)
    usd_account = serializers.CharField(source='usd_acc.account_name', read_only=True)
    eur_account = serializers.CharField(source='eur_acc.account_name', read_only=True)

    rub_balance = serializers.CharField(source="rub_acc.balance", read_only=True)
    usd_balance = serializers.CharField(source="usd_acc.balance", read_only=True)
    eur_balance = serializers.CharField(source="eur_acc.balance", read_only=True)


    class Meta:
        model = CustomUser
        fields = [
            "id",
            "username",
            "slug",
            "email",
            "founder",
            "rub_account",
            "rub_balance",
            'usd_account',
            "usd_account",
            "usd_balance",
            "eur_account",
            "eur_balance",
            "user_info",
            "user_docs",
            "user_bank",
            "status",
            "legal_status",
            'paid_entrance_rub',
            'paid_entrance_usd',
            'paid_entrance_eur',
        ]
        read_only_fields = [
            "id",
            "user",
            "email",
            "slug",
            "founder",
            "rub_balance",
            "usd_balance",
            "eur_balance",
        ]

    def create(self, validated_data):
        user_info_data = validated_data.pop("user_info", [])
        user_docs_data = validated_data.pop("user_docs", [])
        user_bank_data = validated_data.pop("user_bank", [])

        user_id = self.context["request"].user.id
        user = CustomUser.objects.get(id=user_id)

        copied_user_info_data = user_info_data.copy()
        try:
            country_data = user_info_data.pop("country", None)
            company_data = user_info_data.pop("company", None)
        except:
            country_data = None
            company_data = None
        for user_info in copied_user_info_data:
            if country_data:
                for countries in country_data:
                    country = Country.objects.get(**country_data)
                    copied_user_info_data["country"] = country
            if company_data:
                for company in company_data:
                    company, _ = UserInfoCompany.objects.get_or_create(**company_data)
                    copied_user_info_data["company"] = company
            info, created = UserInfo.objects.update_or_create(
                user=user, **copied_user_info_data
            )

        for user_docs in user_docs_data:
            docs, created = UserDoc.objects.get_or_create(user=user, **user_docs_data)
        for user_bank in user_bank_data:
            bank, created = BankAccount.objects.get_or_create(user=user, **user_bank)

        return user

    def update(self, instance, validated_data):
        user_info_data = validated_data.pop("user_info", [])
        user_docs_data = validated_data.pop("user_docs", [])
        user_bank_data = validated_data.pop("user_bank", [])

        if user_docs_data:
            try:
                docs = UserDoc.objects.get(user=instance)
                for attr, value in user_docs_data.items():
                    setattr(docs, attr, value)
                    docs.save()
            except UserDoc.DoesNotExist:
                docs = UserDoc.objects.create(user=instance)

        if user_bank_data:
            user_bank_instance = BankAccount.objects.filter(user=instance).first()
            if user_bank_instance:
                for user_bank in user_bank_data:
                    for attr, value in user_bank.items():
                        setattr(user_bank_instance, attr, value)
                user_bank_instance.save()
            else:
                user_bank = None
                user_bank["user"] = instance
                BankAccount.objects.create(**user_bank_data)

        copied_user_info_data = user_info_data.copy()
        try:
            country_data = user_info_data.pop("country", None)
            company_data = copied_user_info_data.pop("company", None)
        except:
            country_data = None
            company_data = None

        for user_info in copied_user_info_data:
            if country_data:
                for countries in country_data:
                    country = Country.objects.get(**country_data)
                    copied_user_info_data["country"] = country
            try:
                info = UserInfo.objects.get(user=instance)
                for attr, value in copied_user_info_data.items():
                    setattr(info, attr, value)
                    info.save()
            except UserInfo.DoesNotExist:
                info = UserInfo.objects.create(user=instance)
        if company_data:
            user_info_instance = instance.user_info
            if user_info_instance:
                company = user_info_instance.company
                if company:
                    for attr, value in company_data.items():
                        setattr(company, attr, value)
                        company.save()
                else:
                    company = UserInfoCompany(**company_data)
                    company.save()
                    user_info_instance.company = company
                    user_info_instance.save()
        instance = super().update(instance, validated_data)

        return instance
