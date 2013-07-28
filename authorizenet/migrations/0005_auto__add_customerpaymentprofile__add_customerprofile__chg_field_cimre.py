# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'CustomerPaymentProfile'
        db.create_table(u'authorizenet_customerpaymentprofile', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('customer', self.gf('django.db.models.fields.related.ForeignKey')(related_name='payment_profiles', to=orm['doctors.Practice'])),
            ('customer_profile', self.gf('django.db.models.fields.related.ForeignKey')(related_name='payment_profiles', to=orm['authorizenet.CustomerProfile'])),
            ('payment_profile_id', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('first_name', self.gf('django.db.models.fields.CharField')(max_length=50, blank=True)),
            ('last_name', self.gf('django.db.models.fields.CharField')(max_length=50, blank=True)),
            ('company', self.gf('django.db.models.fields.CharField')(max_length=60, blank=True)),
            ('phone_number', self.gf('django.db.models.fields.CharField')(max_length=25, blank=True)),
            ('fax_number', self.gf('django.db.models.fields.CharField')(max_length=25, blank=True)),
            ('address', self.gf('django.db.models.fields.CharField')(max_length=60, blank=True)),
            ('city', self.gf('django.db.models.fields.CharField')(max_length=40, blank=True)),
            ('state', self.gf('django.db.models.fields.CharField')(max_length=40, blank=True)),
            ('zip', self.gf('django.db.models.fields.CharField')(max_length=20, blank=True)),
            ('country', self.gf('django.db.models.fields.CharField')(max_length=60, blank=True)),
            ('card_number', self.gf('django.db.models.fields.CharField')(max_length=16, blank=True)),
            ('expiration_date', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'authorizenet', ['CustomerPaymentProfile'])

        # Adding model 'CustomerProfile'
        db.create_table(u'authorizenet_customerprofile', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('customer', self.gf('django.db.models.fields.related.OneToOneField')(related_name='customer_profile', unique=True, to=orm['doctors.Practice'])),
            ('profile_id', self.gf('django.db.models.fields.CharField')(max_length=50)),
        ))
        db.send_create_signal(u'authorizenet', ['CustomerProfile'])


        # Changing field 'CIMResponse.result_text'
        db.alter_column(u'authorizenet_cimresponse', 'result_text', self.gf('django.db.models.fields.TextField')())

    def backwards(self, orm):
        # Deleting model 'CustomerPaymentProfile'
        db.delete_table(u'authorizenet_customerpaymentprofile')

        # Deleting model 'CustomerProfile'
        db.delete_table(u'authorizenet_customerprofile')


        # Changing field 'CIMResponse.result_text'
        db.alter_column(u'authorizenet_cimresponse', 'result_text', self.gf('django.db.models.fields.TextField')(max_length=1023))

    models = {
        u'authorizenet.cimresponse': {
            'Meta': {'object_name': 'CIMResponse'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'result': ('django.db.models.fields.CharField', [], {'max_length': '8'}),
            'result_code': ('django.db.models.fields.CharField', [], {'max_length': '8'}),
            'result_text': ('django.db.models.fields.TextField', [], {}),
            'transaction_response': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['authorizenet.Response']", 'null': 'True', 'blank': 'True'})
        },
        u'authorizenet.customerpaymentprofile': {
            'Meta': {'object_name': 'CustomerPaymentProfile'},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '60', 'blank': 'True'}),
            'card_number': ('django.db.models.fields.CharField', [], {'max_length': '16', 'blank': 'True'}),
            'city': ('django.db.models.fields.CharField', [], {'max_length': '40', 'blank': 'True'}),
            'company': ('django.db.models.fields.CharField', [], {'max_length': '60', 'blank': 'True'}),
            'country': ('django.db.models.fields.CharField', [], {'max_length': '60', 'blank': 'True'}),
            'customer': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'payment_profiles'", 'to': u"orm['doctors.Practice']"}),
            'customer_profile': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'payment_profiles'", 'to': u"orm['authorizenet.CustomerProfile']"}),
            'expiration_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'fax_number': ('django.db.models.fields.CharField', [], {'max_length': '25', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'payment_profile_id': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'phone_number': ('django.db.models.fields.CharField', [], {'max_length': '25', 'blank': 'True'}),
            'state': ('django.db.models.fields.CharField', [], {'max_length': '40', 'blank': 'True'}),
            'zip': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'})
        },
        u'authorizenet.customerprofile': {
            'Meta': {'object_name': 'CustomerProfile'},
            'customer': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'customer_profile'", 'unique': 'True', 'to': u"orm['doctors.Practice']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'profile_id': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'authorizenet.response': {
            'MD5_Hash': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'Meta': {'object_name': 'Response'},
            'account_number': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '10', 'blank': 'True'}),
            'address': ('django.db.models.fields.CharField', [], {'max_length': '60'}),
            'amount': ('django.db.models.fields.CharField', [], {'max_length': '16'}),
            'auth_code': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'avs_code': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'card_type': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '10', 'blank': 'True'}),
            'cavv_response': ('django.db.models.fields.CharField', [], {'max_length': '2', 'blank': 'True'}),
            'city': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'company': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'country': ('django.db.models.fields.CharField', [], {'max_length': '60'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'cust_id': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'cvv2_resp_code': ('django.db.models.fields.CharField', [], {'max_length': '2', 'blank': 'True'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'duty': ('django.db.models.fields.CharField', [], {'max_length': '16', 'blank': 'True'}),
            'email': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'fax': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'freight': ('django.db.models.fields.CharField', [], {'max_length': '16', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'invoice_num': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'method': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'po_num': ('django.db.models.fields.CharField', [], {'max_length': '25', 'blank': 'True'}),
            'response_code': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            'response_reason_code': ('django.db.models.fields.CharField', [], {'max_length': '15'}),
            'response_reason_text': ('django.db.models.fields.TextField', [], {}),
            'response_subcode': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'ship_to_address': ('django.db.models.fields.CharField', [], {'max_length': '60', 'blank': 'True'}),
            'ship_to_city': ('django.db.models.fields.CharField', [], {'max_length': '40', 'blank': 'True'}),
            'ship_to_company': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'ship_to_country': ('django.db.models.fields.CharField', [], {'max_length': '60', 'blank': 'True'}),
            'ship_to_first_name': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'ship_to_last_name': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'ship_to_state': ('django.db.models.fields.CharField', [], {'max_length': '40', 'blank': 'True'}),
            'ship_to_zip': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'}),
            'state': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'tax': ('django.db.models.fields.CharField', [], {'max_length': '16', 'blank': 'True'}),
            'tax_exempt': ('django.db.models.fields.CharField', [], {'max_length': '16', 'blank': 'True'}),
            'test_request': ('django.db.models.fields.CharField', [], {'default': "'FALSE'", 'max_length': '10', 'blank': 'True'}),
            'trans_id': ('django.db.models.fields.CharField', [], {'max_length': '255', 'db_index': 'True'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '20', 'db_index': 'True'}),
            'zip': ('django.db.models.fields.CharField', [], {'max_length': '20'})
        },
        u'base.address': {
            'Meta': {'object_name': 'Address'},
            'address1': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'address2': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'city': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'state': ('django_localflavor_us.models.USStateField', [], {'max_length': '2', 'blank': 'True'}),
            'zip': ('django.db.models.fields.CharField', [], {'max_length': '10', 'blank': 'True'})
        },
        u'doctors.employeetype': {
            'Meta': {'object_name': 'EmployeeType'},
            'has_profile': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_doctor': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_schedulable': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '30'})
        },
        u'doctors.practice': {
            'Meta': {'object_name': 'Practice'},
            'accepted_insurance': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['medical.InsurancePlan']", 'symmetrical': 'False', 'blank': 'True'}),
            'addresses': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['base.Address']", 'through': u"orm['doctors.PracticeAddress']", 'symmetrical': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'phone': ('base.fields.PhoneNumberField', [], {'max_length': '20'}),
            'practice_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['doctors.PracticeType']"}),
            'statement': ('django.db.models.fields.TextField', [], {'max_length': '5000', 'blank': 'True'}),
            'timezone': ('timezone_field.fields.TimeZoneField', [], {})
        },
        u'doctors.practiceaddress': {
            'Meta': {'object_name': 'PracticeAddress'},
            'address': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['base.Address']", 'unique': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'practice': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['doctors.Practice']"})
        },
        u'doctors.practiceemployeetype': {
            'Meta': {'ordering': "['order']", 'object_name': 'PracticeEmployeeType', 'db_table': "'doctors_practicetype_employee_types'"},
            'employeetype': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['doctors.EmployeeType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'order': ('django.db.models.fields.PositiveIntegerField', [], {'default': '1', 'db_index': 'True'}),
            'practicetype': ('adminsortable.fields.SortableForeignKey', [], {'to': u"orm['doctors.PracticeType']"})
        },
        u'doctors.practicetype': {
            'Meta': {'ordering': "['order']", 'object_name': 'PracticeType'},
            'employee_types': ('sortedm2m.fields.SortedManyToManyField', [], {'to': u"orm['doctors.EmployeeType']", 'through': u"orm['doctors.PracticeEmployeeType']", 'symmetrical': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'order': ('django.db.models.fields.PositiveIntegerField', [], {'default': '1', 'db_index': 'True'}),
            'specialties': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['medical.DoctorSpecialty']", 'symmetrical': 'False'})
        },
        u'medical.appointmenttype': {
            'Meta': {'ordering': "['order']", 'object_name': 'AppointmentType'},
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['medical.BillingCategory']", 'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'order': ('django.db.models.fields.PositiveIntegerField', [], {'default': '1', 'db_index': 'True'}),
            'specialty': ('adminsortable.fields.SortableForeignKey', [], {'related_name': "'appointment_types'", 'to': u"orm['medical.DoctorSpecialty']"})
        },
        u'medical.billingcategory': {
            'Meta': {'object_name': 'BillingCategory'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'medical.doctorspecialty': {
            'Meta': {'ordering': "['order']", 'object_name': 'DoctorSpecialty'},
            'default_appointment_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['medical.AppointmentType']", 'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'order': ('django.db.models.fields.PositiveIntegerField', [], {'default': '1', 'db_index': 'True'})
        },
        u'medical.insuranceplan': {
            'Meta': {'ordering': "['provider__name', 'name']", 'object_name': 'InsurancePlan'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'provider': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'plans'", 'to': u"orm['medical.InsuranceProvider']"})
        },
        u'medical.insuranceprovider': {
            'Meta': {'ordering': "['name']", 'object_name': 'InsuranceProvider'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['authorizenet']