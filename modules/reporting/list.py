import framework
# unique to module
import csv

class Module(framework.module):

    def __init__(self, params):
        framework.module.__init__(self, params)
        self.register_option('table', 'hosts', 'yes', 'source table of the data for the list')
        self.register_option('column', 'ip_address', 'yes', 'source column of the data for the list')
        self.register_option('unique', False, 'yes', 'only return unique items from the dataset')
        self.register_option('nulls', True, 'yes', 'include nulls in the dataset')
        self.register_option('filename', '%s/list.txt' % (self.workspace), 'yes', 'path and filename for output')
        self.info = {
                     'Name': 'List Creator',
                     'Author': 'Tim Tomes (@LaNMaSteR53)',
                     'Description': 'Creates a file containing a list of records from the database.',
                     'Comments': []
                     }

    def module_run(self):
        # validate that file can be created
        filename = self.options['filename']['value']
        outfile = open(filename, 'w')
        # handle the source of information for the report
        column = self.options['column']['value']
        table = self.options['table']['value']
        nulls = ' WHERE %s IS NOT NULL' % (column) if not self.options['nulls']['value'] else ''
        unique = 'DISTINCT ' if self.options['unique']['value'] else ''
        values = (unique, column, table, nulls)
        query = 'SELECT %s%s FROM %s%s ORDER BY 1' % values
        rows = self.query(query)
        for row in [x[0] for x in rows]:
            row = row if row else ''
            outfile.write('%s\n' % (row))
            print row
        outfile.close()
        self.output('%d items added to \'%s\'.' % (len(rows), filename))
