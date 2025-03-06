from django.db import models

class PCConfigurator(models.Model):
    name = models.CharField(max_length=200, verbose_name="Название ПК")
    description = models.TextField(verbose_name="Описание")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена")
    category = models.CharField(
        max_length=50,
        choices=[
            ('cheap', 'Недорогие ПК'),
            ('gaming', 'Игровые ПК'),
            ('powerful', 'Мощные ПК'),
            ('amd', 'ПК на базе AMD'),
        ],
        verbose_name="Категория"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")

    def __str__(self):
        return f"{self.name} - {self.category}"

class Component(models.Model):
    COMPONENT_TYPE_CHOICES = [
        ('cpu', 'Процессор'),
        ('cooling', 'Охлаждение'),
        ('motherboard', 'Материнская плата'),
        ('ram', 'Оперативная память'),
        ('gpu', 'Видеокарта'),
        ('hdd', 'Жёсткий диск'),
        ('ssd', 'SSD диск'),
        ('psu', 'Блок питания'),
        ('case', 'Корпус'),
        ('wifi', 'Wi-Fi адаптер'),
        ('sound_card', 'Звуковая карта'),
        ('os', 'Операционная система'),
        ('mouse', 'Мышь'),
        ('keyboard', 'Клавиатура'),
        ('monitor', 'Монитор'),
        ('headset', 'Гарнитура')
    ]

    name = models.CharField(max_length=255, verbose_name="Название компонента")
    component_type = models.CharField(max_length=20, choices=COMPONENT_TYPE_CHOICES, verbose_name="Тип компонента")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")

    def __str__(self):
        return self.name

class PCConfiguration(models.Model):
    cpu = models.ForeignKey(Component, on_delete=models.SET_NULL, null=True, blank=True, related_name='cpus', limit_choices_to={'component_type': 'cpu'}, verbose_name="Процессор")
    cooling = models.ForeignKey(Component, on_delete=models.SET_NULL, null=True, blank=True, related_name='coolings', limit_choices_to={'component_type': 'cooling'}, verbose_name="Охлаждение")
    motherboard = models.ForeignKey(Component, on_delete=models.SET_NULL, null=True, blank=True, related_name='motherboards', limit_choices_to={'component_type': 'motherboard'}, verbose_name="Материнская плата")
    ram = models.ForeignKey(Component, on_delete=models.SET_NULL, null=True, blank=True, related_name='rams', limit_choices_to={'component_type': 'ram'}, verbose_name="Оперативная память")
    gpu = models.ForeignKey(Component, on_delete=models.SET_NULL, null=True, blank=True, related_name='gpus', limit_choices_to={'component_type': 'gpu'}, verbose_name="Видеокарта")
    hdd = models.ForeignKey(Component, on_delete=models.SET_NULL, null=True, blank=True, related_name='hdds', limit_choices_to={'component_type': 'hdd'}, verbose_name="Жёсткий диск")
    ssd = models.ForeignKey(Component, on_delete=models.SET_NULL, null=True, blank=True, related_name='ssds', limit_choices_to={'component_type': 'ssd'}, verbose_name="SSD диск")
    psu = models.ForeignKey(Component, on_delete=models.SET_NULL, null=True, blank=True, related_name='psus', limit_choices_to={'component_type': 'psu'}, verbose_name="Блок питания")
    case = models.ForeignKey(Component, on_delete=models.SET_NULL, null=True, blank=True, related_name='cases', limit_choices_to={'component_type': 'case'}, verbose_name="Корпус")
    wifi = models.ForeignKey(Component, on_delete=models.SET_NULL, null=True, blank=True, related_name='wifis', limit_choices_to={'component_type': 'wifi'}, verbose_name="Wi-Fi адаптер")
    sound_card = models.ForeignKey(Component, on_delete=models.SET_NULL, null=True, blank=True, related_name='sound_cards', limit_choices_to={'component_type': 'sound_card'}, verbose_name="Звуковая карта")
    os = models.ForeignKey(Component, on_delete=models.SET_NULL, null=True, blank=True, related_name='oss', limit_choices_to={'component_type': 'os'}, verbose_name="Операционная система")
    mouse = models.ForeignKey(Component, on_delete=models.SET_NULL, null=True, blank=True, related_name='mouses', limit_choices_to={'component_type': 'mouse'}, verbose_name="Мышь")
    keyboard = models.ForeignKey(Component, on_delete=models.SET_NULL, null=True, blank=True, related_name='keyboards', limit_choices_to={'component_type': 'keyboard'}, verbose_name="Клавиатура") # Добавлено on_delete
    monitor = models.ForeignKey(Component, on_delete=models.SET_NULL, null=True, blank=True, related_name='monitors', limit_choices_to={'component_type': 'monitor'}, verbose_name="Монитор")
    headset = models.ForeignKey(Component, on_delete=models.SET_NULL, null=True, blank=True, related_name='headsets', limit_choices_to={'component_type': 'headset'}, verbose_name="Гарнитура")

    configurator = models.ForeignKey(
        PCConfigurator,
        on_delete=models.CASCADE,
        related_name="configurations"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")

    @property
    def total_price(self):
        components = [
            self.cpu, self.cooling, self.motherboard, self.ram, self.gpu,
            self.hdd, self.ssd, self.psu, self.case, self.wifi,
            self.sound_card, self.os, self.mouse, self.keyboard,
            self.monitor, self.headset
        ]
        return sum(component.price for component in components if component)

    def __str__(self):
        return f"Конфигурация ПК #{self.id} (Цена: {self.total_price} руб.)"

