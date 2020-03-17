from django.test import TestCase
from Patients.models import *
# Create your tests here.

class testCaseSetUp(APITestCase):
    def setUp(self):
        self.patient = Patient.objects.create(
            patientID= "123abcd",
			studyID= "123abcd",
			date_of_birth= "2020-03-17",
			prefix= "Miss",
			firstName= "Emily",
			middleName= "March",
			lastName= "Bronte",
			suffix= "",
			com_name= "Emily",
			gender= "F",
			householdID= "3",
			dur_hh= "1",
			notes= "",
			lvl_edu= "TERTIARY",
			work_status= "EMPLOYED",
			marital_status= "MARRIED",
			motherFirstName= "Charlotte",
			motherLastName= "March",
			tel1_num= "0123170335",
			tel1_owner= "SELF",
			tel1_owner_rel= "SELF",
			tel2_num= "",
			tel2_owner= "",
			tel2_owner_rel= "",
			enumeratorID= "1",
			nationalID= "980720327163",
			deceased= 0,
			deceased_date= None,
			responder= "Emily Bronte",
			proxy_name= "",
			proxy_rel= ""
        )