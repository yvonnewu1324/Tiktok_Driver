import pandas as pd


def extract_columns(input_csv, output_csv):
    # read the original CSV file
    df = pd.read_csv(input_csv)

    # extract the specified columns
    columns_to_extract = [
        'video_id', 'video_description', 'video_sharecount',
        'video_commentcount', 'video_playcount',
        'author_username', 'author_name'
    ]
    df_extracted = df[columns_to_extract]

    # save the extracted columns to a new CSV file
    df_extracted.to_csv(output_csv, index=False)
    print(f"Extracted columns saved to {output_csv}")


input_csv = "tiktok_data.csv"
output_csv = "extracted_tiktok.csv"
extract_columns(input_csv, output_csv)
