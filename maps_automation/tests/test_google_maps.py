import time
import pytest
from maps_automation.pages.google_maps_page import GoogleMapsPage
from maps_automation.utils.helpers import coords_close

@pytest.fixture(autouse=True)
def setup(driver):
    page = GoogleMapsPage(driver)
    page.open_maps()
    return page

#Search for a specific address and verify search suggestions & map zooms in, also marker points to the right location
def test_search_city_and_verify_zoom(driver, setup):
    page = setup

    # calculating the lan/lon/zoom coordinates before making any action in the map & will be compared with
    # lan/lon/coordinates after that action
    before_lat, before_lon, before_zoom = page.parse_lat_lon_from_url()

    page.search_location("528 Pontius Ave N", False)
    suggestions = page.collect_suggestions_list()

    assert len(suggestions) > 0, "No autocomplete results shown"

    top_text = suggestions[0].text
    assert "528" in top_text, "Autocomplete suggestions irrelevant"

    after_lat, after_lon, after_zoom = page.parse_lat_lon_from_url()

    assert after_zoom and (after_zoom > before_zoom or after_zoom > 5), "Map did not zoom in"
    assert page.is_info_panel_visible(), "Info panel missing after search"


#Verify zoom in/out controls update zoom level in the map
def test_zoom_controls(driver, setup):

    page = setup
    before_lat, before_lon, before_zoom = page.parse_lat_lon_from_url()
    page.zoom_in()
    time.sleep(1) #to allow sometime for the zoom to happen
    after_lat, after_lon, after_zoom = page.parse_lat_lon_from_url()
    assert after_zoom > before_zoom, f"Zoom in failed: {before_zoom} -> {after_zoom}"

    page.zoom_out()
    page.zoom_out()
    time.sleep(1) #to allow sometime for the zoom to happen
    lat3, lon3, zoom3 = page.parse_lat_lon_from_url()
    assert zoom3 < after_zoom, f"Zoom out failed: {after_zoom} -> {zoom3}"

#verify searched location's coordinates
def test_known_location_coordinates(driver, setup):
    page = setup
    page.search_location("T mobile Building 3")
    lat, lon, zoom = page.parse_lat_lon_from_url()
    assert coords_close(lat, lon, 47.5766, -122.1700), f"Incorrect coordinates: {lat}, {lon}"

#simulate map drag & verify its coordinates are changes
def test_pan_map(driver, setup):
    page = setup
    before_lat, before_lon, before_zoom = page.parse_lat_lon_from_url()

    # this is to avoid the following issue
    # as we are using Javascript executor, sometimes it doesn't execute as there are some overlaying elements in the browser
    # to get rid of that element, we are doing a dummy click. So that the focus stays in that dom/canvas
    page.do_dummy_click()

    #map drag via Javascript executor
    page.pan_map(dx=250, dy=0)

    after_lat, after_lon, after_zoom = page.parse_lat_lon_from_url()
    moved = not coords_close(before_lat, before_lon, after_lat, after_lon, tol=1e-5)
    assert moved, f"Map did not move: before=({before_lat},{before_lon}) after=({after_lat},{after_lon})"
