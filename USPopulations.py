import pandas as pd
import geemap
import ee


class USPopulations:
    def __init__(self, col='8b0000'):
        self.mep_type = False
        self.col = col
        self.df = pd.read_csv('./assets/USPopulations.csv')

        self.mep = geemap.Map()
        self.mep.add_basemap('Esri.NatGeoWorldMap')

        self.nlcd = ee.ImageCollection("USFS/GTAC/LCMS/v2022-8")
        self.land = self.nlcd.filterDate('2021', '2022').filter(
            'study_area == "CONUS"').first()
        self.land = self.land.select('Land_Use').eq(2)

    def show(self):
        return self.mep

    def sim_plague(self):
        self.land = self.land.updateMask(self.land).visualize(palette=self.col)
        self.mep.addLayer(self.land, {}, 'Plague')

        ee_list = self.df.apply(lambda row: ee.Feature(ee.Geometry.Point(
            [row['LONG'], row['LAT']]), {'POPULATION': row['POPULATION']}), axis=1).tolist()
        city_fc = ee.FeatureCollection(ee_list)
        heatMap = ee.Image().float().paint(city_fc, 'POPULATION')
        heatmap_vis = {
            'min': 0,
            'max': float(self.df['POPULATION'].max()),
            'palette': [self.col]
        }
        self.mep.addLayer(heatMap, heatmap_vis, 'Population Density Heatmap')

        self.mep.clear_controls()
        self.mep.setCenter(-98.5795, 39.8283, 4)
        return self.mep

    def calculate_cover(self, circle):
        points = self.df.apply(
            lambda row: {'LONG': row['LONG'], 'LAT': row['LAT']}, axis=1).to_list()

        ee_fc = ee.FeatureCollection(
            [ee.Geometry.Point([point['LONG'], point['LAT']]) for point in points])
        contained_points = ee_fc.filterBounds(circle)
        contained_indices = contained_points.toList(contained_points.size()).map(
            lambda feature: ee.Feature(feature).get('system:index')).getInfo()

        self.PTS = contained_points
        return self.df.iloc[contained_indices]['POPULATION'].sum()

    def find_closest_radius(self, target, center):
        self.CENTER = ee.Geometry.Point(*center)
        self.CC = center
        # MAX_RADIUS = 2750000 # USE RARELY
        MAX_RADIUS = 4750000
        MIN_RADIUS = 1000

        def bad_rem(a, b):
            FACTOR = 10
            if abs((a - b)/100) < FACTOR:
                return False

            return True

        left = MIN_RADIUS
        right = MAX_RADIUS
        reg = None
        cover = 0
        itr = 20

        while bad_rem(cover, target) and itr > 0:
            itr -= 1
            rad = (right + left) / 2

            reg = ee.FeatureCollection(self.CENTER.buffer(rad))
            cover = self.calculate_cover(reg)

            if cover > target:
                right = rad
            else:
                left = rad

        self.apx_error = abs(cover - target) / 100
        self.rad = rad

        return self.rad

    def shade(self):
        self.roi = ee.FeatureCollection(self.CENTER.buffer(self.rad))
        self.mep.setCenter(*self.CC, zoom=6)

        self.mep.addLayer(self.PTS, {'color': self.col}, 'Pops')

    def simulate(self, target, center):
        self.find_closest_radius(target, center)
        self.shade()
        return self.show()
