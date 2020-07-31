import streamlit as st
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd

COLOR = "black"
BACKGROUND_COLOR = "#F9F9F9"
padding_right: int = 1
padding_left: int = 1
padding_bottom: int = 10
padding_top: int = 5
max_width: int = 1200
max_width_str = f"max-width: {max_width}px;"
st.markdown(
        f"""
<style>
    .reportview-container .main .block-container{{
        {max_width_str}
        padding-top: {padding_top}rem;
        padding-right: {padding_right}rem;
        padding-left: {padding_left}rem;
        padding-bottom: {padding_bottom}rem;
    }}
    .reportview-container .main {{
        color: {COLOR};
        background-color: {BACKGROUND_COLOR};
    }}
</style>
""",
        unsafe_allow_html=True,
    )

st.sidebar.image("https://raw.githubusercontent.com/KoxNoob/final_checkpoint/master/sidebargif.jpeg", width=300)

st.sidebar.title("Menu")
vue = st.sidebar.radio("", ('Accueil', 'Analyse exploratoire', 'PowerBI', 'Machine learning', 'Bonus'))


@st.cache(persist=True)
def csv(path):
    df = pd.read_csv(path)
    df.drop(['Unnamed: 0'], axis=1, inplace=True)
    return df

anpe = csv('https://raw.githubusercontent.com/KoxNoob/final_checkpoint/master/data_checkpoint')
first_model = csv('https://raw.githubusercontent.com/KoxNoob/final_checkpoint/master/df_results_first_model')
prediction = csv('https://raw.githubusercontent.com/KoxNoob/final_checkpoint/master/prediction')
second_model = csv('https://raw.githubusercontent.com/KoxNoob/final_checkpoint/master/second_model')
prediction2 = csv('https://raw.githubusercontent.com/KoxNoob/final_checkpoint/master/bonus')

# Définition des variables

colonne1 = 'secteurActiviteLibelle'
colonne2 = 'accessibleTH'
colonne3 = 'entreprise.nom'
colonne4 = 'qualificationLibelle'
colonne5 = 'dureeTravailLibelle'
colonne6 = 'qualitesProfessionnelles'
present = "Oui"
absent = "Non"
colors = ['green', 'red']

if vue == "Accueil":
    st.markdown(
        "<h2 style='text-align: center; color: gray; size = 0'>WCS, c'est fini...</h2>",
        unsafe_allow_html=True)
    st.markdown('<p align="center"><img width="500" height="550" \
    src="https://raw.githubusercontent.com/KoxNoob/final_checkpoint/master/accueilfinal.jpeg"</p>', unsafe_allow_html=True)

