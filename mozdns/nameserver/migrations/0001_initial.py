# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Nameserver'
        db.create_table('static_interface', (
            ('domain', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['domain.Domain'])),
            ('label', self.gf('django.db.models.fields.CharField')(max_length=63, null=True, blank=True)),
            ('fqdn', self.gf('django.db.models.fields.CharField')(db_index=True, max_length=255, null=True, blank=True)),
            ('ttl', self.gf('django.db.models.fields.PositiveIntegerField')(default=3600, null=True, blank=True)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=1000, null=True, blank=True)),
            ('ip_str', self.gf('django.db.models.fields.CharField')(max_length=39)),
            ('ip_upper', self.gf('django.db.models.fields.BigIntegerField')(null=True, blank=True)),
            ('ip_lower', self.gf('django.db.models.fields.BigIntegerField')(null=True, blank=True)),
            ('ip_type', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('mac', self.gf('django.db.models.fields.CharField')(max_length=17)),
            ('reverse_domain', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='staticintrdomain_set', null=True, to=orm['domain.Domain'])),
            ('system', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['systems.System'], null=True, blank=True)),
            ('dhcp_enabled', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('dns_enabled', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.create_table('nameserver', (
            ('ttl', self.gf('django.db.models.fields.PositiveIntegerField')(default=3600, null=True, blank=True)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=1000, null=True, blank=True)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('domain', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['domain.Domain'])),
            ('server', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('addr_glue', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='nameserver_set', null=True, to=orm['address_record.AddressRecord'])),
            ('intr_glue', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='intrnameserver_set', null=True, to=orm['static_intr.StaticReg'])),
        ))
        db.send_create_signal('nameserver', ['Nameserver'])

        # Adding unique constraint on 'Nameserver', fields ['domain', 'server']
        db.create_unique('nameserver', ['domain_id', 'server'])

        # Adding M2M table for field views on 'Nameserver'
        db.create_table('nameserver_views', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('nameserver', models.ForeignKey(orm['nameserver.nameserver'], null=False)),
            ('view', models.ForeignKey(orm['view.view'], null=False))
        ))
        db.create_unique('nameserver_views', ['nameserver_id', 'view_id'])


    def backwards(self, orm):
        # Removing unique constraint on 'Nameserver', fields ['domain', 'server']
        db.delete_unique('nameserver', ['domain_id', 'server'])

        # Deleting model 'Nameserver'
        db.delete_table('nameserver')

        # Removing M2M table for field views on 'Nameserver'
        db.delete_table('nameserver_views')


    models = {
        'address_record.addressrecord': {
            'Meta': {'unique_together': "(('label', 'domain', 'fqdn', 'ip_upper', 'ip_lower', 'ip_type'),)", 'object_name': 'AddressRecord', 'db_table': "'address_record'"},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '1000', 'null': 'True', 'blank': 'True'}),
            'domain': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['domain.Domain']"}),
            'fqdn': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ip_lower': ('django.db.models.fields.BigIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'ip_str': ('django.db.models.fields.CharField', [], {'max_length': '39'}),
            'ip_type': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'ip_upper': ('django.db.models.fields.BigIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'max_length': '63', 'null': 'True', 'blank': 'True'}),
            'ttl': ('django.db.models.fields.PositiveIntegerField', [], {'default': '3600', 'null': 'True', 'blank': 'True'}),
            'views': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['view.View']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'domain.domain': {
            'Meta': {'object_name': 'Domain', 'db_table': "'domain'"},
            'delegated': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'dirty': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_reverse': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'master_domain': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'to': "orm['domain.Domain']", 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'purgeable': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'soa': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'to': "orm['soa.SOA']", 'null': 'True', 'blank': 'True'})
        },
        'nameserver.nameserver': {
            'Meta': {'unique_together': "(('domain', 'server'),)", 'object_name': 'Nameserver', 'db_table': "'nameserver'"},
            'addr_glue': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'nameserver_set'", 'null': 'True', 'to': "orm['address_record.AddressRecord']"}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '1000', 'null': 'True', 'blank': 'True'}),
            'domain': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['domain.Domain']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'intr_glue': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'intrnameserver_set'", 'null': 'True', 'to': "orm['static_intr.StaticReg']"}),
            'server': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'ttl': ('django.db.models.fields.PositiveIntegerField', [], {'default': '3600', 'null': 'True', 'blank': 'True'}),
            'views': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['view.View']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'soa.soa': {
            'Meta': {'unique_together': "(('primary', 'contact', 'description'),)", 'object_name': 'SOA', 'db_table': "'soa'"},
            'contact': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'dirty': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'expire': ('django.db.models.fields.PositiveIntegerField', [], {'default': '1209600'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'minimum': ('django.db.models.fields.PositiveIntegerField', [], {'default': '180'}),
            'primary': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'refresh': ('django.db.models.fields.PositiveIntegerField', [], {'default': '180'}),
            'retry': ('django.db.models.fields.PositiveIntegerField', [], {'default': '86400'}),
            'serial': ('django.db.models.fields.PositiveIntegerField', [], {'default': '1360538201'}),
            'ttl': ('django.db.models.fields.PositiveIntegerField', [], {'default': '3600', 'null': 'True', 'blank': 'True'})
        },
        'static_intr.staticinterface': {
            'Meta': {'unique_together': "(('ip_upper', 'ip_lower', 'label', 'domain', 'mac'),)", 'object_name': 'StaticReg', 'db_table': "'static_interface'"},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '1000', 'null': 'True', 'blank': 'True'}),
            'dhcp_enabled': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'dns_enabled': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'domain': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['domain.Domain']"}),
            'fqdn': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ip_lower': ('django.db.models.fields.BigIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'ip_str': ('django.db.models.fields.CharField', [], {'max_length': '39'}),
            'ip_type': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'ip_upper': ('django.db.models.fields.BigIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'max_length': '63', 'null': 'True', 'blank': 'True'}),
            'mac': ('django.db.models.fields.CharField', [], {'max_length': '17'}),
            'reverse_domain': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'staticintrdomain_set'", 'null': 'True', 'to': "orm['domain.Domain']"}),
            'system': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['systems.System']", 'null': 'True', 'blank': 'True'}),
            'ttl': ('django.db.models.fields.PositiveIntegerField', [], {'default': '3600', 'null': 'True', 'blank': 'True'}),
            'views': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['view.View']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'systems.allocation': {
            'Meta': {'ordering': "['name']", 'object_name': 'Allocation', 'db_table': "u'allocations'"},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'systems.location': {
            'Meta': {'ordering': "['name']", 'object_name': 'Location', 'db_table': "u'locations'"},
            'address': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255', 'blank': 'True'}),
            'note': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'})
        },
        'systems.operatingsystem': {
            'Meta': {'ordering': "['name', 'version']", 'object_name': 'OperatingSystem', 'db_table': "u'operating_systems'"},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'version': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'})
        },
        'systems.servermodel': {
            'Meta': {'ordering': "['vendor', 'model']", 'object_name': 'ServerModel', 'db_table': "u'server_models'"},
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'part_number': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'vendor': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'})
        },
        'systems.system': {
            'Meta': {'object_name': 'System', 'db_table': "u'systems'"},
            'allocation': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['systems.Allocation']", 'null': 'True', 'blank': 'True'}),
            'asset_tag': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'change_password': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'created_on': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'hostname': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_dhcp_server': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'is_dns_server': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'is_nagios_server': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'is_puppet_server': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'is_switch': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'licenses': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'notes': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'oob_ip': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True', 'blank': 'True'}),
            'oob_switch_port': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'operating_system': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['systems.OperatingSystem']", 'null': 'True', 'blank': 'True'}),
            'patch_panel_port': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'purchase_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'purchase_price': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'rack_order': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '6', 'decimal_places': '2', 'blank': 'True'}),
            'ram': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'serial': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'server_model': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['systems.ServerModel']", 'null': 'True', 'blank': 'True'}),
            'switch_ports': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'system_rack': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['systems.SystemRack']", 'null': 'True', 'blank': 'True'}),
            'system_status': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['systems.SystemStatus']", 'null': 'True', 'blank': 'True'}),
            'updated_on': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'})
        },
        'systems.systemrack': {
            'Meta': {'ordering': "['name']", 'object_name': 'SystemRack', 'db_table': "u'system_racks'"},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['systems.Location']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'})
        },
        'systems.systemstatus': {
            'Meta': {'ordering': "['status']", 'object_name': 'SystemStatus', 'db_table': "u'system_statuses'"},
            'color': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'color_code': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'})
        },
        'view.view': {
            'Meta': {'unique_together': "(('name',),)", 'object_name': 'View', 'db_table': "'view'"},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        }
    }

    complete_apps = ['nameserver']
