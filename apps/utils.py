import random
import string
from django.utils.text import slugify

def generate_slug(name, max_length=50):
    """
    Génère un slug basé sur le nom fourni et limite sa longueur.

    :param name: Le nom à convertir en slug.
    :param max_length: La longueur maximale du slug.
    :return: Un slug formaté et tronqué si nécessaire.
    """
    slug = slugify(name)
    if len(slug) > max_length:
        slug = slug[:max_length].rstrip('-')  # Tronquer et enlever les tirets de fin
    return slug

def remove_html_tags(text):
    """Remove html tags from a string"""
    import re

    clean = re.compile("<.*?>")
    string = re.sub(clean, "", text)
    return string.encode("utf-8", "ignore").decode("utf-8")


def get_utf8_standardized_string(string):
    string = "".join(e for e in string if (e.isalnum() or e.isspace()))
    return string.encode("utf-8", "ignore").decode("utf-8")


def generate_username(email):
    """Allows you to retrieve the email address and generate a random username with this address"""
    username = ""

    part_one = email.split("@")[0]
    bad_characters = ".'!?"

    username += "".join(x for x in part_one if x not in bad_characters)
    end = "".join(random.sample(string.ascii_lowercase + string.digits, 6))
    username += "_" + end
    return username


def get_common_tags(article_tags, size):
    common_tags = []
    dict_tags = count_to_dict(article_tags, False)
    tags_sorted = dict(
        sorted(dict_tags.items(), key=lambda item: item[1], reverse=True)
    )

    for tag in tags_sorted.keys():
        common_tags.append(tag)
        if len(common_tags) == size:
            break
    return common_tags


def count_to_dict(lst, if_occurency):
    if if_occurency is True:
        return {k: lst.count(k) for k in lst}
    else:
        return {k: (lst.count(k)) for k in lst}
