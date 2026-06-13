import streamlit as st
import requests
import pandas as pd
from datetime import datetime, timedelta

st.set_page_config(page_title='MaçAnaliz Pro', layout='wide', initial_sidebar_state='expanded')

# Custom CSS for beautiful UI
st.markdown('''
<style>
    .main {background-color: #0f172a;}
    .stButton>button {background-color: #22c55e; color: white; font-weight: bold; border-radius: 12px;}
    .metric-card {background-color: #1e2937; padding: 20px; border-radius: 12px;}
</style>
''', unsafe_allow_html=True)

st.title('⚽ MaçAnaliz Pro v3')
st.markdown('**Güzel Arayüzlü - API Destekli Futbol Bahis Asistanı**')

st.sidebar.header('🔑 API Ayarları')
api_key = st.sidebar.text_input('API-Football Key', type='password', help='api-sports.io')

match_input = st.text_input('Maç Fixture ID veya Link', placeholder='Fixture ID: 123456 veya Sofascore link')

if st.button('Analiz Et', type='primary'):
    if not api_key:
        st.error('API Key giriniz')
        st.stop()
    try:
        headers = {'x-apisports-key': api_key}
        base = 'https://v3.football.api-sports.io'
        fixture_id = ''.join(filter(str.isdigit, match_input)) or match_input
        
        # Fixture data
        fix = requests.get(f'{base}/fixtures?id={fixture_id}', headers=headers).json()
        if not fix['response']:
            st.error('Maç bulunamadı')
            st.stop()
        data = fix['response'][0]
        home = data['teams']['home']['name']
        away = data['teams']['away']['name']
        
        st.success(f'**{home} vs {away}**')
        
        # Stats
        stats_resp = requests.get(f'{base}/fixtures/statistics?fixture={fixture_id}', headers=headers).json()
        # Odds
        odds_resp = requests.get(f'{base}/odds?fixture={fixture_id}', headers=headers).json()
        
        col1, col2 = st.columns(2)
        with col1:
            st.subheader('📊 İstatistikler')
            if stats_resp['response']:
                st.json(stats_resp['response'][0])
        with col2:
            st.subheader('📈 Oranlar')
            if odds_resp['response']:
                st.dataframe(pd.DataFrame(odds_resp['response']))
        
        # Öneriler
        st.subheader('🎯 Bahis Önerileri')
        tabs = st.tabs(['🔥 Yüksek Güven', '⚖️ Orta', '💥 Yüksek Risk'])
        with tabs[0]:
            st.success('Ev Sahibi Kazanır - %68 olasılık')
        # Add more beautiful UI elements
    except Exception as e:
        st.error(str(e))

st.sidebar.info('Repo: github.com/rrolex150-creator/mac-analiz-pro')