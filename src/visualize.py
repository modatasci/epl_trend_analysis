
# load libraries
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd

color_dict = {
        1: "#5E8C61",  # 1st
        2: '#0E6BA8',  # 2nd
        3: '#0E6BA8',  # 3rd
        4: '#0E6BA8',  
        5: "#6DB6E7",
        6: "#6DB6E7",
        7: '#6DB6E7',
        8: '#DDD8D8',
        9: '#DDD8D8',
        10: '#DDD8D8',
        11: '#DDD8D8',
        12: '#DDD8D8',
        13: '#DDD8D8',
        14: "#DDD8D8",
        15: '#EB9151',
        16: '#EB9151',
        17: "#EB9151",
        18: '#EB5160',
        19: '#EB5160',
        20: '#EB5160',
    }


def visualize_league_standings(df: pd.DataFrame, project_root: str = None):

    fig, ax = plt.subplots(figsize=(12,6),facecolor='#FAF9F4')

    
    sns.scatterplot( data=df
                    , x='Season', y='total_points'
                    , hue='rank',palette=color_dict,edgecolor='black',alpha=0.8, linewidth=0.3
                    , ax=ax
                    )

    # set axis color
    ax.set_facecolor('#FAF9F4')

    # set grid
    ax.grid(axis='y',color='grey',linestyle='-',alpha=0.1)

    # set legend position
    ax.legend(title='Rank',bbox_to_anchor=(1.02, 1), loc='upper left',facecolor='#FAF9F4',edgecolor='#FAF9F4')


    # set xaxis ticks
    ax.set_xticklabels(ax.get_xticklabels(), rotation=45,fontname='Verdana',weight='light',size=8)
    ax.set_xlabel(None)

    # set yaxis title
    ax.set_ylabel("Total Points")

    ax.tick_params(axis='y',labelcolor='black',colors='grey',length=0)


    # set border
    ax.spines[['left','right']].set_visible(False)

    plt.rcParams['font.family'] = 'Roboto Slab'

    # set figure title
    plt.suptitle("Evolution of Premier League Competitiveness",x=0.05,ha='left',y=1,color='#071013',fontsize=14)

    # set figure subtitle
    fig.text(0.05, 0.94, "Final league points since 05/06 until 24/25", ha='left', fontsize=10, color="#686868",fontname='Verdana',fontweight='medium')

    plt.tight_layout()

    plt.savefig(f"{project_root}/figures/league_points.png",dpi=600,bbox_inches="tight",facecolor='#FAF9F4')

    plt.show()


def main():
    print("This is the python script to visualize the EPL league points data")


if __name__ == "__main__":
    main()