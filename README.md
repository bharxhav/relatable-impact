# Relatable Impact!

Watch [this](https://youtu.be/UT_-BeZl2o4) `5min` YouTube video for the premise of the project.
[![bk2899](./assets/meta/thumbnail.jpeg)](https://www.youtube.com/watch?v=UT_-BeZl2o4)

---

# Case Studies

I hope you found the video helpful. It can seem daunting to visualize so many datapoints, or to even find the landcover for your required population count. I went an extra mile, and created two libraries which you can call to __optimally__ find desired `region-of-interest`.

The added advantage of using this library is that you can play around with the widget in your jupyter notebook, all you have to do is grant Google Earth Engine permissions to your google cloud platform so that it can render your desired results.

## SPACE

What if the Australian BushFires of 2019-20 happened in NYC.

```python
bands = [3]
nyc = (-73.968285, 40.785091)
aus_cover = 59000

USLandCover().simulate(bands, aus_cover, nyc)
```

![NYC Bushfire](./assets/meta/nyc-bf.jpeg)

Extra MILE: Showing the number of trees the [Team Trees](https://teamtrees.org/) planted.

```python
bands = [3]
nyc = (-73.968285, 40.785091)
tt_cover = 244.95

USLandCover('008b00').simulate(bands, tt_cover, nyc)
```

![NYC TT](assets/meta/nyc-tt.jpeg)

## TIME

What if the Spanish Plague reappeared.

```python
USPopulations().sim_plague()
```

![US Spanish Plague](./assets/meta/us-sp.jpeg)

## REALITY

What if Genghis Khan sailed to US instead of Columbus.

```python
nyc = (-73.968285, 40.785091)
gg_dt = 40000000

USPopulations().simulate(gg_dt, nyc)
```

![NYC Genghis Khan](./assets/meta/nyc-gk.jpeg)

## GOOD STUFF

```python
up = USPopulations('FFFF00')
up.mep.add_basemap('CartoDB.DarkMatter')
up.sim_plague()
```

![US DIWALI](assets/meta/us-diwali.png)

---

# Credits

All the data are as latest as possible. The population data was released on Jul 2023, corresponding to 2022 closing populations.

Population Data: [US Gov](https://www.census.gov/data/tables/time-series/demo/popest/2020s-total-cities-and-towns.html)

Geemap Library: [geemap](https://geemap.org/)
