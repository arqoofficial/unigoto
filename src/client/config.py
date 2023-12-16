import os

__all__ = [
    "VERSIONS_MD",
    "ENDPOINT_PING",
    "ENDPOINT_SEARCH",
    "CONTRIBUTORS_MD",
    "LINKS_MD",
    "REQUEST_BODY",
    "USER_INPUT",
    "METRICS",
]

# versions
VERSIONS = [
    {
        "name": "Web",
        "version": "0.0.5",
    },
]
VERSIONS_MD = [f"**{item['name']}** – {item['version']}" for item in VERSIONS]

# api endpoints
ENDPOINT_PING = os.getenv("CLIENT_API_PING_URI")
ENDPOINT_SEARCH = os.getenv("CLIENT_API_SEARCH_URI")

# used in st.markdown()
CONTRIBUTORS = [
    {
        "name": "Туомас Эдвард",
        "github": "https://github.com/ToyOwl",
    },
    {
        "name": "Анисимова Татьяна",
        "github": "https://github.com/t-linguist",
    },
    {
        "name": "Голубев Артём",
        "github": "https://github.com/arqoofficial",
    },
    {
        "name": "Гуков Алексей",
        "github": "https://github.com/brain4power",
    },
    {
        "name": "Колотий Вячеслав",
        "github": "https://github.com/kv49",
    },
    {
        "name": "Ротерман Виктор",
        "github": "https://github.com/ViktorRtm",
    },
]
CONTRIBUTORS_MD = [f"[{item['name']}]({item['github']})" for item in CONTRIBUTORS]

LINKS = [
    {
        "name": "GitHub",
        "link": "https://github.com/brain4power/hackathon_unigoto",
    },
]
LINKS_MD = [f"[{item['name']}]({item['link']})" for item in LINKS]

# input
REQUEST_BODY = {
    "city_title": "",
    "about": "",
    "activities": "",
    "books": "",
    "games": "",
    "interests": "",
    "threshold": 1,
    "limit": 20,
}

USER_INPUT = [
    {
        "option": "city_title",
        "markdown": "Название города",
        "example": "Москва",
    },
    {
        "option": "about",
        "markdown": "О себе",
        "example": "Студент",
    },
    {
        "option": "activities",
        "markdown": "Вид деятельности",
        "example": "Программирование, математика",
    },
    {
        "option": "books",
        "markdown": "Любимые книги",
        "example": "Задачи по математике",
    },
    {
        "option": "games",
        "markdown": "Любимые игры",
        "example": "Стратегии",
    },
    {
        "option": "interests",
        "markdown": "Интересы",
        "example": "Музыка, велосипед",
    },
]

# table
METRICS = [
    "cosine_distance",
]
