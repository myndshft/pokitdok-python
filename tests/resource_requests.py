from __future__ import absolute_import
import os
# resources.py contains sample API request

appointment_book_request = {
    "patient": {
        "_uuid": "500ef469-2767-4901-b705-425e9b6f7f83",
        "email": "john@hondoe.com",
        "phone": "800-555-1212",
        "birth_date": "1970-01-01",
        "first_name": "John",
        "last_name": "Doe",
        "member_id": "M000001"
    }
}

authorization_request = {
    'event': {
        'category': 'health_services_review',
        'certification_type': 'initial',
        'delivery': {
            'quantity': 1,
            'quantity_qualifier': 'visits'
        },
        'diagnoses': [
            {
                'code': '789.00',
                'date': '2014-10-01'
            }
        ],
        'place_of_service': 'office',
        'provider': {
            'organization_name': 'KELLY ULTRASOUND CENTER, LLC',
            'npi': '1760779011',
            'phone': '8642341234'
        },
        'services': [
            {
                'cpt_code': '76700',
                'measurement': 'unit',
                'quantity': 1
            }
        ],
        'type': 'diagnostic_medical'
    },
    'patient': {
        'birth_date': '1970-01-01',
        'first_name': 'JANE',
        'last_name': 'DOE',
        'id': '1234567890'
    },
    'provider': {
        'first_name': 'JEROME',
        'npi': '1467560003',
        'last_name': 'AYA-AY'
    },
    'trading_partner_id': 'MOCKPAYER'
}

claim_request = {
    'transaction_code': 'chargeable',
    'trading_partner_id': 'MOCKPAYER',
    'billing_provider': {
        'taxonomy_code': '207Q00000X',
        'first_name': 'Jerome',
        'last_name': 'Aya-Ay',
        'npi': '1467560003',
        'address': {
            'address_lines': [
                '8311 WARREN H ABERNATHY HWY'
            ],
            'city': 'SPARTANBURG',
            'state': 'SC',
            'zipcode': '29301'
        },
        'tax_id': '123456789'
    },
    'subscriber': {
        'first_name': 'Jane',
        'last_name': 'Doe',
        'member_id': 'W000000000',
        'address': {
            'address_lines': ['123 N MAIN ST'],
            'city': 'SPARTANBURG',
            'state': 'SC',
            'zipcode': '29301'
        },
        'birth_date': '1970-01-01',
        'gender': 'female'
    },
    'claim': {
        'total_charge_amount': 60.0,
        'service_lines': [
            {
                'procedure_code': '99213',
                'charge_amount': 60.0,
                'unit_count': 1.0,
                'diagnosis_codes': [
                    '487.1'
                ],
                'service_date': '2014-06-01'
            }
        ]
    }
}

claim_status_request = {
    'patient': {
        'birth_date': '1970-01-01',
        'first_name': 'JANE',
        'last_name': 'DOE',
        'id': '1234567890'
    },
    'provider': {
        'first_name': 'Jerome',
        'last_name': 'Aya-Ay',
        'npi': '1467560003'
    },
    'service_date': '2014-01-01',
    'trading_partner_id': 'MOCKPAYER'
}

claims_convert_request = """ISA*00*          *00*          *01*9012345720000  *01*9088877320000  *151004*2235*U*00501*000000007*0*T*:~
GS*HC*901234572000*908887732000*20151004*2235*7*X*005010X222~
ST*837*0001~
BHT*0019*00*2KYXDRE61GU20TFMBPA*20151004*2231*CH~
NM1*41*2*Pokitdok, Inc.*****46*12345~
PER*IC**EM*x12info@pokitdok.com~
NM1*40*2*MOCKPAYER*****46*12345~
HL*1**20*1~
PRV*BI*PXC*207Q00000X~
NM1*85*1*Aya-Ay*Jerome****XX*1467560003~
N3*8311 WARREN H ABERNATHY HWY~
N4*SPARTANBURG*SC*293010000~
REF*EI*123456789~
HL*2*1*22*0~
SBR*P*18*******ZZ~
NM1*IL*1*Doe*Jane****MI*W000000000~
N3*123 N MAIN ST~
N4*SPARTANBURG*SC*29301~
DMG*D8*19700101*F~
NM1*PR*2*MOCKPAYER*****PI*12345~
CLM*0f17b46dd39a4bb0add152e99633adbc*60***11:B:1*Y*A*Y*I~
HI*BK:4871~
LX*1~
SV1*HC:99213*60*UN*1.0***1~
DTP*472*D8*20140601~
SE*24*0001~
GE*1*905~
IEA*1*000000905~
"""

eligibility_request = {
    'member': {
        'birth_date': '1970-01-01',
        'first_name': 'Jane',
        'last_name': 'Doe',
        'id': 'W000000000'
    },
    'provider': {
        'first_name': 'JEROME',
        'last_name': 'AYA-AY',
        'npi': '1467560003'
    },
    'trading_partner_id': 'MOCKPAYER'
}

