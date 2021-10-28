import streamlit as st
import pandas as pd
import numpy as np

import matplotlib.pyplot as plt
plt.style.use('ggplot')

plt.rcParams['font.family'] = 'Source Sans Pro'

import seaborn as sns
import calendar

TITLE_SIZE = 30
TITLE_PADDING = 20
DEFAULT_CMAP = plt.rcParams['axes.prop_cycle'].by_key()['color']


# ---------------------------------------------------------------------------------- #

# SETTING PAGE CONFIG TO WIDE MODE
st.set_page_config(page_title="SF Purchasing Data Dashboard", 
                   layout="wide",
                   initial_sidebar_state="expanded")



departments = {
               'Airport Commission': 'AIR',
               'Assessor / Recorder': 'ASR',
               'Building Inspection': 'DBI',
               'City Planning': 'CPC',
               'Elections': 'REG',
               'Emergency Management': 'DEM',
               'Fire Department': 'FIR',
               'GSA - City Administrator': 'ADM',
               'GSA - Public Works': 'DPW',
               'GSA - Technology': 'DT ',
               'General City / Unallocated': 'GEN',
               'Human Services Agency': 'HSA',
               'Municipal Transprtn Agncy': 'MTA',
               'Police': 'POL',
               'Port': 'PRT',
               'Public Health': 'DPH',
               'Public Library': 'LIB',
               'Public Utilities Commsn': 'PUC',
               'Recreation & Park Commsn': 'REC',
               'Sheriff': 'SHF'
              }

commodities = [
               'AUTOMOTIVE AND TRAILER EQUIPMENT AND PARTS',
               'AUTOMOTIVE VEHICLES AND RELATED TRANSPORTATION EQUIPMENT (IN',
               'CHEMICALS AND SOLVENTS COMMERCIAL (IN BULK)',
               'CLOTHING: ATHLETIC CASUAL DRESS UNIFORM WEATHER AND WORK',
               'COMPUTER HARDWARE AND PERIPHERALS FOR MICROCOMPUTERS',
               'COMPUTER SOFTWARE FOR MINI AND MAINFRAME COMPUTERS (PREPROGR',
               'ELECTRICAL EQUIPMENT AND SUPPLIES (EXCEPT CABLE AND WIRE)',
               'Emergency Showers and Wash Stations',
               'FIRST AID AND SAFETY EQUIPMENT AND SUPPLIES (EXCEPT NUCLEAR',
               'FURNITURE: OFFICE',
               'HOSPITAL AND SURGICAL EQUIPMENT INSTRUMENTS AND SUPPLIES',
               'HOSPITAL SURGICAL AND MEDICAL RELATED ACCESSORIES AND SUND',
               'LABORATORY EQUIPMENT ACCESSORIES AND SUPPLIES: GENERAL ANAL',
               'PLUMBING EQUIPMENT FIXTURES AND SUPPLIES',
               'POLICE AND PRISON EQUIPMENT AND SUPPLIES',
               'Personal Protective Equipment (PPE) (Bloodborne Pathogen Pr',
               'RADIO COMMUNICATION TELEPHONE AND TELECOMMUNICATION EQUIPM',
               'Spreaders Self-Propelled (For Aggregates Sand etc.)',
               'Surgical Support Supplies incl. Post-Surgery (Not Otherwise',
               'Tools and Supplies for Copper and Fiber Optic Wiring Systems'
              ]
               
vendors = [
         'AZCO SUPPLY INC',
         'BAY MEDICAL CO INC',
         'CARDINALHEALTH MEDICAL PRODUCTS & SVCS',
         'COMPUTERLAND SILICON VALLEY',
         'CONNECTION',
         'Cummins Inc',
         'GALLS LLC QUARTERMASTER LLC',
         'HANSON AGGREGATES MID-PACIFIC INC',
         'INSIGHT PUBLIC SECTOR INC',
         'Intervision Systems LLC',
         "Jimmie Muscatello's",
         'MEDLINE INDUSTRIES INC',
         'North Eastern Bus Rebuilders Inc.',
         'PACIFIC POWER PRODUCTS',
         'R & B COMPANY',
         'TROLLEY SUPPORT LLC',
         'UNITED SITE SERVICES OF CALIFORNIA INC',
         'VORTECH INDUSTRIES',
         'XTECH',
         'ZONES LLC'
          ]
               


# ---------------------------------------------------------------------------------- #

DATA_URL = "https://streamlit-testdata.s3.eu-central-1.amazonaws.com/purchase_data_processed.csv"

