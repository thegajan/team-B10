from django.shortcuts import render
from .placesapi import search_places
import datetime
from .display_utils import *
import json
from .display_utils import format_schedule
from collections import namedtuple
Attraction = namedtuple('Attraction', ['places_id','lat','lon', 'score', 'is_restaurant'])
attr_info = namedtuple('attr_info', ['name','location'])

def home(request):
    return render(request, 'maps/home.html')

def maps(request):
    return render(request, 'maps/maps.html')

def survey(request):
    return render(request, 'maps/survey.html')

def loading(request):
    return render(request, 'maps/loading.html')

def display(request):
    # NEEDS: VALIDATION/DEFUALT VALUES
    # get data from url
    dest_and_dates = json.loads(request.GET['dest_and_dates'])
    survey_result = json.loads(request.GET['survey_result'])

    destination = dest_and_dates['destination']
    lat = dest_and_dates['cityLat'][0]
    lon = dest_and_dates['cityLng'][0]
    start_date = dest_and_dates['date'][0]
    end_date = dest_and_dates['date'][1]
    num_days = days_between(start_date, end_date)

    start_in_time = datetime.datetime.strptime(survey_result['start_day'], "%I:%M %p")
    start_out_time = datetime.datetime.strftime(start_in_time, "%H:%M:%S")
    end_in_time = datetime.datetime.strptime(survey_result['end_day'], "%I:%M %p")
    end_out_time = datetime.datetime.strftime(end_in_time, "%H:%M:%S")

    hours = (start_out_time, end_out_time)
    hours_mod = (time_string_to_decimals(start_out_time), time_string_to_decimals(end_out_time))
    k_attractions = survey_result['number_of_attractions']
    have_breakfast = survey_result['have_breakfast']
    k_restaurants = 3 if have_breakfast else 2

    # places api search
    radius = 16093
    api = 'AIzaSyB0Y13M5LBvl2gVR0c0eZVOyPAgBaEj8cs'
    attrs = search_places(str(lat) + ',' + str(lon), radius, 'tourist_attraction', api)
    rests = search_places(str(lat) + ',' + str(lon), radius, 'restaurant', api)

    # format attrs and rests
    attrs_tup = attr_to_tup(attrs)
    rests_tup = attr_to_tup(rests, True)
    attrs_and_rests = attrs_tup + rests_tup

    # clustering
    attraction_list_clusters, centroids = clustering(num_days, have_breakfast, k_attractions, attrs_and_rests)
    # get hotel
    hotel_dict = find_hotel(centroids, api, radius)
    hotel_tup = attr_to_tup([hotel_dict], True)[0]

    # scheduling
    schedules = scheduling(attraction_list_clusters, int(k_attractions), k_restaurants, hotel_tup, hours_mod)


    placeid_dict = make_dict(attrs+rests)
    schedule_list = []
    tpa_list = []
    tpr_list = []
    hotel_name = hotels[0]['name']
    #*******replace code below******#
    schedule = [([0.4057137091336608, Attraction(places_id='asdf', lat=-2.180228205246836, lon=-4.001666389604681, score=9.053986522844989, is_restaurant=False), 0.618172714241416, Attraction(places_id='asdf', lat=-2.0089966827975267, lon=-4.454155118915776, score=7.692790899139238, is_restaurant=False), 0.18392860891624427, Attraction(places_id='asdf', lat=0.008785250829872604, lon=-9.653201360155721, score=4.362757934152183, is_restaurant=True), 0.6726163323730452, Attraction(places_id='asdf', lat=-4.136568449219548, lon=-3.0182693918292927, score=9.696860772658779, is_restaurant=False), 0.593984777603214, Attraction(places_id='asdf', lat=0.08295751400808903, lon=-13.795694847641734, score=8.201901844338309, is_restaurant=False), 0.7666097393775685, Attraction(places_id='asdf', lat=-4.377386483269133, lon=-11.215880617868779, score=8.520866189293686, is_restaurant=True), 0.2900272346606112, Attraction(places_id='asdf', lat=-7.857630136177638, lon=-11.921656543232203, score=9.091532756367794, is_restaurant=False), 0.7456485112476189], 1.3879094823357863, 0.8918754803838448),
                ([0.4057137091336608, Attraction(places_id='asdf', lat=-2.180228205246836, lon=-4.001666389604681, score=9.053986522844989, is_restaurant=False), 0.618172714241416, Attraction(places_id='asdf', lat=-2.0089966827975267, lon=-4.454155118915776, score=7.692790899139238, is_restaurant=False), 0.18392860891624427, Attraction(places_id='asdf', lat=0.008785250829872604, lon=-9.653201360155721, score=4.362757934152183, is_restaurant=True), 0.6726163323730452, Attraction(places_id='asdf', lat=-4.136568449219548, lon=-3.0182693918292927, score=9.696860772658779, is_restaurant=False), 0.593984777603214, Attraction(places_id='asdf', lat=0.08295751400808903, lon=-13.795694847641734, score=8.201901844338309, is_restaurant=False), 0.7666097393775685, Attraction(places_id='asdf', lat=-4.377386483269133, lon=-11.215880617868779, score=8.520866189293686, is_restaurant=True), 0.2900272346606112, Attraction(places_id='asdf', lat=-7.857630136177638, lon=-11.921656543232203, score=9.091532756367794, is_restaurant=False), 0.7456485112476189], 1.3879094823357863, 0.8918754803838448)]
    placeid_dict['asdf'] = attr_info('attr_name', 'loc_name')
    #*******************************#

    for schedule_day in schedule:
        schedule_list.append(schedule_day[0])
        tpa_list.append(schedule_day[1])
        tpr_list.append(schedule_day[2])

    events_list = format_schedule(start_date, end_date, placeid_dict, schedule_list, tpa_list, tpr_list, hotel_name, start_out_time, end_out_time)
    return render(request, 'maps/display.html', {'itinerary_in_json': json.dumps(events_list)})

def about(request):
    return render(request, 'maps/about.html', {'title': 'About'})
