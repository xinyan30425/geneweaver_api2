# test_crud.py
import unittest
from unittest.mock import patch
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from api.database import Base, get_db  
from api import crud, models
import json


class TestCRUD(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Setup in-memory database before all tests
        cls.engine = create_engine("sqlite:///:memory:", connect_args={"check_same_thread": False})
        Base.metadata.create_all(cls.engine)
        cls.TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=cls.engine)

    def setUp(self):
        # Create a new session for each test
        self.db = self.TestingSessionLocal()
        self.load_test_data()

    def tearDown(self):
        # Close the session after each test
        self.db.close()
        
    def clean_database(self):
        # Clear all data from the database tables
        self.db.query(models.GeneSet).delete()
        self.db.query(models.AnalysisRun).delete()
        self.db.query(models.AnalysisResult).delete()
        self.db.commit()
    
    def load_test_data(self):
    # Create test data
        test_data = [
            {
            "geneweaver_id": 65469,
            "entrez": '1278',
            "ensembl_gene": 'ENSG00000206075',
            "unigene": 'Hs.59495|Hs.55279|Hs.387|Hs.94960|Hs.554190|Hs.58230|Hs.514912' 
        },
        {
            "geneweaver_id": 65243,
            "entrez": '22943',
            "ensembl_gene": 'ENSG00000107984',
            "unigene": 'Hs.720381|Hs.75389|Hs.726439|Hs.728292|Hs.40499'
        },
            
        ]
        for record in test_data:
            unigene_list = record["unigene"].split('|')
            unigene_dict = {"unigene": unigene_list}
            unigene_json = json.dumps(unigene_dict)
            test_geneset = models.GeneSet(
                geneweaver_id=record["geneweaver_id"],
                entrez=record["entrez"],
                ensembl_gene=record["ensembl_gene"],
                unigene=unigene_json,
            # ... include other fields as necessary
            )
            self.db.add(test_geneset)
        self.db.commit()


    # Test cases
    # def test_create_geneset(self):
    #     geneset_create = {"geneweaver_id": 2, "entrez": 'entrez', "ensembl_gene": 'gene', "unigene": ['unigene']}
    #     geneset = crud.create_geneset(self.db, geneset_create)
    #     self.assertEqual(geneset.geneweaver_id, 2)
    #     self.assertEqual(geneset.entrez, 'entrez')
    
    
    # @patch('api.crud.BooleanAlgebra')
    # def test_perform_boolean_algebra(self, MockBooleanAlgebra):
    #     mock_result = MockBooleanAlgebra.return_value.run.return_value
    #     mock_result.result_geneset_ids = {'mocked_result'}
    #     result = crud.perform_boolean_algebra(self.db, 'union', [65066, 65243])
    #     self.assertIn('mocked_result', result)

    # def test_create_analysis_run(self):
    #     new_run = crud.create_analysis_run(self.db)
    #     self.assertIsNotNone(new_run, "Newly created analysis run should not be None")

    def test_get_geneset_unigenes(self):
        unigenes = crud.get_geneset_unigenes(self.db, 65243)
        expected_unigenes = {'Hs.720381','Hs.75389','Hs.726439','Hs.728292','Hs.40499'}
        
        # Convert sets to sorted lists
        sorted_unigenes = sorted(list(unigenes))
        sorted_expected_unigenes = sorted(list(expected_unigenes))
    
        # Now use assertListEqual to compare the sorted lists
        self.assertListEqual(sorted_unigenes, sorted_expected_unigenes)

    @patch('api.crud.get_geneset_unigenes')
    def test_perform_boolean_algebra_analysis(self, mock_get_geneset_unigenes):
    # Mocking the gene sets for the provided GeneWeaver IDs
        mock_get_geneset_unigenes.side_effect = [
            {'Hs.59495', 'Hs.55279', 'Hs.387', 'Hs.94960', 'Hs.554190', 'Hs.58230', 'Hs.514912'},  # Genes for GeneWeaver ID 65469
            {'Hs.720381', 'Hs.75389', 'Hs.726439', 'Hs.728292', 'Hs.40499'}  # Genes for GeneWeaver ID 65243
        ]

        task_id = 1
        gene_weaver_ids = [65469, 65243]
        operation = "union"
        crud.perform_boolean_algebra_analysis(task_id, self.db, gene_weaver_ids, operation)
    
        run = self.db.query(models.AnalysisRun).filter_by(id=task_id).first()
        result = self.db.query(models.AnalysisResult).filter_by(run_id=task_id).first()

        self.assertEqual(run.status, models.RunStatus.COMPLETED.value)
        self.assertIsNotNone(result)

        # Assuming the analysis is supposed to return a union of the genesets
        expected_result = {'Hs.59495', 'Hs.55279', 'Hs.387', 'Hs.94960', 'Hs.554190', 'Hs.58230', 'Hs.514912', 'Hs.720381', 'Hs.75389', 'Hs.726439', 'Hs.728292', 'Hs.40499'}
    
        # Convert the result to a set for comparison
        actual_result_set = set(json.loads(result.result_data)['result'])
    
        self.assertEqual(actual_result_set, expected_result)

        
        
        
        
        

    # def test_update_run_status_and_time(self):
    #     run_id = 1
    #     status = models.RunStatus.RUNNING
    #     crud.update_run_status_and_time(self.db, run_id, status, start_time=True)
    #     run = self.db.query(models.AnalysisRun).filter_by(id=run_id).first()
    #     self.assertEqual(run.status, status, "Run status should be updated to RUNNING")
    #     self.assertIsNotNone(run.start_time, "Start time should not be None")


    # def test_get_all_runs(self):
    #     runs = crud.get_all_runs(self.db)
    #     self.assertIsNotNone(runs, "Runs should not be None")

    # def test_cancel_run(self):
    #     run_id = 1
    #     canceled_run = crud.cancel_run(self.db, run_id)
    #     # self.assertIsNotNone(canceled_run, "Canceled run should not be None")
    #     self.assertEqual(canceled_run.status, models.RunStatus.CANCELED, "Run status should be CANCELED")

    # def test_save_analysis_result(self):
    #     run_id = 1
    #     result_data = ["gene1", "gene2"]
    #     crud.save_analysis_result(self.db, run_id, result_data)
    #     result = self.db.query(models.AnalysisResult).filter_by(run_id=run_id).first()
    #     # self.assertIsNotNone(result, "Result should not be None")
    #     self.assertEqual(json.loads(result.result_data)["result"], result_data, "Result data should match the saved data")

    # def test_get_run_result(self):
    #     run_id = 1
    #     result = crud.get_run_result(self.db, run_id)
    #     self.assertIsNotNone(result, "Result should not be None")

    # def test_get_runstatus(self):
    #     run_id = 1
    #     status = crud.get_runstatus(self.db, run_id)
    #     self.assertIsNotNone(status, "Complete")

    
if __name__=="__main__":
    unittest.main()




