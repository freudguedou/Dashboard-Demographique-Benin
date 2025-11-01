"""
Visualisations Démographiques - Bénin
Auteur: Freud GUEDOU
Date: Octobre 2024

Script de création de visualisations pour le dashboard démographique du Bénin
"""

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

# Configuration
plt.rcParams['figure.figsize'] = (12, 7)
plt.rcParams['font.size'] = 10
plt.style.use('seaborn-v0_8-darkgrid')

def charger_donnees():
    """
    Charge tous les fichiers de données
    """
    print("📂 Chargement des données...")
    
    df_pop = pd.read_csv('/mnt/user-data/outputs/donnees_population_benin.csv')
    df_age = pd.read_csv('/mnt/user-data/outputs/donnees_structure_age.csv')
    df_dept = pd.read_csv('/mnt/user-data/outputs/donnees_departements.csv')
    df_social = pd.read_csv('/mnt/user-data/outputs/donnees_indicateurs_sociaux.csv')
    
    print("✅ Données chargées avec succès!\n")
    return df_pop, df_age, df_dept, df_social

def visualiser_evolution_population(df_pop):
    """
    Graphique de l'évolution de la population totale
    """
    print("📊 Création: Évolution de la population...")
    
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 10))
    
    # Graphique 1: Population totale
    ax1.plot(df_pop['Annee'], df_pop['Population_Totale']/1e6, 
             linewidth=3, color='#2c3e50', marker='o', markersize=4)
    ax1.fill_between(df_pop['Annee'], df_pop['Population_Totale']/1e6, 
                      alpha=0.3, color='#3498db')
    ax1.set_title('Évolution de la Population du Bénin (1990-2024)', 
                  fontsize=16, fontweight='bold', pad=20)
    ax1.set_xlabel('Année', fontsize=12)
    ax1.set_ylabel('Population (millions)', fontsize=12)
    ax1.grid(True, alpha=0.3)
    
    # Ajouter les valeurs au début et à la fin
    ax1.text(df_pop['Annee'].iloc[0], df_pop['Population_Totale'].iloc[0]/1e6,
             f"{df_pop['Population_Totale'].iloc[0]/1e6:.1f}M", 
             fontsize=10, ha='right', va='bottom')
    ax1.text(df_pop['Annee'].iloc[-1], df_pop['Population_Totale'].iloc[-1]/1e6,
             f"{df_pop['Population_Totale'].iloc[-1]/1e6:.1f}M", 
             fontsize=10, ha='left', va='bottom')
    
    # Graphique 2: Population urbaine vs rurale
    ax2.plot(df_pop['Annee'], df_pop['Population_Urbaine']/1e6, 
             linewidth=2.5, color='#e74c3c', marker='s', markersize=4, label='Urbaine')
    ax2.plot(df_pop['Annee'], df_pop['Population_Rurale']/1e6, 
             linewidth=2.5, color='#27ae60', marker='^', markersize=4, label='Rurale')
    ax2.set_title('Évolution Population Urbaine vs Rurale', 
                  fontsize=14, fontweight='bold', pad=15)
    ax2.set_xlabel('Année', fontsize=12)
    ax2.set_ylabel('Population (millions)', fontsize=12)
    ax2.legend(loc='upper left', fontsize=11)
    ax2.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('/mnt/user-data/outputs/viz_evolution_population.png', dpi=300, bbox_inches='tight')
    print("✅ Sauvegardé: viz_evolution_population.png\n")
    plt.close()

def visualiser_pyramide_age(df_age):
    """
    Pyramide des âges
    """
    print("📊 Création: Pyramide des âges...")
    
    fig, ax = plt.subplots(figsize=(12, 10))
    
    # Préparer les données
    y_pos = np.arange(len(df_age))
    hommes = -df_age['Hommes'] / 1000  # Négatif pour gauche, en milliers
    femmes = df_age['Femmes'] / 1000    # En milliers
    
    # Créer les barres
    ax.barh(y_pos, hommes, color='#3498db', label='Hommes', height=0.8)
    ax.barh(y_pos, femmes, color='#e74c3c', label='Femmes', height=0.8)
    
    # Configuration
    ax.set_yticks(y_pos)
    ax.set_yticklabels(df_age['Groupe_Age'])
    ax.set_xlabel('Population (milliers)', fontsize=12)
    ax.set_title('Pyramide des Âges du Bénin (2024)', 
                 fontsize=16, fontweight='bold', pad=20)
    ax.axvline(0, color='black', linewidth=0.8)
    ax.legend(loc='upper right', fontsize=11)
    ax.grid(True, alpha=0.3, axis='x')
    
    # Ajuster les limites x pour symétrie
    max_val = max(abs(hommes).max(), femmes.max())
    ax.set_xlim(-max_val*1.1, max_val*1.1)
    
    # Formater les labels de l'axe x en valeurs absolues
    ax.set_xticklabels([f'{abs(int(x))}' for x in ax.get_xticks()])
    
    plt.tight_layout()
    plt.savefig('/mnt/user-data/outputs/viz_pyramide_ages.png', dpi=300, bbox_inches='tight')
    print("✅ Sauvegardé: viz_pyramide_ages.png\n")
    plt.close()

