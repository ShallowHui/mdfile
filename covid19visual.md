---
title: 世界新冠疫情数据的动态可视化
date: 2020-11-16 10:36:28
tags: 数据可视化
categories: Python
cover: https://cdn.jsdelivr.net/gh/shallowhui/cdn/top_img/python.jpg
description: 用Python中较为流行的matplotlib可视化库来绘制新冠疫情爆发至今，展示世界疫情变化情况的动态可视化地图。
---
## 前言

多余的话也不想多说哈，

**愿大家都平平安安，幸福安康。**

下面就直接开始完成~~Python大作业~~世界新冠疫情数据的动态可视化~

## 数据获取

首先导入绘制图像需要的库：

```python
import requests
import pandas as pd
import matplotlib.pyplot as plt
import geopandas as gpd #基于pandas库的用来绘制地图的库
import io
import PIL #处理图像的库
```

+ 注意，geopandas库的安装比较麻烦，不是简单的`pip`下载安装就能搞定的，请自行百度安装教程。

### 疫情数据集

美国约翰霍普金斯大学在github上公开了他们每日收集到的关于新冠疫情的数据，相关数据可以从以下网址获得：

[https://github.com/CSSEGISandData/COVID-19](https://github.com/CSSEGISandData/COVID-19)

编写在线获取数据的函数：

``` python
def getDataFromGithub():
    #这个url链接的文件是关于新冠疫情爆发至今，世界上每个国家确诊人数的时间线
    url = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv'
    try:
        response = requests.get(url)
        with open('time_series_covid19_confirmed_global.csv','wb') as f:
            f.write(response.content)
    except:
        print('在线获取失败！')
        return -1
```

但由于某些原因，raw.githubusercontent.com域名可能会访问错误，所以我事先准备好了数据文件（直接把github仓库clone下来），然后用下面的函数读取即可：

```python
def getData():
    return pd.read_csv('time_series_covid19_confirmed_global.csv') #返回一个pandas的DataFrame数据类型
```

可以看看数据长啥样：

<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Province/State</th>
      <th>Country/Region</th>
      <th>Lat</th>
      <th>Long</th>
      <th>1/22/20</th>
      <th>1/23/20</th>
      <th>1/24/20</th>
      <th>1/25/20</th>
      <th>1/26/20</th>
      <th>1/27/20</th>
      <th>...</th>
      <th>11/3/20</th>
      <th>11/4/20</th>
      <th>11/5/20</th>
      <th>11/6/20</th>
      <th>11/7/20</th>
      <th>11/8/20</th>
      <th>11/9/20</th>
      <th>11/10/20</th>
      <th>11/11/20</th>
      <th>11/12/20</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>NaN</td>
      <td>Afghanistan</td>
      <td>33.939110</td>
      <td>67.709953</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>...</td>
      <td>41728</td>
      <td>41814</td>
      <td>41935</td>
      <td>41975</td>
      <td>42033</td>
      <td>42092</td>
      <td>42297</td>
      <td>42463</td>
      <td>42609</td>
      <td>42795</td>
    </tr>
    <tr>
      <th>1</th>
      <td>NaN</td>
      <td>Albania</td>
      <td>41.153300</td>
      <td>20.168300</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>...</td>
      <td>21904</td>
      <td>22300</td>
      <td>22721</td>
      <td>23210</td>
      <td>23705</td>
      <td>24206</td>
      <td>24731</td>
      <td>25294</td>
      <td>25801</td>
      <td>26211</td>
    </tr>
    <tr>
      <th>2</th>
      <td>NaN</td>
      <td>Algeria</td>
      <td>28.033900</td>
      <td>1.659600</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>...</td>
      <td>58979</td>
      <td>59527</td>
      <td>60169</td>
      <td>60800</td>
      <td>61381</td>
      <td>62051</td>
      <td>62693</td>
      <td>63446</td>
      <td>64257</td>
      <td>65108</td>
    </tr>
    <tr>
      <th>3</th>
      <td>NaN</td>
      <td>Andorra</td>
      <td>42.506300</td>
      <td>1.521800</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>...</td>
      <td>4910</td>
      <td>5045</td>
      <td>5135</td>
      <td>5135</td>
      <td>5319</td>
      <td>5383</td>
      <td>5437</td>
      <td>5477</td>
      <td>5567</td>
      <td>5616</td>
    </tr>
    <tr>
      <th>4</th>
      <td>NaN</td>
      <td>Angola</td>
      <td>-11.202700</td>
      <td>17.873900</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>...</td>
      <td>11577</td>
      <td>11813</td>
      <td>12102</td>
      <td>12223</td>
      <td>12335</td>
      <td>12433</td>
      <td>12680</td>
      <td>12816</td>
      <td>12953</td>
      <td>13053</td>
    </tr>
    <tr>
      <th>...</th>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
    </tr>
    <tr>
      <th>264</th>
      <td>NaN</td>
      <td>West Bank and Gaza</td>
      <td>31.952200</td>
      <td>35.233200</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>...</td>
      <td>55408</td>
      <td>56090</td>
      <td>56672</td>
      <td>57226</td>
      <td>57657</td>
      <td>58158</td>
      <td>58838</td>
      <td>59422</td>
      <td>60065</td>
      <td>60784</td>
    </tr>
    <tr>
      <th>265</th>
      <td>NaN</td>
      <td>Western Sahara</td>
      <td>24.215500</td>
      <td>-12.885800</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>...</td>
      <td>10</td>
      <td>10</td>
      <td>10</td>
      <td>10</td>
      <td>10</td>
      <td>10</td>
      <td>10</td>
      <td>10</td>
      <td>10</td>
      <td>10</td>
    </tr>
    <tr>
      <th>266</th>
      <td>NaN</td>
      <td>Yemen</td>
      <td>15.552727</td>
      <td>48.516388</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>...</td>
      <td>2063</td>
      <td>2063</td>
      <td>2063</td>
      <td>2067</td>
      <td>2070</td>
      <td>2070</td>
      <td>2071</td>
      <td>2071</td>
      <td>2071</td>
      <td>2071</td>
    </tr>
    <tr>
      <th>267</th>
      <td>NaN</td>
      <td>Zambia</td>
      <td>-13.133897</td>
      <td>27.849332</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>...</td>
      <td>16661</td>
      <td>16698</td>
      <td>16770</td>
      <td>16819</td>
      <td>16908</td>
      <td>16954</td>
      <td>16971</td>
      <td>16997</td>
      <td>17036</td>
      <td>17056</td>
    </tr>
    <tr>
      <th>268</th>
      <td>NaN</td>
      <td>Zimbabwe</td>
      <td>-19.015438</td>
      <td>29.154857</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>...</td>
      <td>8410</td>
      <td>8427</td>
      <td>8444</td>
      <td>8471</td>
      <td>8498</td>
      <td>8531</td>
      <td>8561</td>
      <td>8610</td>
      <td>8667</td>
      <td>8696</td>
    </tr>
  </tbody>
</table>
<p>269 rows × 300 columns</p>
</div>

### 国家地理数据集

现在加载世界上每个国家的地理数据集，以便用geopandas模块绘制出世界地图，注意这里用的地图数据集不是geopandas模块自带的，是从以下网址获取的：

[https://www.naturalearthdata.com/downloads/10m-cultural-vectors/](https://www.naturalearthdata.com/downloads/10m-cultural-vectors/)

如果不知道要下载什么文件，可以直接到我的github上下载`countries`文件夹，放到代码文件目录下：

[https://github.com/ShallowHui/interesting-small-project](https://github.com/ShallowHui/interesting-small-project)

用下面的函数读取数据文件：

```python
def getGeoData():
    world = gpd.read_file('countries') #将下载得到的数据集文件全部放在同目录下的countries文件夹下，然后用geopandas模块读取
    return world #返回一个geopandas模块的GeoDataFrame数据类型
```

看看数据长啥样：

<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>featurecla</th>
      <th>scalerank</th>
      <th>LABELRANK</th>
      <th>SOVEREIGNT</th>
      <th>SOV_A3</th>
      <th>ADM0_DIF</th>
      <th>LEVEL</th>
      <th>TYPE</th>
      <th>ADMIN</th>
      <th>ADM0_A3</th>
      <th>...</th>
      <th>NAME_KO</th>
      <th>NAME_NL</th>
      <th>NAME_PL</th>
      <th>NAME_PT</th>
      <th>NAME_RU</th>
      <th>NAME_SV</th>
      <th>NAME_TR</th>
      <th>NAME_VI</th>
      <th>NAME_ZH</th>
      <th>geometry</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>Admin-0 country</td>
      <td>5</td>
      <td>2</td>
      <td>Indonesia</td>
      <td>IDN</td>
      <td>0</td>
      <td>2</td>
      <td>Sovereign country</td>
      <td>Indonesia</td>
      <td>IDN</td>
      <td>...</td>
      <td>인도네시아</td>
      <td>Indonesië</td>
      <td>Indonezja</td>
      <td>Indonésia</td>
      <td>Индонезия</td>
      <td>Indonesien</td>
      <td>Endonezya</td>
      <td>Indonesia</td>
      <td>印度尼西亚</td>
      <td>MULTIPOLYGON (((117.70361 4.16341, 117.70361 4...</td>
    </tr>
    <tr>
      <th>1</th>
      <td>Admin-0 country</td>
      <td>5</td>
      <td>3</td>
      <td>Malaysia</td>
      <td>MYS</td>
      <td>0</td>
      <td>2</td>
      <td>Sovereign country</td>
      <td>Malaysia</td>
      <td>MYS</td>
      <td>...</td>
      <td>말레이시아</td>
      <td>Maleisië</td>
      <td>Malezja</td>
      <td>Malásia</td>
      <td>Малайзия</td>
      <td>Malaysia</td>
      <td>Malezya</td>
      <td>Malaysia</td>
      <td>马来西亚</td>
      <td>MULTIPOLYGON (((117.70361 4.16341, 117.69711 4...</td>
    </tr>
    <tr>
      <th>2</th>
      <td>Admin-0 country</td>
      <td>6</td>
      <td>2</td>
      <td>Chile</td>
      <td>CHL</td>
      <td>0</td>
      <td>2</td>
      <td>Sovereign country</td>
      <td>Chile</td>
      <td>CHL</td>
      <td>...</td>
      <td>칠레</td>
      <td>Chili</td>
      <td>Chile</td>
      <td>Chile</td>
      <td>Чили</td>
      <td>Chile</td>
      <td>Şili</td>
      <td>Chile</td>
      <td>智利</td>
      <td>MULTIPOLYGON (((-69.51009 -17.50659, -69.50611...</td>
    </tr>
    <tr>
      <th>3</th>
      <td>Admin-0 country</td>
      <td>0</td>
      <td>3</td>
      <td>Bolivia</td>
      <td>BOL</td>
      <td>0</td>
      <td>2</td>
      <td>Sovereign country</td>
      <td>Bolivia</td>
      <td>BOL</td>
      <td>...</td>
      <td>볼리비아</td>
      <td>Bolivia</td>
      <td>Boliwia</td>
      <td>Bolívia</td>
      <td>Боливия</td>
      <td>Bolivia</td>
      <td>Bolivya</td>
      <td>Bolivia</td>
      <td>玻利維亞</td>
      <td>POLYGON ((-69.51009 -17.50659, -69.51009 -17.5...</td>
    </tr>
    <tr>
      <th>4</th>
      <td>Admin-0 country</td>
      <td>0</td>
      <td>2</td>
      <td>Peru</td>
      <td>PER</td>
      <td>0</td>
      <td>2</td>
      <td>Sovereign country</td>
      <td>Peru</td>
      <td>PER</td>
      <td>...</td>
      <td>페루</td>
      <td>Peru</td>
      <td>Peru</td>
      <td>Peru</td>
      <td>Перу</td>
      <td>Peru</td>
      <td>Peru</td>
      <td>Peru</td>
      <td>秘鲁</td>
      <td>MULTIPOLYGON (((-69.51009 -17.50659, -69.63832...</td>
    </tr>
    <tr>
      <th>...</th>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
    </tr>
    <tr>
      <th>250</th>
      <td>Admin-0 country</td>
      <td>0</td>
      <td>4</td>
      <td>China</td>
      <td>CH1</td>
      <td>1</td>
      <td>2</td>
      <td>Country</td>
      <td>Macao S.A.R</td>
      <td>MAC</td>
      <td>...</td>
      <td>마카오</td>
      <td>Macau</td>
      <td>Makau</td>
      <td>Macau</td>
      <td>Макао</td>
      <td>Macao</td>
      <td>Makao</td>
      <td>Ma Cao</td>
      <td>澳門</td>
      <td>MULTIPOLYGON (((113.55860 22.16303, 113.56943 ...</td>
    </tr>
    <tr>
      <th>251</th>
      <td>Admin-0 country</td>
      <td>6</td>
      <td>5</td>
      <td>Australia</td>
      <td>AU1</td>
      <td>1</td>
      <td>2</td>
      <td>Dependency</td>
      <td>Ashmore and Cartier Islands</td>
      <td>ATC</td>
      <td>...</td>
      <td>애시모어 카르티에 제도</td>
      <td>Ashmore- en Cartiereilanden</td>
      <td>Wyspy Ashmore i Cartiera</td>
      <td>Ilhas Ashmore e Cartier</td>
      <td>Острова Ашмор и Картье</td>
      <td>Ashmore- och Cartieröarna</td>
      <td>Ashmore ve Cartier Adaları</td>
      <td>Quần đảo Ashmore và Cartier</td>
      <td>阿什莫尔和卡捷岛</td>
      <td>POLYGON ((123.59702 -12.42832, 123.59775 -12.4...</td>
    </tr>
    <tr>
      <th>252</th>
      <td>Admin-0 country</td>
      <td>6</td>
      <td>8</td>
      <td>Bajo Nuevo Bank (Petrel Is.)</td>
      <td>BJN</td>
      <td>0</td>
      <td>2</td>
      <td>Indeterminate</td>
      <td>Bajo Nuevo Bank (Petrel Is.)</td>
      <td>BJN</td>
      <td>...</td>
      <td>바호 누에보 뱅크</td>
      <td>Bajo Nuevo</td>
      <td>Bajo Nuevo</td>
      <td>Ilha Baixo Novo</td>
      <td>Бахо-Нуэво</td>
      <td>Bajo Nuevo</td>
      <td>Bajo Nuevo Bank</td>
      <td>Bajo Nuevo Bank</td>
      <td>巴霍努埃沃礁</td>
      <td>POLYGON ((-79.98929 15.79495, -79.98782 15.796...</td>
    </tr>
    <tr>
      <th>253</th>
      <td>Admin-0 country</td>
      <td>6</td>
      <td>5</td>
      <td>Serranilla Bank</td>
      <td>SER</td>
      <td>0</td>
      <td>2</td>
      <td>Indeterminate</td>
      <td>Serranilla Bank</td>
      <td>SER</td>
      <td>...</td>
      <td>세라냐 뱅크</td>
      <td>Serranilla</td>
      <td>Isla Serranilla</td>
      <td>Ilha Serranilla</td>
      <td>Серранилья-Банк</td>
      <td>Serranilla Bank</td>
      <td>Serranilla Bank</td>
      <td>Serranilla Bank</td>
      <td>塞拉纳浅滩</td>
      <td>POLYGON ((-78.63707 15.86209, -78.64041 15.864...</td>
    </tr>
    <tr>
      <th>254</th>
      <td>Admin-0 country</td>
      <td>6</td>
      <td>6</td>
      <td>Scarborough Reef</td>
      <td>SCR</td>
      <td>0</td>
      <td>2</td>
      <td>Indeterminate</td>
      <td>Scarborough Reef</td>
      <td>SCR</td>
      <td>...</td>
      <td>스카버러 암초</td>
      <td>Scarborough-rif</td>
      <td>Huangyan Dao</td>
      <td>Recife de Scarborough</td>
      <td>Скарборо-Шол</td>
      <td>Scarboroughrevet</td>
      <td>Scarborough Shoal</td>
      <td>Bãi cạn Scarborough</td>
      <td>黄岩岛</td>
      <td>POLYGON ((117.75389 15.15437, 117.75569 15.151...</td>
    </tr>
  </tbody>
</table>
<p>255 rows × 95 columns</p>
</div>

## 数据清洗

现在我们有了两个数据集，一个关于疫情的，一个是国家地理数据，但这两个数据集都有一些问题：

```python
#两个数据集都是把台湾地区单独列出来的
df = getData()
df[df['Country/Region'].isin(['Taiwan*'])] #在jupyter notebook中写的代码
```

<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Province/State</th>
      <th>Country/Region</th>
      <th>Lat</th>
      <th>Long</th>
      <th>1/22/20</th>
      <th>1/23/20</th>
      <th>1/24/20</th>
      <th>1/25/20</th>
      <th>1/26/20</th>
      <th>1/27/20</th>
      <th>...</th>
      <th>11/3/20</th>
      <th>11/4/20</th>
      <th>11/5/20</th>
      <th>11/6/20</th>
      <th>11/7/20</th>
      <th>11/8/20</th>
      <th>11/9/20</th>
      <th>11/10/20</th>
      <th>11/11/20</th>
      <th>11/12/20</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>235</th>
      <td>NaN</td>
      <td>Taiwan*</td>
      <td>23.7</td>
      <td>121.0</td>
      <td>1</td>
      <td>1</td>
      <td>3</td>
      <td>3</td>
      <td>4</td>
      <td>5</td>
      <td>...</td>
      <td>567</td>
      <td>568</td>
      <td>569</td>
      <td>573</td>
      <td>573</td>
      <td>577</td>
      <td>578</td>
      <td>580</td>
      <td>584</td>
      <td>589</td>
    </tr>
  </tbody>
</table>
<p>1 rows × 300 columns</p>
</div>

``` python
countries = getGeoData()
countries[countries['SOVEREIGNT'].isin(['Taiwan'])] #SOVEREIGNT：主权
```

<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>featurecla</th>
      <th>scalerank</th>
      <th>LABELRANK</th>
      <th>SOVEREIGNT</th>
      <th>SOV_A3</th>
      <th>ADM0_DIF</th>
      <th>LEVEL</th>
      <th>TYPE</th>
      <th>ADMIN</th>
      <th>ADM0_A3</th>
      <th>...</th>
      <th>NAME_KO</th>
      <th>NAME_NL</th>
      <th>NAME_PL</th>
      <th>NAME_PT</th>
      <th>NAME_RU</th>
      <th>NAME_SV</th>
      <th>NAME_TR</th>
      <th>NAME_VI</th>
      <th>NAME_ZH</th>
      <th>geometry</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>185</th>
      <td>Admin-0 country</td>
      <td>0</td>
      <td>3</td>
      <td>Taiwan</td>
      <td>TWN</td>
      <td>0</td>
      <td>2</td>
      <td>Sovereign country</td>
      <td>Taiwan</td>
      <td>TWN</td>
      <td>...</td>
      <td>중화민국</td>
      <td>Taiwan</td>
      <td>Republika Chińska</td>
      <td>Taiwan</td>
      <td>Китайская Республика</td>
      <td>Taiwan</td>
      <td>Çin Cumhuriyeti</td>
      <td>Đài Loan</td>
      <td>中華民國</td>
      <td>MULTIPOLYGON (((121.90577 24.95010, 121.83473 ...</td>
    </tr>
  </tbody>
</table>
<p>1 rows × 95 columns</p>
</div>

以及两个数据集中的国家名不一定对得上：

```python
sum = 0

for country in df['Country/Region']:
    if country not in countries['SOVEREIGNT'].to_list(): #需要将geopandas模块的GeoSeries数据类型转化为列表
        sum = sum + 1
        print(country)

sum
```

    Bahamas
    Burma
    Congo (Brazzaville)
    Congo (Kinshasa)
    Cote d'Ivoire
    Diamond Princess
    Eswatini
    Holy See
    Korea, South
    MS Zaandam
    North Macedonia
    Sao Tome and Principe
    Serbia
    Taiwan*
    Tanzania
    Timor-Leste
    US
    West Bank and Gaza



    18

所以我们要去清洗整理数据，并把两个数据集合并在一起，为此编写了下面这个函数：

```python
def MergeData(df,countries): #接收df：疫情数据集，countries：国家地理数据集
    #将台湾地区设置为中国
    df['Country/Region'].replace('Taiwan*','China',inplace=True)
    countries['SOVEREIGNT'].replace('Taiwan','China',inplace=True)
    
    #删除疫情数据集中的经纬度数据，因为这在地理数据集中有
    df = df.drop(columns=['Lat','Long'])
    #因为疫情数据集中有一些国家是按省份、州进行统计的，一国数据分散，所以要把它们合并
    df = df.groupby('Country/Region').sum()
    
    #简化地理数据集，只用保留坐标列和主权名即可
    countries = countries.drop(columns=[col for col in countries.columns if col not in ['SOVEREIGNT','geometry']])
    #然后尽可能地将地理数据集中的国家名改成跟疫情数据集一样
    countries['SOVEREIGNT'].replace('United States of America','US',inplace=True)
    countries['SOVEREIGNT'].replace('South Korea','Korea, South',inplace=True)
    countries['SOVEREIGNT'].replace('Vatican','Holy See',inplace=True)
    countries['SOVEREIGNT'].replace('eSwatini','Eswatini',inplace=True)
    countries['SOVEREIGNT'].replace('United Republic of Tanzania','Tanzania',inplace=True)
    
    #合并数据集
    return countries.join(df,how='right',on='SOVEREIGNT')
```

两个数据集合并后的样子：

<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>SOVEREIGNT</th>
      <th>geometry</th>
      <th>1/22/20</th>
      <th>1/23/20</th>
      <th>1/24/20</th>
      <th>1/25/20</th>
      <th>1/26/20</th>
      <th>1/27/20</th>
      <th>1/28/20</th>
      <th>1/29/20</th>
      <th>...</th>
      <th>11/3/20</th>
      <th>11/4/20</th>
      <th>11/5/20</th>
      <th>11/6/20</th>
      <th>11/7/20</th>
      <th>11/8/20</th>
      <th>11/9/20</th>
      <th>11/10/20</th>
      <th>11/11/20</th>
      <th>11/12/20</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>129.0</th>
      <td>Afghanistan</td>
      <td>POLYGON ((74.54235 37.02167, 74.54742 37.01567...</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>...</td>
      <td>41728</td>
      <td>41814</td>
      <td>41935</td>
      <td>41975</td>
      <td>42033</td>
      <td>42092</td>
      <td>42297</td>
      <td>42463</td>
      <td>42609</td>
      <td>42795</td>
    </tr>
    <tr>
      <th>63.0</th>
      <td>Albania</td>
      <td>POLYGON ((20.56715 41.87318, 20.54172 41.86158...</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>...</td>
      <td>21904</td>
      <td>22300</td>
      <td>22721</td>
      <td>23210</td>
      <td>23705</td>
      <td>24206</td>
      <td>24731</td>
      <td>25294</td>
      <td>25801</td>
      <td>26211</td>
    </tr>
    <tr>
      <th>121.0</th>
      <td>Algeria</td>
      <td>POLYGON ((-4.82161 24.99506, -4.99519 25.10209...</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>...</td>
      <td>58979</td>
      <td>59527</td>
      <td>60169</td>
      <td>60800</td>
      <td>61381</td>
      <td>62051</td>
      <td>62693</td>
      <td>63446</td>
      <td>64257</td>
      <td>65108</td>
    </tr>
    <tr>
      <th>128.0</th>
      <td>Andorra</td>
      <td>POLYGON ((1.70701 42.50278, 1.69750 42.49446, ...</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>...</td>
      <td>4910</td>
      <td>5045</td>
      <td>5135</td>
      <td>5135</td>
      <td>5319</td>
      <td>5383</td>
      <td>5437</td>
      <td>5477</td>
      <td>5567</td>
      <td>5616</td>
    </tr>
    <tr>
      <th>102.0</th>
      <td>Angola</td>
      <td>MULTIPOLYGON (((13.07370 -4.63532, 13.06533 -4...</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>...</td>
      <td>11577</td>
      <td>11813</td>
      <td>12102</td>
      <td>12223</td>
      <td>12335</td>
      <td>12433</td>
      <td>12680</td>
      <td>12816</td>
      <td>12953</td>
      <td>13053</td>
    </tr>
    <tr>
      <th>...</th>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
    </tr>
    <tr>
      <th>NaN</th>
      <td>West Bank and Gaza</td>
      <td>None</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>...</td>
      <td>55408</td>
      <td>56090</td>
      <td>56672</td>
      <td>57226</td>
      <td>57657</td>
      <td>58158</td>
      <td>58838</td>
      <td>59422</td>
      <td>60065</td>
      <td>60784</td>
    </tr>
    <tr>
      <th>28.0</th>
      <td>Western Sahara</td>
      <td>POLYGON ((-8.81703 27.66146, -8.81654 27.66147...</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>...</td>
      <td>10</td>
      <td>10</td>
      <td>10</td>
      <td>10</td>
      <td>10</td>
      <td>10</td>
      <td>10</td>
      <td>10</td>
      <td>10</td>
      <td>10</td>
    </tr>
    <tr>
      <th>161.0</th>
      <td>Yemen</td>
      <td>MULTIPOLYGON (((51.97861 18.99564, 51.98569 18...</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>...</td>
      <td>2063</td>
      <td>2063</td>
      <td>2063</td>
      <td>2067</td>
      <td>2070</td>
      <td>2070</td>
      <td>2071</td>
      <td>2071</td>
      <td>2071</td>
      <td>2071</td>
    </tr>
    <tr>
      <th>81.0</th>
      <td>Zambia</td>
      <td>POLYGON ((32.92086 -9.40790, 32.92303 -9.46629...</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>...</td>
      <td>16661</td>
      <td>16698</td>
      <td>16770</td>
      <td>16819</td>
      <td>16908</td>
      <td>16954</td>
      <td>16971</td>
      <td>16997</td>
      <td>17036</td>
      <td>17056</td>
    </tr>
    <tr>
      <th>108.0</th>
      <td>Zimbabwe</td>
      <td>POLYGON ((25.25978 -17.79411, 25.26671 -17.800...</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>...</td>
      <td>8410</td>
      <td>8427</td>
      <td>8444</td>
      <td>8471</td>
      <td>8498</td>
      <td>8531</td>
      <td>8561</td>
      <td>8610</td>
      <td>8667</td>
      <td>8696</td>
    </tr>
  </tbody>
</table>
<p>240 rows × 298 columns</p>
</div>

现在就可以用这个合并后的数据集绘制某一天的世界疫情图看看：

``` python
#代码调试是在jupyter上进行的，所以有些变量是一直保持的，至于完整的代码我会在最后放出哈
mergeData = MergeData(df,countries)

fig,ax = plt.subplots(figsize=(23,10))
plt.title('Total confirmed cases of COVID-19 in the World') #设置画布标题
plt.text(-35,-30,'11/11/20',fontdict={'size':26 , 'color':'blue'}) #显示当前日期
mergeData.plot(
    column = '11/11/20', #绘制哪一列的数据
    scheme = 'userdefined', #用户自定义模式
    classification_kwds = {'bins':[0,100,1000,10000,100000,1000000]}, #定义分位点，即疫情严重程度
    cmap = 'Reds', #颜色
    legend = True, #显示图例
    legend_kwds = dict(loc='lower left'), #指定图例显示位置
    ax = ax #在指定画布的坐标轴上绘制
)
```

![世界疫情地图](https://cdn.jsdelivr.net/gh/shallowhui/cdn/img/covid19/output_17_1.png)

## 实现动态可视化

实现动态可视化的一个思路就是根据每一天的疫情数据，画出若干张图，然后把这些图片合并在一起，形成一个GIF图，为此编写下面这个函数：

``` python
def ImgToGif(data):
    GIF = [] #保存gif动图里的每一张图片
    dates = data.columns[2:50] #获取数据集中的日期数据
    fig,ax = plt.subplots(figsize=(23,10))
    sum = 0
    length = len(dates)
    #循环生成每一天的世界疫情图
    for date in dates:
        plt.title('Total confirmed cases of COVID-19 in the World, '+date,fontdict={'size':30}) #设置画布标题
        data.plot(
            column = date, #绘制哪一列的数据
            scheme = 'userdefined', #用户自定义模式
            classification_kwds = {'bins':[0,100,1000,10000,100000,1000000]}, #定义分位点，即疫情严重程度
            cmap = 'Reds', #颜色
            legend = True, #显示图例
            legend_kwds = dict(loc='lower left'), #指定图例显示位置
            ax = ax #在指定画布的坐标轴上绘制
        )
        img = ax.get_figure() #获取绘制完成后的画布
        f = io.BytesIO() #打开IO流
        img.savefig(f,format='png') #将图片写入IO流
        f.seek(0) #文件指针移回初始位置
        GIF.append(PIL.Image.open(f)) #用PIL模块的专门处理图像的子模块读取IO流，并将流式数据转化成PngImageFile数据类型存放到GIF列表中
        sum = sum + 1
        print('\r生成动图中：{:.2f}%'.format(sum*100./length),end='')
        
    #将列表里的所有图片合并生成GIT图
    GIF[0].save(
        'COVID-19_visual.gif',
        format='GIF', #保存为GIF动图
        append_images=GIF[1:],
        save_all=True,
        duration=200, #动图时间间隔，单位毫秒
        loop=0 #loop=0代表无限循环播放动图
    )
    f.close()
    print('\n\r动图生成完成！')
```

生成的gif动图大概有60M大小，我就不上图了，可以自己试试运行代码看看。

## 总结

数据动态可视化就介绍到这了，这篇文章的项目完整代码可以自取：

[https://github.com/ShallowHui/interesting-small-project/blob/master/COVID-19_visual.py](https://github.com/ShallowHui/interesting-small-project/blob/master/COVID-19_visual.py)