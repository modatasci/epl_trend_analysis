from pathlib import Path
from src.data_prep import scrap_raw_dataset, import_dataset, format_dataset
from src.visualize import visualize_league_standings

def main():
    
    # Setup
    project_root = Path.cwd()
    
    # Load data
    df = import_dataset()

    # modify data
    dataset = format_dataset(df)

    # store dataset to processed folder
    dataset.to_csv(f"{project_root}/data/processed/total_points_by_season.csv",index=False)
    
    # Visualize
    visualize_league_standings(dataset, project_root=project_root)
    

if __name__ == "__main__":
    main()