def visualiser_departements(df_dept):
    """
    Visualisations par département
    """
    print("📊 Création: Analyse par département...")
    
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(16, 12))
    
    # Trier par population
    df_sorted = df_dept.sort_values('Population', ascending=True)
    
    # 1. Population par département
    colors1 = plt.cm.viridis(np.linspace(0.3, 0.9, len(df_sorted)))
    ax1.barh(df_sorted['Departement'], df_sorted['Population']/1000, color=colors1)
    ax1.set_xlabel('Population (milliers)', fontsize=11)
    ax1.set_title('Population par Département', fontsize=13, fontweight='bold')
    ax1.grid(True, alpha=0.3, axis='x')
    
    # 2. Densité de population
    df_density = df_dept.sort_values('Densite_km2', ascending=True)
    colors2 = plt.cm.RdYlGn_r(np.linspace(0.2, 0.8, len(df_density)))
    ax2.barh(df_density['Departement'], df_density['Densite_km2'], color=colors2)
    ax2.set_xlabel('Densité (hab/km²)', fontsize=11)
    ax2.set_title('Densité de Population par Département', fontsize=13, fontweight='bold')
    ax2.grid(True, alpha=0.3, axis='x')
    
    # 3. Part de la population nationale
    top10 = df_dept.nlargest(10, 'Pct_Population_Nationale')
    colors3 = plt.cm.Set3(np.linspace(0, 1, len(top10)))
    wedges, texts, autotexts = ax3.pie(top10['Pct_Population_Nationale'], 
                                         labels=top10['Departement'],
                                         autopct='%1.1f%%',
                                         colors=colors3,
                                         startangle=90)
    ax3.set_title('Répartition de la Population Nationale\n(Top 10 Départements)', 
                  fontsize=13, fontweight='bold')
    for autotext in autotexts:
        autotext.set_color('black')
        autotext.set_fontsize(9)
    
    # 4. Taux d'urbanisation par département
    df_urban = df_dept.sort_values('Taux_Urbanisation_%', ascending=True)
    colors4 = plt.cm.coolwarm(np.linspace(0.2, 0.8, len(df_urban)))
    ax4.barh(df_urban['Departement'], df_urban['Taux_Urbanisation_%'], color=colors4)
    ax4.set_xlabel('Taux d\'Urbanisation (%)', fontsize=11)
    ax4.set_title('Taux d\'Urbanisation par Département', fontsize=13, fontweight='bold')
    ax4.grid(True, alpha=0.3, axis='x')
    ax4.axvline(df_dept['Taux_Urbanisation_%'].mean(), color='red', 
                linestyle='--', linewidth=2, label='Moyenne nationale')
    ax4.legend()
    
    plt.tight_layout()
    plt.savefig('/mnt/user-data/outputs/viz_analyse_departements.png', dpi=300, bbox_inches='tight')
    print("✅ Sauvegardé: viz_analyse_departements.png\n")
    plt.close()

