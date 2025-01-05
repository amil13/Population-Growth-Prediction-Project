import csv
import os
from django.core.management.base import BaseCommand
from population.models import PopulationData

class Command(BaseCommand):
    """
    Django management command to load population data into the database from CSV files.
    
    This command reads all CSV files in a specified folder, processes each row, 
    and inserts the data into the PopulationData model in batches for efficiency.
    
    Attributes:
        help (str): Short description of the command.
    """
    
    help = 'Load population data into the database from all CSV files in the cleaned_data folder'

    def add_arguments(self, parser):
        """
        Adds arguments to the command line parser. 
        Allows users to specify the input folder containing the cleaned CSV files.

        Args:
            parser (ArgumentParser): Argument parser for adding custom command line arguments.
        """
        # Add an argument for the input folder where CSV files are located
        parser.add_argument(
            'input_folder', 
            type=str, 
            help='Folder containing the cleaned CSV files to be loaded into the database.'
        )

    def handle(self, *args, **kwargs):
        """
        Handles the main logic of the command. Iterates through all CSV files in the specified 
        input folder, processes them row by row, and inserts data into the PopulationData model 
        in batches for efficiency.
        
        Args:
            *args: Additional positional arguments (unused).
            **kwargs: Keyword arguments, including the input folder specified by the user.
        """
        # Get the input folder from the command arguments
        input_folder = kwargs['input_folder']
        batch_size = 1000  # The batch size to control memory usage when inserting records

        # Check if the input folder exists
        if not os.path.exists(input_folder):
            self.stdout.write(self.style.ERROR(f"The folder '{input_folder}' does not exist."))
            return

        # Iterate through all CSV files in the input folder
        for file_name in os.listdir(input_folder):
            if file_name.endswith('.csv'):
                file_path = os.path.join(input_folder, file_name)
                ## Debugging
                # self.stdout.write(self.style.NOTICE(f'Loading {file_name}'))

                # List to accumulate records to insert into the database
                records_to_create = []

                # Open the CSV file for reading
                with open(file_path, 'r') as file:
                    reader = csv.DictReader(file)

                    # Process each row in the CSV
                    for row in reader:
                        try:
                            # Ensure the required fields are present and valid
                            if not row['Valor'] or not row['Data_Referencia']:
                                ## Debugging
                                # self.stdout.write(self.style.WARNING(f'Skipping row with missing data: {row}'))
                                continue

                            ## Debug log: Check the content of the current row
                            # self.stdout.write(self.style.NOTICE(f"Processing row: {row}"))

                            # Append the row as a new PopulationData object
                            records_to_create.append(PopulationData(
                                date=row['Data_Referencia'],
                                population_count=row['Valor'],  # Map 'Valor' from the CSV to the model's field
                                nationality=row['NACIONALITAT_G'],
                            ))

                            # Insert records in batches to optimize memory usage
                            if len(records_to_create) >= batch_size:
                                PopulationData.objects.bulk_create(records_to_create)
                                records_to_create = []  # Reset the list after insertion

                        except KeyError as e:
                            # Handle case where a column is missing in the current row
                            self.stdout.write(self.style.ERROR(f"Missing column in row: {e}. Row: {row}"))
                        except Exception as e:
                            # Handle any other errors
                            self.stdout.write(self.style.ERROR(f"Error processing row: {e}. Row: {row}"))

                # Insert any remaining records after processing the file
                if records_to_create:
                    PopulationData.objects.bulk_create(records_to_create)
                ## Debugging
                # self.stdout.write(self.style.SUCCESS(f'Successfully loaded data from {file_name}'))

        # Final success message after all files are processed
        self.stdout.write(self.style.SUCCESS('All CSV data loaded successfully!'))
