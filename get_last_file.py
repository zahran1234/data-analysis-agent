
def get_last_uploaded_file(dir:str):
    date_with_path={}
    dates=[]
    from pathlib import Path

    # Specify the directory
    directory = Path(dir)

    # Get all files (non-recursively)
    files = [f for f in directory.iterdir() if f.is_file()]

    for i in files:
        # Specify the PDF file path
        file_path = i
        # Read the PDF file
        reader = PdfReader(file_path)

        # Extract metadata
        metadata = reader.metadata

        # Access specific metadata fields
        creation_date = metadata.get("/CreationDate", "Unknown")
        modification_date = metadata.get("/ModDate", "Unknown")

            # Step 1: Remove the "D:" prefix
        if creation_date.startswith("D:"):
            creation_date = creation_date[2:]

        # Step 2: Remove the timezone offset
        creation_date = creation_date.split("+")[0]

        # Step 3: Parse the cleaned date
        parsed_date = datetime.strptime(creation_date, "%Y%m%d%H%M%S")
        dates.append(parsed_date)
        date_with_path[parsed_date]= i
    return date_with_path[sorted(dates)[-1]]


