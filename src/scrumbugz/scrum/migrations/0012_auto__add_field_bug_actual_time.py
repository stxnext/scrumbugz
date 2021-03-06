# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Bug.actual_time'
        db.add_column('scrum_bug', 'actual_time',
                      self.gf('django.db.models.fields.FloatField')(default=0.0),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Bug.actual_time'
        db.delete_column('scrum_bug', 'actual_time')


    models = {
        'scrum.bug': {
            'Meta': {'ordering': "('id',)", 'object_name': 'Bug'},
            'actual_time': ('django.db.models.fields.FloatField', [], {'default': '0.0'}),
            'assigned_to': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'blocks': ('jsonfield.fields.JSONField', [], {'blank': 'True'}),
            'comments_count': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0'}),
            'component': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'creation_time': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'depends_on': ('jsonfield.fields.JSONField', [], {'blank': 'True'}),
            'history': ('scrum.models.CompressedJSONField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.PositiveIntegerField', [], {'primary_key': 'True'}),
            'last_change_time': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_synced_time': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'priority': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'}),
            'product': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'bugs'", 'null': 'True', 'on_delete': 'models.SET_NULL', 'to': "orm['scrum.Project']"}),
            'resolution': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'}),
            'severity': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'}),
            'sprint': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'bugs'", 'null': 'True', 'on_delete': 'models.SET_NULL', 'to': "orm['scrum.Sprint']"}),
            'status': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'story_component': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'story_points': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0'}),
            'story_user': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'summary': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'target_milestone': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'}),
            'whiteboard': ('django.db.models.fields.CharField', [], {'max_length': '2048', 'blank': 'True'})
        },
        'scrum.bugsprintlog': {
            'Meta': {'ordering': "('-timestamp',)", 'object_name': 'BugSprintLog'},
            'action': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            'bug': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'sprint_actions'", 'to': "orm['scrum.Bug']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'sprint': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'bug_actions'", 'to': "orm['scrum.Sprint']"}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'})
        },
        'scrum.bugzillaurl': {
            'Meta': {'ordering': "('id',)", 'object_name': 'BugzillaURL'},
            'date_synced': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2012, 10, 16, 0, 0)'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'one_time': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'urls'", 'null': 'True', 'to': "orm['scrum.Project']"}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '2048'})
        },
        'scrum.bzproduct': {
            'Meta': {'object_name': 'BZProduct'},
            'component': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'products'", 'to': "orm['scrum.Project']"})
        },
        'scrum.project': {
            'Meta': {'ordering': "('name',)", 'object_name': 'Project'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'slug': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50', 'db_index': 'True'}),
            'team': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'projects'", 'null': 'True', 'to': "orm['scrum.Team']"})
        },
        'scrum.sprint': {
            'Meta': {'ordering': "['-start_date']", 'unique_together': "(('team', 'slug'),)", 'object_name': 'Sprint'},
            'bugs_data_cache': ('jsonfield.fields.JSONField', [], {'null': 'True'}),
            'bz_url': ('django.db.models.fields.URLField', [], {'max_length': '2048', 'null': 'True', 'blank': 'True'}),
            'created_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'end_date': ('django.db.models.fields.DateField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'notes': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'notes_html': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'slug': ('django.db.models.fields.CharField', [], {'max_length': '200', 'db_index': 'True'}),
            'start_date': ('django.db.models.fields.DateField', [], {}),
            'team': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'sprints'", 'to': "orm['scrum.Team']"})
        },
        'scrum.team': {
            'Meta': {'ordering': "('name',)", 'object_name': 'Team'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'slug': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50', 'db_index': 'True'})
        }
    }

    complete_apps = ['scrum']