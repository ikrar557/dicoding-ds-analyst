import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.ticker as ticker

# Membaca data
hours_df = pd.read_csv('dashboard/hour_cleaned.csv')
days_df = pd.read_csv('dashboard/day_cleaned.csv')

st.markdown("<h1 style='text-align: center;'>Bike Sharing Dataset</h1>", unsafe_allow_html=True)

total_rentals = days_df['count'].sum()

season_rentals = days_df.groupby('season')['count'].sum().reset_index()
highest_season = season_rentals.loc[season_rentals['count'].idxmax()]

highest_date = days_df.loc[days_df['count'].idxmax()]

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Total Peminjaman Sepeda", total_rentals)

with col2:
    st.metric("Season dengan Peminjaman Tertinggi", f"{highest_season['season']} ({highest_season['count']})")

with col3:
    st.metric("Tanggal dengan Peminjaman Tertinggi", f"{highest_date['dteday']}")

# Pertanyaan 1: Bagaimana cuaca memengaruhi jumlah peminjaman sepeda?
st.header("Heatmap Jumlah Peminjaman Sepeda Berdasarkan Jam dan Cuaca")

heatmap_data = hours_df.groupby(['hours', 'weather_situation'])['count'].sum().unstack()

hours_order = sorted(hours_df['hours'].unique())
weather_order = ['clear', 'cloudy', 'light_rain', 'heavy_rain']

heatmap_data = heatmap_data.reindex(index=hours_order, columns=weather_order, fill_value=0)

plt.figure(figsize=(12, 8))
sns.heatmap(
    heatmap_data,
    cmap='YlGnBu',
    annot=True,
    fmt='g',
    cbar_kws={'label': 'Jumlah Peminjaman'},
    linewidths=0.5,
    linecolor='gray'
)

plt.title('Heatmap Jumlah Peminjaman Sepeda Berdasarkan Jam dan Cuaca', fontsize=20)
plt.xlabel('Kondisi Cuaca', fontsize=14)
plt.ylabel('Jam', fontsize=14)
plt.xticks(rotation=45)  
st.pyplot(plt)

# Pertanyaan 2: Apakah terdapat perbedaan dalam penggunaan sepeda berdasarkan musim?
st.header("Grafik Jumlah Peminjaman Sepeda Antar Musim")

colors = ["#90CAF9", "#D3D3D3", "#D3D3D3", "#D3D3D3"]

total_rentals_by_season = days_df.groupby('season')['count'].sum().reset_index()

total_rentals_by_season = total_rentals_by_season.sort_values(by='count', ascending=False)

fig, ax = plt.subplots(figsize=(20, 10))

sns.barplot(
    x="count", 
    y="season",
    data=total_rentals_by_season,
    palette=colors,
    order=total_rentals_by_season['season'],
    ax=ax
)

ax.set_title("Grafik Jumlah Peminjaman Sepeda Antar Musim", loc="center", fontsize=30)
ax.set_ylabel("Musim", fontsize=20)
ax.set_xlabel("Jumlah Peminjaman", fontsize=20)
ax.tick_params(axis='x', labelsize=20)
ax.tick_params(axis='y', labelsize=20)

ax.xaxis.set_major_formatter(ticker.StrMethodFormatter('{x:0.0f}'))  

st.pyplot(fig)

# Pertanyaan 3: Siapa yang lebih aktif menggunakan sepeda, pengguna terdaftar atau non-terdaftar setiap tahunnya?
st.header("Penyewaan Sepeda Bulanan untuk Pengguna Terdaftar dan Non-Terdaftar")

days_df['month'] = pd.Categorical(days_df['month'], categories=[
    'january', 'february', 'march', 'april', 'may', 'june',
    'july', 'august', 'september', 'october', 'november', 'december'
], ordered=True)

monthly_rentals = days_df.groupby(['year', 'month']).agg({
    'registered': 'sum',
    'casual': 'sum'
}).reset_index()

fig, axes = plt.subplots(2, 1, figsize=(12, 10), sharex=True)

data_2011 = monthly_rentals[monthly_rentals['year'] == 2011]
axes[0].plot(
    data_2011['month'], 
    data_2011['registered'], 
    marker='o', 
    label='Pengguna Registered', 
    color='blue'
)
axes[0].plot(
    data_2011['month'], 
    data_2011['casual'], 
    marker='o', 
    label='Pengguna Casual', 
    color='orange'
)

axes[0].set_title('Penyewaan Sepeda Bulanan Tahun 2011', fontsize=14)
axes[0].set_ylabel('Jumlah Penyewaan', fontsize=12)
axes[0].legend(title="Tipe Pengguna", fontsize=10)
axes[0].grid(alpha=0.3)

data_2012 = monthly_rentals[monthly_rentals['year'] == 2012]
axes[1].plot(
    data_2012['month'], 
    data_2012['registered'], 
    marker='o', 
    label='Pengguna Registered', 
    color='blue'
)
axes[1].plot(
    data_2012['month'], 
    data_2012['casual'], 
    marker='o', 
    label='Pengguna Casual', 
    color='orange'
)

axes[1].set_title('Penyewaan Sepeda Bulanan Tahun 2012', fontsize=14)
axes[1].set_ylabel('Jumlah Penyewaan', fontsize=12)
axes[1].legend(title="Tipe Pengguna", fontsize=10)
axes[1].grid(alpha=0.3)

axes[1].set_xticks(range(len(data_2011['month'])))
axes[1].set_xticklabels(['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 
                         'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])

plt.tight_layout()
st.pyplot(fig)

# Pertanyaan 4: Bagaimana pengaruh hari kerja dan hari libur terhadap penggunaan sepeda?
st.header("Pengaruh Hari Kerja dan Hari Libur terhadap Penggunaan Sepeda")

usage_by_category = days_df.groupby('category_days')['count'].sum().reset_index()

labels = usage_by_category['category_days'].replace({
    'weekend': 'Hari Libur',
    'weekdays': 'Hari Kerja'
})

sizes = usage_by_category['count']

colors = ["#72BCD4", "#D3D3D3"]

explode = (0.1, 0) 

plt.figure(figsize=(8, 6))
plt.pie(sizes, explode=explode, labels=labels, colors=colors, autopct='%1.1f%%',
        shadow=True, startangle=90)

plt.axis('equal')

plt.title('Pengaruh Hari Kerja dan Hari Libur terhadap Penggunaan Sepeda')

st.pyplot(plt)

# Analisis optional dengan clustering
st.title("Analisis optional dengan clustering")
st.subheader("Analisis Peminjaman Sepeda Berdasarkan Kategori Frekuensi")

def frequency_group(value):
    if value >= 100:
        return 'Sangat Tinggi'
    elif value >= 50:
        return 'Tinggi'
    elif value >= 10:
        return 'Sedang'
    else:
        return 'Rendah'

hours_df['Frequency_Group'] = hours_df['count'].apply(frequency_group)

frequency_counts = hours_df['Frequency_Group'].value_counts()

colors = ["#90CAF9", "#D3D3D3", "#D3D3D3", "#D3D3D3"]

fig, ax = plt.subplots(figsize=(10, 6))

sns.barplot(x=frequency_counts.index, y=frequency_counts.values, palette=colors, ax=ax)

ax.set_title('Distribusi Jumlah Peminjaman Berdasarkan Kategori Frekuensi', fontsize=16)
ax.set_xlabel(None)
ax.set_ylabel('Jumlah Peminjaman', fontsize=14)

for i, value in enumerate(frequency_counts.values):
    ax.text(i, value, str(value), ha='center', va='bottom', fontsize=12)

st.pyplot(fig)

