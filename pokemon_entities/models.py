from django.db import models


class Pokemon(models.Model):
    title_ru = models.CharField(max_length=200, verbose_name='Имя на русском')
    title_en = models.CharField(max_length=200, verbose_name='Имя на английском', blank=True)
    title_jp = models.CharField(max_length=200, verbose_name='Имя на японском', blank=True)
    image = models.ImageField(upload_to='pokemons', blank=True, verbose_name='Картинка покемона')
    description = models.TextField(blank=True, verbose_name='Описание')
    evolution_from= models.ForeignKey('Pokemon', null=True, related_name='evolutions', blank=True, on_delete=models.SET_NULL, verbose_name='Эволюционировал из')
    
    def __str__(self):
        return f"{self.title.ru}"

class PokemonEntity(models.Model):
    latitude = models.FloatField(verbose_name='Координата широты')
    longitude = models.FloatField(verbose_name='Координата долготы')
    pokemon = models.ForeignKey(Pokemon, on_delete=models.CASCADE, verbose_name='Покемон', related_name='pokemon_entities')
    appeared_at = models.DateTimeField(null=True, verbose_name='Время появления')
    disappeared_at = models.DateTimeField(null=True, verbose_name='Время исчезновения')
    level = models.IntegerField(null=True, blank=True, verbose_name='Уровень')
    health = models.IntegerField(null=True, blank=True, verbose_name='Здоровье')
    strength = models.IntegerField(null=True, blank=True, verbose_name='Сила')
    defence = models.IntegerField(null=True, blank=True, verbose_name='Защита')
    stamina = models.IntegerField(null=True, blank=True, verbose_name='Выносливость')

    def __str__(self):
        return "Pokemon {}_{} level {}".format(self.pokemon, self.id, self.level)
    