# use streamlit's cache decorator to avoid constant reloading of large data set
@st.cache
def read_and_prepare_data():
  df = pd.read_csv(DATA_URL)
  df.po_dt = pd.to_datetime(df.po_dt)
  diff = df.po_dt.max() - df.po_dt
  df["days_after_purchase"] = diff.dt.days
  return df

data = read_and_prepare_data()


# ---------------------------------------------------------------------------------- #

time_frame = st.sidebar.selectbox(
                            "Choose time frame",
                            ("Last week", "Last 30 days", "Last 90 days", 
                             "Last 120 days", "Last 180 days", "Last 360 days")
                            )


filter_dept = st.sidebar.selectbox(
                            "Choose department",
                            ("All depts", *departments.keys(),
                             )
                            )

filter_comm = st.sidebar.selectbox(
                            "Choose commodity",
                            ("All commodities", *commodities,
                             )
                            )

filter_vend = st.sidebar.selectbox(
                            "Choose vendor",
                            ("All vendors", *vendors,
                             )
                            )


# filter time frame
if time_frame == "Last 30 days":
  sf = data[data.days_after_purchase < 30].copy()
elif time_frame == "Last 90 days":
  sf = data[data.days_after_purchase < 90].copy()
elif time_frame == "Last 120 days":
  sf = data[data.days_after_purchase < 120].copy()
elif time_frame == "Last 180 days":
  sf = data[data.days_after_purchase < 180].copy()
elif time_frame == "Last 360 days":
  sf = data[data.days_after_purchase < 360].copy()
else:
  sf = data[data.days_after_purchase < 7].copy()

# filter department
if filter_dept == "All depts":
  pass
else:
  sf = sf[sf.department==departments[filter_dept]].copy()

# filter commodity
if filter_comm == "All commodities":
  pass
else:
  sf = sf[sf.commodity_title==filter_comm].copy()

# filter vendor
if filter_vend == "All vendors":
  pass
else:
  sf = sf[sf.vendor_name==filter_vend].copy()


# ---------------------------------------------------------------------------------- #

if sf.shape[0] ==0:
  st.write("# 🤕 No data available. Please filter differently.")