if vue == "Analyse exploratoire":
    st.markdown(
        "<h2 style='text-align: center; color: gray; size = 0'>Analyse exploratoire</h2>",
        unsafe_allow_html=True)

    st.write("Afin de faciliter l'exploitation des données, certaines colonnes qui n'apportaient pas ou très peu \
    d'information ont été supprimées.")

    fig = make_subplots(rows=3, cols=2, subplot_titles=['L\'info ' + str(colonne1) + ' est présente ?',
                                                        'L\'info ' + str(colonne2) + ' est présente ?',
                                                        'L\'info ' + str(colonne3) + ' est présente ?',
                                                        'L\'info ' + str(colonne4) + ' est présente ?',
                                                        'L\'info ' + str(colonne5) + ' est présente ?',
                                                        'L\'info ' + str(colonne6) + ' est présente ?'],
                        specs=[[{"type": "pie"}, {"type": "pie"}],[{"type": "pie"},
                                {"type": "pie"}],[{"type": "pie"},{"type": "pie"}]])

    fig.add_trace(
        go.Pie(labels=[present,absent], values=[len(anpe) - anpe[colonne1].isnull().sum(), anpe[colonne1].isnull().sum()]),
        row=1, col=1
    )

    fig.add_trace(
        go.Pie(labels=[present,absent], values=[len(anpe) - anpe[colonne2].isnull().sum(), anpe[colonne2].isnull().sum()]),
        row=1, col=2
    )

    fig.add_trace(
        go.Pie(labels=[present,absent], values=[len(anpe) - anpe[colonne3].isnull().sum(), anpe[colonne4].isnull().sum()]),
        row=2, col=1
    )

    fig.add_trace(
        go.Pie(labels=[present,absent], values=[len(anpe) - anpe[colonne4].isnull().sum(), anpe[colonne4].isnull().sum()]),
        row=2, col=2
    )

    fig.add_trace(
        go.Pie(labels=[present,absent], values=[len(anpe) - anpe[colonne5].isnull().sum(), anpe[colonne5].isnull().sum()]),
        row=3, col=1
    )

    fig.add_trace(
        go.Pie(labels=[present,absent], values=[len(anpe) - anpe[colonne6].isnull().sum(), anpe[colonne6].isnull().sum()]),
        row=3, col=2
    )

    fig.update_traces(hoverinfo='label+percent', textfont_size=12,
                    marker=dict(colors=colors, line=dict(color='#000000', width=2)))
    fig.update_layout(height=800, width=1300, title_text="Analyse de certaines informations", margin=dict(l=20, r=0, t=100, b=20, pad=0))
    st.plotly_chart(fig, use_container_width=True)

    st.write("On se rend compte que certaines informations relativement importantes n'ont pas été renseignées par \
             l'entreprise. Cela pourrait avoir un impact quant à la lisibilité de l'annonce, son impact sur les \
             potentiels candidats et sur la compréhension des attentes du poste.")
    st.markdown(
        "<h3 style='text-align: center; color: gray; size = 0'>Postes les plus recherchés</h3>",
        unsafe_allow_html=True)
    liste_postes = []
    nombre_postes = []

    for poste in anpe['appellationlibelle'].unique():
        liste_postes.append(poste)
        nombre_postes.append(len(anpe[anpe['appellationlibelle'] == poste]))
    liste_postes_top10 = liste_postes[0:10]
    nombre_postes_top10 = nombre_postes[0:10]

    top10 = dict(zip(liste_postes_top10, nombre_postes_top10))
    top10_sorted = sorted(top10.items(), key=lambda x: x[1], reverse=True)
    liste_postes_sorted = []
    nombre_postes_sorted = []

    for i in range(len(top10_sorted)):
        liste_postes_sorted.append(top10_sorted[i][0])
        nombre_postes_sorted.append(top10_sorted[i][1])

    liste_postes_sorted.reverse()
    nombre_postes_sorted.reverse()
    fig2 = px.bar(y=liste_postes_sorted, x=nombre_postes_sorted, orientation='h')
    fig2.update_layout(height=500, width=1000,margin=dict(l=50, r=50, t=20, b=20, pad=30),
                       xaxis_title="Nb d'offres d'emploi",
                       yaxis_title="Postes proposés",)
    st.plotly_chart(fig2)


    st.write("Quand on regarde les postes les plus recherchés, on se rend compte qu'il y a plein d'appellations \
     différentes pour des postes plutôt similaires")

    st.markdown(
        "<h3 style='text-align: center; color: gray; size = 0'>Expériences recherchées</h3>",
        unsafe_allow_html=True)

    liste_experience = []
    nb_experience = []

    for exp in anpe['experienceLibelle'].unique():
        liste_experience.append(exp)
        nb_experience.append(len(anpe[anpe['experienceLibelle'] == exp]))

    liste_experience_top10 = liste_experience[0:10]
    nb_experience_top10 = nb_experience[0:10]

    top10_exp = dict(zip(liste_experience_top10, nb_experience_top10))
    top10_exp_sorted = sorted(top10_exp.items(), key=lambda x: x[1], reverse=True)

    liste_exp_sorted = []
    nombre_exp_sorted = []

    for i in range(len(top10_exp_sorted)):
        liste_exp_sorted.append(top10_exp_sorted[i][0])
        nombre_exp_sorted.append(top10_exp_sorted[i][1])

    liste_exp_sorted.reverse()
    nombre_exp_sorted.reverse()

    fig3 = px.bar(y=liste_exp_sorted, x=nombre_exp_sorted, orientation='h')
    fig3.update_layout(height=500, width=1000,margin=dict(l=50, r=50, t=20, b=20, pad=30),
                       xaxis_title="Nombres d'offres concernées",
                       yaxis_title="Expériences demandées",)
    st.plotly_chart(fig3)

    st.write("Dans un peu moins de 50% des annonces, il est noté que des débutants sont acceptés, théoriquement.")

    st.markdown(
        "<h3 style='text-align: center; color: gray; size = 0'>Contrats recherchés</h3>",
        unsafe_allow_html=True)

    liste_contrat = []
    nb_contrat = []

    for exp in anpe['typeContrat'].unique():
        liste_contrat.append(exp)
        nb_contrat.append(len(anpe[anpe['typeContrat'] == exp]))

    liste_contrat = liste_contrat[0:10]
    nb_contrat = nb_contrat[0:10]

    top_contrat = dict(zip(liste_contrat, nb_contrat))
    top_contrat = sorted(top_contrat.items(), key=lambda x: x[1], reverse=True)

    liste_contrat_sorted = []
    nombre_contrat_sorted = []

    for i in range(len(top_contrat)):
        liste_contrat_sorted.append(top_contrat[i][0])
        nombre_contrat_sorted.append(top_contrat[i][1])

    liste_contrat_sorted.reverse()
    nombre_contrat_sorted.reverse()

    fig4 = px.bar(y=liste_contrat_sorted, x=nombre_contrat_sorted, orientation='h')
    fig4.update_layout(height=500, width=1000,margin=dict(l=50, r=50, t=20, b=20, pad=30),
                       xaxis_title="Nb de contrats",
                       yaxis_title="Contrats proposés",)
    st.plotly_chart(fig4)

    st.write("Chose étonnante, nous avons plus d'offres en profession libérale qu'en CDD. De plus, on s'aperçoit \
             que majoritairement, nous avons des CDI qui sont proposés.")

    st.markdown(
        "<h3 style='text-align: center; color: gray; size = 0'>Et récemment ?</h3>",
        unsafe_allow_html=True)
    df_recent = anpe.sort_values(by='dateActualisation', ascending=False)
    df_recent = df_recent.iloc[:500, :]
    liste_contrat_recent = []
    nb_contrat_recent = []

    for exp in df_recent['typeContrat'].unique():
        liste_contrat_recent.append(exp)
        nb_contrat_recent.append(len(df_recent[df_recent['typeContrat'] == exp]))

    liste_contrat_recent = liste_contrat_recent[0:10]
    nb_contrat_recent = nb_contrat_recent[0:10]

    top_contrat_recent = dict(zip(liste_contrat_recent, nb_contrat_recent))
    top_contrat_recent = sorted(top_contrat_recent.items(), key=lambda x: x[1], reverse=True)

    liste_contrat_recent_sorted = []
    nombre_contrat_recent_sorted = []

    for i in range(len(top_contrat_recent)):
        liste_contrat_recent_sorted.append(top_contrat_recent[i][0])
        nombre_contrat_recent_sorted.append(top_contrat_recent[i][1])

    liste_contrat_recent_sorted.reverse()
    nombre_contrat_recent_sorted.reverse()

    fig5 = px.bar(y=liste_contrat_recent_sorted, x=nombre_contrat_recent_sorted, orientation='h')
    fig5.update_layout(height=500, width=1000,margin=dict(l=50, r=50, t=20, b=20, pad=30),
                       xaxis_title="Nb de contrats",
                       yaxis_title="Contrats proposés",
                       )
    st.plotly_chart(fig5)