enrollment_request = {
    'action': 'Change',
    'dependents': [],
    'master_policy_number': 'ABCD012354',
    'payer': {
        'tax_id': '654456654'
    },
    'purpose': 'Original',
    'sponsor': {
        'tax_id': '999888777'
    },
    'subscriber': {
        'address': {
            'city': 'CAMP HILL',
            'county': 'CUMBERLAND',
            'line': '100 MARKET ST',
            'line2': 'APT 3G',
            'postal_code': '17011',
            'state': 'PA'
        },
        'benefit_status': 'Active',
        'benefits': [
            {
                'begin_date': ' 2015-01-01',
                'benefit_type': 'Health',
                'coordination_of_benefits': [
                    {
                        'group_or_policy_number': '890111',
                        'payer_responsibility': 'Primary',
                        'status': 'Unknown'
                    }
                ],
                'late_enrollment': False,
                'maintenance_type': 'Addition'
            },
            {
                'begin_date': '2015-01-01',
                'benefit_type': 'Dental',
                'late_enrollment': False,
                'maintenance_type': 'Addition'
            },
            {
                'begin_date': '2015-01-01',
                'benefit_type': 'Vision',
                'late_enrollment': False,
                'maintenance_type': 'Addition'
            }
        ],
        'birth_date': '1940-01-01',
        'contacts': [
            {
                'communication_number2': '7172341240',
                'communication_type2': 'Work Phone Number',
                'primary_communication_number': '7172343334',
                'primary_communication_type': 'Home Phone Number'
            }
        ],
        'eligibility_begin_date': '2014-01-01',
        'employment_status': 'Full-time',
        'first_name': 'JOHN',
        'gender': 'Male',
        'group_or_policy_number': '123456001',
        'handicapped': False,
        'last_name': 'DOE',
        'maintenance_reason': 'Active',
        'maintenance_type': 'Addition',
        'member_id': '123456789',
        'middle_name': 'P',
        'relationship': 'Self',
        'ssn': '123456789',
        'subscriber_number': '123456789',
        'substance_abuse': False,
        'tobacco_use': False
    },
    'trading_partner_id': 'MOCKPAYER',
}

_module_directory = os.path.dirname(__file__)
_x12_file_path = os.path.join(_module_directory, 'enrollment.834')

enrollment_snapshot_request = {'trading_partner_id': 'MOCKPAYER', 'x12_file': _x12_file_path}

files_request = {'trading_partner_id': 'MOCKPAYER', 'x12_file': _x12_file_path}

identity_request = {
    'prefix': 'Mr.',
    'first_name': 'Oscar',
    'middle_name': 'Harold',
    'last_name': 'Whitmire',
    'suffix': 'IV',
    'birth_date': '2000-05-01',
    'gender': 'male',
    'email': 'oscar@pokitdok.com',
    'phone': '555-555-5555',
    'secondary_phone': '333-333-4444',
    'address': {
        'address_lines': ['1400 Anyhoo Avenue'],
        'city': 'Springfield',
        'state': 'IL',
        'zipcode': '90210'
    },
    'identifiers': [
        {
            'location': [-121.93831, 37.53901],
            'provider_uuid': '1917f12b-fb6a-4016-93bc-adeb83204c83',
            'system_uuid': '967d207f-b024-41cc-8cac-89575a1f6fef',
            'value': 'W90100-IG-88'

        }
    ]
}

referrals_request = {
    'event': {
        'category': 'specialty_care_review',
        'certification_type': 'initial',
        'delivery': {
            'quantity': 1,
            'quantity_qualifier': 'visits'
        },
        'diagnoses': [
            {
                'code': '384.20',
                'date': '2014-09-30'
            }
        ],
        'place_of_service': 'office',
        'provider': {
            'first_name': 'JOHN',
            'npi': '1154387751',
            'last_name': 'FOSTER',
            'phone': '8645822900'
        },
        'type': 'consultation'
    },
    'patient': {
        'birth_date': '1970-01-01',
        'first_name': 'JANE',
        'last_name': 'DOE',
        'id': '1234567890'
    },
    'provider': {
        'first_name': 'CHRISTINA',
        'last_name': 'BERTOLAMI',
        'npi': '1619131232'
    },
    'trading_partner_id': 'MOCKPAYER'
}

slot_create_request = {
    'pd_provider_uuid': 'fd0d75d2-6285-4ecc-aca0-017f0f313bd6',
    'location': [32.7844314, -79.9994895],
    'appointment_type': 'ATYP1',
    'start_date': '2014-03-17T08:00:00',
    'end_date': '2014-03-17T09:00:00'
}
