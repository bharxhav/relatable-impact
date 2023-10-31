import pandas as pd
import geemap
import ee


class USLandCover:
    def __init__(self, col='8b0000'):
        self.mep_type = False
        self.col = col

        self.mep = geemap.Map()
        self.mep.add_basemap('Hybrid')

        self.nlcd = ee.ImageCollection("USFS/GTAC/LCMS/v2022-8")
        self.land = self.nlcd.filterDate('2021', '2022').filter(
            'study_area == "CONUS"').first()
        self.land = self.land.select('Land_Use')

    def show(self):
        return self.mep

    def calculate_cover(self, attributes, reg):
        self.df = geemap.image_area_by_group(self.land, scale=1000, groups=attributes, verbose=False,
                                             denominator=1e6, decimal_places=4, region=reg)

        return self.df.area.sum()

    def find_closest_radius(self, attributes, target, center):
        self.CENTER = ee.Geometry.Point(*center)
        self.CC = center
        MAX_RADIUS = 2750000
        MIN_RADIUS = 1000

        def bad_rem(a, b):
            FACTOR = 0.1
            if abs((a - b)/100) < FACTOR:
                return False

            return True

        left = MIN_RADIUS
        right = MAX_RADIUS
        reg = None
        cover = 0

        while bad_rem(cover, target):
            rad = (right + left) / 2

            reg = ee.FeatureCollection(self.CENTER.buffer(rad))
            cover = self.calculate_cover(attributes, reg)

            if cover > target:
                right = rad
            else:
                left = rad

        self.apx_error = abs(cover - target) / 100
        self.rad = rad

        return self.rad

    def shade(self):
        self.roi = ee.FeatureCollection(self.CENTER.buffer(self.rad))
        self.mep.setCenter(*self.CC)

        class_palette = [0, 1, 2, 3, 4, 5, 6]
        vis_params = {
            'min': 1,
            'max': 7,
            'palette': ['e68a00', '000000', self.col, '97ffff', 'a1a1a1', 'c2b34a', '1b1716'],
        }

        self.land = self.land.remap(
            class_palette, list(range(len(class_palette))))
        self.land_clipped = self.land.clip(self.roi)

        self.mep.addLayer(self.land_clipped, vis_params, 'NLCD Land Use 2022')
        self.mep.setCenter(*self.CC, 7)

    def simulate(self, attributes, target, center):
        self.find_closest_radius(attributes, target, center)
        self.shade()
        return self.show()
