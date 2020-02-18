"""
This module operates over a csv file and the user input
of his location and year of the films he would like to check.
The locations of the those films are to be displayed on the map.
"""
from math import sqrt

import folium
import pandas as pd
from opencage.geocoder import OpenCageGeocode

KEY = '69c11d0466ce4af7a4f5e8dd41be807b'
GEOCODER = OpenCageGeocode(KEY)


def read_sel_year(file_path, inp_year=2006):
    """
    Returns a dataframe, with movies of a chosen year.
    """
    init_df = pd.read_csv(file_path, error_bad_lines=False, warn_bad_lines=False)[::10]
    del init_df['add_info']
    new_df = init_df.loc[init_df['year'] == str(inp_year)]
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
    return sqrt(diff_1 ** 2 + diff_2 ** 2)


def main_func_1(loc, inp_year):
    """
    (None) -> (list)
    Returns a list of lists, containing the closest to the loc
    movies' names and their locations.
    """
    given_df = read_sel_year('locations.csv', inp_year)

    mov_lst = [mov for mov in given_df['movie']]
    locs_lst = [loc for loc in given_df['location']]
    lst_of_distance = []

    print("Map is generating...")
    print("Please wait...")
    city_and_country = GEOCODER.reverse_geocode(loc[0], loc[1], language="en", no_annotations='1')[0]['formatted']

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
            result = GEOCODER.geocode(address, no_annotations='1')
            longitude = result[0]['geometry']['lng']
            latitude = result[0]['geometry']['lat']
            coords = [latitude, longitude]
            final_list_of_locs.append(coords)
            lst_of_distance.append(find_distance(coords, loc))
        except IndexError:
            pass
        i += 1

    lst_of_movies = [i[0] for i in res_lst]
    lst_of_locats = [j[1] for j in res_lst]
    final_lst_zip = list(zip(lst_of_movies, lst_of_locats, lst_of_distance))
    df_with_dist = pd.DataFrame(final_lst_zip, columns=['movie', 'location', 'distance'])
    final_df = df_with_dist.sort_values(by='distance')[:10]
    final_list_of_films = [i for i in final_df['movie']]
    final_list = list(zip(final_list_of_films, final_list_of_locs))
    return final_list


def add_to_map(lst_to_map, inp_loc):
    """

    :param lst_to_map:
    :return:
    """
    user_loc = [float(inp_loc[0]), float(inp_loc[1])]
    result_map = folium.Map(location=user_loc,
                            zoom_start=10)
    fg_mp = folium.FeatureGroup(name="World map")
    fg_mv = folium.FeatureGroup(name="Movie locations")
    result_map.add_child(folium.CircleMarker(location=user_loc,
                                             radius=10,
                                             popup='I am here',
                                             icon=folium.Icon(),
                                             color='green',
                                             fill_opacity=0.5))
    for film, film_loc in lst_to_map:
        fg_mv.add_children(folium.CircleMarker(location=film_loc,
                                               radius=14,
                                               popup=film,
                                               color='red',
                                               fill_opacity=0.8))
    result_map.add_child(fg_mv)
    result_map.add_child(fg_mp)
    result_map.save('Map_1.html')


if __name__ == "__main__":
    YEAR = int(input("Please enter a year you would like to have a map for: "))
    LOCATION = get_us_location()
    RESULT = main_func_1(LOCATION, YEAR)
    add_to_map(RESULT, LOCATION)
    print("Finished. Please have look at the map" + str(YEAR) + "_movies_map.html")
