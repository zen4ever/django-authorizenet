# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Adding field 'Response.card_type'
        db.add_column('authorizenet_response', 'card_type', self.gf('django.db.models.fields.CharField')(default='', max_length=10, blank=True), keep_default=False)

        # Adding field 'Response.account_number'
        db.add_column('authorizenet_response', 'account_number', self.gf('django.db.models.fields.CharField')(default='', max_length=10, blank=True), keep_default=False)

    def backwards(self, orm):

        # Deleting field 'Response.card_type'
        db.delete_column('authorizenet_response', 'card_type')

        # Deleting field 'Response.account_number'
        db.delete_column('authorizenet_response', 'account_number')

    models = {
        'authorizenet.cimresponse': {
            'Meta': {'object_name': 'CIMResponse'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'result': ('django.db.models.fields.CharField', [], {'max_length': '8'}),
            'result_code': ('django.db.models.fields.CharField', [], {'max_length': '8'}),
            'result_text': ('django.db.models.fields.CharField', [], {'max_length': '1023'}),
            'transaction_response': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['authorizenet.Response']", 'null': 'True', 'blank': 'True'})
        },
        'authorizenet.response': {
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
            'cust_id': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'cvv2_resp_code': ('django.db.models.fields.CharField', [], {'max_length': '2', 'blank': 'True'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'duty': ('django.db.models.fields.CharField', [], {'max_length': '16', 'blank': 'True'}),
            'email': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'fax': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'freight': ('django.db.models.fields.CharField', [], {'max_length': '16', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
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
        }
    }

    complete_apps = ['authorizenet']
