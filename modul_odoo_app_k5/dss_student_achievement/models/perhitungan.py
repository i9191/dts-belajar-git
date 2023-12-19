# Import the odoo models module
from odoo import models, fields, api
# Import the numpy and pandas libraries
import numpy as np
import pandas as pd
# Import the base64 library
import base64
import logging
_logger = logging.getLogger(__name__)

# Define the class for the wizard_readCsv model
class Wizard_readCsv(models.TransientModel):
    # Define the name of the model
    _name = "wizard.readcsv"
    # Define the description of the model
    _description = "Wizard to read csv file as input for the selection calculation"

    # Define the fields for the model
    # The file field will store the binary data of the csv file
    file = fields.Binary(string="File CSV", required=True)
    # The filename field will store the name of the csv file
    filename = fields.Char(string="Filename")

    # Define a method to read the csv file and return the dataframe
    @api.model
    def read_csv(self):
        # Decode the binary data of the file field
        data = base64.b64decode(self.file)
        # Read the csv file as a dataframe
        df = pd.read_csv(data)
        # Return the dataframe
        return df

    # Define a method to get all data
    @api.model
    def get_data_mhs(self):
        _logger.info("Get Data Mahasiswa...")
        mhs_model = "mahasiswa.dataakademik"
        return self.env[mhs_model].search([])

    # Define a method to get the criteria and alternatives from the dataframe
    @api.model
    def get_criteria_alternatives(self):
        _logger.info("Get Criteria & Alternatives...")
        datamhs = self.get_data_mhs()
        data_list = []
        for row in datamhs:
            if any(elem['nim'] == row.nim for elem in data_list):
                print("nope")
            else:
                data_list.append({
                    'nim': row.nim,
                    'nama': row.nama,
                    'Prestasi': row.prestasi,
                    'Kompen': row.kompen,
                    **row.nilai
                })

        # Create the DataFrame
        datamhs_df = pd.DataFrame(data_list)
        # Define the criteria and alternatives
        # criteria = ["Nilai Prestasi", "Manajemen Proyek", "Keamanan Informasi", "E-Business", "Pemrograman Platform Bergerak (Mobile)", "Sistem Pendukung Keputusan", "Pengolahan Citra Digital", "Proyek Tingkat III", "Alpaku"]
        # alternatives = df["Nama"]
        # matkul = list(datamhs[0].nilai.keys())
        # criteria = ["prestasi"]
        # criteria.extend(matkul)
        # criteria.append("kompen")
        criteria = []
        for row in self.env['rank.stage'].search([], order='sequence asc'):
            criteria.append(row.criteria)
        alternatives = datamhs_df["nim"]

        # Extract the decision matrix from the dataframe
        # matrix = df[criteria].to_numpy()
        matrix = datamhs_df[criteria].to_numpy()

        # Return the criteria, alternatives, and matrix
        return criteria, alternatives, matrix

    # Define a method to calculate the weights using ROC method
    @api.model
    def calculate_weights(self,length):
        _logger.info("Calculate Weigth...")

        # Define the rank of the criteria
        # rank = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        rank = []
        for x in range(length):
            rank.append(x+1)
        # Calculate the length of the rank list
        n = len(rank)
        # Initialize an empty list for the weights
        weights = []
        # Loop through each value in the rank list
        for i in rank:
            # Calculate the weight for each value
            w = sum([1 / j for j in range(i, n + 1)]) / n
            # Append the weight to the list
            weights.append(w)
        # Convert the list to a numpy array
        weights = np.array(weights)
        # Return the weights
        return weights

    # Define a method to normalize the matrix using vector normalization
    @api.model
    def normalize_matrix(self):
        _logger.info("Normalize Matx...")
        # Get the matrix from the get_criteria_alternatives method
        criteria, alternatives, matrix = self.get_criteria_alternatives()
        # Normalize the matrix using vector normalization
        norm_matrix = matrix / np.sqrt(np.sum(matrix ** 2, axis=0))
        # Return the normalized matrix
        return norm_matrix, criteria

    # Define a method to calculate the weighted normalized matrix
    @api.model
    def calculate_weighted_matrix(self):
        _logger.info("Calculate Weigthed Matx...")
        # Get the normalized matrix from the normalize_matrix method
        norm_matrix, criteria = self.normalize_matrix()
        # Get the weights from the calculate_weights method
        weights = self.calculate_weights(len(criteria))
        # Calculate the weighted normalized matrix
        weighted_matrix = norm_matrix * weights
        # Return the weighted normalized matrix
        return weighted_matrix

    # Define a method to separate the benefit and cost criteria from the weighted matrix
    @api.model
    def separate_benefit_cost(self):
        _logger.info("Benefit-Cost...")
        # Get the weighted normalized matrix from the calculate_weighted_matrix method
        weighted_matrix = self.calculate_weighted_matrix()
        # Separate the benefit and cost criteria from the weighted matrix
        benefit_criteria = weighted_matrix[:, :-1]  # All columns except the last one
        cost_criteria = weighted_matrix[:, -1]  # The last column
        # Return the benefit and cost criteria
        return benefit_criteria, cost_criteria

    # Define a method to calculate the MOORA ratio for each alternative
    @api.model
    def calculate_ratio(self):
        _logger.info("Calculate Ratio...")
        # Get the benefit and cost criteria from the separate_benefit_cost method
        benefit_criteria, cost_criteria = self.separate_benefit_cost()
        # Calculate the MOORA ratio for each alternative
        ratio = np.sum(benefit_criteria, axis=1) - cost_criteria
        # Return the ratio
        return ratio

    # Define a method to rank the alternatives based on the MOORA ratio
    @api.model
    def rank_alternatives(self):
        _logger.info("Ranking...")
        # Get the alternatives and ratio from the get_criteria_alternatives and calculate_ratio methods
        criteria, alternatives, matrix = self.get_criteria_alternatives()
        ratio = self.calculate_ratio()
        # Create a dataframe with the alternative and ratio columns
        rank_df = pd.DataFrame({"Alternative": alternatives, "Ratio": ratio})
        # Sort the dataframe by the ratio column in descending order
        rank_df = rank_df.sort_values(by="Ratio", ascending=False)
        # Reset the index of the dataframe
        rank_df = rank_df.reset_index(drop=True)
        # Return the dataframe
        return rank_df
    
    # Define a method to display the ranking result
    @api.model
    def display_result(self):
        # Get the dataframe from the rank_alternatives method
        rank_df = self.rank_alternatives()
        # Print the result
        print("The ranking of the alternatives based on the MOORA method are:")
        print(rank_df)

    def hitung_dss(self):
        _logger.info("ok")
        rank_df = self.rank_alternatives()
        # _logger.info(rank_df)
        rankmodel = self.env['rank.model']
        # panggil fungsi create dari models rank.model
        rankmodel.set_df(rank_df)
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'rank.model',
            'view_mode': 'tree,form',
            'view_type': 'tree'
        }