def visualiser_indicateurs_sociaux(df_social):
    """
    Indicateurs sociaux
    """
    print("📊 Création: Indicateurs sociaux...")
    
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(16, 12))
    
    # 1. Alphabétisation
    ax1.plot(df_social['Annee'], df_social['Taux_Alphabetisation_Hommes_%'], 
             linewidth=2.5, marker='o', color='#3498db', label='Hommes')
    ax1.plot(df_social['Annee'], df_social['Taux_Alphabetisation_Femmes_%'], 
             linewidth=2.5, marker='s', color='#e74c3c', label='Femmes')
    ax1.set_title('Évolution du Taux d\'Alphabétisation', fontsize=13, fontweight='bold')
    ax1.set_xlabel('Année', fontsize=11)
    ax1.set_ylabel('Taux (%)', fontsize=11)
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    
    # 2. Scolarisation
    ax2.plot(df_social['Annee'], df_social['Taux_Scolarisation_Primaire_%'], 
             linewidth=2.5, marker='o', color='#27ae60', label='Primaire')
    ax2.plot(df_social['Annee'], df_social['Taux_Scolarisation_Secondaire_%'], 
             linewidth=2.5, marker='s', color='#f39c12', label='Secondaire')
    ax2.set_title('Évolution des Taux de Scolarisation', fontsize=13, fontweight='bold')
    ax2.set_xlabel('Année', fontsize=11)
    ax2.set_ylabel('Taux (%)', fontsize=11)
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    
    # 3. Accès aux services de base
    ax3.plot(df_social['Annee'], df_social['Acces_Eau_Potable_%'], 
             linewidth=2.5, marker='o', label='Eau potable')
    ax3.plot(df_social['Annee'], df_social['Acces_Electricite_%'], 
             linewidth=2.5, marker='s', label='Électricité')
    ax3.plot(df_social['Annee'], df_social['Acces_Soins_Sante_%'], 
             linewidth=2.5, marker='^', label='Soins de santé')
    ax3.set_title('Accès aux Services de Base', fontsize=13, fontweight='bold')
    ax3.set_xlabel('Année', fontsize=11)
    ax3.set_ylabel('Taux d\'accès (%)', fontsize=11)
    ax3.legend()
    ax3.grid(True, alpha=0.3)
    
    # 4. Comparaison 2010 vs 2024
    derniere_annee = df_social.iloc[-1]
    premiere_annee = df_social.iloc[0]
    
    categories = ['Alphabétisation\n(Moyenne)', 'Scolarisation\nPrimaire', 
                  'Eau Potable', 'Électricité']
    valeurs_2010 = [
        (premiere_annee['Taux_Alphabetisation_Hommes_%'] + premiere_annee['Taux_Alphabetisation_Femmes_%'])/2,
        premiere_annee['Taux_Scolarisation_Primaire_%'],
        premiere_annee['Acces_Eau_Potable_%'],
        premiere_annee['Acces_Electricite_%']
    ]
    valeurs_2024 = [
        (derniere_annee['Taux_Alphabetisation_Hommes_%'] + derniere_annee['Taux_Alphabetisation_Femmes_%'])/2,
        derniere_annee['Taux_Scolarisation_Primaire_%'],
        derniere_annee['Acces_Eau_Potable_%'],
        derniere_annee['Acces_Electricite_%']
    ]
    
    x = np.arange(len(categories))
    width = 0.35
    
    ax4.bar(x - width/2, valeurs_2010, width, label='2010', color='#95a5a6')
    ax4.bar(x + width/2, valeurs_2024, width, label='2024', color='#2ecc71')
    ax4.set_title('Progrès des Indicateurs Sociaux (2010 vs 2024)', 
                  fontsize=13, fontweight='bold')
    ax4.set_ylabel('Taux (%)', fontsize=11)
    ax4.set_xticks(x)
    ax4.set_xticklabels(categories)
    ax4.legend()
    ax4.grid(True, alpha=0.3, axis='y')
    
    plt.tight_layout()
    plt.savefig('/mnt/user-data/outputs/viz_indicateurs_sociaux.png', dpi=300, bbox_inches='tight')
    print("✅ Sauvegardé: viz_indicateurs_sociaux.png\n")
    plt.close()

