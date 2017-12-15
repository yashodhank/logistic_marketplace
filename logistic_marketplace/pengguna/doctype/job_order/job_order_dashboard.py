from frappe import _

def get_data():
	return {
		'heatmap': True,
		'heatmap_message': _('This is List of Documents Related'),
		'fieldname': 'job_order',
		'transactions': [
			{
				'label': _('Update'),
				'items': ['Job Order Update']
			}
			
		]
	}