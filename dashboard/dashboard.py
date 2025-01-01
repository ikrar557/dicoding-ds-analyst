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

# Sidebar untuk input filter
st.sidebar.header("Filter Options")
selected_season = st.sidebar.selectbox("Musim", options=['Semua Musim'] + list(days_df['season'].unique()))
selected_year = st.sidebar.selectbox("Pilih Tahun:", ["Semua Tahun", 2011, 2012])

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

if selected_season == 'Semua Musim':
    total_rentals_by_season = days_df.groupby('season')['count'].sum().reset_index()
else:
    total_rentals_by_season = days_df[days_df['season'] == selected_season].groupby('season')['count'].sum().reset_index()

total_rentals_by_season = total_rentals_by_season.sort_values(by='count', ascending=False)

colors = ["#90CAF9", "#D3D3D3", "#D3D3D3", "#D3D3D3"]

fig, ax = plt.subplots(figsize=(20, 10))
sns.barplot(
    x="count", 
    y="season",
    data=total_rentals_by_season,
    palette=colors,
    order=total_rentals_by_season['season'],
    ax=ax
)

for i in range(len(total_rentals_by_season)):
    ax.text(
        total_rentals_by_season['count'].iloc[i],
        i,
        str(total_rentals_by_season['count'].iloc[i]),
        va='center',
        ha='center',
        fontsize=20 
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

if selected_year == "Semua Tahun":
    for year in [2011, 2012]:
        data_year = monthly_rentals[monthly_rentals['year'] == year]
        axes[year - 2011].plot(
            data_year['month'], 
            data_year['registered'], 
            marker='o', 
            label='Pengguna Registered', 
            color='blue'
        )
        axes[year - 2011].plot(
            data_year['month'], 
            data_year['casual'], 
            marker='o', 
            label='Pengguna Casual', 
            color='orange'
        )

        axes[year - 2011].set_title(f'Penyewaan Sepeda Bulanan Tahun {year}', fontsize=14)
        axes[year - 2011].set_ylabel('Jumlah Penyewaan', fontsize=12)
        axes[year - 2011].legend(title="Tipe Pengguna", fontsize=10)
        axes[year - 2011].grid(alpha=0.3)

    # Terapkan xticks dan xticklabels dengan rotasi 45 derajat
    axes[1].set_xticks(range(len(data_year['month'])))
    axes[1].set_xticklabels(['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 
                             'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'], rotation=45)

elif selected_year in [2011, 2012]:
    data_year = monthly_rentals[monthly_rentals['year'] == selected_year]
    fig, ax = plt.subplots(figsize=(12, 5))  # Buat ulang hanya satu subplot

    ax.plot(
        data_year['month'], 
        data_year['registered'], 
        marker='o', 
        label='Pengguna Registered', 
        color='blue'
    )
    ax.plot(
        data_year['month'], 
        data_year['casual'], 
        marker='o', 
        label='Pengguna Casual', 
        color='orange'
    )
    
    ax.set_title(f'Penyewaan Sepeda Bulanan Tahun {selected_year}', fontsize=14)
    ax.set_ylabel('Jumlah Penyewaan', fontsize=12)
    ax.legend(title="Tipe Pengguna", fontsize=10)
    ax.grid(alpha=0.3)

    # Pastikan label bulan muncul di sumbu x dengan rotasi 45 derajat
    ax.set_xticks(range(len(data_year['month'])))
    ax.set_xticklabels(['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 
                        'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'], rotation=45)

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

# Analisis optional 
st.title("Analisis Optional")

## RFM analysis
hours_df['dteday'] = pd.to_datetime(hours_df['dteday'])
current_date = max(hours_df['dteday'])

rfm_df = hours_df.groupby('registered').agg(
    Recency=('dteday', lambda x: (current_date - x.max()).days),
    Frequency=('dteday', 'count'),
    Monetary=('count', 'sum')
).reset_index()

st.subheader("RFM Analysis")

fig1, ax1 = plt.subplots(figsize=(10, 6))
sns.barplot(
    y="Recency",
    x="registered",
    data=rfm_df.sort_values(by="Recency", ascending=False).head(5),
    palette=["#72BCD4"] * 5,
    ax=ax1,
)
ax1.set_ylabel("Recency (days)", fontsize=15)
ax1.set_xlabel('Registered ID', fontsize=15)
ax1.set_title("Top 5 Customers by Recency (days)", loc="center", fontsize=18)
ax1.tick_params(axis="x", labelsize=12)

st.pyplot(fig1)

fig2, ax2 = plt.subplots(figsize=(10, 6))
sns.barplot(
    y="Frequency",
    x="registered",
    data=rfm_df.sort_values(by="Frequency", ascending=False).head(5),
    palette=["#72BCD4"] * 5,
    ax=ax2,
)
ax2.set_ylabel("Frequency", fontsize=15)
ax2.set_xlabel('Registered ID', fontsize=15)
ax2.set_title("Top 5 Customers by Frequency", loc="center", fontsize=18)
ax2.tick_params(axis="x", labelsize=12)

st.pyplot(fig2)

fig3, ax3 = plt.subplots(figsize=(10, 6))
sns.barplot(
    y="Monetary",
    x="registered",
    data=rfm_df.sort_values(by="Monetary", ascending=False).head(5),
    palette=["#72BCD4"] * 5,
    ax=ax3,
)
ax3.set_ylabel("Monetary", fontsize=15)
ax3.set_xlabel('Registered ID', fontsize=15)
ax3.set_title("Top 5 Customers by Monetary", loc="center", fontsize=18)
ax3.tick_params(axis="x", labelsize=12)

st.pyplot(fig3)


## Clustering analysis
st.subheader("Clustering Analysis dengan asd")

def temperature_group(value):
    if value <= 0.33:
        return 'Rendah'
    elif value <= 0.66:
        return 'Sedang'
    else:
        return 'Tinggi'

hours_df['Temperature_Group'] = hours_df['temp'].apply(temperature_group)

temperature_counts = hours_df['Temperature_Group'].value_counts()

plt.figure(figsize=(10, 6))

sns.barplot(x=temperature_counts.index, y=temperature_counts.values, palette='viridis')

plt.title('Distribusi Jumlah Peminjaman Berdasarkan Kategori Suhu', fontsize=16)
plt.xlabel(None)
plt.ylabel('Jumlah Peminjaman', fontsize=14)

for i, value in enumerate(temperature_counts.values):
    plt.text(i, value, str(value), ha='center', va='bottom', fontsize=12)

plt.tight_layout()

st.pyplot(plt)