def creer_dashboard_resume(df_pop, df_age, df_dept):
    """
    Crée un dashboard résumé avec les KPIs principaux
    """
    print("📊 Création: Dashboard résumé...")
    
    fig = plt.figure(figsize=(16, 10))
    gs = fig.add_gridspec(3, 3, hspace=0.3, wspace=0.3)
    
    # Couleurs
    color_primary = '#2c3e50'
    color_accent = '#3498db'
    
    # KPI 1: Population actuelle
    ax1 = fig.add_subplot(gs[0, 0])
    ax1.text(0.5, 0.7, f"{df_pop['Population_Totale'].iloc[-1]/1e6:.2f}M", 
             ha='center', va='center', fontsize=40, fontweight='bold', color=color_primary)
    ax1.text(0.5, 0.3, 'Population Totale\n(2024)', 
             ha='center', va='center', fontsize=14, color='gray')
    ax1.axis('off')
    
    # KPI 2: Taux de croissance
    ax2 = fig.add_subplot(gs[0, 1])
    ax2.text(0.5, 0.7, f"+{df_pop['Taux_Croissance_%'].iloc[-1]:.1f}%", 
             ha='center', va='center', fontsize=40, fontweight='bold', color='#27ae60')
    ax2.text(0.5, 0.3, 'Taux de Croissance\nAnnuel', 
             ha='center', va='center', fontsize=14, color='gray')
    ax2.axis('off')
    
    # KPI 3: Âge médian
    ax3 = fig.add_subplot(gs[0, 2])
    ax3.text(0.5, 0.7, '18 ans', 
             ha='center', va='center', fontsize=40, fontweight='bold', color='#e74c3c')
    ax3.text(0.5, 0.3, 'Âge Médian\n(Population jeune)', 
             ha='center', va='center', fontsize=14, color='gray')
    ax3.axis('off')
    
    # Graphique: Évolution population (petit)
    ax4 = fig.add_subplot(gs[1, :])
    ax4.plot(df_pop['Annee'], df_pop['Population_Totale']/1e6, 
             linewidth=3, color=color_accent)
    ax4.fill_between(df_pop['Annee'], df_pop['Population_Totale']/1e6, alpha=0.3, color=color_accent)
    ax4.set_title('Croissance de la Population (1990-2024)', fontsize=14, fontweight='bold')
    ax4.set_ylabel('Population (millions)', fontsize=11)
    ax4.grid(True, alpha=0.3)
    
    # Top 5 départements
    ax5 = fig.add_subplot(gs[2, :2])
    top5 = df_dept.nlargest(5, 'Population')
    colors = plt.cm.viridis(np.linspace(0.3, 0.9, len(top5)))
    ax5.barh(top5['Departement'], top5['Population']/1000, color=colors)
    ax5.set_xlabel('Population (milliers)', fontsize=11)
    ax5.set_title('Top 5 Départements les Plus Peuplés', fontsize=12, fontweight='bold')
    ax5.grid(True, alpha=0.3, axis='x')
    
    # Répartition par genre (estimation)
    ax6 = fig.add_subplot(gs[2, 2])
    total_hommes = df_age['Hommes'].sum()
    total_femmes = df_age['Femmes'].sum()
    sizes = [total_hommes, total_femmes]
    colors = ['#3498db', '#e74c3c']
    wedges, texts, autotexts = ax6.pie(sizes, labels=['Hommes', 'Femmes'], 
                                         autopct='%1.1f%%', colors=colors, startangle=90)
    ax6.set_title('Répartition par Genre', fontsize=12, fontweight='bold')
    for autotext in autotexts:
        autotext.set_color('white')
        autotext.set_fontweight('bold')
    
    plt.suptitle('DASHBOARD DÉMOGRAPHIQUE - BÉNIN 2024', 
                 fontsize=18, fontweight='bold', y=0.98)
    
    plt.savefig('/mnt/user-data/outputs/viz_dashboard_resume.png', dpi=300, bbox_inches='tight')
    print("✅ Sauvegardé: viz_dashboard_resume.png\n")
    plt.close()

def main():
    """
    Fonction principale
    """
    print("\n" + "="*70)
    print("  GÉNÉRATION DES VISUALISATIONS DÉMOGRAPHIQUES")
    print("  Auteur: Freud GUEDOU | Octobre 2024")
    print("="*70 + "\n")
    
    # Charger les données
    df_pop, df_age, df_dept, df_social = charger_donnees()
    
    # Créer toutes les visualisations
    visualiser_evolution_population(df_pop)
    visualiser_pyramide_age(df_age)
    visualiser_departements(df_dept)
    visualiser_indicateurs_sociaux(df_social)
    creer_dashboard_resume(df_pop, df_age, df_dept)
    
    print("="*70)
    print("✅ TOUTES LES VISUALISATIONS ONT ÉTÉ CRÉÉES!")
    print("="*70)
    print("\n📁 Fichiers générés:")
    print("   • viz_evolution_population.png")
    print("   • viz_pyramide_ages.png")
    print("   • viz_analyse_departements.png")
    print("   • viz_indicateurs_sociaux.png")
    print("   • viz_dashboard_resume.png")
    print("\n🎯 Ces visualisations peuvent être:")
    print("   • Utilisées dans des présentations")
    print("   • Intégrées dans Power BI/Tableau")
    print("   • Ajoutées à des rapports Excel")
    print("\n" + "="*70 + "\n")

if __name__ == "__main__":
    main()
