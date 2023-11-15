from rest_framework import serializers
from django.utils import timezone
from drf_spectacular.utils import extend_schema_field
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from typing import Dict, Union



from app.raiting.serializers import RatingSerializer
from .models import CustomUser, UserInfo, UserSpecialization, UserInfoCompany
from app.portfolio.serializers import WorkSerializer
from app.categories.serializers import SpecializationSerializer
from app.categories.models import Specialization


class CustomUserSerializer(serializers.ModelSerializer):
    time_registered = serializers.SerializerMethodField()
    class Meta:
        model = CustomUser
        fields = [
            "id",
            "email",
            "status",
            "referal_link",
            "rub_acc",
            "usd_acc",
            'eur_acc',
            'time_registered',
        ]
    
    @extend_schema_field(serializers.DateField())
    def get_time_registered(self, obj):
        today = timezone.now().date()
        time_registered = (today - obj.date_joined).days
        return time_registered
        


class RegisterUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ["email", "password", "referal_link"]



class LoginUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ("id", "email", "password")



class ResetPasswordLinkRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ("email",)
        
        
        
class ChangePasswordSerializer(serializers.ModelSerializer):
    old_password = serializers.CharField(required=True, write_only=True)
    new_password = serializers.CharField(required=True, write_only=True)

    class Meta:
        model = CustomUser
        fields = ("old_password", "new_password")

    def create(self, validated_data):
        instance = self.context['request'].user
        if instance.check_password(validated_data.get("old_password")):
            instance.set_password(validated_data.get("new_password"))
            instance.save()
            return instance
        raise serializers.ValidationError(
            {"old_password": "Invalid data provided in this field"}
        )


class ResetPasswordSecureTokenSerializer(serializers.ModelSerializer):
    uid = serializers.CharField()
    link_token = serializers.CharField()

    class Meta:
        model = CustomUser
        fields = ("uid", "link_token")



class ResetPasswordSerializer(serializers.ModelSerializer):
    new_password = serializers.CharField()
    new_password2 = serializers.CharField()

    class Meta:
        model = CustomUser
        fields = ("new_password", 'new_password2')
        
    def validate(self, attrs):
        new_password = attrs.get('new_password')
        new_password2 = attrs.get('new_password2')
        if new_password != new_password2:
            raise serializers.ValidationError('Пароли не совпадают')
        try:
            validate_password(new_password)
        except ValidationError as e:
            raise serializers.ValidationError(e.messages)
        return attrs



class CustomuserResponseSerializer(serializers.Serializer):
    status = serializers.BooleanField()
    errors = serializers.CharField()
    uid = serializers.CharField()
    token = serializers.CharField()



class UserSpecializationSerializer(serializers.ModelSerializer):
    specialization = SpecializationSerializer()

    class Meta:
        model = UserSpecialization
        fields = ["id", "specialization", "is_main"]
        read_only_fields = [
            "id",
        ]

    def create(self, validated_data):
        specialization_data = validated_data.pop("specialization", [])
        is_main = validated_data.pop("is_main", False)
        user_info = validated_data["user"].user_info
        for specialization_param in specialization_data:
            specialization = Specialization.objects.get(**specialization_data)

            has_specialization = UserSpecialization.objects.filter(
                user=user_info, specialization=specialization
            ).first()
            if not has_specialization:
                UserSpecialization.objects.create(
                    user=user_info, specialization=specialization, is_main=is_main
                )
        return user_info

    def update(self, instance, validated_data):
        specialization_data = validated_data.pop("specialization", [])
        is_main = validated_data.pop("is_main", False)
        user_info = self.context["user"].user_info
        user_spec_id = self.context["id"]

        if is_main:
            UserSpecialization.objects.filter(id=user_spec_id).update(is_main=True)
            UserSpecialization.objects.exclude(id=user_spec_id).filter(user=user_info, is_main=True).update(is_main=False)

        for specialization_param in specialization_data:
            specialization = Specialization.objects.get(**specialization_data)

            has_specialization = UserSpecialization.objects.filter(
                user=user_info, specialization=specialization, id=user_spec_id
            ).first()
            if not has_specialization:
                UserSpecialization.objects.filter(id=user_spec_id).update(
                    specialization=specialization
                )
        return instance



