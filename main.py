import pandas as pd
from opencage.geocoder import OpenCageGeocode
from math import sqrt
import folium

key = '046974c5028244bdb4b99e82a9f971ee'
geocoder = OpenCageGeocode(key)


def read_sel_year(file_path, inp_year=2006):
    """
    Returns a dataframe, with movies of a chosen year.
    """
    df = pd.read_csv(file_path, error_bad_lines=False, warn_bad_lines=False)[::10]
    del df['add_info']
    new_df = df.loc[df['year'] == str(inp_year)]
    del new_df['year']
    return new_df[new_df.location != 'NO DATA']


def get_us_location():
    """
    (None) -> (list)
    Collects coordinates of a location, chosen by the user.
    """
    inp_loc = input('Please enter your location (format: lat, long): ').split(',')
    return inp_loc


def find_distance(coord_1, coord_2):
    """
    (list, list) -> (float)
    Calculates the distance between two points,
    given their coordinates in the lists.
    >>> find_distance([50.411778, 30.469194], [49.83826, 24.02324])
    6.471417608719129
    """
    diff_1 = float(coord_1[0]) - float(coord_2[0])
    diff_2 = float(coord_1[1]) - float(coord_2[1])
    return sqrt(diff_1**2 + diff_2**2)


def main_func_1():
    """
    (None) -> (list)
    """
    given_df = read_sel_year('locations.csv', 2009)

    mov_lst = [mov for mov in given_df['movie']]
    locs_lst = [loc for loc in given_df['location']]
    lst_of_distance = []
    location = get_us_location()
    city_and_country = geocoder.reverse_geocode(location[0], location[1], language="en", no_annotations='1')[0]['formatted']

    ls_of_address = [j.strip() for j in str(city_and_country).split(',')]
    info_zip = list(zip(mov_lst, locs_lst))
    res_lst = []
    for j in info_zip:
        el_var = j[1].split()[-1].strip()
        if el_var == ls_of_address[-1]:
            res_lst.append(j)

    i = 0
    final_list_of_locs = []
    while i < len(res_lst):
        try:
            address = res_lst[i][1]
            result = geocoder.geocode(address, no_annotations='1')
            longitude = result[0]['geometry']['lng']
            latitude = result[0]['geometry']['lat']
            coords = [latitude, longitude]
            final_list_of_locs.append(coords)
            lst_of_distance.append(find_distance(coords, location))
        except IndexError:
            pass
        i += 1

    lst_of_movies = [i[0] for i in res_lst]
    lst_of_locats = [j[1] for j in res_lst]
    final_lst_zip = list(zip(lst_of_movies, lst_of_locats, lst_of_distance))
    df_with_dist = pd.DataFrame(final_lst_zip, columns=['movie', 'location', 'distance'])
    final_df = df_with_dist.sort_values(by='distance')[:10]
    final_list_of_films = [i for i in final_df['movie']]
    final_list = zip(list(final_list_of_films, final_list_of_locs))
    return final_list