else:
  start_date = sf.po_dt.min().strftime('%d.%m.%Y')
  end_date = sf.po_dt.max().strftime('%d.%m.%Y')

  diff = sf.po_dt.max() - sf.po_dt.min()
  days = diff.days


  st.markdown("# 🌉 San Francisco Purchasing Data Dashboard")
  st.subheader(f"Data overview for purchases from {time_frame.lower()}")
  st.markdown(f"##### First available date: {start_date} | Last available date: {end_date}\n---")


  purchase_count = sf.shape[0]
  dept_count = sf.department.nunique()
  vendor_count = sf.vendor_name.nunique()
  commodity_count = sf.commodity_code.nunique()

  sales_volume = sf.price.sum()
  price_mean = sf.price.mean()
  price_median = sf.price.median()
  highest_sale = sf.price.max()



  purchase_count_delta = int(purchase_count / days - 1_090) * days
  dept_count_delta = None
  vendor_count_delta = None 
  commodity_count_delta = int(commodity_count / days - 135)

  sales_volume_delta = int(sales_volume / days - 3_064_348) * days
  price_mean_delta = int(price_mean - 2_813)
  price_median_delta = int(price_median - 45) 
  highest_sale_delta = None



  metric_names = ["🛒  Total purchases made", 
                  "🏦 Department count",
                  "👩🏻‍💼 Vendor count 👨🏻‍💼", 
                  "🛍 Unique goods purchased",

                  "🔎 Total sales volume",
                  "Average order volume",
                  "Median order volume",
                  "🔥 Highest sale",
                  ]

  metric_values = [purchase_count, 
                   dept_count,
                   vendor_count,
                   commodity_count,

                   sales_volume,
                   price_mean,
                   price_median,
                   highest_sale,
                   ]


  delta_values = [purchase_count_delta,
                  dept_count_delta, 
                  vendor_count_delta,
                  commodity_count_delta,

                  sales_volume_delta, 
                  price_mean_delta, 
                  price_median_delta, 
                  highest_sale_delta, 
                  ]


  for idx in [0, 4]:
    columns = st.columns(4)
    for col, name, val, delta in zip(columns, 
                              metric_names[idx:idx+4], 
                              metric_values[idx:idx+4],
                              delta_values[idx:idx+4]
                              ):
      with col:
        if idx!=0:
          sign = "$"
        else:
          sign = ""  
        if delta != None:
          st.metric(name, f"{val:,.0f} {sign}", f"{delta:,.0f}") 
        else:
          st.metric(name, f"{val:,.0f} {sign}", None)

  st.markdown(f"---")


  # ---------------------------------------------------------------------------------- #


  # st.markdown("### Sales volume per calendar week")
  fig, ax = plt.subplots(figsize=(16,6))
  sf.groupby(sf.po_dt.dt.isocalendar().week).price.sum().plot.bar(ax=ax)
  plt.title(f"Sales volume per calendar week", 
            size=TITLE_SIZE, pad=TITLE_PADDING, loc='left', fontweight='bold')
  plt.ticklabel_format(axis="y", style="plain")
  plt.xticks(rotation=0)
  plt.ylabel("Sales volume in USD")
  plt.xlabel("Calendar week")
  plt.tight_layout()
  st.pyplot(fig)

  # st.markdown("### Sales volume per weekday")
  fig, ax = plt.subplots(figsize=(16,6))
  sf.groupby(sf.po_dt.dt.weekday).price.sum().plot.bar(ax=ax)
  plt.title(f"Sales volume per weekday", 
            size=TITLE_SIZE, pad=TITLE_PADDING, loc='left', fontweight='bold')
  plt.ticklabel_format(axis="y", style="plain")
  plt.xticks(ticks=range(0, 7), labels=list(calendar.day_abbr), rotation=0)
  plt.ylabel("Sales volume in USD")
  plt.xlabel("Weekday")
  plt.tight_layout()
  st.pyplot(fig)

  st.markdown(f"---")


  # ---------------------------------------------------------------------------------- #

  top_n = 10
  figsize = (16, 6)
  ytick_size = 18


  tmp = sf.groupby("department_title").price.sum().sort_values(ascending=False)[:top_n]
  tmp = pd.DataFrame(tmp).reset_index()
  # st.markdown(f"### Top {top_n} departments by sales volume")
  fig, ax = plt.subplots(figsize=figsize)
  sns.barplot(data=tmp, y="department_title", x="price", ax=ax, color=DEFAULT_CMAP[0])
  plt.title(f"Top {top_n} departments by sales volume", 
            size=TITLE_SIZE, pad=TITLE_PADDING, loc='left', fontweight='bold')
  plt.xlabel("Sum of sales, in USD", size=8)
  plt.yticks(size=ytick_size)
  plt.ylabel("")
  plt.tight_layout()
  st.pyplot(fig)

  tmp = sf.groupby("commodity_title").price.sum().sort_values(ascending=False)[:top_n]
  tmp = pd.DataFrame(tmp).reset_index()
  # st.markdown(f"### Top {top_n} commodities by sales volume")
  fig, ax = plt.subplots(figsize=figsize)
  sns.barplot(data=tmp, y="commodity_title", x="price", ax=ax, color=DEFAULT_CMAP[0])
  plt.title(f"Top {top_n} commodities by sales volume", 
            size=TITLE_SIZE, pad=TITLE_PADDING, loc='left', fontweight='bold')
  plt.xlabel("Sum of sales, in USD", size=8)
  labels = [f"{x.capitalize()[:25]}..." for x in tmp.commodity_title.values]
  plt.yticks(ticks=range(tmp.shape[0]), labels=labels, size=ytick_size)
  plt.ylabel("")
  plt.tight_layout()
  st.pyplot(fig)

  tmp = sf.groupby("vendor_name").price.sum().sort_values(ascending=False)[:top_n]
  tmp = pd.DataFrame(tmp).reset_index()
  fig, ax = plt.subplots(figsize=figsize)
  sns.barplot(data=tmp, y="vendor_name", x="price", ax=ax, color=DEFAULT_CMAP[0])
  plt.title(f"Top {top_n} vendors by sales volume", 
            size=TITLE_SIZE, pad=TITLE_PADDING, loc='left', fontweight='bold')
  labels = [f"{x.capitalize()}..." for x in tmp.vendor_name.values]
  plt.yticks(ticks=range(tmp.shape[0]), labels=labels, size=ytick_size)
  plt.ylabel("")
  plt.xlabel("Sum of sales, in USD", size=8)
  plt.tight_layout()
  st.pyplot(fig)

  st.markdown(f"---")




'''
*FHWN Fachvertiefung Data Science Kompetenz | Patrick Arnecke 2021*
'''