class UserInfoListSerializer(serializers.ModelSerializer):
    user_specializations = UserSpecializationSerializer(many=True)

    class Meta:
        model = UserInfo
        fields = (
            "id",
            "first_name",
            "last_name",
            "skill",
            "experience",
            "avatar",
            "review_ratio",
            "cost_of_hour_work",
            "profile_description",
            "baner",
            "phone_number",
            "on_vacation",
            "user_specializations",
            'polzunok'
        )
        read_only_fields = ["user"]



class UserInfoCompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = UserInfoCompany
        fields = [
            "id",
            "employee_position",
            "company_name",
            "short_company_name",
            "ceo_name",
            "ceo_post",
            "adress_in_law",
            "adress_fact",
            "reg_number",
            "company_number",
            "kpp_number",
            "certificate",
            "certificate_file",
            "company_site",
            "company_phone",
            "company_email",
            "social_site",
        ]



class FreelancerCompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = UserInfoCompany
        fields = (
            "employee_position",
            "company_name",
        )

   
# class CaptchaSerilizer(serializers.Serializer):
#     recaptcha = ReCaptchaField()



 
class CustomUserListSerializer(serializers.ModelSerializer):
    time_registered = serializers.SerializerMethodField()
    orders = serializers.SerializerMethodField()
    contests = serializers.SerializerMethodField()
    positive_reviews = serializers.SerializerMethodField()
    negative_reviews = serializers.SerializerMethodField()
    rating = serializers.SerializerMethodField()
    portfolio = serializers.SerializerMethodField()
    user_info = serializers.SerializerMethodField()
    # recaptcha = ReCaptchaField()
    
    class Meta:
        model = CustomUser
        fields = [
            "id",
            "username",
            "rating",
            "status",
            "email_confirm",
            "email",
            "orders",
            "negative_reviews",
            "positive_reviews",
            "slug",
            "legal_status",
            "time_registered",
            "contests",
            "user_info",
            "portfolio",
        ]
    
    def get_portfolio(self, instance) -> Dict[str, Union[Dict, str]]:
        try:
            return WorkSerializer(
                instance.works, many=True,
                context=self.context
            ).data
        except AttributeError as e:
            return {
                'status': 'No items in portfolio founded.',
                'error': str(e)
            }

    @extend_schema_field(serializers.DateField())
    def get_time_registered(self, obj):
        today = timezone.now().date()
        time_registered = (today - obj.date_joined).days
        return time_registered

    @extend_schema_field(serializers.IntegerField())
    def get_rating(self, instance):
        try:
            return RatingSerializer(
                instance.ratings, context=self.context, read_only=True
            ).data
        except AttributeError:
            return {"error": "Rating instance not found!"}

    @extend_schema_field(serializers.IntegerField())
    def get_orders(self, instance):
        return (
            instance.order_responses.filter(executor_status="EX").count()
            + instance.order_customers.count()
        )

    @extend_schema_field(serializers.IntegerField())
    def get_negative_reviews(self, instance):
        return (
            instance.review_customer.filter(status="NT").count()
            + instance.review_executor.filter(status="NT").count()
        )

    @extend_schema_field(serializers.IntegerField())
    def get_positive_reviews(self, instance):
        return (
            instance.review_customer.filter(status="PT").count()
            + instance.review_executor.filter(status="PT").count()
        )

    @extend_schema_field(serializers.IntegerField())
    def get_contests(self, instance):
        return (
            instance.contest_customers.count()
            + instance.contest_responses.filter(executor_status="EX").count()
        )


    def get_user_info(self, instance) -> Dict[str, Union[Dict, str]]:
        try:
            if instance.legal_status == "PS":
                return UserInfoListSerializer(
                    instance.user_info, context=self.context, read_only=True
                ).data
            return {
                **UserInfoListSerializer(
                    instance.user_info, context=self.context, read_only=True
                ).data,
                **FreelancerCompanySerializer(
                    UserInfoCompany.objects.get(
                        id=instance.user_info.company_id
                    ),
                    context=self.context,
                    read_only=True,
                ).data,
            }
        except AttributeError:
            return {"error": "User info not found"}



