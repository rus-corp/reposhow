import uuid
from transliterate import translit
from django.utils.crypto import get_random_string
from django.utils.text import slugify
from .models import CustomUser



class CustomnUserService:
    model = CustomUser

    @classmethod
    def get_username_slug(cls, username: str) -> str:
        slug = None
        try:
            name = translit(username, reversed=True)
            slug = slugify(name)
        except:
            slug = slugify(username)
        while cls.model.objects.filter(slug=slug).exists():
            slug = f"{slug}-{get_random_string(length=4)}"
        return slug

    @classmethod
    def get_referal_link(cls, user: CustomUser) -> str:
        code = str(uuid.uuid4()).replace("-", "")[:12]
        referal_link = f"https://clik-work.ru/registration/{code}/"
        while cls.model.objects.filter(referal_link=referal_link).exists():
            code = str(uuid.uuid4()).replace("-", "")[:12]
            referal_link = f"https://clik-work.ru/registration/{code}/"
        return referal_link 
