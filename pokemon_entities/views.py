import folium
import json
import os

from django.http import HttpResponseNotFound
from django.shortcuts import render
from pokemon_entities.models import Pokemon, PokemonEntity

MOSCOW_CENTER = [55.751244, 37.618423]
DEFAULT_IMAGE_URL = "https://vignette.wikia.nocookie.net/pokemon/images/6/6e/%21.png/revision/latest/fixed-aspect-ratio-down/width/240/height/240?cb=20130525215832&fill=transparent"

def add_pokemon(folium_map, lat, lon, name, image_url=DEFAULT_IMAGE_URL):
    icon = folium.features.CustomIcon(
        image_url,
        icon_size=(50, 50),
    )
    folium.Marker(
        [lat, lon],
        tooltip=name,
        icon=icon,
    ).add_to(folium_map)


def show_all_pokemons(request):
    pokemons = PokemonEntity.objects.all()
    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    for pokemon_entity in pokemons:
        add_pokemon(
            folium_map, pokemon_entity.latitude, pokemon_entity.longitude,
            pokemon_entity.pokemon.title_ru, request.build_absolute_uri(pokemon_entity.pokemon.image.url),)
    pokemons = Pokemon.objects.all()
    pokemons_on_page = []
    for pokemon in pokemons:
        if pokemon.image:
            pokemons_on_page.append({
                'pokemon_id': pokemon.id,
                'img_url': pokemon.image.url,
                'title_ru': pokemon.title_ru,
            })

    return render(request, "mainpage.html", context={
        'map': folium_map._repr_html_(),
        'pokemons': pokemons_on_page,
    })


def show_pokemon(request, pokemon_id):
    pokemon = Pokemon.objects.get(id=pokemon_id)
    evolution_from = pokemon.evolution_from
    evolution_to = pokemon.evolutions.all()

    if evolution_to:
        evolution_to = {
            "title_ru": evolution_to[0].title_ru,
            "pokemon_id": evolution_to[0].id,
            "img_url": evolution_to[0].image.url
        }

    if evolution_from:
        evolution_from = {
            "title_ru": evolution_from.title_ru,
            "pokemon_id": evolution_from.id,
            "img_url": evolution_from.image.url
        }
    pokemon_info = {
        'pokemon_id': pokemon_id,
        'img_url': pokemon.image.url,
        'title_ru': pokemon.title_ru,
        'title_en': pokemon.title_en,
        'title_jp': pokemon.title_jp,
        'description': pokemon.description,
        'next_evolution': evolution_to,
        'previous_evolution': evolution_from
    }

    pokemon_entities = PokemonEntity.objects.select_related('pokemon').filter(pokemon=pokemon)

    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    for pokemon_entity in pokemon_entities:
        add_pokemon(
            folium_map, pokemon_entity.latitude, pokemon_entity.longitude,
            pokemon_entity.pokemon.title_ru, pokemon_entity.pokemon.image.path)

    return render(request, "pokemon.html", context={'map': folium_map._repr_html_(),
                                                    'pokemon': pokemon_info})