if vue == "PowerBI":
    st.markdown("""<iframe width="1140" height="541.25" 
    src="https://app.powerbi.com/reportEmbed?reportId=fee0e7df-25f4-4cfb-9d05-8d3a277da80f&autoAuth=true&ctid=1452f717-4912-415b-af85-d7679ac41d06&config=eyJjbHVzdGVyVXJsIjoiaHR0cHM6Ly93YWJpLWZyYW5jZS1jZW50cmFsLWEtcHJpbWFyeS1yZWRpcmVjdC5hbmFseXNpcy53aW5kb3dzLm5ldC8ifQ%3D%3D" 
    frameborder="0" allowFullScreen="true"></iframe>""", unsafe_allow_html=True)

if vue == 'Machine learning':
    st.markdown('<p align="center"><img width="700" height="550" \
        src="https://raw.githubusercontent.com/KoxNoob/final_checkpoint/master/image.png"</p>',
        unsafe_allow_html=True)

    st.write('J\'ai décidé de regarder si en fonction de la description d\'une offre d\'emploi, j\'arrivais à prédire l\'intitulé du poste\
    concerné. Pour cela, après avoir préparé mes données, j\'en ai extrait des features afin de prédire le poste. J\'ai \
    testé sur plusieurs nombres de features, voici le graph des résultats.')

    fig6 = px.bar(first_model,x=first_model['Nb de features'], y=first_model['Accuracy'],log_y=True)
    fig6.update_layout(height=500, width=1000,margin=dict(l=50, r=50, t=20, b=20, pad=30))
    st.plotly_chart(fig6)
    st.write("Voici le tableau récapitulant les nombres de features avec les résultats correspondant et les meilleurs paramètres.")
    st.table(first_model)

    st.write("A la lecture des résultats, on pourrait se dire que le modèle n'est pas très performant. Effectivement, \
    un score aux alentours de 57% ne semble pas bon. Seulement, en le mettant en regard des 94 intitulés de postes \
    différents et quand on sait que certains intitulés sont quasi similaires, cela semble être plutôt un bon score.")

    st.write("On peut maintenant regarder nos prédictions et voir s'il y a de grosses absurdités, ou non...")

    st.table(prediction)


if vue == "Bonus":

    st.write("Et si en fonction de la description, on pouvait prédire dans quelle ville est le poste ? Après avoir \
             entrainé le modèle, voici le graph des résultats.")

    fig7 = px.bar(second_model, x=second_model['Nb de features'], y=second_model['Accuracy'], log_y=True)
    fig7.update_layout(height=500, width=1000, margin=dict(l=50, r=50, t=20, b=20, pad=30))
    st.plotly_chart(fig7)
    st.write(
        "Voici le tableau récapitulant les nombres de features avec les résultats correspondant et les meilleurs paramètres.")
    st.table(second_model)

    st.write("Bon, ce n'était pas forcément pertinent finalement...........")

    st.markdown('<p align="center"><img width="500" height="250" \
        src="https://media.giphy.com/media/GDnomdqpSHlIs/giphy.gif"</p>',
                unsafe_allow_html=True)

    st.write("On peut maintenant regarder nos prédictions et voir les grosses absurdités.......")

    st.table(prediction2)