from dateutil.relativedelta import relativedelta
from datetime import datetime as dt

from django.db import models


class RatingCalculateConstant(models.Model):
    """Модель с константами для рейтинга."""

    reg_time = models.IntegerField(
        "Месяцев с момента регистрации:",
    )
    orders = models.IntegerField(
        "Заказов:",
    )
    peace_orders = models.IntegerField(
        "Мировых соглашений:",
    )
    arbit = models.IntegerField(
        "Арбитражей:",
    )
    contest = models.IntegerField(
        "Контестов созданных/посещенных:",
    )
    wins_1_place = models.IntegerField(
        "Победа в контесте:",
    )
    wins_2_place = models.IntegerField(
        "Второе место в контесте:",
    )
    wins_3_place = models.IntegerField(
        "Третье место в контесте:",
    )
    review_positive = models.IntegerField(
        "Позитивный отзыв:",
    )
    review_negative = models.IntegerField("Негативный отзыв:")
    reply_time_1_hour = models.IntegerField("Ответ на оффер в течение часа:")
    reply_time_6_hour = models.IntegerField("Ответ на оффер в течение 6 часов")
    reply_time_more = models.IntegerField("Ответ на оффер ≥12 часов")
    vote_participation = models.IntegerField(
        "Участие в голосовании:",
    )
    vote_ignore = models.IntegerField(
        "Игнор голосования:",
    )


class Rating(models.Model):
    """Таблица с рейтингом фрилансеров."""

    freelancer = models.OneToOneField(
        to="main_users.CustomUser",
        related_name="ratings",
        verbose_name="Фрилансер:",
        help_text="выберите подходящий user instance",
        on_delete=models.CASCADE,
    )
    reg_time = models.IntegerField(
        verbose_name="Время пошедшее с момента регистрации",
        help_text="поле можно оставить пустым",
        blank=True,
        default=0,
    )
    orders = models.IntegerField(
        verbose_name="Кол-во заказов:",
        blank=True,
        help_text="поле можно оставить пустым",
        default=0,
    )
    peace_orders = models.IntegerField(
        verbose_name="Кол-во мировых соглашений:",
        blank=True,
        help_text="поле можно оставить пустым",
        default=0,
    )
    contest = models.IntegerField(
        verbose_name="Кол-во учрежденных или посещенных контестов:",
        blank=True,
        help_text="поле можно оставить пустым",
        default=0,
    )
    arbit = models.IntegerField(
        verbose_name="Кол-во арбитражей:",
        blank=True,
        default=0,
        help_text="поле можно оставить пустым",
    )
    wins = models.IntegerField(
        verbose_name="Кол-во побед в контестах:",
        blank=True,
        default=0,
        help_text="поле можно оставить пустым",
    )
    wins_1_place_value = models.IntegerField(
        "Победа в контесте:", blank=True, default=0
    )
    wins_2_place_value = models.IntegerField(
        "Второе место в контесте:", blank=True, default=0
    )
    wins_3_place_value = models.IntegerField(
        "Третье место в контесте:", blank=True, default=0
    )
    reviews = models.IntegerField(
        verbose_name="Кол-во отзывов:",
        blank=True,
        help_text="поле можно оставить пустым",
    )
    review_positive_value = models.IntegerField(
        "Позитивный отзыв:", blank=True, default=0
    )
    review_negative_value = models.IntegerField(
        "Негативный отзыв:", blank=True, default=0
    )
    reply_time = models.IntegerField(
        verbose_name="Продолжительность ответа на оффер:",
        blank=True,
        default=0,
        help_text="поле можно оставить пустым",
    )
    reply_time_1_hour_value = models.IntegerField(
        "Ответ на оффер в течение часа:", blank=True, default=0
    )
    reply_time_6_hour_value = models.IntegerField(
        "Ответ на оффер в течение 6 часов", blank=True, default=0
    )
    reply_time_more_value = models.IntegerField(
        "Ответ на оффер ≥12 часов", blank=True, default=0
    )
    vote_participation = models.IntegerField(
        verbose_name="Участие в голосованиях:",
        default=0,
        blank=True,
        help_text="поле можно оставить пустым",
    )
    vote_participation_value = models.IntegerField(
        "Участие в голосовании:", blank=True, default=0
    )
    vote_ignore_value = models.IntegerField(
        "Игнор голосования:", blank=True, default=0
    )

    def save(self, *args, **kwargs) -> None:
        constants = RatingCalculateConstant.objects.first()
        if constants is None:
            constants = RatingCalculateConstant.objects.create(
                reg_time=1,
                orders=1,
                peace_orders=-10,
                arbit=-50,
                contest=10,
                wins_1_place=60,
                wins_2_place=40,
                wins_3_place=10,
                review_positive=1,
                review_negative=-5,
                reply_time_1_hour=0,
                reply_time_6_hour=0,
                reply_time_more=-1,
                vote_participation=5,
                vote_ignore=-10,
            )
        self.review_negative_value = self.freelancer.review_executor.filter(
            status="NT"
        ).count()
        self.review_positive_value = self.freelancer.review_executor.filter(
            status="PT"
        ).count()
        self.vote_participation_value = self.freelancer.voites.count()
        self.wins_1_place_value = self.freelancer.contest_responses.filter(
            executor_place="FP"
        ).count()
        self.wins_2_place_value = self.freelancer.contest_responses.filter(
            executor_place="SC"
        ).count()
        self.wins_3_place_value = self.freelancer.contest_responses.filter(
            executor_place="TP"
        ).count()
        self.reviews = (
            self.review_positive_value * constants.review_positive
            + self.review_negative_value * constants.review_negative
        )
        self.reg_time = (
            relativedelta(dt.now().date(), self.freelancer.date_joined).months
            * constants.reg_time
        )
        self.orders = (
            self.freelancer.order_responses.filter(
                executor_status="EX", order__status="CP"
            ).count()
            * constants.orders
        )
        # self.reply_time = (
        #     self.freelancer.order_responses.
        # ) нужно продумать оптимальный ORM запрос
        self.vote_participation = (
            self.vote_participation_value * constants.vote_participation
        )  # не понятно как отследить игнор голосования

        self.wins = (
            self.wins_1_place_value * constants.wins_1_place
            + self.wins_2_place_value * constants.wins_2_place
            + self.wins_3_place_value * constants.wins_3_place
        )
        # self.arbit не раелизовано
        # self.peace_orders не реализовано
        return super().save(*args, **kwargs)
