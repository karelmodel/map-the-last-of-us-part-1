import streamlit as st
import plotly.graph_objects as go
import pandas as pd

# Cache para carregar dados dos capítulos
@st.cache_data
def carregar_capitulos():
    return [
        {"cidade": "Austin, TX", "lat": 30.2672, "lon": -97.7431, "historia": "Início do surto. Joel e Sarah tentam escapar."},
        {"cidade": "Boston, MA", "lat": 42.3601, "lon": -71.0589, "historia": "Joel vive sob quarentena e conhece Ellie."},
        {"cidade": "Lincoln, MA", "lat": 42.4139, "lon": -71.2062, "historia": "Bill ajuda Joel e Ellie a conseguir um carro."},
        {"cidade": "Pittsburgh, PA", "lat": 40.4406, "lon": -79.9959, "historia": "Emboscada. Conflito com caçadores."},
        {"cidade": "Jackson, WY", "lat": 43.4799, "lon": -110.7624, "historia": "Joel reencontra Tommy e considera deixar Ellie com ele."},
        {"cidade": "Universidade do Leste do Colorado", "lat": 38.9936, "lon": -104.7008, "historia": "Busca pelos Vagalumes. Joel se fere."},
        {"cidade": "Lakeside Resort, CO", "lat": 39.5501, "lon": -105.7821, "historia": "Ellie enfrenta David enquanto cuida de Joel."},
        {"cidade": "Salt Lake City, UT", "lat": 40.7608, "lon": -111.8910, "historia": "Hospital dos Vagalumes. Decisão final de Joel."},
    ]

def criar_mapa(df, capitulos):
    hover_text = [f"<b>{cap['cidade']}</b><br>{cap['historia'][:60]}..." for cap in capitulos]
    fig = go.Figure()

    # Linha da rota
    fig.add_trace(go.Scattergeo(
        lon=df["lon"],
        lat=df["lat"],
        mode="lines",
        line=dict(width=2, color="orange"),
        name="Rota de Joel e Ellie",
        hoverinfo="skip"
    ))

    # Pontos de parada
    fig.add_trace(go.Scattergeo(
        lon=df["lon"],
        lat=df["lat"],
        mode="markers+text",
        marker=dict(size=10, color="orange"),
        text=[f"<b>{cap['cidade']}</b>" for cap in capitulos],
        textposition="top center",
        textfont=dict(color="white", size=12, family="Arial Black"),
        hovertext=hover_text,
        hoverinfo="text",
        name="Cidades",
    ))

    # Layout escuro
    fig.update_layout(
        geo=dict(
            scope="usa",
            projection_type="albers usa",
            bgcolor="#000000",
            showland=True,
            landcolor="#1a1a1a",
            lakecolor="#000000",
            showlakes=True,
            oceancolor="#000000",
            showocean=True
        ),
        paper_bgcolor="#000000",
        plot_bgcolor="#000000",
        margin=dict(l=0, r=0, t=40, b=0),
        title=dict(
            text="🗺️ Mapa da Jornada",
            x=0.5,
            xanchor="center",
            font=dict(color="white", size=20)
        ),
        legend=dict(
            font=dict(color="white"),
            bgcolor="#111",
            bordercolor="white"
        )
    )
    return fig

def tocar_audio():
    # Player de som ambiente
    audio_file = open("assets/som_ambiente.mp3", "rb")
    audio_bytes = audio_file.read()
    st.audio(audio_bytes, format='audio/mp3', start_time=0)

def main():
    st.set_page_config(page_title="The Last of Us - Mapa Narrativo", layout="centered")
    st.title("🧟 The Last of Us - Parte I: Mapa Narrativo")
    st.markdown("Acompanhe a jornada de Joel e Ellie pelos EUA. Cada parada traz um momento marcante da história.")

    capitulos = carregar_capitulos()
    df = pd.DataFrame(capitulos)

    cap_nomes = [f"{i+1}. {cap['cidade']}" for i, cap in enumerate(capitulos)]
    cap_index = st.selectbox("📍 Escolha um ponto da jornada", cap_nomes, index=0)
    cidade_index = int(cap_index.split(".")[0]) - 1
    cap_atual = capitulos[cidade_index]

    # Tocar áudio ambiente
    tocar_audio()

    with st.spinner("Carregando mapa..."):
        fig = criar_mapa(df, capitulos)
        st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")
    st.subheader(f"📖 Capítulo {cidade_index+1}: {cap_atual['cidade']}")
    st.markdown(f"<p style='color:white; font-size: 18px'>{cap_atual['historia']}</p>", unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("<p style='text-align: center; color: gray;'>🎮 Uma homenagem à narrativa de <i>The Last of Us - Parte I</i></p>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()
