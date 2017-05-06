from tweets.migrations.migration import Migration


class InitialMigration(Migration):
    """
    Migration that creates initial tables for seventweets.
    """

    def id(self):
        return 1

    def upgrade(self, cursor):
        cursor.execute('''
            CREATE TABLE tweets (
            id SERIAL PRIMARY KEY,
            name VARCHAR(20) NOT NULL,
            tweet TEXT);
        ''')

    def downgrade(self, cursor):
        cursor.execute('''
            DROP TABLE tweets;
        ''')