# Define the class for the rank_model model
class Rank_model(models.Model):
    # Define the name of the model
    _name = "rank.model"
    # Define the description of the model
    _description = "Model to store the ranking result"
    _order = "rank"

    # Define the fields for the model
    # The name field will store the name of the alternative
    nim = fields.Char(string="NIM", required=True)
    name = fields.Char(string="Name", required=True)
    # The ratio field will store the MOORA ratio of the alternative
    ratio = fields.Float(string="Ratio", required=True)
    # The rank field will store the rank of the alternative
    rank = fields.Integer(string="Rank", required=True)
    # stage_id = fields.Integer(string="Stage")

    @api.model
    def set_df(self, rank_df):
        # Loop through each row of the dataframe
        for index, row in rank_df.iterrows():
            # Create a dictionary with the field values
            record = self.search([('nim', '=', row["Alternative"])])
            if record:
                vals = {
                    "ratio": row["Ratio"],
                    "rank": index + 1
                }
                # edit a record with the dictionary
                record.write(vals)
            else:
                vals = {
                    "nim": row["Alternative"],
                    "name": self.env['mahasiswa.data'].search([('nim', '=', row["Alternative"])]).nama,
                    "ratio": row["Ratio"],
                    "rank": index + 1
                }
                # Create a record with the dictionary
                self.create(vals)
        record = self.search([], limit=5)
        var = {}
        for i, row in enumerate(record):
            # tambahkan key-value pair dengan format 'nama{i}':nama
            var[f'name{i+1}'] = row.name
            # tambahkan key-value pair dengan format 'nilai{i}':nilai
            var[f'value{i+1}'] = row.ratio
        self.env['x_my_model'].create(var)

    def action_rank(self):
        # kembalikan action yang sudah didefinisikan di views xml
        return self.env.ref('import_data_mahasiswa.action_rank').read()[0]
    def action_hitung_dss(self):
        # kembalikan action yang sudah didefinisikan di views xml
        return self.env.ref('dss_student_achievement.action_hitung_dss').read()[0]

