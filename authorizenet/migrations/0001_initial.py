# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Adding model 'Response'
        db.create_table('authorizenet_response', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('response_code', self.gf('django.db.models.fields.CharField')(max_length=2)),
            ('response_subcode', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('response_reason_code', self.gf('django.db.models.fields.CharField')(max_length=15)),
            ('response_reason_text', self.gf('django.db.models.fields.TextField')()),
            ('auth_code', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('avs_code', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('trans_id', self.gf('django.db.models.fields.CharField')(max_length=255, db_index=True)),
            ('invoice_num', self.gf('django.db.models.fields.CharField')(max_length=20, blank=True)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('amount', self.gf('django.db.models.fields.CharField')(max_length=16)),
            ('method', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('type', self.gf('django.db.models.fields.CharField')(max_length=20, db_index=True)),
            ('cust_id', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('first_name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('last_name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('company', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('address', self.gf('django.db.models.fields.CharField')(max_length=60)),
            ('city', self.gf('django.db.models.fields.CharField')(max_length=40)),
            ('state', self.gf('django.db.models.fields.CharField')(max_length=40)),
            ('zip', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('country', self.gf('django.db.models.fields.CharField')(max_length=60)),
            ('phone', self.gf('django.db.models.fields.CharField')(max_length=25)),
            ('fax', self.gf('django.db.models.fields.CharField')(max_length=25)),
            ('email', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('ship_to_first_name', self.gf('django.db.models.fields.CharField')(max_length=50, blank=True)),
            ('ship_to_last_name', self.gf('django.db.models.fields.CharField')(max_length=50, blank=True)),
            ('ship_to_company', self.gf('django.db.models.fields.CharField')(max_length=50, blank=True)),
            ('ship_to_address', self.gf('django.db.models.fields.CharField')(max_length=60, blank=True)),
            ('ship_to_city', self.gf('django.db.models.fields.CharField')(max_length=40, blank=True)),
            ('ship_to_state', self.gf('django.db.models.fields.CharField')(max_length=40, blank=True)),
            ('ship_to_zip', self.gf('django.db.models.fields.CharField')(max_length=20, blank=True)),
            ('ship_to_country', self.gf('django.db.models.fields.CharField')(max_length=60, blank=True)),
            ('tax', self.gf('django.db.models.fields.CharField')(max_length=16, blank=True)),
            ('duty', self.gf('django.db.models.fields.CharField')(max_length=16, blank=True)),
            ('freight', self.gf('django.db.models.fields.CharField')(max_length=16, blank=True)),
            ('tax_exempt', self.gf('django.db.models.fields.CharField')(max_length=16, blank=True)),
            ('po_num', self.gf('django.db.models.fields.CharField')(max_length=25, blank=True)),
            ('MD5_Hash', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('cvv2_resp_code', self.gf('django.db.models.fields.CharField')(max_length=2, blank=True)),
            ('cavv_response', self.gf('django.db.models.fields.CharField')(max_length=2, blank=True)),
            ('test_request', self.gf('django.db.models.fields.CharField')(default='FALSE', max_length=10, blank=True)),
        ))
        db.send_create_signal('authorizenet', ['Response'])

    def backwards(self, orm):

        # Deleting model 'Response'
        db.delete_table('authorizenet_response')

    models = {
        'authorizenet.response': {
            'MD5_Hash': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'Meta': {'object_name': 'Response'},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '60'}),
            'amount': ('django.db.models.fields.CharField', [], {'max_length': '16'}),
            'auth_code': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'avs_code': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
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
